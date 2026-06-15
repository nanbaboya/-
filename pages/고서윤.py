import streamlit as st
import datetime

# 페이지 설정
st.set_page_config(page_title="스마트 공부 계획 플래너", page_icon="📅", layout="centered")

# 제목 및 소개
st.title("📅 스마트 공부 계획 플래너")
st.write("당신의 목표를 입력하시면 효율적인 공부 일정을 제안해 드립니다!")

st.markdown("---")

# 사용자 입력 섹션
st.sidebar.header("📋 목표 및 일정 설정")
subject = st.sidebar.text_input("공부할 과목/주제", placeholder="예: 파이썬 기초, 정보처리기사")
goal = st.sidebar.text_area("최종 목표", placeholder="예: 기초 문법 마스터, 기출문제 5회독")

# 날짜 선택
today = datetime.date.today()
start_date = st.sidebar.date_input("시작일", today)
end_date = st.sidebar.date_input("종료일", today + datetime.timedelta(days=7))

# 하루 공부 시간
daily_hours = st.sidebar.slider("하루 목표 공부 시간 (시간)", 1, 12, 3)

# 계획 생성 버튼
if st.sidebar.button("🗓️ 공부 계획 짜기"):
    if not subject or not goal:
        st.error("⚠️ 공부할 과목과 최종 목표를 입력해 주세요!")
    elif start_date > end_date:
        st.error("⚠️ 종료일은 시작일보다 늦어야 합니다!")
    else:
        # 총 기간 계산
        total_days = (end_date - start_date).days + 1
        total_hours = total_days * daily_hours
        
        # 결과 화면 출력
        st.subheader(f"✨ '{subject}' 공부 계획 결과")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("총 공부 기간", f"{total_days}일")
        col2.metric("하루 투자 시간", f"{daily_hours}시간")
        col3.metric("총 예상 시간", f"{total_hours}시간")
        
        st.info(f"🎯 **최종 목표:** {goal}")
        
        st.markdown("### 📅 주차별 권장 로드맵")
        
        # 간단한 기간별 분배 로직 (예시)
        if total_days <= 7:
            st.success("**[단기 집중형 계획]**")
            st.write("- **처음 1~3일:** 핵심 개념 파악 및 이론 정리")
            st.write("- **중간 4~5일:** 집중 문제 풀이 및 실습")
            st.write("- **마지막 6~7일:** 오답 노트 확인 및 최종 복습")
        else:
            weeks = total_days // 7
            st.success(f"**[장기 체계형 계획] 총 {weeks}주 과정**")
            st.write("- **1주차 (기반 다지기):** 기본 개념 및 용어 익히기")
            for w in range(2, weeks):
                st.write(f"- **{w}주차 (심화 학습):** 핵심 이론 깊게 파기 및 중간 점검")
            st.write(f"- **마지막 주차 (실전 대비):** 문제 풀이, 실전 연습 및 최종 보완")
            
        st.balloons()  # 성공 축하 효과
