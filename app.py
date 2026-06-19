import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="예측 이벤트", layout="wide")

st_autorefresh(interval=5000, key="refresh")

# -------------------------
# 상태
# -------------------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "submitted" not in st.session_state:
    st.session_state.submitted = {}

if "result" not in st.session_state:
    st.session_state.result = None


# -------------------------
# 헤더 + 관리자 버튼 (우측 상단)
# -------------------------
col1, col2 = st.columns([9, 1])

with col1:
    st.title("⚽ 대한민국 : 남아공 경기 예측 이벤트")

with col2:
    admin_mode = st.button("관리자")


# -------------------------
# 관리자 영역
# -------------------------
if admin_mode:
    st.subheader("🔧 관리자 - 경기 결과 입력")

    rh = st.number_input("실제 한국 득점", 0, 20, 0)
    ra = st.number_input("실제 상대 득점", 0, 20, 0)

    if st.button("결과 확정"):
        st.session_state.result = (rh, ra)
        st.success("결과 저장 완료")


# -------------------------
# 사용자 입력
# -------------------------
st.divider()
st.subheader("📌 승/무/패 입력")

email = st.text_input("사내 이메일 입력")

outcome = st.radio("승/무/패 선택", ["WIN", "DRAW", "LOSE"])

st.subheader("⚽ 스코어 입력")

home = st.number_input("한국 득점", 0, 20)
away = st.number_input("상대 득점", 0, 20)


# -------------------------
# 제출 가능 여부
# -------------------------
can_submit = email != ""


# -------------------------
# 제출
# -------------------------
if st.button("참여 완료", disabled=not can_submit):

    st.session_state.users[email] = {
        "outcome": outcome,
        "home": home,
        "away": away
    }

    st.success("🎉 참여해주셔서 감사합니다!")


# -------------------------
# 랭킹 계산
# -------------------------
def get_outcome(h, a):
    if h > a:
        return "WIN"
    elif h == a:
        return "DRAW"
    else:
        return "LOSE"


if st.session_state.result:
    st.subheader("🏆 TOP 10")

    rh, ra = st.session_state.result
    actual = get_outcome(rh, ra)

    rows = []

    for email, v in st.session_state.users.items():

        pred_outcome = v["outcome"]
        score_diff = abs(v["home"] - rh) + abs(v["away"] - ra)

        rows.append({
            "email": email,
            "match": pred_outcome == actual,
            "diff": score_diff
        })

    df = pd.DataFrame(rows)

    df = df.sort_values(by=["match", "diff"], ascending=[False, True])

    st.dataframe(df.head(10), use_container_width=True)
