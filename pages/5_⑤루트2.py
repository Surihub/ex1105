import pandas as pd
import streamlit as st


def long_division(a, b):
    """정수 부분, 나눗셈 단계, 순환 시작 위치를 구합니다."""
    whole, remainder = divmod(a, b)
    rows = []
    seen = {remainder: 0}
    start = None
    while remainder:
        dividend = remainder * 10
        quotient, remainder = divmod(dividend, b)
        rows.append((dividend, quotient, remainder))
        if remainder in seen:
            start = seen[remainder]
            break
        seen[remainder] = len(rows)
    return whole, rows, start


st.title("분수를 소수로 나타내기")
st.write("다음 몫과 나머지를 구하고, 나머지에서 소수의 규칙을 찾아보세요.")
st.caption("1/4, 1/3, 1/6, 1/7을 비교해 보세요.")

if "log" not in st.session_state:
    st.session_state.log = []

left, right = st.columns(2)
a = left.number_input("분자", min_value=1, max_value=1000, value=1, step=1)
b = right.number_input("분모", min_value=2, max_value=1000, value=7, step=1)

activity = st.session_state.get("division_activity")
if activity and activity["fraction"] != (a, b):
    del st.session_state.division_activity
    activity = None

if activity is None:
    with st.form("division_prediction"):
        prediction = st.radio(
            "이 분수의 소수 전개는 어떻게 될까요?",
            ["끝날 것 같습니다", "같은 숫자 묶음이 반복될 것 같습니다"],
            index=None,
        )
        begin = st.form_submit_button("예상하고 시작하기")
    if begin:
        if prediction is None:
            st.warning("예상을 하나 골라 주세요. 틀려도 괜찮습니다.")
        else:
            whole, rows, start = long_division(a, b)
            run_id = st.session_state.get("division_run_id", 0) + 1
            st.session_state.division_run_id = run_id
            st.session_state.division_activity = {
                "fraction": (a, b), "prediction": prediction,
                "whole": whole, "rows": rows, "start": start,
                "solved": 0, "finished": False, "run_id": run_id,
            }
            st.rerun()

