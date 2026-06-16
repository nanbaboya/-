import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="딴짓차단기", page_icon="🚫", layout="centered")

st.title("🚫 딴짓차단기")
st.markdown("---")

# 2. 세션 상태 초기화 (작동 여부 저장)
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# 3. 시작 / 종료 버튼 구성
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ 차단기 시작", use_container_width=True, type="primary"):
        st.session_state.is_running = True
        st.rerun()

with col2:
    if st.button("⏹️ 차단기 종료", use_container_width=True):
        st.session_state.is_running = False
        st.rerun()

st.markdown("---")

# 4. 차단기가 켜져 있을 때만 알림 감지 스크립트 실행
if st.session_state.is_running:
    st.markdown("### 🔒 현재 딴짓 알림 감지 중...")
    st.info("💡 **필수 확인:** 차단기 시작 후, 브라우저 주소창 왼쪽에 뜨는 권한 팝업에서 **[알림 허용]**을 반드시 눌러주셔야 바탕화면 팝업이 작동합니다.")
    
    # 빨간 화면 UI를 완전히 지우고, 오직 바탕화면 알림 팝업만 발생시키는 스크립트
    clean_notification_script = """
    <script>
        (function() {
            // 앱이 시작되면 브라우저에 알림 권한을 요청합니다.
            if (window.Notification) {
                Notification.requestPermission();
            }

            // 알림을 직접 발송하는 공통 함수
            function sendAlert() {
                try {
                    if (Notification.permission === "granted" || window.Notification) {
                        new Notification("🚨 딴짓차단기 경고", {
                            body: "화면을 이탈했습니다! 즉시 업무 화면으로 복귀하세요.",
                            icon: "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=128&h=128&fit=crop",
                            tag: "distraction-alert" // 알림이 밀리지 않고 즉시 갱신
                        });
                    }
                } catch (err) {
                    console.log("알림 발송 제한 우회 처리 중", err);
                }
            }

            // [기능 1] 다른 탭으로 이동하거나 창을 내렸을 때 감지하여 알림 발송
            document.addEventListener("visibilitychange", () => {
                if (document.hidden) {
                    sendAlert();
                }
            });

            // [기능 2] 다른 프로그램 창(카톡, 메모장 등)을 클릭해서 포커스가 나갔을 때 감지하여 알림 발송
            window.addEventListener('blur', () => {
                sendAlert();
            });
        })();
    </script>
    """
    # 보이지 않게 처리하여 알림 기능만 백그라운드에서 동작하게 만듭니다.
    components.html(clean_notification_script, height=0)
    
    st.warning("⚠️ **테스트 방법:** 버튼을 누르고 알림 권한을 허용한 뒤, 다른 인터넷 탭을 누르거나 바탕화면을 클릭해 보세요. 화면 우측 하단에 알림 팝업이 바로 생성됩니다.")

else:
    st.write("대기 상태입니다. 상단의 '차단기 시작' 버튼을 누르면 작동합니다.")
