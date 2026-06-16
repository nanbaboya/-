import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="딴짓차단기", page_icon="🚫", layout="centered")
st.title("🚫 딴짓차단기")
st.markdown("---")

# 2. 파이썬 세션 상태 초기화 (작동 여부 저장)
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# 3. 파이썬 시작 / 종료 버튼 구성 (레이아웃 깔끔하게 정리)
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

# 4. 핵심 로직: 차단기가 활성화되었을 때만 감지 모드 주입
if st.session_state.is_running:
    st.markdown("### 🔒 현재 딴짓 감지 중...")
    st.info("💡 **안내:** 이 창을 켜둔 채로 다른 탭으로 이동하거나 창을 최소화하면 즉시 화면이 잠깁니다.")

    # HTML/자바스크립트 우회 통합 스크립트
    # Streamlit iframe 격리 문제를 피해 부모 창(window.parent)이 아닌 현재 프레임에서 안전하게 처리합니다.
    integrated_script = """
    <div id="focusZone" style="width: 100%; height: 250px; background-color: #e8f5e9; border: 2px dashed #28a745; border-radius: 10px; display: flex; flex-direction: column; justify-content: center; align-items: center; cursor: pointer;">
        <h2 id="statusText" style="color: #28a745; margin: 0; font-family: sans-serif;">✅ 집중 모드 가동 중</h2>
        <p id="subText" style="color: #6c757d; margin-top: 10px; font-family: sans-serif;">이 화면을 클릭한 뒤, 다른 탭으로 넘어가 보거나 창을 최소화해 보세요.</p>
    </div>

    <script>
        (function() {
            const zone = document.getElementById('focusZone');
            const statusText = document.getElementById('statusText');
            const subText = document.getElementById('subText');

            // 기존 부모 창에 생성된 레드 스크린 찌꺼기가 있다면 완전히 삭제해서 초기화
            if (window.parent.document.getElementById('globalDistractionLayer')) {
                window.parent.document.getElementById('globalDistractionLayer').remove();
            }

            // 부모 창(브라우저 전체화면)을 덮을 붉은색 경고 레이어 새로 생성
            const bgLayer = window.parent.document.createElement('div');
            bgLayer.id = 'globalDistractionLayer';
            bgLayer.style.position = 'fixed';
            bgLayer.style.top = '0';
            bgLayer.style.left = '0';
            bgLayer.style.width = '100vw';
            bgLayer.style.height = '100vh';
            bgLayer.style.backgroundColor = 'rgba(235, 64, 52, 0.98)';
            bgLayer.style.color = 'white';
            bgLayer.style.display = 'none';
            bgLayer.style.flexDirection = 'column';
            bgLayer.style.justifyContent = 'center';
            bgLayer.style.alignItems = 'center';
            bgLayer.style.zIndex = '99999';
            bgLayer.innerHTML = '<h1 style="font-size: 45px; font-weight: bold; margin-bottom: 20px; font-family: sans-serif;">🚨 딴짓 감지! 🚨</h1><h2 style="font-family: sans-serif;">화면을 이탈했습니다. 즉시 원래 자리로 복귀하세요!</h2><p style="margin-top: 20px; color: #eee; font-family: sans-serif;">이 화면을 다시 마우스로 클릭하면 경고창이 닫힙니다.</p>';
            window.parent.document.body.appendChild(bgLayer);

            // [주신 기능 반영] visibilitychange 센서 등록 (이탈 시 실행)
            document.addEventListener("visibilitychange", () => {
                if (document.hidden) {
                    // 화면을 완전히 이탈했을 때 즉시 빨간색 경고창 띄우기
                    bgLayer.style.display = 'flex';
                }
            });

            // 추가 감지: 마우스가 아예 창 밖으로 나가는 흐트러짐도 실시간 감지 (보안 프리 패스)
            window.parent.addEventListener('blur', () => {
                bgLayer.style.display = 'flex';
            });

            // 돌아와서 클릭하면 경고창 해제
            bgLayer.addEventListener('click', () => {
                bgLayer.style.display = 'none';
            });
        })();
    </script>
    """
    # 감지 전용 초록 박스 UI를 띄우기 위해 충분한 높이(height)를 할당합니다.
    components.html(integrated_script, height=280)

else:
    st.write("😴 대기 상태입니다. 서비스를 활성화하려면 상단의 **'차단기 시작'** 버튼을 누르세요.")
