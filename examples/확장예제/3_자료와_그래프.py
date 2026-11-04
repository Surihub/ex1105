import streamlit as st
import pandas as pd
import io

st.title("③ 자료와 그래프")
st.caption("dataframe · line_chart · bar_chart · scatter_chart · file_uploader")
tab1, tab2 = st.tabs(["직접 만든 자료", "CSV 업로드"])
with tab1:
    rule = st.selectbox("자료 생성 규칙", ["일차식", "제곱", "절댓값"])
    a = st.slider("계수 a", -4, 4, 2)
    xs = list(range(-5, 6))
    ys = [a*x if rule == "일차식" else x*x if rule == "제곱" else abs(x) for x in xs]
    df = pd.DataFrame({"x": xs, "y": ys})
    st.dataframe(df, hide_index=True)
    chart = st.radio("그래프 유형", ["선", "막대", "산점도"], horizontal=True)
    if chart == "선": st.line_chart(df.set_index("x"))
    elif chart == "막대": st.bar_chart(df.set_index("x"))
    else: st.scatter_chart(df, x="x", y="y")
    st.download_button("자료 CSV 다운로드", df.to_csv(index=False).encode("utf-8-sig"), "math_data.csv", "text/csv")
with tab2:
    file = st.file_uploader("숫자 자료가 포함된 CSV 업로드", type="csv")
    if file:
        try:
            uploaded = pd.read_csv(file)
            st.dataframe(uploaded.head(100))
            nums = uploaded.select_dtypes(include="number")
            if not nums.empty:
                st.bar_chart(nums.head(100))
            else: st.warning("그래프로 표시할 숫자 열이 없습니다.")
        except Exception as e:
            st.error(f"파일을 읽지 못했습니다: {e}")
