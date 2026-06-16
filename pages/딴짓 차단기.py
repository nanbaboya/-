import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="딴짓차단기", page_icon="🚫", layout="centered")

st.title("🚫 딴짓차단기")
st.markdown("---")

# 2. 세션 상태 초기화
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# 3. [핵심 수정] 새로고침 후 브라우저 깨우기용 상호작용 장치
# 시작 버튼을 순수 Streamlit 파이썬 버튼으로 크게 유지하여 무조건 클릭을 유도합니다.
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ 차단기 시작 (활성화)", use_container_width=True, type="primary"):
        st.session_state.is_running = True
        st.rerun()

with col2:
    if st.button("⏹️ 차단기 종료", use_container_width=True):
        st.session_state.is_running = False
        st.rerun()

st.markdown("---")

# 4. 차단기 가동 및 자바스크립트 주입
if st.session_state.is_running:
    st.markdown("### 🔒 현재 딴짓 알림 감지 중...")
    
    clean_notification_script = """
    <script>
        (function() {
            // 브라우저 권한 체크 및 재요청
            if (window.Notification) {
                Notification.requestPermission();
            }

            function sendAlert() {
                try {
                    if (Notification.permission === "granted") {
                        new Notification("🚨 딴짓차단기 경고", {
                            body: "화면을 이탈했습니다! 즉시 업무 화면으로 복귀하세요.",
                            icon: "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=128&h=128&fit=crop",
                            tag: "distraction-alert"
                        });
                    }
                } catch (err) {
                    console.log("알림 발송 제한 우회 처리 중", err);
                }
            }

            // 탭 전환 감지
            document.addEventListener("visibilitychange", () => {
                if (document.hidden) {
                    sendAlert();
                }
            });

            // 다른 창 클릭 감지
            window.addEventListener('blur', () => {
                sendAlert();
            });
        })();
    </script>
    """
    components.html(clean_notification_script, height=0)
    
    st.warning("⚠️ **새로고침 후 행동 요령:** 페이지를 새로고침(F5)했다면, 반드시 위의 **[▶️ 차단기 시작]** 버튼을 다시 한 번 꾹 눌러주셔야 브라우저가 잠금에서 깨어나 알림을 정상적으로 보냅니다!")

else:
    st.write("대기 상태입니다. 상단의 '차단기 시작' 버튼을 누르세요.")
