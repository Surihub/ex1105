from pathlib import Path

import streamlit as st

st.set_page_config(page_title="수학 앱 만들기", page_icon="📐", layout="wide")
st.title("📐 수학 앱 만들기")
st.info("이 페이지에서는 글·수식·메시지와 미디어를 출력합니다. 문구와 수식을 바꾸며 화면의 변화를 확인해 보세요.")

st.header("글과 수식 출력")
st.subheader("1. 피타고라스 정리")
st.markdown("**직각삼각형**의 세 변 사이에는 다음 관계가 있습니다.")
st.latex(r"a^2+b^2=c^2")
st.latex(r"(a+b)^2=a^2+2ab+b^2")
st.latex(r"\bar{x}=\frac{x_1+\cdots+x_n}{n}")
st.code('st.latex(r"a^2+b^2=c^2")', language="python")

st.subheader("2. 메시지 출력")
st.success("정답입니다!")
st.warning("계산을 다시 확인해 보세요.")
st.error("숫자를 입력해 주세요.")
st.info("각 메시지의 문구를 원하는 내용으로 바꿔 보세요.")

with st.expander("이미지와 영상"):
    st.image(str(Path(__file__).parent / "assets" / "triangle.svg"), width=420)
    st.video("https://www.youtube.com/watch?v=v0YEaeIClKY")

st.link_button("Desmos 계산기 열기", "https://www.desmos.com/calculator")
with st.expander("외부 도구 넣기"):
    st.components.v1.iframe("https://www.desmos.com/calculator", height=400)
