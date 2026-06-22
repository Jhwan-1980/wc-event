import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="예측 이벤트", layout="wide")

# =========================================================
# 파일 저장
# =========================================================
DATA_FILE = "event_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


# =========================================================
# 상태 초기화
# =========================================================
if "step" not in st.session_state:
    st.session_state.step = 1

if "users" not in st.session_state:
    st.session_state.users = load_data()

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
# 🔐 관리자 패널 (유지)
# =========================================================
if st.session_state.admin_mode and is_admin:

    st.subheader("🔐 관리자 패널")

    if st.button("메인으로 복귀"):
        st.session_state.admin_mode = False

    st.divider()

    rh = st.number_input("대한민국 스코어", 0, 20, 0)
    ra = st.number_input("남아공 스코어", 0, 20, 0)

    if st.button("결과 확정"):
        st.session_state.result = (rh, ra)
        st.success("결과 저장 완료")

    st.divider()

    st.subheader(f"📊 전체 참여자 결과 (총 {len(st.session_state.users)}명)")

    if st.session_state.users:

        def calc_score(v, rh, ra):
            base = 1 if v["outcome"] == ("승" if rh > ra else "무" if rh == ra else "패") else 0
            diff = abs(v["home"] - rh) + abs(v["away"] - ra)
            return round(base + (10 - diff) * 0.1, 2)

        rows = []

        for k, v in st.session_state.users.items():
            rows.append({
                "참여자 ID": k,
                "승무패": v["outcome"],
                "대한민국 스코어": v["home"],
                "남아공 스코어": v["away"],
                "획득 점수": calc_score(v, rh, ra)
            })

        df = pd.DataFrame(rows)

        df = df.sort_values(by="획득 점수", ascending=False)

        df["순위"] = df["획득 점수"].rank(method="dense", ascending=False)

        st.dataframe(df, use_container_width=True)

    st.divider()

    # 초기화 유지
    st.subheader("⚠️ 게임 초기화")

    if st.button("초기화 시작"):
        st.session_state.reset_step = True

    if st.session_state.reset_step:

        st.warning("정말 초기화하시겠습니까?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("취소"):
                st.session_state.reset_step = False

        with col2:
            if st.button("확인"):
                st.session_state.users = {}
                save_data({})
                st.session_state.reset_step = False
                st.session_state.step = 1

                st.success("초기화 완료")


# =========================================================
# 👤 STEP FLOW
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

    st.subheader("2️⃣ 스코어 입력")

    home = st.number_input("대한민국", 0, 20)
    away = st.number_input("남아공", 0, 20)

    if st.button("다음"):

        outcome = "승" if home > away else "무" if home == away else "패"

        st.session_state.home = home
        st.session_state.away = away
        st.session_state.outcome = outcome

        st.session_state.step = 3
        st.rerun()


# =========================================================
# ⭐ STEP 3 (수정 핵심: 제출 후 현황 표시)
# =========================================================
elif st.session_state.step == 3:

    st.subheader("3️⃣ 최종 제출")

    st.info(f"자동 판정 결과: {st.session_state.outcome}")

    if st.button("참여 완료"):

        st.session_state.users[st.session_state.knox_id] = {
            "outcome": st.session_state.outcome,
            "home": st.session_state.home,
            "away": st.session_state.away
        }

        save_data(st.session_state.users)

        st.success("🎉 참여 완료!")

        # =====================================================
        # ⭐ 추가 기능: 현재 참여 현황 표시
        # =====================================================
        st.divider()
        st.subheader("📊 현재 참여 현황")

        df_live = pd.DataFrame([
            {
                "ID": k,
                "스코어": f"{v['home']} : {v['away']}",
                "승/무/패": v["outcome"]
            }
            for k, v in st.session_state.users.items()
        ])

        st.dataframe(df_live, use_container_width=True)

    if st.button("처음으로"):
        st.session_state.step = 1
        st.rerun()
    
