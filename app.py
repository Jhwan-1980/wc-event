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

if "reset_confirm" not in st.session_state:
    st.session_state.reset_confirm = False


# ---------------------------
# 헤더
# ---------------------------
col1, col2 = st.columns([9, 1])

with col1:
    st.title("🏆 대한민국 : 남아공 경기 예측 이벤트")

with col2:
    if st.button("관리자"):
        st.session_state.admin_view = True


# ---------------------------
# Knox ID 입력 (변경 요청 반영)
# ---------------------------
knox_id = st.text_input("Knox ID 입력 후 엔터")


is_admin = (knox_id == "jhwan1.choi")


# =========================================================
# 사용자 화면
# =========================================================
if not (st.session_state.admin_view and is_admin):

    st.divider()

    st.subheader("📌 승/무/패 입력")

    outcome_map = {
        "승": "WIN",
        "무": "DRAW",
        "패": "LOSE"
    }

    outcome_kr = st.radio(
        "승 / 무 / 패 선택",
        ["승", "무", "패"]
    )

    st.subheader("⚽ 스코어 입력")

    home = st.number_input("한국 득점", 0, 20)
    away = st.number_input("상대 득점", 0, 20)

    # ---------------------------
    # UX 강화 메시지
    # ---------------------------
    st.info("👉 입력이 완료되면 아래 '참여완료' 버튼을 눌러 제출해주세요!")

    if knox_id:

        st.warning("⚠️ 참여는 반드시 '참여완료' 버튼 클릭 후 최종 제출됩니다.")

        # ---------------------------
        # 버튼 스타일 강화 (CSS)
        # ---------------------------
        st.markdown("""
            <style>
            div.stButton > button {
                background-color: #1f77b4;
                color: white;
                height: 60px;
                font-size: 22px;
                font-weight: bold;
                border-radius: 10px;
            }
            div.stButton > button:hover {
                background-color: #0d5fa0;
                color: white;
            }
            </style>
        """, unsafe_allow_html=True)

        if st.button("🚀 참여 완료", use_container_width=True):

            st.session_state.users[knox_id] = {
                "outcome": outcome_map[outcome_kr],
                "home": home,
                "away": away
            }

            st.success("🎉 참여해주셔서 감사합니다!")

    else:
        st.warning("Knox ID를 입력하세요")


# =========================================================
# 관리자 화면 (기존 유지)
# =========================================================
else:

    st.subheader("🔐 관리자 패널")

    if st.button("메인화면으로 복귀"):
        st.session_state.admin_view = False

    st.divider()

    rh = st.number_input("한국 득점", 0, 20, 0)
    ra = st.number_input("상대 득점", 0, 20, 0)

    if st.button("결과 확정"):
        st.session_state.result = (rh, ra)
        st.success("결과 저장 완료")


# =========================================================
# 랭킹
# =========================================================
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
            "승부 적중": v["outcome"] == actual,
            "오차": diff
        })

    df = pd.DataFrame(rows)

    df = df.sort_values(by=["승부 적중", "오차"], ascending=[False, True])

    st.dataframe(df.head(10), use_container_width=True)
