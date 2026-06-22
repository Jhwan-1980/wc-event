import streamlit as st
import pandas as pd

st.set_page_config(page_title="예측 이벤트", layout="wide")

# =========================================================
# 상태 초기화
# =========================================================
if "step" not in st.session_state:
    st.session_state.step = 1

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
# 헤더 (항상 고정)
# =========================================================
st.title("🏆 대한민국 : 남아공 경기 예측 이벤트")


# =========================================================
# 관리자 판별
# =========================================================
is_admin = (st.session_state.knox_id == "jhwan1.choi")


# =========================================================
# 관리자 버튼 (항상 표시)
# =========================================================
col1, col2 = st.columns([9, 1])

with col2:
    if is_admin:
        if st.button("관리자"):
            st.session_state.admin_mode = True


# =========================================================
# =========================================================
# 🔐 관리자 화면 (STEP 99)
# =========================================================
# =========================================================
if st.session_state.admin_mode and is_admin:

    st.subheader("🔐 관리자 패널")

    # 메인 복귀
    if st.button("메인으로 복귀"):
        st.session_state.admin_mode = False

    st.divider()

    # ================================
    # 📊 전체 결과 (항상 표시)
    # ================================
    st.subheader("📊 전체 참여자 결과")

    if st.session_state.users:

        rows = []

        for k, v in st.session_state.users.items():

            rows.append({
                "참여자 ID": k,
                "승무패": v["outcome"],
                "대한민국 스코어": v["home"],
                "남아공 스코어": v["away"],
            })

        df = pd.DataFrame(rows)

        st.dataframe(df, use_container_width=True)

    else:
        st.info("데이터 없음")

    st.divider()

    # ================================
    # 🧮 경기 결과 입력 (선택)
    # ================================
    rh = st.number_input("대한민국 스코어", 0, 20, 0)
    ra = st.number_input("남아공 스코어", 0, 20, 0)

    if st.button("결과 확정"):
        st.session_state.result = (rh, ra)
        st.success("결과 저장 완료")

    st.divider()

    # ================================
    # 🚨 초기화 (2단계)
    # ================================
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
                st.session_state.step = 1   # ⭐ 핵심: 자동 시작화면 복귀

                st.success("🔥 초기화 완료 → 자동으로 시작 화면으로 이동")


# =========================================================
# =========================================================
# 👤 사용자 STEP FLOW
# =========================================================
# =========================================================

elif st.session_state.step == 1:

    st.subheader("1️⃣ Knox ID 입력")

    knox = st.text_input("Knox ID")

    if st.button("다음"):
        if knox:
            st.session_state.knox_id = knox
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Knox ID 입력 필요")


elif st.session_state.step == 2:

    st.subheader("2️⃣ 승 / 무 / 패 선택")

    choice = st.radio("선택", ["승", "무", "패"])

    if st.button("다음"):
        st.session_state.choice = choice
        st.session_state.step = 3
        st.rerun()

    if st.button("이전"):
        st.session_state.step = 1
        st.rerun()


elif st.session_state.step == 3:

    st.subheader("3️⃣ 스코어 입력")

    home = st.number_input("대한민국", 0, 20)
    away = st.number_input("남아공", 0, 20)

    if st.button("다음"):
        st.session_state.home = home
        st.session_state.away = away
        st.session_state.step = 4
        st.rerun()

    if st.button("이전"):
        st.session_state.step = 2
        st.rerun()


elif st.session_state.step == 4:

    st.subheader("4️⃣ 최종 제출")

    if st.button("참여 완료"):

        st.session_state.users[st.session_state.knox_id] = {
            "outcome": st.session_state.choice,
            "home": st.session_state.home,
            "away": st.session_state.away
        }

        st.success("🎉 참여 완료!")

    if st.button("처음으로"):
        st.session_state.step = 1
        st.rerun()