if activity is not None:
    whole, rows, start = activity["whole"], activity["rows"], activity["start"]
    solved = activity["solved"]
    st.caption(f"처음 예상: {activity['prediction']}")
    st.write(f"정수 부분은 {whole}, 처음 나머지는 {a % b}입니다.")

    if solved:
        st.subheader("직접 구한 나눗셈")
        table = pd.DataFrame(rows[:solved], columns=["이전 나머지 × 10", "몫", "새 나머지"])
        table.index = range(1, solved + 1)
        st.dataframe(table)
        st.write(f"지금까지 구한 값: {whole}." + "".join(str(q) for _, q, _ in rows[:solved]))

    if solved < len(rows):
        remainder = a % b if solved == 0 else rows[solved - 1][2]
        st.subheader(f"{solved + 1}번째 자리 구하기")
        st.write(f"현재 나머지는 {remainder}입니다. {remainder} × 10을 {b}로 나누어 보세요.")
        with st.form(f"division_step_{activity['run_id']}_{solved}"):
            left, right = st.columns(2)
            quotient_answer = left.number_input("다음 몫 (0~9)", min_value=0, max_value=9, value=None, step=1)
            remainder_answer = right.number_input("다음 나머지", min_value=0, max_value=b - 1, value=None, step=1)
            check = st.form_submit_button("확인하고 한 줄 진행하기")
        if check:
            if quotient_answer is None or remainder_answer is None:
                st.warning("몫과 나머지를 모두 입력해 주세요.")
            elif (quotient_answer, remainder_answer) != rows[solved][1:]:
                st.warning(f"다시 계산해 보세요. {b} × 몫 + 나머지 = {remainder * 10}이어야 합니다.")
            else:
                activity["solved"] += 1
                st.rerun()
        with st.expander("계산이 막히면 힌트"):
            st.write("나머지에 10을 곱한 수 안에 분모가 몇 번 들어가는지 구하세요. 남은 수가 새 나머지입니다.")

    elif not activity["finished"]:
        st.subheader("나머지에서 규칙 찾기")
        st.write("마지막 나머지를 처음 나머지 및 앞선 줄의 나머지와 비교해 보세요.")
        with st.form(f"division_conclusion_{activity['run_id']}"):
            conclusion = st.radio(
                "나눗셈을 마무리할 수 있는 까닭은?",
                ["나머지가 0이 되었습니다", "앞에서 나온 나머지가 다시 나왔습니다"],
                index=None,
            )
            period_answer = st.text_input("순환마디를 찾아 쓰세요. 끝나는 소수라면 '없음'을 쓰세요.")
            start_answer = st.number_input(
                "반복이 시작되는 소수 몇 번째 자리인가요? 끝나는 소수라면 0을 쓰세요.",
                min_value=0, max_value=max(1, len(rows)), value=None, step=1,
            )
            finish = st.form_submit_button("판단 확인하고 결과 정리하기")
        if finish:
            expected = "나머지가 0이 되었습니다" if start is None else "앞에서 나온 나머지가 다시 나왔습니다"
            expected_period = "없음" if start is None else "".join(str(q) for _, q, _ in rows[start:])
            expected_start = 0 if start is None else start + 1
            if conclusion is None or not period_answer.strip() or start_answer is None:
                st.warning("까닭을 고르고, 순환마디와 반복이 시작되는 자리를 입력해 주세요.")
            elif conclusion != expected:
                st.warning("마지막 나머지가 0인지, 앞서 나왔던 수인지 다시 살펴보세요. 처음 나머지도 포함해서 비교해 보세요.")
            elif period_answer.strip() != expected_period or start_answer != expected_start:
                st.warning("같은 나머지 다음에는 같은 몫이 나옵니다. 같은 나머지가 처음 나온 곳 바로 다음 자리부터 몫을 읽어 보세요. 나머지가 0이면 순환마디는 '없음', 시작 자리는 0입니다.")
            else:
                activity["finished"] = True
                st.rerun()

    if activity["finished"]:
        digits = [str(q) for _, q, _ in rows]
        if start is None:
            decimal = f"{whole}." + ("".join(digits) or "0")
            period, kind = "", "유한소수"
            st.success("나머지가 0이 되어 나눗셈이 끝납니다.")
        else:
            nonrep = "".join(digits[:start])
            period = "".join(digits[start:])
            decimal = f"{whole}.{nonrep}{period}{period}…"
            kind = "순환소수"
            st.success(f"같은 나머지가 다시 나왔습니다. {start + 1}번째 자리부터 {len(period)}자리가 반복됩니다.")
        st.write(f"{a}/{b} = {decimal} ({kind})")
        predicted_finite = activity["prediction"] == "끝날 것 같습니다"
        st.info("처음 예상과 같습니다." if predicted_finite == (start is None) else "처음 예상과 다릅니다. 어떤 나머지에서 생각이 바뀌었는지 돌아보세요.")
        item = {"분수": f"{a}/{b}", "소수": decimal, "순환마디": period or "없음", "마디 길이": len(period)}
        if item not in st.session_state.log:
            st.session_state.log.append(item)
        st.subheader("설명하기")
        st.text_area("같은 나머지가 나오면, 그다음 몫과 나머지도 같아지는 까닭은 무엇인가요?", key=f"reason_{activity['run_id']}")
        st.text_area(f"분모가 {b}일 때 0이 아닌 나머지는 몇 가지인가요? 순환마디의 길이와 연결해 설명해 보세요.", key=f"period_reason_{activity['run_id']}")

    if st.button("같은 분수 다시 풀기"):
        del st.session_state.division_activity
        st.rerun()

if st.session_state.log:
    with st.expander("완료한 분수 기록 보기"):
        st.dataframe(pd.DataFrame(st.session_state.log), hide_index=True)
        st.caption("1/3과 1/6의 순환마디와 반복이 시작되는 자리를 각각 비교해 보세요.")
