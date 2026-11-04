import random
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

from math_tools import polynomial


st.title("⑥ 응답 연동과 자동 피드백")
st.caption("수식의 동치 · 단계별 풀이 · 여러 조건 검증 · 시도 기록")
if 'linked_attempts' not in st.session_state:
    st.session_state.linked_attempts = []


def record(activity, answer, correct):
    st.session_state.linked_attempts.append({
        '시각': datetime.now().strftime('%H:%M:%S'), '활동': activity,
        '응답': str(answer), '결과': '성공' if correct else '다시 시도',
    })


st.subheader("1. 모양이 달라도 같은 수식이면 정답")
st.write("(x + 2)²과 같은 다항식을 입력하세요. 전개한 식과 곱으로 쓴 식을 모두 인정합니다.")
expression = st.text_input("다항식", placeholder="예: x*x + 4*x + 4")
st.caption("곱셈은 *로 입력합니다. x의 다항식만 다루며, 분모에 x가 있는 유리식과 삼각함수는 제외합니다.")
if st.button("수식 확인"):
    try:
        actual = polynomial(expression)
        expected = polynomial('(x+2)^2')
        correct = actual == expected
        record('수식 동치', expression, correct)
        if correct:
            st.success("같은 다항식입니다. 계수가 모두 일치합니다.")
        else:
            missing = [f'x의 {degree}차 항' if degree else '상수항'
                       for degree in sorted(set(actual) | set(expected), reverse=True)
                       if actual.get(degree, 0) != expected.get(degree, 0)]
            st.warning('다시 확인할 부분: ' + ', '.join(missing))
    except (ValueError, OverflowError, RecursionError) as exc:
        st.warning(str(exc))


st.subheader("2. 앞 단계에 맞춰 다음 단계 열기")
st.write("문제가 새로 생성되어도 풀이 중에는 계수가 유지됩니다. 각 단계의 오답 원인에 맞춰 힌트를 제공합니다.")
if 'linked_equation' not in st.session_state:
    st.session_state.linked_equation = (random.randint(2, 7), random.randint(1, 9), random.randint(2, 9))
    st.session_state.linked_step = 0
if st.button("새 방정식 만들기"):
    st.session_state.linked_equation = (random.randint(2, 7), random.randint(1, 9), random.randint(2, 9))
    st.session_state.linked_step = 0
    for key in ('linked_rhs', 'linked_root'):
        st.session_state.pop(key, None)
a, b, root = st.session_state.linked_equation
rhs = a*root+b
st.latex(rf'{a}x+{b}={rhs}')
step_progress = st.progress(st.session_state.linked_step / 2)
intermediate = st.number_input(f"1단계: 양변에서 {b}을 빼면 {a}x = ?", value=None, step=1, key='linked_rhs')
if st.button("1단계 확인"):
    if intermediate is None:
        st.info('값을 입력해 주세요.')
    else:
        correct = intermediate == rhs-b
        st.session_state.linked_step = 1 if correct else 0
        record('방정식 1단계', intermediate, correct)
        if correct:
            st.success('이항이 정확합니다. 아래에서 x를 구해 보세요.')
        elif intermediate == rhs+b:
            st.warning(f'양변에 {b}을 더하지 않고 빼야 합니다.')
        else:
            st.warning(f'오른쪽의 {rhs} - {b}부터 계산해 보세요.')
if st.session_state.linked_step >= 1:
    answer = st.number_input('2단계: x = ?', value=None, step=1, key='linked_root')
    if st.button('2단계 확인'):
        if answer is None:
            st.info('값을 입력해 주세요.')
        else:
            correct = answer == root
            record('방정식 2단계', answer, correct)
            if correct:
                st.session_state.linked_step = 2
                st.success(f'완료했습니다. x = {root}을 원래 식에 넣으면 양변이 {rhs}로 같습니다.')
            else:
                st.warning(f'{a}x = {rhs-b}의 양변을 {a}으로 나누어 보세요.')
step_progress.progress(st.session_state.linked_step / 2)
st.caption(f"완료한 단계: {st.session_state.linked_step} / 2")


st.subheader("3. 여러 조건을 동시에 만족하는 함수 만들기")
st.write('꼭짓점이 (1, -2)이고 점 (0, 0)을 지나는 이차함수를 만들어 보세요.')
st.latex(r'y=ax^2+bx+c')
c1, c2, c3 = st.columns(3)
with c1:
    qa = st.number_input('a', -5.0, 5.0, 1.0, 0.5)
with c2:
    qb = st.number_input('b', -10.0, 10.0, 0.0, 0.5)
with c3:
    qc = st.number_input('c', -10.0, 10.0, 0.0, 0.5)
x = np.linspace(-3, 5, 161)
st.line_chart(pd.DataFrame({'x': x, '입력한 함수': qa*x*x+qb*x+qc}).set_index('x'))
if st.button('세 조건 확인'):
    quadratic = qa != 0
    vertex = quadratic and abs(-qb/(2*qa)-1) < 1e-9 and abs(qa+qb+qc+2) < 1e-9
    through = abs(qc) < 1e-9
    for label, ok in [('이차함수인가?', quadratic), ('꼭짓점이 (1, -2)인가?', vertex), ('점 (0, 0)을 지나는가?', through)]:
        st.write(('✅ ' if ok else '⬜ ') + label)
    record('함수 조건', f'{qa}x² + {qb}x + {qc}', quadratic and vertex and through)
    if quadratic and vertex and through:
        st.success('모든 조건을 만족합니다.')
    else:
        st.info('통과하지 못한 조건을 보고 계수를 조절해 보세요.')


st.subheader('시도 기록')
rows = st.session_state.linked_attempts
if rows:
    df = pd.DataFrame(rows)
    st.dataframe(df, hide_index=True)
    st.bar_chart(pd.crosstab(df['활동'], df['결과']))
    st.download_button('기록 CSV 저장', df.to_csv(index=False).encode('utf-8-sig'), 'feedback_history.csv', 'text/csv')
    if st.button('시도 기록 지우기'):
        st.session_state.linked_attempts = []
        st.rerun()
else:
    st.caption('각 활동에 응답하면 성공과 재시도 기록이 쌓입니다.')
st.caption('이 기록은 현재 사용자 세션에서 유지됩니다.')
