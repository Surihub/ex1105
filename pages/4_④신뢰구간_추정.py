import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("④ 신뢰구간 추정 시뮬레이션")
st.info("버튼을 한 번 누를 때마다 표본 하나를 뽑고, 95% 신뢰구간을 하나씩 추가합니다.")

# 고정된 난수로 같은 모집단을 만듭니다.
population = np.random.default_rng(42).normal(50, 10, 10000)
population_mean = population.mean()
sigma = population.std()

st.subheader("1. 모집단 확인")
show_mean = st.checkbox("모평균 공개", value=False)
left, middle, right = st.columns(3)
left.metric("모집단 크기", "10,000개")
middle.metric("모평균", f"{population_mean:.2f}" if show_mean else "비공개")
right.metric("모표준편차", f"{sigma:.2f}")

st.subheader("2. 표본 추출하기")
sample_size = st.slider("한 번에 뽑을 표본 크기", 10, 200, 30)
repeats = st.slider("목표 추출 횟수", 10, 50, 20)
st.caption("매번 모집단에서 복원추출합니다. 설정을 바꾸면 진행 결과가 초기화됩니다.")

if "ci_steps" not in st.session_state or st.session_state.ci_steps["settings"] != (sample_size, repeats):
    st.session_state.ci_steps = {"settings": (sample_size, repeats), "means": []}

means_list = st.session_state.ci_steps["means"]
left, right = st.columns(2)
if left.button("처음부터 다시 하기"):
    means_list.clear()
if right.button("표본 하나 뽑기 →", disabled=len(means_list) >= repeats, type="primary"):
    sample = np.random.default_rng().choice(population, size=sample_size, replace=True)
    means_list.append(float(sample.mean()))

st.progress(len(means_list) / repeats, text=f"진행: {len(means_list)} / {repeats}회")

if means_list:
    means = np.array(means_list)
    margin = 1.96 * sigma / np.sqrt(sample_size)
    lower = means - margin
    upper = means + margin
    included = (lower <= population_mean) & (population_mean <= upper)

    st.subheader("3. 결과 확인")
    st.write(f"이번 표본평균: {means[-1]:.2f} / 95% 신뢰구간: [{lower[-1]:.2f}, {upper[-1]:.2f}]")
    if show_mean:
        if included[-1]:
            st.success("이번 신뢰구간은 실제 모평균을 포함합니다.")
        else:
            st.warning("이번 신뢰구간은 실제 모평균을 포함하지 않습니다.")
        left, right = st.columns(2)
        left.metric("모평균을 포함한 구간", f"{included.sum()} / {len(means)}개")
        right.metric("포함 비율", f"{included.mean():.1%}")
    st.write("선 하나가 한 번 추출한 표본의 95% 신뢰구간입니다.")

    fig, ax = plt.subplots(figsize=(8, max(4, repeats * 0.16)))
    for i in range(len(means)):
        color = "tomato" if show_mean and not included[i] else "steelblue"
        ax.errorbar(means[i], i + 1, xerr=margin, fmt="o", color=color, capsize=3)
    if show_mean:
        ax.axvline(population_mean, color="black", linestyle="--", label="Population mean")
        ax.legend()
    ax.set_xlabel("Mean")
    ax.set_ylabel("Trial")
    ax.set_yticks(range(1, repeats + 1, 5))
    ax.set_ylim(repeats + 1, 0)
    padding = margin * 0.5
    ax.set_xlim(lower.min() - padding, upper.max() + padding)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    if show_mean:
        st.caption("파란색: 모평균 포함 / 빨간색: 모평균 미포함 / 검은 점선: 실제 모평균")
    else:
        st.caption("모평균의 위치를 예상해 본 뒤, 위의 ‘모평균 공개’를 선택해 확인해 보세요.")
    if len(means) == repeats:
        st.info("목표 횟수에 도달했습니다. 처음부터 다시 하거나 설정을 바꿔 비교해 보세요.")

st.caption("같은 조건에서 표본 크기가 커지면 구간이 좁아집니다. 포함 비율은 매번 달라지며 정확히 95%가 되지는 않습니다.")
with st.expander("계산 공식 보기"):
    st.latex(r"\bar{x}\pm 1.96\frac{\sigma}{\sqrt{n}}")
    st.write("고정된 모집단에서 복원추출하며, 모표준편차를 이용해 정규근사 신뢰구간을 계산합니다.")
