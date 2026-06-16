import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime

st.set_page_config(
    page_title="공부시간 타이머",
    page_icon="⏱️",
    layout="centered"
)

# ----------------------------
# Gemini Client 생성
# ----------------------------
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# ----------------------------
# Session State 초기화
# ----------------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------
# 공부 타이머
# ----------------------------
st.title("📚 공부시간 타이머")

col1, col2 = st.columns(2)

with col1:
    if st.button("공부 시작"):
        if st.session_state.start_time is None:
            st.session_state.start_time = datetime.now()
            st.success("타이머 시작!")

with col2:
    if st.button("공부 종료"):
        if st.session_state.start_time is not None:
            elapsed = (
                datetime.now() - st.session_state.start_time
            ).total_seconds()

            st.session_state.total_seconds += int(elapsed)
            st.session_state.start_time = None
            st.success("공부 종료!")

# 현재 진행중 시간 반영
current_total = st.session_state.total_seconds

if st.session_state.start_time is not None:
    current_total += int(
        (datetime.now() - st.session_state.start_time).total_seconds()
    )

hours = current_total // 3600
minutes = (current_total % 3600) // 60
seconds = current_total % 60

st.metric(
    "누적 공부시간",
    f"{hours:02d}:{minutes:02d}:{seconds:02d}"
)

st.divider()

# ----------------------------
# Gemini 채팅
# ----------------------------
st.subheader("🤖 공부 도우미 AI")

# 기존 채팅 출력
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("질문을 입력하세요")

if user_input:
    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # 이전 대화 기록 구성
        history_text = ""

        for msg in st.session_state.chat_history:
            role = "사용자" if msg["role"] == "user" else "AI"
            history_text += f"{role}: {msg['content']}\n"

        prompt = f"""
다음은 이전 대화 기록입니다.

{history_text}

위 대화를 참고하여 마지막 사용자 질문에 답변하세요.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7
            )
        )

        answer = response.text

    except Exception as e:
        answer = f"오류가 발생했습니다.\n\n{str(e)}"

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.markdown(answer)
