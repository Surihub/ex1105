import math

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import streamlit as st


st.title("② 피타고라스 정리 실험실")
st.caption("직각변의 길이를 정하고, 세 변 위 정사각형의 넓이를 비교해 보세요.")

with st.form("pythagoras_controls"):
    col_a, col_b = st.columns(2)
    with col_a:
        a = st.slider("가로 변 a", 2, 9, 6)
    with col_b:
        b = st.slider("세로 변 b", 2, 9, 4)
    st.form_submit_button("도형 그리기")

c = math.sqrt(a**2 + b**2)
c_squared = a**2 + b**2

left, right = st.columns([1, 1.6], gap="large")

with left:
    st.metric("빗변 c", f"{c:.2f}")
    st.latex(rf"{a}^2+{b}^2=c^2")
    st.latex(rf"{a**2}+{b**2}={c_squared}")
    st.write(f"두 작은 정사각형의 넓이 합은 **{a**2 + b**2}**입니다.")

with right:
    fig, ax = plt.subplots(figsize=(6, 5))

    p1, p2 = (a, 0), (0, b)
    p3, p4 = (b, a + b), (a + b, a)
    squares = (
        ([(0, 0), (a, 0), (a, -a), (0, -a)], "#8ECAE6", f"a² = {a**2}", (a / 2, -a / 2)),
        ([(0, 0), (0, b), (-b, b), (-b, 0)], "#FFB703", f"b² = {b**2}", (-b / 2, b / 2)),
        ([p1, p2, p3, p4], "#90BE6D", f"c² = {c_squared}",
         ((p1[0] + p2[0] + p3[0] + p4[0]) / 4,
          (p1[1] + p2[1] + p3[1] + p4[1]) / 4)),
    )
    for vertices, color, label, center in squares:
        ax.add_patch(Polygon(vertices, closed=True, facecolor=color, edgecolor="white", alpha=0.95))
        ax.text(*center, label, ha="center", va="center", fontsize=10)

    ax.add_patch(Polygon([(0, 0), p1, p2], closed=True,
                         facecolor="#F4F7FB", edgecolor="#34495E", linewidth=2))
    ax.text(a / 2, -0.45, f"a = {a}", ha="center", va="top", fontsize=9)
    ax.text(-0.45, b / 2, f"b = {b}", ha="right", va="center", fontsize=9)
    ax.text(a / 2, b / 2, f"c = {c:.2f}", ha="center", va="center", fontsize=9)

    # 축 범위를 고정해 입력을 바꿔도 도형이 화면 안에서 확대·축소되거나 이동하지 않습니다.
    ax.set_xlim(-10, 20)
    ax.set_ylim(-10, 20)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    st.pyplot(fig)
    plt.close(fig)

st.info("직각삼각형에서 빗변 위 정사각형의 넓이는 다른 두 변 위 정사각형의 넓이 합과 같습니다.")
