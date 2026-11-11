import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st


st.title("⑥ 수학 문제와 단계별 피드백")
st.write("탭을 선택해 문제를 풀고, 답에 맞는 피드백을 확인해 보세요.")

expansion_tab, sign_tab, proof_tab, graph_tab, equation_tab, data_tab = st.tabs(
    ["식 전개", "부호 바꾸기", "증명 빈칸", "그래프 읽기", "이차방정식", "Seaborn 그래프"]
)

with expansion_tab:
    st.subheader("다음 식을 전개하면 어떻게 될까요?")
    st.latex(r"(x+3)^2")
    with st.form("form1"):
        answer1 = st.radio(
            "전개한 식을 선택하세요.",
            [r"$x^2 + 9$", r"$x^2 + 3x + 9$", r"$x^2 + 6x + 9$", r"$x^2 + 6x + 6$"],
            index=None,
        )
        submitted1 = st.form_submit_button("내 선택 확인하기")

    if submitted1:
        if answer1 is None:
            st.warning("먼저 식을 하나 선택해 주세요.")
        elif answer1 == r"$x^2 + 9$":
            st.warning("두 괄호 사이에서 곱해지는 항을 더 찾아보세요.")
            st.latex(r"(x+3)(x+3)")
        elif answer1 == r"$x^2 + 3x + 9$":
            st.warning("x와 3을 곱하는 항이 두 개 나옵니다. 두 항을 모두 더해 보세요.")
            st.latex(r"x\cdot3\quad\text{과}\quad3\cdot x")
        elif answer1 == r"$x^2 + 6x + 9$":
            st.success("맞습니다. 괄호의 항을 모두 곱하고 동류항을 모았습니다.")
            st.latex(r"(x+3)^2=x^2+3x+3x+9=x^2+6x+9")
        else:
            st.warning("마지막 상수항은 두 괄호의 3을 곱한 값입니다.")
            st.latex(r"3\times3")

with sign_tab:
    st.subheader("부호가 바뀌면 어떻게 될까요?")
    st.latex(r"(x-3)^2")
    with st.form("form2"):
        answer2 = st.radio(
            "전개한 식을 선택하세요.",
            [r"$x^2 + 6x + 9$", r"$x^2 - 6x - 9$", r"$x^2 - 6x + 9$"],
            index=None,
        )
        submitted2 = st.form_submit_button("변형 문제 확인")

    if submitted2:
        if answer2 is None:
            st.warning("먼저 식을 하나 선택해 주세요.")
        elif answer2 == r"$x^2 + 6x + 9$":
            st.warning("가운데 항은 x와 -3을 곱한 두 항에서 나옵니다. 부호를 살펴보세요.")
            st.latex(r"x\cdot(-3)+(-3)\cdot x")
        elif answer2 == r"$x^2 - 6x - 9$":
            st.warning("상수항은 음수끼리 곱한 값입니다.")
            st.latex(r"(-3)\times(-3)")
        else:
            st.success("맞습니다. 가운데 항은 음수이고 상수항은 양수입니다.")
            st.latex(r"(x-3)^2=x^2-3x-3x+9=x^2-6x+9")

with proof_tab:
    st.subheader("증명 빈칸 채우기: √2는 유리수가 아니다")
    if "proof_answers" not in st.session_state:
        st.session_state.proof_answers = []

    with st.form("proof_reset"):
        submitted_reset = st.form_submit_button("증명 처음부터 다시 하기")
    if submitted_reset:
        st.session_state.proof_answers = []

    step = len(st.session_state.proof_answers)
    st.progress(step / 7, text=f"채운 빈칸: {step} / 7")
    prompts = [
        ("√2가", "라고 가정한다."),
        ("양변을 제곱하면 n² =", "이다."),
        ("n²이", "이므로 n도 짝수이다."),
        ("n = 2k를 대입하면 m² =", "이다."),
        ("m²이", "이므로 m도 짝수이다."),
        ("m, n은 모두 짝수이므로 공약수", "를 가져 서로소라는 가정에 모순이다."),
        ("따라서 √2는", "이다."),
    ]

    for i in range(7):
        if step == i:
            with st.form(f"proof_step_{i}"):
                before, after = prompts[i]
                st.write(before)
                answer3 = st.text_input("빈칸에 들어갈 말", key=f"proof_answer_{i}")
                st.write(after)
                submitted3 = st.form_submit_button("다음 문장으로")
            if submitted3:
                if answer3.strip():
                    st.session_state.proof_answers.append(answer3.strip())
                    st.rerun()
                else:
                    st.warning("빈칸을 채워 주세요.")

