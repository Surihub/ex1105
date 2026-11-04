import math
from datetime import datetime

import pandas as pd
import streamlit as st


st.title("⑤ 여러 방식으로 풀어 보는 수학 퀴즈")
st.caption("숫자 입력 · 단답형 · 선택 목록 · 복수 선택 · 체크박스 · 슬라이더 · 풀이 서술")

if "quiz_attempts_v2" not in st.session_state:
    st.session_state.quiz_attempts_v2 = []
for row in st.session_state.quiz_attempts_v2:
    row.pop("자신감", None)

PROBLEMS = {
    "일차방정식 / 숫자 입력": {
        "level": "중학교", "widget": "number", "question": "방정식의 해 x를 입력하세요.",
        "latex": r"3x-7=8", "answer": 5, "solution": "양변에 7을 더하고 3으로 나누면 x = 5입니다.",
    },
    "제곱근 / 단답형": {
        "level": "중학교", "widget": "text", "question": "49의 제곱근을 모두 입력하세요. 쉼표로 구분해 주세요.",
        "answer": "-7, 7", "solution": "제곱해서 49가 되는 수는 -7과 7입니다.",
    },
    "삼각비 / 선택 목록": {
        "level": "중학교", "widget": "select", "question": "다음 삼각비의 값을 선택하세요.",
        "latex": r"\sin 30^\circ", "options": ["0", "1/2", "√2/2", "√3/2", "1"],
        "answer": "1/2", "solution": "30°의 맞은편 변은 빗변 길이의 절반이므로 sin 30° = 1/2입니다.",
    },
    "소수 / 복수 선택": {
        "level": "중학교", "widget": "multi", "question": "소수를 모두 선택하세요.",
        "options": [1, 2, 3, 4, 5, 9, 11], "answer": [2, 3, 5, 11],
        "solution": "소수는 1보다 크고 약수가 1과 자기 자신뿐인 자연수입니다. 1은 소수가 아닙니다.",
    },
    "명제 / 체크박스": {
        "level": "고등학교", "widget": "check", "question": "참인 명제에만 체크하세요. 거짓인 명제는 비워 두세요.",
        "options": ["모든 실수 x에 대하여 x² ≥ 0이다.", "x² = 4이면 반드시 x = 2이다.", "x > 2이면 x > 1이다."],
        "answer": [True, False, True], "solution": "두 번째 명제는 x = -2가 반례이므로 거짓입니다. 첫 번째와 세 번째 명제는 참입니다.",
    },
    "확률 / 슬라이더": {
        "level": "중학교", "widget": "slider", "question": "공정한 주사위에서 3의 배수가 나올 확률은 몇 %일까요? 소수 첫째 자리까지 맞춰 보세요.",
        "answer": 33.3, "solution": "가능한 눈 6개 중 3과 6의 두 가지이므로 2/6 = 1/3 ≈ 33.3%입니다.",
    },
    "미분 / 숫자 입력": {
        "level": "고등학교", "widget": "number", "question": "x = 2에서의 순간변화율을 입력하세요.",
        "latex": r"f(x)=x^3-2x", "answer": 10,
        "solution": "f′(x) = 3x² - 2이므로 f′(2) = 12 - 2 = 10입니다.",
    },
    "평균과 중앙값 / 풀이 서술": {
        "level": "중학교", "widget": "essay", "question": "자료 4, 5, 5, 6, 7에 100을 추가하면 평균과 중앙값 중 무엇이 더 크게 변할까요? 이유와 계산을 적어 보세요.",
        "answer": "자기 점검", "solution": "평균은 5.4에서 약 21.17로, 중앙값은 5에서 5.5로 바뀝니다. 극단적인 값의 영향을 크게 받는 평균이 더 많이 변합니다.",
    },
}

