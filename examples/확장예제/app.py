import streamlit as st

st.set_page_config(page_title="수학 실습 도구상자", page_icon="📐", layout="wide")
st.title("📐 수학 실습 도구상자")
st.write("수학 예시로 Streamlit의 기본 기능을 체험하고 입력값과 문구를 직접 바꿔 보세요.")
st.info("왼쪽 메뉴에서 각 실습 페이지로 이동하세요. 모든 데이터는 실습용이며 외부 서버에 저장하지 않습니다.")

st.header("기본 출력")
st.subheader("수학식 표현")
st.markdown("**정수**, *함수*, **확률**, **통계**를 다양하게 표현할 수 있습니다.")
st.latex(r"(a+b)^2=a^2+2ab+b^2")
st.code('st.latex(r"(a+b)^2=a^2+2ab+b^2")', language="python")

st.markdown("**중학교 수학**")
for formula in (
    r"-3+8=5",
    r"2x+5=13 \quad\Longrightarrow\quad x=4",
    r"x^2+5x+6=(x+2)(x+3)",
    r"a^2+b^2=c^2",
):
    st.latex(formula)

st.markdown("**고등학교 수학**")
for formula in (
    r"\frac{x^2-1}{x-1}=x+1 \quad (x\ne 1)",
    r"\sin^2\theta+\cos^2\theta=1",
    r"\log_a(MN)=\log_a M+\log_a N",
    r"\sum_{k=1}^{n}k=\frac{n(n+1)}{2}",
    r"P(A\mid B)=\frac{P(A\cap B)}{P(B)}",
    r"y'=2x \quad\text{if}\quad y=x^2",
):
    st.latex(formula)

st.success("정답 피드백")
st.warning("풀이를 다시 확인하세요.")
st.error("조건에 맞지 않는 입력")
st.link_button("Desmos 그래핑 계산기", "https://www.desmos.com/calculator")

st.components.v1.iframe(
    "https://www.desmos.com/calculator",
    height=500
)

with st.expander("수학 학습에 활용할 이미지와 영상"):
    st.write("이미지: st.image('파일명.png') / 영상: st.video('영상 URL')")
    st.image("https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTZwd2NnYmtqamw1cXZ2Nmw2M3V1MWZiaXJxdnNjeXp2ZThob3ZiOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/8qUjDf9PZlHZ6/giphy.webp")
    st.video("https://www.youtube.com/watch?v=v0YEaeIClKY")
    st.caption("직접 준비한 수학 그림이나 설명 영상을 연결해 보세요.")

st.header("페이지 이동")
st.write("pages 폴더에 파일을 추가하면 사이드바에 페이지가 자동 생성됩니다.")
if st.button("입력과 계산 페이지 열기"):
    st.switch_page("pages/1_입력과_계산.py")
