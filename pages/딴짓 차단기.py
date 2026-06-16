import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정
st.set_page_config(page_title="딴짓차단기", page_icon="🚫", layout="centered")

st.title("🚫 딴짓차단기")
st.markdown("---")

# 2. 세션 상태 초기화 (시작/종료 상태 저장)
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# 3. 제어 버튼 (시작 / 종료)
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ 차단기 시작", use_container_width=True):
        st.session_state.is_running = True
        st.success("딴짓 감지가 시작되었습니다! 브라우저 권한 팝업이 뜨면 '허용'을 눌러주세요.")

with col2:
    if st.button("⏹️ 차단기 종료", use_container_width=True):
        st.session_state.is_running = False
        st.info("딴짓 감지가 종료되었습니다.")

st.markdown("---")

# 4. 차단기가 활성화되었을 때만 감지 스크립트 가동
if st.session_state.is_running:
    st.markdown("### 🔒 현재 초정밀 딴짓 감지 중...")

    # 화면 잠금 UI + 시스템 알림 결합 스크립트
    total_block_script = """
    <script>
        // [알림 권한] 시작 버튼 활성화와 동시에 브라우저 알림 권한 강력 요청
        if (window.Notification) {
            Notification.requestPermission();
        }

        // [화면 잠금 UI] 경고 레이어 미리 생성 및 설정
        const bgLayer = document.createElement('div');
        bgLayer.style.position = 'fixed';
        bgLayer.style.top = '0';
        bgLayer.style.left = '0';
        bgLayer.style.width = '100vw';
        bgLayer.style.height = '100vh';
        bgLayer.style.backgroundColor = 'rgba(235, 64, 52, 0.95)';
        bgLayer.style.color = 'white';
        bgLayer.style.display = 'none';
        bgLayer.style.flexDirection = 'column';
        bgLayer.style.justifyContent = 'center';
        bgLayer.style.alignItems = 'center';
        bgLayer.style.zIndex = '99999';
        bgLayer.innerHTML = '<h1 style="font-size: 45px; font-weight: bold; margin-bottom: 20px;">🚨 딴짓 감지! 🚨</h1><h2>시스템 알림이 발송되었습니다. 즉시 복귀하세요.</h2><p style="margin-top: 20px; color: #eee;">이 화면을 마우스로 다시 클릭하면 경고가 숨겨집니다.</p>';
        window.parent.document.body.appendChild(bgLayer);

        // 사용자가 다른 창을 클릭하여 이탈하는 순간 (blur) 즉시 실행
        window.parent.addEventListener('blur', () => {
            // 1. 빨간 화면 잠금 켜기
            bgLayer.style.display = 'flex';

            // 2. 바탕화면 시스템 알림 강제 발송
            try {
                if (Notification.permission === "granted" || window.Notification) {
                    new Notification("🚨 딴짓차단기 경고", {
                        body: "화면을 이탈했습니다! 즉시 복귀하세요.",
                        icon: "
