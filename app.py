import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

ALLOWED_DOMAIN = "ax.samsung.com"

st.set_page_config(page_title="WC Prediction", layout="wide")

st_autorefresh(interval=5000, key="refresh")

if "users" not in st.session_state:
    st.session_state.users = {}

if "result" not in st.session_state:
    st.session_state.result = None


st.title("⚽ 대한민국 경기 예측 이벤트")

email = st.text_input("사내 이메일 입력")

if email:
    if not email.endswith(ALLOWED_DOMAIN):
        st.error("사내 이메일만 사용 가능합니다.")
        st.stop()

    st.success("로그인 완료")

    if email not in st.session_state.users:
        st.subheader("예측 입력")

        home = st.number_input("한국 득점", 0, 20, key=email+"_h")
        away = st.number_input("상대 득점", 0, 20, key=email+"_a")

        if st.button("제출"):
            st.session_state.users[email] = {
                "home": home,
                "away": away
            }
            st.success("제출 완료")
    else:
        st.info("이미 제출 완료")


st.divider()
st.subheader("관리자")

rh = st.number_input("실제 한국 득점", key="rh")
ra = st.number_input("실제 상대 득점", key="ra")

if st.button("결과 확정"):
    st.session_state.result = (rh, ra)
    st.success("결과 저장 완료")


def outcome(h, a):
    return "WIN" if h > a else "DRAW" if h == a else "LOSE"


if st.session_state.result:
    st.subheader("🏆 TOP 10")

    rh, ra = st.session_state.result
    actual = outcome(rh, ra)

    rows = []

    for email, v in st.session_state.users.items():
        pred = outcome(v["home"], v["away"])
        diff = abs(v["home"] - rh) + abs(v["away"] - ra)

        rows.append([email, pred == actual, diff])

    df = pd.DataFrame(rows, columns=["email", "match", "diff"])
    df = df.sort_values(by=["match", "diff"], ascending=[False, True])

    st.dataframe(df.head(10), use_container_width=True)