import streamlit as st
import datetime
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="스마트 공부 플래너", page_icon="📅", layout="wide")

st.title("📅 일별 공부 계획 플래너")
st.write("기간을 설정하면 날짜별로 공부할 내용을 표와 달력 형태로 깔끔하게 정리해 드립니다.")

st.markdown("---")

col_input, col_display = st.columns([1, 2])

with col_input:
    st.header("📋 목표 설정")
    subject = st.text_input("공부할 과목/주제", placeholder="예: 파이썬 데이터 분석")
    goal = st.text_area("최종 목표", placeholder="예: 기본 문법 마스터 및 실습 완성")
    
    today = datetime.date.today()
    start_date = st.date_input("시작일", today)
    end_date = st.date_input("종료일", today + datetime.timedelta(days=6))
    daily_hours = st.slider("하루 공부 시간 (시간)", 1, 12, 2)
    
    generate_btn = st.button("🗓️ 공부 계획 생성하기", use_container_width=True)

with col_display:
    if generate_btn:
        if not subject or not goal:
            st.error("⚠️ 공부할 과목과 최종 목표를 입력해 주세요!")
        elif start_date > end_date:
            st.error("⚠️ 종료일은 시작일보다 늦어야 합니다!")
        else:
            total_days = (end_date - start_date).days + 1
            
            st.subheader(f"✨ '{subject}' 상세 일정표")
            
            # 데이터프레임 생성을 위한 리스트
            plan_data = []
            current_date = start_date
            day_count = 1
            
            while current_date <= end_date:
                progress = day_count / total_days
                if progress <= 0.3:
                    task = "✍️ 기본 이론 및 핵심 개념 학습"
                elif progress <= 0.7:
                    task = "💻 예제 실습 및 집중 문제 풀이"
                else:
                    task = "🔥 오답 노트 정리 및 최종 복습"
                
                # 요일 구하기
                weekday_str = ["월", "화", "수", "목", "금", "토", "일"][current_date.weekday()]
                
                plan_data.append({
                    "날짜": current_date.strftime("%Y-%m-%d"),
                    "요일": weekday_str,
                    "공부 내용": task,
                    "목표 시간": f"{daily_hours}시간"
                })
                
                current_date += datetime.timedelta(days=1)
                day_count += 1
            
            # 판다스 데이터프레임 변환
            df = pd.DataFrame(plan_data)
            
            # 스트림릿 표(Dataframe)로 시각적으로 출력
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.success(f"🎯 총 {total_days}일 동안 하루 {daily_hours}시간씩, 총 {total_days * daily_hours}시간의 계획이 완료되었습니다!")
            st.balloons()
    else:
        st.info("👈 왼쪽에서 공부 목표와 기간을 입력한 뒤 버튼을 누르면 일별 계획 표가 나타납니다.")
