import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="예측 이벤트", layout="wide")

st_autorefresh(interval=5000, key="refresh")

# =========================================================
# 상태 초기화 (핵심 안정 구조)
# =========================================================
if "users" not in st.session_state:
    st.session_state.users = {}

if "result" not in st.session_state:
    st.session_state.result = None

if "admin_view" not in st.session_state:
    st.session_state.admin_view = False

if "knox_id" not in st.session_state:
    st.session_state.knox_id = ""


# =========================================================
# 헤더 (모든 화면 공통 유지)
# =========================================================
st.title("🏆 대한민국 : 남아공 경기 예측 이벤트")


# =========================================================
# Knox ID 입력 (세션 저장 핵심)
# =========================================================
knox_input = st.text_input("Knox ID 입력 후 엔터")

if knox_input:
    st.session_state.knox_id = knox_input


# =========================================================
# 관리자 권한 (세션 기준)
# =========================================================
is_admin = st.session_state.knox_id == "jhwan1.choi"


# =========================================================
# 관리자 버튼 (항상 표시)
# =========================================================
col1, col2 = st.columns([9, 1])

with col2:
    if is_admin:
        if st.button("관리자"):
            st.session_state.admin_view = True


# =========================================================
# =========================================================
# 🧑‍💼 관리자 패널
# =========================================================
# =========================================================
if st.session_state.admin_view and is_admin:

    st.subheader("🔐 관리자 패널")

    # 메인 복귀
    if st.button("메인화면으로 복귀"):
        st.session_state.admin_view = False

    st.divider()

    # -------------------------
    # 경기 결과 입력
    # -------------------------
    rh = st.number_input("한국 득점", 0, 20, 0)
    ra = st.number_input("상대 득점", 0, 20, 0)

    if st.button("결과 확정"):
        st.session_state.result = (rh, ra)
        st.success("결과 저장 완료")

    st.divider()

    # -------------------------
    # 📊 관리자 데이터 테이블
    # -------------------------
    st.subheader("📊 참여 데이터 (Excel View)")

    if st.session_state.users:

        df = pd.DataFrame([
            {
                "Knox ID": k,
                "승/무/패": v["outcome"],
                "한국": v["home"],
                "남아공": v["away"]
            }
            for k, v in st.session_state.users.items()
        ])

        st.dataframe(df, use_container_width=True)

    else:
        st.info("아직 데이터 없음")


# =========================================================
# =========================================================
# 👤 사용자 화면
# =========================================================
# =========================================================
else:

    st.divider()
    st.subheader("📌 승/무/패 입력")

    outcome_map = {
        "승": "WIN",
        "무": "DRAW",
        "패": "LOSE"
    }

    outcome_kr = st.radio("승 / 무 / 패 선택", ["승", "무", "패"])

    st.subheader("⚽ 스코어 입력")

    home = st.number_input("한국 득점", 0, 20)
    away = st.number_input("남아공 득점", 0, 20)


    # -------------------------
    # UX 안내 메시지
    # -------------------------
    st.info("👉 입력 후 반드시 '참여완료' 버튼을 눌러야 제출됩니다.")

    if st.session_state.knox_id:

        st.warning("⚠️ 제출은 Knox ID 기준으로 1회만 기록됩니다.")

        if st.button("🚀 참여 완료", use_container_width=True):

            st.session_state.users[st.session_state.knox_id] = {
                "outcome": outcome_map[outcome_kr],
                "home": home,
                "away": away
            }

            st.success("🎉 참여해주셔서 감사합니다!")

    else:
        st.warning("Knox ID를 먼저 입력하세요")


# =========================================================
# =========================================================
# 🏆 랭킹 시스템
# =========================================================
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
