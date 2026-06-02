import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 설정 및 초기화
st.set_page_config(page_title="AI 문제 생성기", page_icon="📝", layout="centered")
st.title("📝 AI 문제 생성기 챗봇")
st.write("원하는 과목, 범위, 난이도를 말씀하시면 맞춤형 문제를 만들어 드립니다!")

# 2. Streamlit Secrets에서 API 키 확인
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 대시보드의 Settings -> Secrets 설정을 확인해주세요.")
    st.stop()

# 3. 세션 상태(Session State) 관리
MODEL_ID = "gemini-2.5-flash-lite"

# 3-1. Gemini 클라이언트 세션 유지 (클라이언트가 닫히는 오류 방지)
if "gemini_client" not in st.session_state:
    try:
        st.session_state.gemini_client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    except Exception as e:
        st.error(f"Gemini 클라이언트 초기화 실패: {e}")
        st.stop()

# 3-2. 화면 표시용 채팅 기록 리스트 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3-3. 연속 대화를 위한 대화 세션(Chat Session) 초기화
if "chat_session" not in st.session_state:
    system_instruction = (
        "당신은 교육 전문가이자 AI 문제 생성기입니다. 사용자가 요청하는 주제, 과목, "
        "난이도에 맞춰 정확하고 교육적인 문제를 만들어야 합니다. "
        "문제, 보기(객관식인 경우), 정답, 그리고 친절한 해설을 함께 제공하세요."
    )
    
    try:
        # 안전하게 세션 상태에 저장된 클라이언트를 사용하여 대화 세션 생성
        st.session_state.chat_session = st.session_state.gemini_client.chats.create(
            model=MODEL_ID,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
    except Exception as e:
        st.error(f"대화 세션 생성 중 오류가 발생했습니다: {e}")
        st.stop()

# 4. 기존 채팅 기록 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력창 및 챗봇 로직 처리
if user_input := st.chat_input("예: '고등학교 1학년 통합과학 산화 환원 반응 객관식 3문제 만들어줘'"):
    
    # 사용자 입력 화면에 띄우고 세션에 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # AI 답변 생성 프로세스
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 문제를 생성하는 중입니다. 잠시만 기다려주세요...")
        
        try:
            # 세션이 끊기지 않는 대화 객체로 메시지 전송
            response = st.session_state.chat_session.send_message(user_input)
            ai_response = response.text
            
            # 응답 출력 및 세션에 기록 저장
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except APIError as ae:
            # Gemini API 응답 실패 예외 처리
            error_msg = f"❌ Gemini API 오류가 발생했습니다: {ae.message} (코드: {ae.code})"
            message_placeholder.markdown(error_msg)
            st.error(error_msg)
        except Exception as e:
            # 기타 시스템 에러 처리
            error_msg = f"❌ 알 수 없는 오류가 발생했습니다: {str(e)}"
            message_placeholder.markdown(error_msg)
            st.error(error_msg)