quiz, records = st.tabs(["문제 풀기", "응답 기록과 통계"])
with quiz:
    for index, (selected, problem) in enumerate(PROBLEMS.items(), start=1):
        kind = problem["widget"]
        st.subheader(f"{index}. {selected}")
        st.write(problem["question"])
        if "latex" in problem:
            st.latex(problem["latex"])

        input_area = st.container() if index <= 3 else st.form(f"quiz_{selected}", border=False)
        with input_area:
            if kind == "number":
                answer = st.number_input("정답", value=0, step=1, key=f"quiz_answer_{index}")
            elif kind == "text":
                answer = st.text_input("정답", placeholder="예: -3, 3", key=f"quiz_answer_{index}")
            elif kind == "select":
                answer = st.selectbox("정답", ["선택하세요"] + problem["options"])
            elif kind == "multi":
                answer = st.multiselect("해당하는 수를 모두 선택하세요", problem["options"])
            elif kind == "check":
                answer = [st.checkbox(statement) for statement in problem["options"]]
            elif kind == "slider":
                answer = st.slider("확률 (%)", 0.0, 100.0, 50.0, 0.1)
            else:
                answer = st.text_area("나의 풀이", height=160)
            submitted = st.form_submit_button("풀이 저장" if kind == "essay" else "채점하기") if index > 3 else False

        if submitted:
            missing = (isinstance(answer, str) and not answer.strip()) or (kind == "select" and answer == "선택하세요")
            if missing:
                st.warning("답을 입력하거나 선택해 주세요.")
            else:
                if kind == "essay":
                    verdict = "자기 점검"
                elif kind == "text":
                    try:
                        pieces = answer.replace("，", ",").split(",")
                        parsed = [float(piece.strip()) for piece in pieces]
                        correct = len(parsed) == 2 and set(parsed) == {-7.0, 7.0}
                    except ValueError:
                        correct = False
                    verdict = "정답" if correct else "오답"
                elif kind == "multi":
                    verdict = "정답" if set(answer) == set(problem["answer"]) else "오답"
                elif kind == "slider":
                    verdict = "정답" if math.isclose(answer, problem["answer"], abs_tol=0.001) else "오답"
                else:
                    verdict = "정답" if answer == problem["answer"] else "오답"
                st.session_state.quiz_attempts_v2.append({
                    "시각": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "문제": selected, "제출": str(answer), "정답여부": verdict,
                })
                st.session_state.setdefault("quiz_feedback_by_problem", {})[selected] = {"verdict": verdict}

        feedback = st.session_state.get("quiz_feedback_by_problem", {}).get(selected)
        if feedback and index > 3:
            if feedback["verdict"] == "정답":
                st.success("정답입니다.")
            elif feedback["verdict"] == "오답":
                st.error("풀이를 다시 확인해 보세요.")
            else:
                st.info("풀이가 저장되었습니다. 예시 풀이와 비교해 스스로 점검해 보세요.")
            with st.expander("정답과 해설 확인"):
                st.write(problem["solution"])

with records:
    rows = st.session_state.quiz_attempts_v2
    if rows:
        df = pd.DataFrame(rows)
        graded = df[df["정답여부"].isin(["정답", "오답"])]
        c1, c2, c3 = st.columns(3)
        c1.metric("전체 제출", len(df))
        c2.metric("자동 채점 문항", len(graded))
        accuracy = graded["정답여부"].eq("정답").mean() if len(graded) else None
        c3.metric("정답률", f"{accuracy:.0%}" if accuracy is not None else "채점 기록 없음")
        if accuracy is not None:
            st.progress(float(accuracy))
            st.write("문제 유형별 정답률")
            rates = graded.assign(정답=graded["정답여부"].eq("정답")).groupby("문제")["정답"].mean()
            st.bar_chart(rates.rename("정답률"))
        only_wrong = st.checkbox("오답 기록만 보기")
        st.dataframe(df[df["정답여부"] == "오답"] if only_wrong else df, hide_index=True)
        st.download_button("전체 기록 CSV 저장", df.to_csv(index=False).encode("utf-8-sig"), "quiz_responses.csv", "text/csv")
        if st.button("응답 기록 초기화"):
            st.session_state.quiz_attempts_v2 = []
            st.session_state.pop("quiz_feedback_by_problem", None)
            st.rerun()
    else:
        st.info("아직 제출한 응답이 없습니다.")
    st.caption("서술형은 자동 채점과 정답률 계산에서 제외합니다. 기록은 현재 세션에서만 유지됩니다.")
