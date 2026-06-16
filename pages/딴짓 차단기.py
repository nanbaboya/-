import streamlit as st
import time
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="딴짓차단기", page_icon="🚫")

st.title("🚫 딴짓차단기: 집중 모드")
st.write("화면을 이탈하면 집중이 중단됩니다. 창을 계속 켜두세요!")

# 세션 상태 초기화
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
    st.session_state.is_running = False

# 자바스크립트를 이용한 화면 이탈 감지 및 경고
import streamlit.components.v1 as components

detection_script = """
<script>
    document.addEventListener("visibilitychange", () => {
        if (document.hidden) {
            window.parent.postMessage({type: 'visibility', status: 'hidden'}, '*');
        } else {
            window.parent.postMessage({type: 'visibility', status: 'visible'}, '*');
        }
    });
</script>
"""
components.html(detection_script, height=0)

# 타이머 로직
col1, col2 = st.columns(2)

if col1.button("공부 시작"):
    st.session_state.start_time = datetime.now()
    st.session_state.is_running = True
    st.success("집중 시작! 화면을 떠나지 마세요.")

if col2.button("공부 종료"):
    st.session_state.is_running = False
    st.info("오늘의 학습 기록이 저장되었습니다.")

# 화면 이탈 알림 UI
placeholder = st.empty()

if st.session_state.is_running:
    elapsed = datetime.now() - st.session_state.start_time
    placeholder.metric("현재 집중 시간", str(elapsed).split('.')[0])
    
    st.warning("⚠️ 집중 중입니다. 브라우저 탭을 변경하지 마세요!")
else:
    placeholder.write("학습을 시작하려면 버튼을 누르세요.")

# 푸터
st.markdown("---")
st.caption("딴짓차단기 - Streamlit 기반 집중력 향상 도구")
