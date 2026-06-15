import streamlit as st
import datetime
from streamlit_calendar import calendar

# 페이지 설정
st.set_page_config(page_title="AI 스마트 달력 플래너", page_icon="📅", layout="wide")

st.title("📅 대화형 공부 계획 달력 플래너")
st.write("목표 기간을 설정하면 달력에 일별 계획을 자동으로 채워줍니다.")

st.markdown("---")

# 레이아웃 분할 (왼쪽: 입력창 / 오른쪽: 달력 결과)
col_input, col_display = st.columns([1, 2])

with col_input:
    st.header("📋 목표 설정")
    subject = st.text_input("공부할 과목/주제", placeholder="예: 파이썬 데이터 분석")
    goal = st.text_area("최종 목표", placeholder="예: 판다스 마스터 및 포트폴리오 완성")
    
    # 날짜 및 시간 설정
    today = datetime.date.today()
    start_date = st.date_input("시작일", today)
    end_date = st.date_input("종료일", today + datetime.timedelta(days=6))
    daily_hours = st.slider("하루 공부 시간 (시간)", 1, 12, 2)
    
    generate_btn = st.button("🗓️ 달력에 계획 반영하기", use_container_width=True)

with col_display:
    if generate_btn:
        if not subject or not goal:
            st.error("⚠️ 공부할 과목과 최종 목표를 입력해 주세요!")
        elif start_date > end_date:
            st.error("⚠️ 종료일은 시작일보다 늦어야 합니다!")
        else:
            total_days = (end_date - start_date).days + 1
            
            st.subheader(f"✨ '{subject}' 학습 일정표")
            
            # 달력에 들어갈 이벤트 데이터 생성 루프
            calendar_events = []
            current_date = start_date
            day_count = 1
            
            while current_date <= end_date:
                # 기간 비율에 따라 공부 내용 동적 배분 (기본 3단계 로직)
                progress = day_count / total_days
                if progress <= 0.3:
                    task = "✍️ 기본 이론 및 개념 학습"
                    color = "#FF9F89" # 살구색
                elif progress <= 0.7:
                    task = "💻 집중 실습 및 문제 풀이"
                    color = "#3788D8" # 파란색
                else:
                    task = "🔥 오답 노트 및 최종 복습"
                    color = "#28A745" # 초록색
                
                # 달력 라이브러리가 인식하는 형식으로 이벤트 추가
                calendar_events.append({
                    "title": f"[{subject}] {task} ({daily_hours}h)",
                    "start": current_date.isoformat(),
                    "end": current_date.isoformat(),
                    "backgroundColor": color,
                    "borderColor": color
                })
                
                current_date += datetime.timedelta(days=1)
                day_count += 1
            
            # 달력 옵션 설정 (FullCalendar 기반 옵션)
            calendar_options = {
                "headerToolbar": {
                    "left": "prev,next today",
                    "center": "title",
                    "right": "dayGridMonth,timeGridWeek"
                },
                "initialDate": start_date.isoformat(),
                "initialView": "dayGridMonth",
                "selectable": True,
            }
            
            # 달력 컴포넌트 렌더링
            calendar(events=calendar_events, options=calendar_options, key="study_calendar")
            
            st.success(f"🎯 총 {total_days}일 동안 하루 {daily_hours}시간씩, 총 {total_days * daily_hours}시간의 계획이 수립되었습니다!")
            st.balloons()
    else:
        # 버튼을 누르기 전 안내 화면
        st.info("👈 왼쪽에서 공부 목표와 기간을 입력한 뒤 버튼을 누르면 여기에 달력이 나타납니다.")
