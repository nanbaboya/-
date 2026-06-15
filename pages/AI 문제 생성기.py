import json
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI 문제 생성기",
    page_icon="📝",
    layout="wide"
)

# -------------------------
# OpenAI 설정
# -------------------------
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    client = None

# -------------------------
# 문제 생성 함수
# -------------------------
def generate_questions(subject, level, count):

    prompt = f"""
당신은 전문 출제위원입니다.

과목: {subject}
난이도: {level}

다음 형식의 객관식 문제 {count}개를 JSON으로 생성하세요.

반드시 아래 형식만 출력하세요.

[
 {{
   "question":"문제",
   "options":["보기1","보기2","보기3","보기4"],
   "answer":"정답"
 }}
]

설명이나 마크다운은 출력하지 마세요.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "당신은 정확한 시험 문제를 생성하는 AI입니다."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.8
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except Exception:
        return []


# -------------------------
# UI
# -------------------------
st.title("📝 AI 문제 생성기")
st.caption("AI가 다양한 분야의 객관식 문제를 자동 생성합니다.")

with st.sidebar:

    st.header("설정")

    subject = st.selectbox(
        "과목",
        [
            "수학",
            "과학",
            "역사",
            "영어",
            "일반상식"
        ]
    )

    level = st.selectbox(
        "난이도",
        [
            "쉬움",
            "보통",
            "어려움"
        ]
    )

    count = st.slider(
        "문제 수",
        min_value=1,
        max_value=10,
        value=5
    )

    generate_btn = st.button(
        "문제 생성",
        use_container_width=True
    )

# -------------------------
# API 확인
# -------------------------
if client is None:
    st.error("OPENAI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# -------------------------
# 상태 저장
# -------------------------
if "questions" not in st.session_state:
    st.session_state.questions = []

if generate_btn:

    with st.spinner("AI가 문제를 생성하는 중입니다..."):

        try:
            questions = generate_questions(
                subject,
                level,
                count
            )

            if questions:
                st.session_state.questions = questions
                st.success("문제가 생성되었습니다.")
            else:
                st.error("문제 생성에 실패했습니다.")

        except Exception as e:
            st.error(f"오류 발생: {e}")

# -------------------------
# 문제 표시
# -------------------------
questions = st.session_state.questions

if questions:

    st.subheader("📚 생성된 문제")

    user_answers = []

    for idx, q in enumerate(questions):

        st.markdown(f"### 문제 {idx+1}")

        st.write(q["question"])

        answer = st.radio(
            "답 선택",
            q["options"],
            key=f"q_{idx}"
        )

        user_answers.append(answer)

        st.divider()

    # -------------------------
    # 채점
    # -------------------------
    if st.button("채점하기", type="primary"):

        score = 0

        st.subheader("결과")

        for idx, q in enumerate(questions):

            correct = q["answer"]

            if user_answers[idx] == correct:
                score += 1
                st.success(
                    f"문제 {idx+1}: 정답"
                )
            else:
                st.error(
                    f"문제 {idx+1}: 오답 "
                    f"(정답: {correct})"
                )

        st.metric(
            "점수",
            f"{score}/{len(questions)}"
        )

    # -------------------------
    # 다운로드
    # -------------------------
    st.download_button(
        "문제 JSON 다운로드",
        data=json.dumps(
            questions,
            ensure_ascii=False,
            indent=2
        ),
        file_name="quiz.json",
        mime="application/json"
    )

else:
    st.info("왼쪽 메뉴에서 문제를 생성해보세요.")
