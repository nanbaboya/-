import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="AI 문제 생성기",
    page_icon="📝",
    layout="wide"
)

st.title("📝 AI 문제 생성기")
st.caption("Gemini AI를 활용하여 다양한 문제를 자동 생성합니다.")

# API Key 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# Gemini Client
client = genai.Client(api_key=api_key)

# 사이드바
with st.sidebar:
    st.header("설정")

    topic = st.text_input(
        "과목 또는 주제",
        placeholder="예: 중학교 과학"
    )

    question_type = st.selectbox(
        "문제 유형",
        [
            "객관식",
            "단답형",
            "서술형"
        ]
    )

    difficulty = st.selectbox(
        "난이도",
        [
            "쉬움",
            "보통",
            "어려움"
        ]
    )

    count = st.slider(
        "문제 개수",
        min_value=1,
        max_value=10,
        value=5
    )

    generate_btn = st.button(
        "문제 생성",
        use_container_width=True
    )

# 안내 화면
if not generate_btn:
    st.info(
        """
        사용 방법
        
        1. 과목 또는 주제를 입력하세요.
        2. 문제 유형을 선택하세요.
        3. 난이도를 선택하세요.
        4. 문제 생성을 클릭하세요.
        """
    )

# 문제 생성
if generate_btn:

    if not topic.strip():
        st.warning("주제를 입력해주세요.")
        st.stop()

    prompt = f"""
당신은 전문 출제자입니다.

다음 조건으로 문제를 생성하세요.

주제: {topic}
문제 유형: {question_type}
난이도: {difficulty}
문제 수: {count}

반드시 아래 형식으로 작성하세요.

문제 1
...
정답:
해설:

문제 2
...
정답:
해설:

모든 문제는 학습에 적합하고 명확하게 작성하세요.
"""

    with st.spinner("AI가 문제를 생성하는 중입니다..."):

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=3000
                )
            )

            result = response.text

            if not result:
                st.error("문제 생성에 실패했습니다.")
                st.stop()

            st.success("문제 생성 완료!")

            st.subheader("생성된 문제")

            st.text_area(
                "결과",
                value=result,
                height=500
            )

            st.download_button(
                label="📥 TXT 다운로드",
                data=result,
                file_name="ai_questions.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"API 오류가 발생했습니다.\n\n{str(e)}")
