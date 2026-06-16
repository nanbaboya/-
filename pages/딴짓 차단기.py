import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(page_title="딴짓차단기", page_icon="🚫", layout="centered")

st.title("🚫 딴짓차단기")
st.markdown("---")

# 2. 파이썬 버튼을 치우고, Streamlit 리런 에러가 없는 '자바스크립트 순정 버튼' 주입
st.markdown("""
    <div style="display: flex; gap: 15px; margin-bottom: 25px;">
        <button id="jsStartBtn" style="flex: 1; padding: 12px; background-color: #28a745; color: white; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer;">▶️ 차단기 시작</button>
        <button id="jsStopBtn" style="flex: 1; padding: 12px; background-color: #dc3545; color: white; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer;">⏹️ 차단기 종료</button>
    </div>
    
    <div id="statusBox" style="padding: 15px; border-radius: 5px; background-color: #f8f9fa; border: 1px solid #dee2e6; margin-bottom: 20px; font-weight: bold; color: #495057;">
        현재 상태: ⚪ 대기 중입니다. '차단기 시작'을 누르세요.
    </div>

    <script>
        // 변수 오염 및 중복 방지를 위한 즉시실행함수(IIFE) 처리
        (function() {
            if (window.Notification) {
                Notification.requestPermission();
            }

            // 1. 기존에 만들어진 경고창 레이어가 이미 있다면 완전 삭제 (초기화)
            if (window.globalBgLayer) {
                window.globalBgLayer.remove();
            }

            // 2. 경고창 레이어 생성 (단 딱 한 번만 부모 창에 등록)
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
            window.globalBgLayer.innerHTML = '<h1 style="font-size: 45px; font-weight: bold; margin-bottom: 20px;">🚨 딴짓 감지! 🚨</h1><h2>시스템 알림이 발송되었습니다. 즉시 복귀하세요.</h2><p style="margin-top: 20px; color: #eee;">이 화면을 마우스로 다시 클릭하면 경고가 숨겨집니다.</p>';
            window.parent.document.body.appendChild(window.globalBgLayer);

            // 작동 플래그 상태 기억 변수
            let isRunning = false;

            // 3. 버튼 오브젝트 매핑
            const startBtn = document.getElementById('jsStartBtn');
            const stopBtn = document.getElementById('jsStopBtn');
            const statusBox = document.getElementById('statusBox');

            // [시작 버튼 클릭]
            startBtn.onclick = function() {
                isRunning = true;
                statusBox.innerHTML = "현재 상태: 🔴 초정밀 딴짓 감지 가동 중!!";
                statusBox.style.backgroundColor = "#fde8e8";
                statusBox.style.borderColor = "#f8b4b4";
                statusBox.style.color = "#9b1c1c";
            };

            // [종료 버튼 클릭]
            stopBtn.onclick = function() {
                isRunning = false;
                window.globalBgLayer.style.display = 'none';
                statusBox.innerHTML = "현재 상태: ⚪ 대기 중입니다. '차단기 시작'을 누르세요.";
                statusBox.style.backgroundColor = "#f8f9fa";
                statusBox.style.borderColor = "#dee2e6";
                statusBox.style.color = "#495057";
            };

            // 4. 감시 센서 (중복 등록 방지를 위해 기존 센서 초기화 후 재등록)
            if (window.globalBlurHandler) {
                window.parent.removeEventListener('blur', window.globalBlurHandler);
            }

            window.globalBlurHandler = function() {
                // 시작 버튼이 눌린 상태에서만 경고창과 알림이 작동하도록 제어
                if (isRunning) {
                    window.globalBgLayer.style.display = 'flex';
                    try {
                        if (Notification.permission === "granted") {
                            new Notification("🚨 딴짓차단기 경고", {
                                body: "화면을 이탈했습니다! 즉시 복귀하세요.",
                                icon: "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=128&h=128&fit=crop",
                                tag: "
