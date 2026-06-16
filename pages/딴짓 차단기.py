import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(page_title="딴짓차단기", page_icon="🚫", layout="centered")

st.title("🚫 딴짓차단기")
st.markdown("---")

# 2. 세션 상태 초기화
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# 3. 제어 버튼
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ 차단기 시작", use_container_width=True):
        st.session_state.is_running = True
        st.success("딴짓 감지가 시작되었습니다!")

with col2:
    if st.button("⏹️ 차단기 종료", use_container_width=True):
        st.session_state.is_running = False
        st.info("딴짓 감지가 종료되었습니다.")

st.markdown("---")

# 4. 활성화 시 자바스크립트 주입
if st.session_state.is_running:
    st.markdown("### 🔒 현재 초정밀 딴짓 감지 중...")

    # 초기화 로직이 추가된 자바스크립트
    st.markdown("""
        <script>
            if (window.Notification) {
                Notification.requestPermission();
            }

            // [핵심 수정] 이전 실행 때 만들어진 경고창 엘리먼트가 남아있다면 완전히 삭제하여 리셋
            if (window.bgLayer) {
                window.bgLayer.remove();
                window.bgLayer = null;
            }

            # 새로운 경고 배경 레이어 생성
            window.bgLayer = document.createElement('div');
            window.bgLayer.style.position = 'fixed';
            window.bgLayer.style.top = '0';
            window.bgLayer.style.left = '0';
            window.bgLayer.style.width = '100vw';
            window.bgLayer.style.height = '100vh';
            window.bgLayer.style.backgroundColor = 'rgba(235, 64, 52, 0.95)';
            window.bgLayer.style.color = 'white';
            window.bgLayer.style.display = 'none';
            window.bgLayer.style.flexDirection = 'column';
            window.bgLayer.style.justifyContent = 'center';
            window.bgLayer.style.alignItems = 'center';
            window.bgLayer.style.zIndex = '99999';
            window.bgLayer.innerHTML = '<h1 style="font-size: 45px; font-weight: bold; margin-bottom: 20px;">🚨 딴짓 감지! 🚨</h1><h2>시스템 알림이 발송되었습니다. 즉시 복귀하세요.</h2><p style="margin-top: 20px; color: #eee;">이 화면을 마우스로 다시 클릭하면 경고가 숨겨집니다.</p>';
            window.parent.document.body.appendChild(window.bgLayer);

            // [핵심 수정] 기존에 등록된 감시 센서(blur 함수)가 있다면 중복 등록 방지를 위해 초기화
            if (window.blurHandler) {
                window.parent.removeEventListener('blur', window.blurHandler);
            }

            // 새로운 감시 함수 정의
            window.blurHandler = function() {
                window.bgLayer.style.display = 'flex';
                try {
                    if (Notification.permission === "granted") {
                        new Notification("🚨 딴짓차단기 경고", {
                            body: "화면을 이탈했습니다! 즉시 복귀하세요.",
                            icon: "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=128&h=128&fit=crop",
                            tag: "distraction-alert"
                        });
                    }
                } catch (err) { }
            };

            // 감시 센서 작동 시작
            window.parent.addEventListener('blur', window.blurHandler);

            // 클릭 시 해제 이벤트
            window.bgLayer.addEventListener('click', () => {
                window.bgLayer.style.display = 'none';
            });
        </script>
    """, unsafe_allow_html=True)

    st.warning("⚠️ '차단기 시작'을 누른 후, 화면을 한 번 클릭했다가 다른 창을 클릭해 보세요!")
else:
    # 차단기 종료 버튼을 누르면 브라우저 감시 센서와 빨간 창을 완전히 제거
    st.markdown("""
        <script>
            if (window.bgLayer) {
                window.bgLayer.remove();
                window.bgLayer = null;
            }
            if (window.blurHandler) {
                window.parent.removeEventListener('blur', window.blurHandler);
                window.blurHandler = null;
            }
        </script>
    """, unsafe_allow_html=True)
    st.write("대기 상태입니다. '차단기 시작' 버튼을 누르세요.")
