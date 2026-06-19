import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="예측 이벤트", layout="wide")

st_autorefresh(interval=5000, key="refresh")

# ---------------------------
# 상태
# ---------------------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "result" not in st.session_state:
    st.session_state.result = None

if "admin_view" not in st.session_state:
    st.session_state.admin_view = False


# ---------------------------
# 헤더
# ---------------------------
col1, col2 = st.columns([9, 1])

with col1:
    st.title("🏆 대한민국 : 남아공 경기 예측 이벤트")

with col2:
    st.session_state.admin_view = False


# ---------------------------
# Knox ID 입력
# ---------------------------
knox_id = st.text_input("Knox ID 입력")


# ---------------------------
# 관리자 권한 체크
# ---------------------------
is_admin = (knox_id == "jhwan1.choi")


if is_admin:
    if st.button("관리자 모드"):
        st.session_state.admin_view = True


# ---------------------------
# 관리자 화면
# ---------------------------
if st.session_state.admin_view and is_admin:

    st.subheader("🔐 관리자 패널")

    if st.button("메인화면으로 복귀"):
        st.session_state.admin_view = False

    st.divider()

    # 결과 입력
    rh = st.number_input("한국 득점", 0, 20, 0)
    ra = st.number_input("상대 득점", 0, 20, 0)

    if st.button("결과 확정"):
        st.session_state.result = (rh, ra)
        st.success("결과 저장 완료")

    st.divider()

    # 📊 엑셀 형태 데이터
    st.subheader("📊 참여 데이터 (Excel View)")

    df = pd.DataFrame([
        {
            "Knox ID": k,
            "승/무/패": v["outcome"],
            "한국": v["home"],
            "상대": v["away"]
        }
        for k, v in st.session_state.users.items()
    ])

    st.dataframe(df, use_container_width=True)


# ---------------------------
# 사용자 화면
# ---------------------------
else:

    st.divider()
    st.subheader("📌 승/무/패 입력")

    outcome_map = {
        "승": "WIN",
        "무": "DRAW",
        "패": "LOSE"
    }

    outcome_kr = st.radio(
        "승/무/패 선택",
        ["승", "무", "패"]
    )

    st.subheader("⚽ 스코어 입력")

    home = st.number_input("한국 득점", 0, 20)
    away = st.number_input("상대 득점", 0, 20)


    can_submit = knox_id != ""

    if st.button("참여 완료", disabled=not can_submit):

        st.session_state.users[knox_id] = {
            "outcome": outcome_map[outcome_kr],
            "home": home,
            "away": away
        }

        st.success("🎉 참여해주셔서 감사합니다!")


# ---------------------------
# 랭킹
# ---------------------------
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

    for k, v in st.session_state.users.items():

        diff = abs(v["home"] - rh) + abs(v["away"] - ra)

        rows.append({
            "Knox ID": k,
            "match": v["outcome"] == actual,
            "diff": diff
        })

    df = pd.DataFrame(rows)

    df = df.sort_values(by=["match", "diff"], ascending=[False, True])

    st.dataframe(df.head(10), use_container_width=True)
