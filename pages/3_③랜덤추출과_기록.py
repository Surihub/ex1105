import random

import streamlit as st

st.title("③ 랜덤 추출")
st.info("버튼을 눌러 번호를 뽑거나 주사위를 던져 보세요. 버튼을 누를 때마다 새로운 결과가 나옵니다.")

st.subheader("1. 번호 뽑기")
st.write("1부터 30까지의 번호 중에서 하나를 뽑습니다.")

if st.button("무작위로 뽑기"):
    result = random.randint(1, 30)
    st.write("뽑힌 번호:", result)

st.subheader("2. 주사위 여러 번 던지기")
st.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGI5eml2ZWlnbjl6czJrZXEzYjBxd3FjcG92cmRra3A1cTRiMWM1aSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ckHAdLU2OmY7knUClD/200.webp")
st.write("주사위는 1부터 6까지 나오며, 같은 숫자가 여러 번 나올 수 있습니다.")
times = st.slider("주사위를 던질 횟수", 1, 20, 5)
if st.button("주사위 던지기"):
    values = [random.randint(1, 6) for _ in range(times)]
    st.write("주사위 결과:", values)
    st.bar_chart({"주사위 눈": values})
