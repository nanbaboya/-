import streamlit as st
import datetime
import pandas as pd
import calendar

# 1. 페이지 및 환경 설정
st.set_page_config(page_title="스마트 달력 공부 플래너", page_icon="📅", layout="wide")

# 스타일 커스텀 (달력 가독성 향상)
st.markdown("""
    <style>
    .stDataFrame { width: 100%; }
    h3 { margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("📅 스마트 달력 공부 계획 플래너")
st.write("공부 범위와 기간을 입력하면 에러 없는 격자형 달력과 대시보드로 일정을 즉시 짜드립니다.")
st.markdown("---")

# 2. 사이드바 - 사용자 입력창
st.sidebar.header("📋 공부 정보 입력")

subject = st.sidebar.text_input("📚 공부할 과목", value="파이썬 데이터 분석", placeholder="예: 정보처리기사, 영어 회화")
range_type = st.sidebar.selectbox("📐 범위 단위", ["페이지(p)", "단원(Ch)", "강의(강)"])
total_range = st.sidebar.number_input(f"🔢 총 공부 범위 ({range_type})", min_value=1, value=150, step=1)

st.sidebar.markdown("---")
st.sidebar.header("📆 기간 및 시간")

today = datetime.date.today()
start_date = st.sidebar.date_input("시작일", today)
end_date = st.sidebar.date_input("종료일", today + datetime.timedelta(days=13)) # 기본 2주 설정
daily_hours = st.sidebar.slider("⏰ 하루 목표 공부 시간 (시간)", 1, 12, 3)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ 스마트 분배 옵션")
skip_weekend = st.sidebar.checkbox("🏖️ 주말(토, 일)은 쉬고 싶어요")
study_style = st.sidebar.selectbox("🎯 학습 스타일", ["균등하게 나누기", "초반 집중형 (벼락치기 방지)", "후반 스퍼트형"])

# 실행 버튼
generate_btn = st.sidebar.button("🗓️ 공부 계획 생성하기", use_container_width=True)

# 3. 메인 화면 로직 및 예외 처리
if generate_btn or 'plan_generated' in st.session_state:
    st.session_state['plan_generated'] = True
    
    if start_date > end_date:
        st.error("⚠️ 오류: 종료일은 시작일보다 늦은 날짜여야 합니다. 기간을 다시 설정해 주세요.")
    else:
        # 전체 날짜 배열 생성
        total_days = (end_date - start_date).days + 1
        date_list = [start_date + datetime.timedelta(days=x) for x in range(total_days)]
        
        # 주말 제외 필터링
        if skip_weekend:
            valid_dates = [d for d in date_list if d.weekday() < 5]
        else:
            valid_dates = date_list
            
        if len(valid_dates) == 0:
            st.error("⚠️ 오류: 선택한 기간에 공부할 수 있는 날(평일)이 없습니다. 기간을 늘려주세요.")
        else:
            # 가중치 알고리즘을 적용한 분량 배분
            num_study_days = len(valid_dates)
            base_chunks = [1.0] * num_study_days
            
            if study_style == "초반 집중형 (벼락치기 방지)":
                base_chunks = [1.5 - (i / num_study_days) for i in range(num_study_days)]
            elif study_style == "후반 스퍼트형":
                base_chunks = [0.5 + (i / num_study_days) for i in range(num_study_days)]
                
            # 가중치 비율에 맞게 총 범위 쪼개기 (정수형 분할 및 반올림 예외 처리)
            total_weight = sum(base_chunks)
            allocated_range = []
            accumulated = 0
            
            for i, w in enumerate(base_chunks):
                if i == num_study_days - 1: # 마지막 날 몰아주기 예외 처리
                    allocated_range.append(int(total_range - accumulated))
                else:
                    share = int(round((w / total_weight) * total_range))
                    # 하루에 최소 1개는 하거나 총량을 넘지 않게 조절
                    if share < 1 and total_range > num_study_days: share = 1
                    allocated_range.append(share)
                    accumulated += share

            # 4. 데이터셋 통합 관리
            study_plan = {}
            idx = 0
            for d in date_list:
                if d in valid_dates:
                    study_plan[d] = f"📖 {allocated_range[idx]}{range_type} ({daily_hours}h)"
                    idx += 1
                else:
                    study_plan[d] = "🏖️ 휴식일"

            # 5. 상단 요약 대시보드 (Metrics)
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("총 공부 기간", f"{total_days}일")
            col2.metric("실제 공부 날짜", f"{num_study_days}일")
            col3.metric("하루 평균 분량", f"{round(total_range/num_study_days, 1)}{range_type}")
            col4.metric("총 예정 시간", f"{num_study_days * daily_hours}시간")
            
            # --- 차별화 기능: 직접 구현한 격자형 달력(Grid Calendar) 생성 ---
            st.subheader(f"📅 {start_date.year}년 {start_date.month}월 달력 형태 계획표")
            
            # 선택한 달의 일수 정보 구하기
            year, month = start_date.year, start_date.month
            cal = calendar.monthcalendar(year, month)
            
            # 스트림릿 표용 데이터프레임 구조 짜기
            cal_data = []
            columns = ["월", "화", "수", "목", "금", "토", "일"]
            
            for week in cal:
                week_row = {}
                for day_idx, day in enumerate(week):
                    day_name = columns[day_idx]
                    if day == 0:
                        week_row[day_name] = ""
                    else:
                        current_lookup = datetime.date(year, month, day)
                        if current_lookup in study_plan:
                            week_row[day_name] = f"[{day}일] {study_plan[current_lookup]}"
                        else:
                            week_row[day_name] = f"[{day}일] -"
                cal_data.append(week_row)
                
            df_cal = pd.DataFrame(cal_data)
            st.dataframe(df_cal, use_container_width=True, hide_index=True)
            
            # 6. 타임라인 리스트 피드 출력
            st.subheader("📋 순차적 일별 디테일 플랜")
            
            timeline_data = []
            for d, task in study_plan.items():
                weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][d.weekday()]
                timeline_data.append({
                    "날짜": d.strftime("%Y-%m-%d"),
                    "요일": weekday_kr,
                    "학습 계획 및 목표 분량": task
                })
            
            df_timeline = pd.DataFrame(timeline_data)
            
            # 조건부 행 강조를 위한 테이블 뷰 (휴식일과 공부일 구별 가독성)
            st.dataframe(
                df_timeline, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "날짜": st.column_config.TextColumn("📅 날짜", width="medium"),
                    "요일": st.column_config.TextColumn("요일", width="small"),
                    "학습 계획 및 목표 분량": st.column_config.TextColumn("🎯 할 일 및 배정 시간")
                }
            )
            st.balloons()
else:
    # 최초 실행 시 안내 메시지
    st.info("💡 왼쪽 사이드바에서 공부할 과목, 범위, 마감일을 지정한 후 [공부 계획 생성하기] 버튼을 눌러주세요!")
