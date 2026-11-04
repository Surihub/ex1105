import math
import random
import statistics

import pandas as pd
import streamlit as st


st.title("④ 확률과 통계 실험실")
st.caption("랜덤 실험을 반복하고, 자료를 더할 때 통계량이 어떻게 달라지는지 관찰해 보세요.")

tab_balls, tab_coins, tab_dice, tab_data = st.tabs(
    ["공 무작위 추출", "동전 던지기", "주사위 두 개", "자료와 평균·중앙값"]
)

with tab_balls:
    st.subheader("주머니에서 빨간 공이 나올 확률")
    st.write("주머니 구성을 정하고 여러 번 추출해, ‘빨간 공이 한 번 이상 나올’ 이론적 확률과 실험 결과를 비교합니다.")
    red_col, blue_col, yellow_col = st.columns(3)
    with red_col:
        red = st.number_input("🔴 빨간 공", 1, 20, 4, key="bag_red")
    with blue_col:
        blue = st.number_input("🔵 파란 공", 0, 20, 3, key="bag_blue")
    with yellow_col:
        yellow = st.number_input("🟡 노란 공", 0, 20, 3, key="bag_yellow")
    population = int(red + blue + yellow)
    draw_n = st.slider("한 번에 뽑는 공 수", 1, population, min(2, population), key="bag_draw_n")
    replacement = st.checkbox("뽑은 공을 다시 넣기", value=False, key="bag_replacement")
    trials = st.select_slider("반복 실험 수", [50, 100, 500, 1000, 5000], value=500, key="bag_trials")

    if st.button("추출 실험 실행", key="run_bag"):
        bag = ["빨강"] * int(red) + ["파랑"] * int(blue) + ["노랑"] * int(yellow)
        hit_count = 0
        color_totals = {"빨강": 0, "파랑": 0, "노랑": 0}
        for _ in range(trials):
            sample = (random.choices(bag, k=draw_n) if replacement
                      else random.sample(bag, k=draw_n))
            hit_count += "빨강" in sample
            for color in color_totals:
                color_totals[color] += sample.count(color)
        p_theory = (1 - (1 - red / population) ** draw_n if replacement
                    else 1 - math.comb(population - int(red), draw_n) / math.comb(population, draw_n))
        st.session_state.bag_result = {
            "hit_count": hit_count, "trials": trials, "p_theory": p_theory,
            "color_totals": color_totals, "draw_n": draw_n, "replacement": replacement,
        }

    if "bag_result" in st.session_state:
        result = st.session_state.bag_result
        observed = result["hit_count"] / result["trials"]
        m1, m2, m3 = st.columns(3)
        m1.metric("빨간 공 포함", f"{result['hit_count']} / {result['trials']}")
        m2.metric("실험 확률", f"{observed:.1%}")
        m3.metric("이론적 확률", f"{result['p_theory']:.1%}", delta=f"{observed-result['p_theory']:+.1%}")
        chart_col, stats_col = st.columns([1.4, 1])
        with chart_col:
            st.write("빨간 공이 한 번 이상 나올 확률")
            st.bar_chart(pd.DataFrame({"확률": [observed, result["p_theory"]]}, index=["실험", "이론값"]))
        with stats_col:
            st.write("전체 실험에서 뽑힌 색깔별 공 수")
            st.bar_chart(pd.DataFrame({"추출 횟수": result["color_totals"]}))

with tab_coins:
    st.subheader("동전 던지기")
    st.write("한 실험에서 동전을 여러 번 던집니다. 앞면이 나온 횟수의 분포를 이항분포의 이론값과 비교합니다.")
    c1, c2 = st.columns(2)
    with c1:
        tosses = st.slider("한 실험의 던지기 횟수", 1, 30, 10, key="coin_tosses")
    with c2:
        experiments = st.select_slider("반복 실험 수", [50, 100, 500, 1000, 5000], value=500, key="coin_experiments")

    if st.button("동전 실험 실행", key="run_coin"):
        heads = [sum(random.randint(0, 1) for _ in range(tosses)) for _ in range(experiments)]
        st.session_state.coin_result = {"heads": heads, "tosses": tosses}

    if "coin_result" in st.session_state:
        result = st.session_state.coin_result
        values = result["heads"]
        n = result["tosses"]
        observed_mean = statistics.mean(values)
        expected_mean = n / 2
        observed_sd = statistics.pstdev(values)
        expected_sd = math.sqrt(n / 4)
        m1, m2, m3 = st.columns(3)
        m1.metric("앞면 횟수 평균", f"{observed_mean:.2f}", delta=f"이론 평균 {expected_mean:.2f}")
        m2.metric("표준편차", f"{observed_sd:.2f}", delta=f"이론 {expected_sd:.2f}")
        m3.metric("반복 횟수", len(values))
        counts = pd.Series(values).value_counts().reindex(range(n + 1), fill_value=0)
        probabilities = [math.comb(n, k) / (2 ** n) for k in range(n + 1)]
        comparison = pd.DataFrame({
            "실험 비율": counts.to_numpy() / len(values),
            "이론적 확률": probabilities,
        }, index=[f"앞면 {k}회" for k in range(n + 1)])
        st.write("앞면 횟수의 실험 분포와 이론적 이항분포")
        st.bar_chart(comparison)

