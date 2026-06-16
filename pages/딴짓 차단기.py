import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="딴짓차단기", page_icon="🚫", layout="centered")

st.title("🚫 딴짓차단기")
st.markdown("---")

# 2. 세션 상태 초기화
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# 3. 제어 버튼
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

# 4. 차단기 가동 시 랜덤 알림 자바스크립트 주입
if st.session_state.is_running:
    st.markdown("### 🔒 현재 딴짓 알림 감지 중...")
    
    # 파이썬 주석(#)을 제거하고 자바스크립트 표준 주석(//)으로 교체한 안전한 스크립트
    random_notification_script = """
    <script>
        (function() {
            if (window.Notification) {
                Notification.requestPermission();
            }

            // 🎯 팀원용 랜덤 알림 문구 세팅
            const warningMessages = [
                "CCTV는 당신을 지켜보고 있습니다. 당장 복귀하세요.",
                "지금 보신 거 재밌으셨나요? 이제 일할 시간입니다.",
                "월급 루팡 시도 감지! 모니터로 눈을 돌리십시오.",
                "팀장님이 뒤에서 걸어오고 계실지도 모릅니다.",
                "집중력이 흐려지셨군요. 다시 업무 화면을 보세요!",
                "앗! 딴짓 필터에 딱 걸리셨습니다. 얼른 돌아오세요.",
                "방금 나간 이탈 기록이 카운트되고 있습니다..."
            ];

            function sendAlert() {
                try {
                    if (Notification.permission === "granted") {
                        const randomIndex = Math.floor(Math.random() * warningMessages.length);
                        const selectedMessage = warningMessages[randomIndex];

                        new Notification("🚨 딴짓차단기 경고", {
                            body: selectedMessage,
                            icon: "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=128&h=128&fit=crop",
                            tag: "alert-" + Date.now() 
                        });
                    }
                } catch (err) {
                    console.log("알림 제한 우회 중", err);
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
    components.html(random_notification_script, height=0)
    
    st.warning("⚠️ **테스트 방법:** 시작 버튼 누르고 화면을 한 번 클릭한 뒤, 다른 창을 연달아 클릭해 보세요. 클릭할 때마다 매번 새로운 문구로 알림이 쏟아집니다.")

else:
    st.write("대기 상태입니다. 상단의 '차단기 시작' 버튼을 누르세요.")
