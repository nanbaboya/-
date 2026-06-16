import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(page_title="딴짓차단기", page_icon="🚫", layout="centered")

st.title("🚫 딴짓차단기")
st.markdown("---")

# 2. 리런 에러가 없는 순정 자바스크립트 버튼 및 상태창 주입
st.markdown("""
    <div style="display: flex; gap: 15px; margin-bottom: 25px;">
        <button id="jsStartBtn" style="flex: 1; padding: 12px; background-color: #28a745; color: white; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer;">▶️ 차단기 시작</button>
        <button id="jsStopBtn" style="flex: 1; padding: 12px; background-color: #dc3545; color: white; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer;">⏹️ 차단기 종료</button>
    </div>
    
    <div id="statusBox" style="padding: 15px; border-radius: 5px; background-color: #f8f9fa; border: 1px solid #dee2e6; margin-bottom: 20px; font-weight: bold; color: #495057;">
        현재 상태: ⚪ 대기 중입니다. '차단기 시작'을 누르세요.
    </div>

    <script>
        (function() {
            // 1. 기존 경고창 엘리먼트 초기화
            if (window.globalBgLayer) {
                window.globalBgLayer.remove();
            }

            // [구글 무료 알람 사운드 링크] 권한 제한 없는 순정 오디오 객체 생성
            if (!window.globalAudio) {
                window.globalAudio = new Audio('https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg');
                window.globalAudio.loop = true; // 돌아올 때까지 무한 반복
            }

            // 2. 경고 화면 레이어 생성
            window.globalBgLayer = document.createElement('div');
            window.globalBgLayer.style.position = 'fixed';
            window.globalBgLayer.style.top = '0';
            window.globalBgLayer.style.left = '0';
            window.globalBgLayer.style.width = '100vw';
            window.globalBgLayer.style.height = '100vh';
            window.globalBgLayer.style.backgroundColor = 'rgba(235, 64, 52, 0.95)';
            window.globalBgLayer.style.color = 'white';
            window.globalBgLayer.style.display = 'none';
            window.globalBgLayer.style.flexDirection = 'column';
            window.globalBgLayer.style.justifyContent = 'center';
            window.globalBgLayer.style.alignItems = 'center';
            window.globalBgLayer.style.zIndex = '99999';
            window.globalBgLayer.innerHTML = '<h1 style="font-size: 45px; font-weight: bold; margin-bottom: 20px;">🚨 딴짓 감지! 🚨</h1><h2>경고음이 울리고 있습니다. 즉시 복귀하세요.</h2><p style="margin-top: 20px; color: #eee;">이 화면을 마우스로 다시 클릭하면 소리가 꺼집니다.</p>';
            window.parent.document.body.appendChild(window.globalBgLayer);

            let isRunning = false;

            const startBtn = document.getElementById('jsStartBtn');
            const stopBtn = document.getElementById('jsStopBtn');
            const statusBox = document.getElementById('statusBox');

            // [시작 버튼]
            startBtn.onclick = function() {
                isRunning = true;
                statusBox.innerHTML = "현재 상태: 🔴 초정밀 소리 폭탄 가동 중!!";
                statusBox.style.backgroundColor = "#fde8e8";
                statusBox.style.borderColor = "#f8b4b4";
                statusBox.style.color = "#9b1c1c";
            };

            // [종료 버튼]
            stopBtn.onclick = function() {
                isRunning = false;
                window.globalAudio.pause();
                window.globalAudio.currentTime = 0;
                window.globalBgLayer.style.display = 'none';
                statusBox.innerHTML = "현재 상태: ⚪ 대기 중입니다. '차단기 시작'을 누르세요.";
                statusBox.style.backgroundColor = "#f8f9fa";
                statusBox.style.borderColor = "#dee2e6";
                statusBox.style.color = "#495057";
            };

            // 3. 기존 센서 초기화 후 재등록
            if (window.globalBlurHandler) {
                window.parent.removeEventListener('blur', window.globalBlurHandler);
            }

            window.globalBlurHandler = function() {
                if (isRunning) {
                    // 화면 빨갛게 바꾸고 바로 소리 지르기
                    window.globalBgLayer.style.display = 'flex';
                    window.globalAudio.play().catch(e => console.log("오디오 재생 트리거"));
                }
            };

            window.parent.addEventListener('blur', window.globalBlurHandler);

            // 경고창 클릭 시 소리 끄고 화면 해제
            window.globalBgLayer.onclick = function() {
                window.globalAudio.pause();
                window.globalAudio.currentTime = 0;
                window.globalBgLayer.style.display = 'none';
            };
        })();
    </script>
""", unsafe_allow_html=True)

st.warning("⚠️ **작동 및 무한 반복 테스트 방법**")
st.markdown("""
1. 컴퓨터 **스피커 소리**를 적당히 키워둡니다.
2. 녹색 **'▶️ 차단기 시작'** 버튼을 클릭합니다.
3. 화면 빈 곳을 마우스로 **콕 한 번 클릭**합니다. (브라우저 정책상 웹페이지 소리를 재생하려면 무조건 이 터치 단계를 거쳐야 합니다.)
4. 다른 프로그램 창(카톡, 메모장 등)을 클릭해 봅니다. **즉시 빨간 화면과 함께 알람 벨소리가 무한 반복**됩니다.
5. 돌아와서 빨간 화면을 클릭해 소리를 끄고, **'⏹️ 차단기 종료'**를 누르면 해제됩니다. 이 짓을 몇 번을 반복해도 똑같이 완벽하게 작동합니다.
""")
