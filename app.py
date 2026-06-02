import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 설정
st.set_page_config(page_title="AI 문제 생성기", page_icon="📝", layout="centered")
st.title("📝 AI 문제 생성기 챗봇")
st.write("원하는 과목, 범위, 난이도를 말씀하시면 맞춤형 문제를 만들어 드립니다!")

# 2. Streamlit Secrets에서 API 키 불러오기 및 클라이언트 초기화
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 관리를 확인해주세요.")
    st.stop()

try:
    # 최신 google-genai SDK 스타일로 클라이언트 생성
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"Gemini 클라이언트 초기화 실패: {e}")
    st.stop()

# 3. 세션 상태(Session State)로 채팅 기록 및 대화(Chat) 세션 유지
# gemini-2.5-flash-lite 모델 지정
MODEL_ID = "gemini-2.5-flash-lite"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    # 챗봇에게 문제 생성기 역할을 부여하는 시스템 지침(System Instruction) 설정
    system_instruction = (
        "당신은 교육 전문가이자 AI 문제 생성기입니다. 사용자가 요청하는 주제, 과목, "
        "난이도에 맞춰 정확하고 교육적인 문제를 만들어야 합니다. "
        "문제, 보기(객관식인 경우), 정답, 그리고 친절한 해설을 함께 제공하세요."
    )
    
    try:
        st.session_state.chat_session = client.chats.create(
            model=MODEL_ID,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
    except Exception as e:
        st.error(f"대화 세션 생성 중 오류가 발생했습니다: {e}")
        st.stop()

# 4. 기존 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 및 챗봇 답변 처리
if user_input := st.chat_input("예: '고등학교 1학년 통합과학 산화 환원 반응 객관식 3문제 만들어줘'"):
    # 사용자 메시지 화면에 표시 및 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # AI 답변 생성 및 표시
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            # 대화 세션을 통해 메시지 전송 (기록 자동 유지)
            response = st.session_state.chat_session.send_message(user_input)
            ai_response = response.text
            
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except APIError as ae:
            # Gemini API 관련 오류 처리
            error_msg = f"Gemini API 오류가 발생했습니다: {ae.message} (코드: {ae.code})"
            message_placeholder.markdown(error_msg)
            st.error(error_msg)
        except Exception as e:
            # 기타 예외 처리
            error_msg = f"알 수 없는 오류가 발생했습니다: {str(e)}"
            message_placeholder.markdown(error_msg)
            st.error(error_msg)
