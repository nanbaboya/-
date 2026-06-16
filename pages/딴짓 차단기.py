import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="딴짓차단기", page_icon="🚫", layout="centered")

st.title("🚫 딴짓차단기 (보안 우회 버전)")
st.markdown("---")

# 시스템 알림창 대신 '소리(Audio)'와 '화면 차단(UI)'을 이용한 무조건 실행 스크립트
bug_free_script = """
<script>
    # 1. 경고음으로 사용할 오디오 생성 (무료 사이렌 사운드)
    const audio = new Audio('https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg');
    audio.loop = true; // 돌아올 때까지 무한 반복

    # 2. 화면을 가릴 경고 레이어 생성
    const warningDiv = document.createElement('div');
    warningDiv.style.position = 'fixed';
    warningDiv.style.top = '0';
    warningDiv.style.left = '0';
    warningDiv.style.width = '100vw';
    warningDiv.style.height = '100vh';
    warningDiv.style.backgroundColor = 'rgba(255, 0, 0, 0.95)';
    warningDiv.style.color = 'white';
    warningDiv.style.display = 'none';
    warningDiv.style.flexDirection = 'column';
    warningDiv.style.justifyContent = 'center';
    warningDiv.style.alignItems = 'center';
    warningDiv.style.zIndex = '99999';
    warningDiv.innerHTML = '<h1 style="font-size: 50px; font-weight: bold; margin-bottom: 20px;">🚨 딴짓 감지됨!! 🚨</h1><h2>즉시 원래 업무 화면으로 복귀하세요.</h2><p style="margin-top: 30px; font-size: 14px; color: #ddd;">이 화면을 클릭하면 경고가 해제됩니다.</p>';
    window.parent.document.body.appendChild(warningDiv);

    # 3. 사용자가 다른 곳을 클릭하거나 창을 나갔을 때 (blur)
    window.parent.addEventListener('blur', () => {
        audio.play().catch(e => console.log("오디오 재생 재생 제한 유도"));
        warningDiv.style.display = 'flex';
    });

    # 4. 사용자가 다시 돌아와서 이 화면을 클릭했을 때 (focus)
    warningDiv.addEventListener('click', () => {
        audio.pause();
        audio.currentTime = 0;
        warningDiv.style.display = 'none';
    });
</script>
"""

# 스크립트 강제 삽입
components.html(bug_free_script, height=0)

# 안내 문구
st.error("### 🔒 초강력 딴짓 감지 모드 가동 중")
st.markdown("""
이 웹페이지를 켜둔 상태에서 **다른 프로그램(메신저, 웹서핑 등)을 클릭하는 순간** 즉시 작동합니다.
* 🚨 **증상:** 귀가 찢어지는 경고음 무한 재생 + 전체 화면이 빨간색 경고창으로 잠김.
* 🔓 **해제 방법:** 빨간색 경고 화면을 마우스로 다시 클릭하면 소리가 꺼집니다.
""")
st.warning("⚠️ **테스트 방법:** 코드 배포 후, 화면 빈 곳을 한 번 클릭해 주신 다음, 메신저나 메모장 등 다른 창을 클릭해 보세요!")
