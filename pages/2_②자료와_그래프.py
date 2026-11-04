import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

penguins = sns.load_dataset("penguins")

st.title("② 자료와 그래프")
st.info("Seaborn의 펭귄 자료를 표와 그래프로 살펴보고, 몸무게의 평균과 중앙값을 확인해 보세요.")

st.subheader("1. 펭귄 자료와 대표값")
st.dataframe(penguins, hide_index=True)
left, right = st.columns(2)
with left:
    st.metric("평균 몸무게", f"{penguins['body_mass_g'].mean():.1f} g")
with right:
    st.metric("몸무게 중앙값", f"{penguins['body_mass_g'].median():.1f} g")

st.subheader("2. Seaborn으로 분포 확인!")
st.write("펭귄의 종별 몸무게 분포 비교하기")
fig = plt.figure()
sns.histplot(data=penguins, x="body_mass_g", binwidth=200, binrange = [2000, 8000])
plt.xlabel("Body mass (g)")
plt.ylabel("Count")
st.pyplot(fig)
plt.close(fig)

fig = plt.figure()
sns.boxplot(data=penguins, x="species", y="body_mass_g")
plt.xlabel("Species")
plt.ylabel("Body mass (g)")
st.pyplot(fig)
plt.close(fig)

st.subheader("3. 부리 길이와 부리 깊이의 산점도")
st.write("가로축은 부리 길이, 세로축은 부리 깊이입니다. 점 색은 종을 나타냅니다.")
fig, ax = plt.subplots()
sns.scatterplot(
    data=penguins,
    x="bill_length_mm",
    y="bill_depth_mm",
    hue="species",
    ax=ax,
)
ax.set_xlabel("Bill length (mm)")
ax.set_ylabel("Bill depth (mm)")
st.pyplot(fig)
plt.close(fig)
