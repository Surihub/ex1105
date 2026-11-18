import sympy as sp
import streamlit as st


st.title("⑥ 응답 저장과 상태 유지")
st.write("문항 답과 버튼 클릭 횟수를 세션에 저장합니다.")

with st.form("form1"):
    answer1 = st.radio(
        "(x + 3)²을 전개한 식을 선택하세요.",
        ["x² + 9", "x² + 3x + 9", "x² + 6x + 9"],
        index=None,
    )
    submitted1 = st.form_submit_button("1번 답 제출")

if submitted1:
    st.session_state["answer1"] = answer1  # 제출한 1번 답을 세션에 저장합니다.

if "answer1" in st.session_state:
    st.write(f"저장된 1번 답: {st.session_state['answer1']}")

with st.form("form2"):
    answer2 = st.radio(
        "(x - 3)²을 전개한 식을 선택하세요.",
        ["x² + 6x + 9", "x² - 6x - 9", "x² - 6x + 9"],
        index=None,
    )
    submitted2 = st.form_submit_button("2번 답 제출")

if submitted2:
    st.session_state["answer2"] = answer2  # 제출한 2번 답을 세션에 저장합니다.

if "answer2" in st.session_state:
    st.write(f"저장된 2번 답: {st.session_state['answer2']}")

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("1 증가"):
    st.session_state.count += 1  # 일반 변수 대신 세션 상태를 수정해 값을 유지합니다.

st.write(st.session_state.count)

st.subheader("SymPy로 이차방정식 풀기")
x = sp.symbols("x")
equation = sp.Eq(x**2 - 5 * x + 6, 0)
solutions = sp.solve(equation, x)
st.latex(sp.latex(equation))
st.write(f"해: {solutions}")
