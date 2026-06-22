import streamlit as st

st.set_page_config(page_title="예측 이벤트", layout="wide")

# ---------------------------
# 상태 초기화
# ---------------------------
if "step" not in st.session_state:
    st.session_state.step = 1

if "users" not in st.session_state:
    st.session_state.users = {}

if "result" not in st.session_state:
    st.session_state.result = None

if "knox_id" not in st.session_state:
    st.session_state.knox_id = ""

if "outcome" not in st.session_state:
    st.session_state.outcome = ""

if "score_home" not in st.session_state:
    st.session_state.score_home = 0

if "score_away" not in st.session_state:
    st.session_state.score_away = 0


# ---------------------------
# 공통 헤더 (모든 페이지 고정)
# ---------------------------
st.title("🏆 대한민국 : 남아공 경기 예측 이벤트")

knox_id_input = st.session_state.knox_id

is_admin = (knox_id_input == "jhwan1.choi")

# 관리자 버튼 (항상 표시)
if is_admin:
    st.sidebar.success("🔐 관리자 모드 활성")
    if st.sidebar.button("관리자 패널"):
        st.session_state.step = 99


# ---------------------------
# STEP 1: Knox ID
# ---------------------------
if st.session_state.step == 1:

    st.subheader("1️⃣ Knox ID 입력")

    knox = st.text_input("Knox ID 입력")

    if st.button("다음"):
        if knox:
            st.session_state.knox_id = knox
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Knox ID를 입력하세요")


# ---------------------------
# STEP 2: 승무패
# ---------------------------
elif st.session_state.step == 2:

    st.subheader("2️⃣ 승 / 무 / 패 선택")

    choice = st.radio("선택", ["승", "무", "패"])

    if st.button("다음"):
        st.session_state.outcome = choice
        st.session_state.step = 3
        st.rerun()

    if st.button("이전"):
        st.session_state.step = 1
        st.rerun()


# ---------------------------
# STEP 3: 스코어
# ---------------------------
elif st.session_state.step == 3:

    st.subheader("3️⃣ 스코어 입력")

    home = st.number_input("한국 득점", 0, 20)
    away = st.number_input("남아공 득점", 0, 20)

    if st.button("다음"):
        st.session_state.score_home = home
        st.session_state.score_away = away
        st.session_state.step = 4
        st.rerun()

    if st.button("이전"):
        st.session_state.step = 2
        st.rerun()


# ---------------------------
# STEP 4: 완료
# ---------------------------
elif st.session_state.step == 4:

    st.subheader("4️⃣ 참여 완료")

    if st.button("참여 완료 제출"):

        st.session_state.users[st.session_state.knox_id] = {
            "outcome": st.session_state.outcome,
            "home": st.session_state.score_home,
            "away": st.session_state.score_away
        }

        st.success("🎉 참여해주셔서 감사합니다!")

    if st.button("처음으로"):
        st.session_state.step = 1
        st.rerun()


# ---------------------------
# 관리자 페이지
# ---------------------------
elif st.session_state.step == 99:

    st.subheader("🔐 관리자 패널")

    if st.button("메인으로 복귀"):
        st.session_state.step = 1
        st.rerun()

    st.write("여기에 기존 관리자 기능 추가 가능")
