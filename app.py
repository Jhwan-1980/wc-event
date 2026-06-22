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
    # 📊 전체 참여자 결과 (엑셀 스타일)
    # =====================================================
    st.subheader("📊 전체 참여자 결과")

    if st.session_state.result:

        rh, ra = st.session_state.result

        def calc_score(v):
            base = 0

            # 승부 적중
            actual_outcome = "WIN" if rh > ra else "DRAW" if rh == ra else "LOSE"

            if v["outcome"] == actual_outcome:
                base += 1

            # 스코어 근접도
            diff = abs(v["home"] - rh) + abs(v["away"] - ra)

            score = base + (10 - diff) * 0.1  # 세분화 점수

            return round(score, 2), diff

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

        # 정렬
        df = df.sort_values(by="획득 점수", ascending=False)

        # 공동순위 처리
        df["순위"] = df["획득 점수"].rank(method="min", ascending=False).astype(int)

        # 보기 좋게 정렬
        df = df.sort_values(by=["순위", "획득 점수"], ascending=[True, False])

        st.dataframe(df, use_container_width=True)


    else:
        st.info("아직 결과가 없습니다.")


    st.divider()

    # =====================================================
    # 🚨 초기화 (2단계 확인)
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

                st.success("🔥 모든 데이터 초기화 완료")


# =========================================================
# 사용자 입력 (간단 유지)
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