with graph_tab:
    st.subheader("그래프로 공의 움직임 읽기")
    st.write("공의 높이를 시간에 따라 나타낸 그래프입니다.")
    time = np.linspace(0, 6, 61)
    height = -(time - 3) ** 2 + 9
    graph_data = pd.DataFrame({"시간 (초)": time, "높이 (m)": height})
    st.line_chart(graph_data.set_index("시간 (초)"))
    with st.form("form4"):
        answer4 = st.radio(
            "공이 올라가는 시간 구간을 고르세요.",
            ["0초부터 3초까지", "3초부터 6초까지", "0초부터 6초까지"],
            index=None,
        )
        submitted4 = st.form_submit_button("그래프 답 확인하기")

    if submitted4:
        if answer4 is None:
            st.warning("공이 올라가는 시간 구간을 선택해 주세요.")
        elif answer4 == "0초부터 3초까지":
            st.success("맞습니다. 꼭짓점에 도달할 때까지 공의 높이가 증가합니다.")
            st.latex(r"0\leq t<3")
        elif answer4 == "3초부터 6초까지":
            st.warning("꼭짓점 뒤에는 그래프가 내려갑니다. 꼭짓점의 왼쪽을 살펴보세요.")
        else:
            st.warning("공은 꼭대기에 도달한 뒤 다시 내려옵니다. 그래프가 올라가는 구간만 고르세요.")

with equation_tab:
    st.subheader("숫자가 바뀌는 이차방정식")
    if "equation_id" not in st.session_state:
        st.session_state.equation_id = 0
        st.session_state.roots = sorted(random.sample(range(-5, 6), 2))

    with st.form("new_equation"):
        submitted5 = st.form_submit_button("새 문제 만들기")
    if submitted5:
        st.session_state.equation_id += 1
        st.session_state.roots = sorted(random.sample(range(-5, 6), 2))

    root_a, root_b = st.session_state.roots
    middle = -(root_a + root_b)
    constant = root_a * root_b
    st.latex(rf"x^2 {middle:+}x {constant:+}=0")

    with st.form(f"equation_answer_{st.session_state.equation_id}"):
        answer6a = st.number_input("첫 번째 해", value=None, step=1, key=f"root_a_{st.session_state.equation_id}")
        answer6b = st.number_input("두 번째 해", value=None, step=1, key=f"root_b_{st.session_state.equation_id}")
        submitted6 = st.form_submit_button("해 확인하기")

    if submitted6:
        if answer6a is None or answer6b is None:
            st.warning("두 해를 모두 입력해 주세요.")
        elif {answer6a, answer6b} == {root_a, root_b}:
            st.success("맞습니다. 두 값을 방정식에 대입하면 모두 0이 됩니다.")
            st.latex(rf"(x {(-root_a):+})(x {(-root_b):+})=0")
        elif answer6a in (root_a, root_b) or answer6b in (root_a, root_b):
            st.warning("한 해는 찾았습니다. 인수분해의 다른 인수도 0이 되는 값을 찾아보세요.")
        else:
            st.warning("인수분해한 두 괄호를 각각 0으로 놓아 해를 찾아보세요.")

with data_tab:
    st.subheader("Seaborn으로 펭귄 데이터 살펴보기")

    @st.cache_data
    def load_penguins():
        return sns.load_dataset("penguins")

    try:
        penguins = load_penguins()
    except Exception as error:
        st.error("펭귄 자료를 불러오지 못했습니다. 데이터 제공 사이트에 연결할 수 있는지 확인해 주세요.")
        st.stop()

    st.write("세 종의 펭귄 몸무게 자료를 비교합니다.")
    st.dataframe(penguins.head(8), hide_index=True)

    body_mass = penguins.dropna(subset=["species", "body_mass_g"])
    means = body_mass.groupby("species")["body_mass_g"].mean().sort_values(ascending=False)
    st.write(f"몸무게가 기록된 펭귄: {len(body_mass)}마리")

    figure, axis = plt.subplots()
    sns.boxplot(data=body_mass, x="species", y="body_mass_g", ax=axis, showmeans=True)
    axis.set_xlabel("Species")
    axis.set_ylabel("Body mass (g)")
    st.pyplot(figure)
    plt.close(figure)

    st.write("종별 평균 몸무게 (g)")
    st.dataframe(means.rename("평균 몸무게 (g)").round(1))

    with st.form("penguin_question"):
        answer7 = st.radio(
            "평균 몸무게가 가장 큰 종을 고르세요.",
            ["Adelie", "Chinstrap", "Gentoo"],
            index=None,
        )
        submitted7 = st.form_submit_button("자료를 보고 답하기")

    if submitted7:
        if answer7 is None:
            st.warning("종을 하나 선택해 주세요.")
        elif answer7 == means.index[0]:
            st.success("맞습니다. 몸무게가 기록된 자료에서 평균이 가장 큰 종입니다.")
            st.write(f"평균 몸무게는 {means.iloc[0]:.1f} g입니다.")
        else:
            st.warning("상자그림의 위치와 종별 평균을 비교해 다시 살펴보세요.")
