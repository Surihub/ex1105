import streamlit as st

st.title("① 입력과 계산")
st.caption("number_input · slider · selectbox · radio · checkbox · multiselect · button · if")
t1, t2 = st.tabs(["사칙연산", "수학적 조건 탐색"])
with t1:
    a = st.number_input("첫 번째 수", -100, 100, 8)
    b = st.number_input("두 번째 수", -100, 100, 3)
    op = st.selectbox("연산", ["더하기", "빼기", "곱하기", "나누기"])
    if st.button("계산하기", type="primary"):
        if op == "더하기": result = a + b
        elif op == "빼기": result = a - b
        elif op == "곱하기": result = a * b
        elif b == 0:
            result = None
            st.error("0으로 나눌 수 없습니다.")
        else: result = a / b
        if result is not None:
            st.metric("계산 결과", f"{result:g}")
            st.success("계산 완료")
with t2:
    n = st.slider("정수 n", -20, 20, 6)
    mode = st.radio("확인할 성질", ["짝수와 홀수", "양수와 음수", "3의 배수"], horizontal=True)
    show = st.checkbox("판정 결과 표시", value=True)
    selected = st.multiselect("함께 비교할 수", [2, 3, 4, 5, 6, 7, 8, 9], default=[2, 3])
    if show:
        if mode == "짝수와 홀수": st.info("짝수" if n % 2 == 0 else "홀수")
        elif mode == "양수와 음수": st.info("양수" if n > 0 else "음수" if n < 0 else "0")
        else: st.info("3의 배수" if n % 3 == 0 else "3의 배수가 아님")
    st.write("선택한 수:", selected)
    st.write("n과의 합:", [n + x for x in selected])
with st.expander("커스터마이징"):
    st.write("연산 종류, 숫자 범위, 판정 조건, 안내 문구를 수정해 보세요.")
