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

# 4. 차단기가 켜져 있을 때만 이탈 감지 실행
if st.session_state.is_running:
    st.markdown("### 🔒 현재 딴짓 감지 중...")
    
    # 두 코드를 완벽하게 합친 콤보 스크립트 (window.parent 완전 제거 버전)
    integrated_clean_script = """
    <div id="alertBox" style="width: 100%; height: 280px; background-color: #e8f5e9; border: 2px dashed #28a745; border-radius: 10px; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: all 0.3s ease;">
        <h2 id="mainAlertText" style="color: #28a745; margin: 0; font-family: sans-serif; font-size: 28px;">✅ 집중 모드 활성화 중</h2>
        <p id="subAlertText" style="color: #6c757d; margin-top: 15px; font-family: sans-serif; font-size: 16px;">다른 탭을 누르거나 창을 내리면 이 구역이 즉시 폭파됩니다.</p>
    </div>

    <script>
        const box = document.getElementById('alertBox');
        const mainText = document.getElementById('mainAlertText');
        const subText = document.getElementById('subAlertText');

        // [주신 코드 기능 1] 사용자가 다른 탭으로 도망치거나 창을 최소화했을 때 감지
        document.addEventListener("visibilitychange", () => {
            if (document.hidden) {
                // 이탈 시 구역 전체를 빨갛게 폭파
                box.style.backgroundColor = '#dc3545';
                box.style.borderColor = '#721c24';
                mainText.style.color = 'white';
                mainText.innerText = '🚨 딴짓 감지됨! 🚨';
                subText.style.color = '#f8d7da';
                subText.innerText = '화면을 이탈한 것이 감지되었습니다. 즉시 복귀하세요!';
            }
        });

        // [주신 코드 기능 2] 다른 창(카톡, 메모장 등)을 클릭해서 포커스가 빠져나갔을 때 감지
        window.addEventListener('blur', () => {
            box.style.backgroundColor = '#dc3545';
            box.style.borderColor = '#721c24';
            mainText.style.color = 'white';
            mainText.innerText = '🚨 딴짓 감지됨! 🚨';
            subText.style.color = '#f8d7da';
            subText.innerText = '다른 프로그램 창을 클릭했습니다. 즉시 복귀하세요!';
        });

        // 사용자가 원래 화면으로 돌아와서 박스를 클릭하면 다시 초록색(정상)으로 복구
        box.addEventListener('click', () => {
            box.style.backgroundColor = '#e8f5e9';
            box.style.borderColor = '#28a745';
            mainText.style.color = '#28a745';
            mainText.innerText = '✅ 집중 모드 활성화 중';
            subText.style.color = '#6c757d';
            subText.innerText = '다른 탭을 누르거나 창을 내리면 이 구역이 즉시 폭파됩니다.';
        });
    </script>
    """
    # 에러 없이 깔끔하게 iframe 내부에 안착시킵니다.
    components.html(integrated_clean_script, height=300)
    
    st.warning("⚠️ **실전 테스트:** '차단기 시작'을 누르고 다른 인터넷 탭을 켜거나, 카카오톡 등 다른 창을 클릭한 뒤 돌아와 보세요. 아래 상자가 빨갛게 폭파되어 있습니다.")

else:
    st.write("대기 상태입니다. 상단의 '차단기 시작' 버튼을 누르면 작동합니다.")
