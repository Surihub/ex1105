import re
# from urllib.parse import parse_qs, urlparse

import pandas as pd
import sympy as sp
import streamlit as st


st.title("⑦ SymPy로 방정식 풀기")
st.write("SymPy를 사용해 이차방정식의 해를 구합니다.")
st.write("SymPy를 쓰면 근삿값만 구하는 계산기와 달리, 식을 기호 그대로 다루고 정확한 해를 구할 수 있습니다.")

x = sp.symbols("x")
equation = sp.Eq(x**2 - 5 * x + 6, 0)
solutions = sp.solve(equation, x)

st.latex(sp.latex(equation))
st.write(f"해: {solutions}")

st.subheader("기하: 직각삼각형의 빗변 구하기")
st.write("가로와 세로가 각각 6, 8인 직각삼각형의 빗변을 피타고라스 정리로 계산합니다.")
a, b = sp.symbols("a b", positive=True)
hypotenuse = sp.sqrt(a**2 + b**2).subs({a: 6, b: 8})
st.latex(r"c=\sqrt{a^2+b^2}")
st.write(f"빗변의 길이: {hypotenuse}")

st.subheader("구글시트 표 불러오기")
st.write("링크가 있는 사용자가 볼 수 있도록 공유된 구글시트의 주소를 입력해 주세요.")
with st.form("google_sheet_form"):
    sheet_url = st.text_input("구글시트 주소")
    load_sheet = st.form_submit_button("시트 불러오기")

if load_sheet:
    match = re.search(r"docs\.google\.com/spreadsheets/d/([\w-]+)", sheet_url)
    if not match: 
        st.error("올바른 구글시트 주소를 입력해 주세요.")
    else:
        sheet_id = match.group(1)
        gid = parse_qs(urlparse(sheet_url).query).get("gid", ["0"])[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        try:
            sheet_data = pd.read_csv(csv_url)
            st.dataframe(sheet_data, hide_index=True)
        except Exception:
            st.error("시트를 불러오지 못했습니다. 공유 설정과 시트 주소를 확인해 주세요.")


