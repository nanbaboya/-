import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="딴짓차단기", page_icon="🚫", layout="centered")

st.title("🚫 딴짓차단기")
st.markdown("---")

# 2. 세션 상태 초기화
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# 3. 제어 버튼 (클릭을 유도하여 브라우저 활성화)
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
    
    # 이탈할 때마다 문구가 랜덤으로 바뀌는 스크립트
    random_notification_script = """
    <script>
        (function() {
            if (window.Notification) {
                Notification.requestPermission();
            }

            // 🎯 팀원들 킹받게 할 랜덤 알림 문구 셋팅 (원하는 대로 수정 가능!)
            const warningMessages = [
                "CCTV는 당신을 지켜보고 있습니다. 당장 복귀하세요.",
                "지금 보신 거 재밌으셨나요? 이제 일할 시간입니다.",
                "월급 루팡 시도 감지! 모니터로 눈을 돌리십시오.",
                "팀장님이 뒤에서 걸어오고 계실지도 모릅니다.",
                "집중력이 흐려지셨군요. 다시 업무 화면을 보세요!",
                "앗! 딴짓 필터에 딱 걸리셨습니다. 얼른 돌아오세요.",
                "방금 나간 이탈 기록이 카운트되고 있습니다... 읍읍"
            ];

            function sendAlert() {
                try {
                    if (Notification.permission === "granted") {
                        // 리스트에서 무작위로 문구 하나 추출
                        const randomIndex = Math.floor(Math.random() * warningMessages.length);
                        const selectedMessage = warningMessages[randomIndex];

                        new Notification("🚨 딴짓차단기 경고", {
                            body: selectedMessage, // 매번 다른 문구 발송
                            icon: "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=128&h=128&fit=crop",
                            // tag를 제거하거나 매번 다르게 주어 브라우저가 새 알림으로 인식하게 만듭니다.
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
