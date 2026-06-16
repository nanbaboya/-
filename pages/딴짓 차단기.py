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
    if st.button("▶️ 차단기 시작", use_container_width=True):
        st.session_state.is_running = True
        st.success("딴짓 감지가 시작되었습니다! 화면을 유지하세요.")

with col2:
    if st.button("⏹️ 차단기 종료", use_container_width=True):
        st.session_state.is_running = False
        st.info("딴짓 감지가 안전하게 종료되었습니다.")

st.markdown("---")

# 4. 차단기가 켜져 있을 때만 이탈 감지 스크립트 실행
if st.session_state.is_running:
    st.markdown("### 🔒 현재 딴짓 감지 중...")
    
    # 이탈 시 화면에 경고 레이어를 띄우는 완전 안정형 스크립트
    ui_warning_script = """
    <script>
        // 경고 화면용 div 생성
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
        bgLayer.innerHTML = '<h1 style="font-size: 45px; font-weight: bold; margin-bottom: 20px;">🚨 딴짓 감지! 🚨</h1><h2>이탈이 기록되고 있습니다. 즉시 복귀하세요.</h2><p style="margin-top: 20px; color: #eee;">이 화면을 다시 클릭하면 경고가 숨겨집니다.</p>';
        window.parent.document.body.appendChild(bgLayer);

        // 사용자가 다른 창을 클릭하는 순간 즉시 빨간 경고창 활성화
        window.parent.addEventListener('blur', () => {
            bgLayer.style.display = 'flex';
        });

        // 다시 돌아와서 클릭하면 경고창 해제
        bgLayer.addEventListener('click', () => {
            bgLayer.style.display = 'none';
        });
    </script>
    """
    components.html(ui_warning_script, height=0)
    
    st.warning("⚠️ 테스트: '차단기 시작'을 누른 상태에서 메모장이나 카카오톡 등 다른 창을 클릭해 보세요. 화면 전체가 즉시 빨갛게 변합니다.")

else:
    st.write("대기 상태입니다. 상단의 '차단기 시작' 버튼을 누르면 작동합니다.")
