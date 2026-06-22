import streamlit as st

st.set_page_config(page_title="예측 이벤트", layout="wide")

# =========================================================
# 상태 초기화
# =========================================================
if "step" not in st.session_state:
    st.session_state.step = 1

if "knox_id" not in st.session_state:
    st.session_state.knox_id = ""

if "choice" not in st.session_state:
    st.session_state.choice = ""

if "home" not in st.session_state:
    st.session_state.home = 0

if "away" not in st.session_state:
    st.session_state.away = 0

if "users" not in st.session_state:
    st.session_state.users = {}

if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

if "result" not in st.session_state:
    st.session_state.result = None


# =========================================================
# 헤더 (항상 고정)
# =========================================================
st.title("🏆 대한민국 : 남아공 경기 예측 이벤트")


# =========================================================
# Knox ID 입력 (항상 표시)
# =========================================================
knox_input = st.text_input("Knox ID 입력")

if knox_input:
    st.session_state.knox_id = knox_input

is_admin = (st.session_state.knox_id == "jhwan1.choi")


# =========================================================
# 관리자 버튼 (항상 우측 상단 역할)
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

    if st.button("메인으로 복귀"):
        st.session_state.admin_mode = False

    st.divider()

    rh = st.number_input("한국 득점", 0, 20, 0)
    ra = st.number_input("남아공 득점", 0, 20, 0)

    if st.button("결과 확정"):
        st.session_state.result = (rh, ra)
        st.success("결과 저장 완료")

    st.divider()

    st.subheader("📊 참여 데이터")

    for k, v in st.session_state.users.items():
        st.write(f"{k} | {v}")


# =========================================================
# =========================================================
# 👤 STEP FLOW (핵심)
# =========================================================
# =========================================================

elif st.session_state.step == 1:

    st.subheader("1️⃣ Knox ID 입력")

    if st.button("다음"):
        if st.session_state.knox_id:
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

    home = st.number_input("한국 득점", 0, 20)
    away = st.number_input("남아공 득점", 0, 20)

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

    st.info("모든 입력 완료 후 참여를 제출합니다.")

    if st.button("참여 완료"):

        st.session_state.users[st.session_state.knox_id] = {
            "outcome": st.session_state.choice,
            "home": st.session_state.home,
            "away": st.session_state.away
        }

        st.success("🎉 참여해주셔서 감사합니다!")

    if st.button("처음으로"):
        st.session_state.step = 1
        st.rerun()


# =========================================================
# =========================================================
# 🏆 랭킹 (옵션 표시)
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
            "승부": v["outcome"],
            "오차": diff,
            "적중": v["outcome"] == actual
        })

    rows = sorted(rows, key=lambda x: (not x["적중"], x["오차"]))

    st.dataframe(rows[:10], use_container_width=True)
