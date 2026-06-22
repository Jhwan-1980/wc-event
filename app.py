import streamlit as st
import pandas as pd

st.set_page_config(page_title="예측 이벤트", layout="wide")

# =========================================================
# 상태 초기화
# =========================================================
if "users" not in st.session_state:
    st.session_state.users = {}

if "result" not in st.session_state:
    st.session_state.result = None

if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

if "reset_step" not in st.session_state:
    st.session_state.reset_step = False

if "knox_id" not in st.session_state:
    st.session_state.knox_id = ""


# =========================================================
# 헤더
# =========================================================
st.title("🏆 대한민국 : 남아공 경기 예측 이벤트")


# =========================================================
# Knox ID
# =========================================================
knox_input = st.text_input("Knox ID 입력")

if knox_input:
    st.session_state.knox_id = knox_input

is_admin = st.session_state.knox_id == "jhwan1.choi"


# =========================================================
# 관리자 버튼
# =========================================================
col1, col2 = st.columns([9, 1])

with col2:
    if is_admin:
        if st.button("관리자"):
            st.session_state.admin_mode = True


# =========================================================
# 관리자 패널
# =========================================================
if st.session_state.admin_mode and is_admin:

    st.subheader("🔐 관리자 패널")

    # -------------------------
    # 메인 복귀
    # -------------------------
    if st.button("메인으로 복귀"):
        st.session_state.admin_mode = False

    st.divider()

    # -------------------------
    # 경기 결과 입력
    # -------------------------
    rh = st.number_input("대한민국 스코어", 0, 20, 0)
    ra = st.number_input("남아공 스코어", 0, 20, 0)

    if st.button("결과 확정"):
        st.session_state.result = (rh, ra)
        st.success("결과 저장 완료")

    st.divider()

    # =====================================================
    # 📊 전체 참여자 결과
    # =====================================================
    st.subheader("📊 전체 참여자 결과")

    if st.session_state.users:

        def calc_score(v):
            actual = "WIN" if rh > ra else "DRAW" if rh == ra else "LOSE"

            base = 1 if v["outcome"] == actual else 0

            diff = abs(v["home"] - rh) + abs(v["away"] - ra)

            score = round(base + (10 - diff) * 0.1, 2)

            return score, diff

        rows = []

        for k, v in st.session_state.users.items():
            score, diff = calc_score(v)

            rows.append({
                "참여자 ID": k,
                "승무패": v["outcome"],
                "대한민국 스코어": v["home"],
                "남아공 스코어": v["away"],
                "획득 점수": score
            })

        df = pd.DataFrame(rows)

        df = df.sort_values(by="획득 점수", ascending=False)

        st.dataframe(df, use_container_width=True)

        st.success("결과 저장 완료")

        # =====================================================
        # 🏆 전체 순위 (추가 요청 기능)
        # =====================================================
        st.subheader("🏆 전체 순위")

        rank_df = df.copy()

        # 공동순위 처리 (dense ranking)
        rank_df["순위"] = rank_df["획득 점수"].rank(method="dense", ascending=False).astype(int)

        # 순위 + 점수 기준 정렬
        rank_df = rank_df.sort_values(by=["순위", "획득 점수"], ascending=[True, False])

        st.dataframe(
            rank_df[[
                "순위",
                "참여자 ID",
                "승무패",
                "대한민국 스코어",
                "남아공 스코어",
                "획득 점수"
            ]],
            use_container_width=True
        )

    else:
        st.info("데이터 없음")


    st.divider()

    # =====================================================
    # 🚨 초기화
    # =====================================================
    st.subheader("⚠️ 게임 초기화")

    if st.button("초기화 시작"):
        st.session_state.reset_step = True

    if st.session_state.reset_step:

        st.warning("정말 모든 데이터를 초기화하시겠습니까?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("취소"):
                st.session_state.reset_step = False

        with col2:
            if st.button("확인 후 초기화"):

                st.session_state.users = {}
                st.session_state.result = None
                st.session_state.reset_step = False
                st.session_state.step = 1

                st.success("🔥 초기화 완료 → 시작 화면 복귀")


# =========================================================
# 사용자 화면 (유지)
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

    home = st.number_input("대한민국 스코어", 0, 20)
    away = st.number_input("남아공 스코어", 0, 20)

    if knox_input:

        if st.button("참여 완료"):

            st.session_state.users[st.session_state.knox_id] = {
                "outcome": outcome_map[outcome_kr],
                "home": home,
                "away": away
            }

            st.success("🎉 참여 완료!")

    else:
        st.warning("Knox ID 입력 필요")