with tab_dice:
    st.subheader("주사위 두 개의 눈 합")
    st.write("두 주사위 눈의 합이 2부터 12까지 어떻게 분포하는지 살펴봅니다.")
    dice_trials = st.select_slider("주사위 시행 횟수", [50, 100, 500, 1000, 5000, 10000], value=1000, key="dice_trials")
    if st.button("주사위 굴리기", key="run_dice"):
        sums = [random.randint(1, 6) + random.randint(1, 6) for _ in range(dice_trials)]
        st.session_state.dice_result = sums

    if "dice_result" in st.session_state:
        values = st.session_state.dice_result
        counts = pd.Series(values).value_counts().reindex(range(2, 13), fill_value=0)
        theory = [sum(1 for x in range(1, 7) for y in range(1, 7) if x + y == total) / 36 for total in range(2, 13)]
        observed = counts.to_numpy() / len(values)
        m1, m2, m3 = st.columns(3)
        m1.metric("실험 평균", f"{statistics.mean(values):.3f}", delta=f"이론 평균 7.000")
        m2.metric("실험 표준편차", f"{statistics.pstdev(values):.3f}", delta=f"이론 {math.sqrt(35/6):.3f}")
        m3.metric("시행 횟수", len(values))
        comparison = pd.DataFrame({"실험 비율": observed, "이론적 확률": theory}, index=range(2, 13))
        st.write("합계별 확률 비교")
        st.bar_chart(comparison)
        st.caption("7이 가장 자주 나오는 까닭은 합이 7이 되는 주사위 조합이 가장 많기 때문입니다.")

with tab_data:
    st.subheader("자료를 더하면 평균과 중앙값은 어떻게 변할까요?")
    st.write("숫자를 하나씩 추가하고, 새 자료가 평균과 중앙값에 미치는 영향을 확인해 보세요.")
    if "number_data" not in st.session_state:
        st.session_state.number_data = [4, 5, 5, 6, 7]
    if "number_data_change" not in st.session_state:
        st.session_state.number_data_change = None
    entry_col, action_col = st.columns([1, 1])
    with entry_col:
        new_value = st.number_input("추가할 자료", min_value=-1000.0, max_value=1000.0, value=20.0, step=1.0, key="new_data_value")
    with action_col:
        st.write("")
        st.write("")
        add_col, outlier_col, clear_col = st.columns(3)
        with add_col:
            add_data = st.button("자료 추가", type="primary", use_container_width=True)
        with outlier_col:
            add_extreme = st.button("큰 값 추가", use_container_width=True)
        with clear_col:
            clear_data = st.button("초기화", use_container_width=True)

    if add_data or add_extreme:
        previous = st.session_state.number_data.copy()
        value_to_add = 100.0 if add_extreme else new_value
        before_mean = statistics.mean(previous) if previous else None
        before_median = statistics.median(previous) if previous else None
        st.session_state.number_data.append(value_to_add)
        after = st.session_state.number_data
        st.session_state.number_data_change = {
            "value": value_to_add,
            "before_mean": before_mean,
            "before_median": before_median,
            "mean_delta": statistics.mean(after) - before_mean if before_mean is not None else None,
            "median_delta": statistics.median(after) - before_median if before_median is not None else None,
        }
    if clear_data:
        st.session_state.number_data = []
        st.session_state.number_data_change = None

    data = st.session_state.number_data
    if data:
        mean_value = statistics.mean(data)
        median_value = statistics.median(data)
        m1, m2, m3 = st.columns(3)
        change = st.session_state.number_data_change
        m1.metric("자료 개수", len(data))
        m2.metric("평균", f"{mean_value:.2f}",
                  delta=f"추가 후 {change['mean_delta']:+.2f}" if change and change["mean_delta"] is not None else None)
        m3.metric("중앙값", f"{median_value:.2f}",
                  delta=f"추가 후 {change['median_delta']:+.2f}" if change and change["median_delta"] is not None else None)
        if change:
            st.caption(
                f"{change['value']:g}을 추가했습니다. "
                + (f"평균은 {change['before_mean']:.2f} → {mean_value:.2f}, 중앙값은 {change['before_median']:.2f} → {median_value:.2f}로 바뀌었습니다."
                   if change["before_mean"] is not None else "첫 자료가 추가되었습니다.")
            )
        chart_col, detail_col = st.columns([1.5, 1])
        with chart_col:
            st.write("값별 등장 횟수")
            frequencies = pd.Series(data).value_counts().sort_index()
            st.bar_chart(pd.DataFrame({"횟수": frequencies}))
        with detail_col:
            st.write("현재 자료")
            st.dataframe(pd.DataFrame({"순서": range(1, len(data) + 1), "값": data}), hide_index=True, height=250)
        st.caption("평균은 모든 값의 합을 자료 개수로 나누므로 큰 값의 영향을 크게 받습니다. 중앙값은 정렬했을 때 가운데 값이라 극단적인 값에 덜 흔들립니다.")
    else:
        st.info("자료가 없습니다. 숫자를 추가해 보세요.")
