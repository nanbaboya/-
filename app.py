# [기존 1번 페이지 설정 아래에 이어서 작성]

# 2. Streamlit Secrets에서 API 키 불러오기
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 관리를 확인해주세요.")
    st.stop()

# 3. 세션 상태(Session State)로 클라이언트, 채팅 기록, 대화 세션 유지
MODEL_ID = "gemini-2.5-flash-lite"

# 클라이언트 객체를 세션 상태에 저장 (앱이 새로고침되어도 닫히지 않도록 방지)
if "gemini_client" not in st.session_state:
    try:
        st.session_state.gemini_client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    except Exception as e:
        st.error(f"Gemini 클라이언트 초기화 실패: {e}")
        st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    system_instruction = (
        "당신은 교육 전문가이자 AI 문제 생성기입니다. 사용자가 요청하는 주제, 과목, "
        "난이도에 맞춰 정확하고 교육적인 문제를 만들어야 합니다. "
        "문제, 보기(객관식인 경우), 정답, 그리고 친절한 해설을 함께 제공하세요."
    )
    
    try:
        # 새로고침 시 유실되지 않는 세션 상태의 클라이언트를 사용해 대화 세션 생성
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

# [이후 4번 기존 채팅 기록 표시 영역부터는 동일합니다]
