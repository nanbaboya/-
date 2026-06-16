import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="딴짓차단기", page_icon="🚫", layout="centered")

st.title("🚫 딴짓차단기 (마우스 가둠 버전)")
st.markdown("---")

# Streamlit 내부 가상 틀(iframe) 안에서 마우스가 나가는 것을 감지하는 스크립트
iframe_lock_script = """
<script>
    // 1. 알람 소리 설정 (구글 무료 오디오 소스)
    const audio = new Audio('https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg');
    audio.loop = true;

    // 2. 경고 화면 스타일 설정
    const warningLayer = document.createElement('div');
    warningLayer.style.position = 'fixed';
    warningLayer.style.top = '0';
    warningLayer.style.left = '0';
    warningLayer.style.width = '100%';
    warningLayer.style.height = '100%';
    warningLayer.style.backgroundColor = 'red';
    warningLayer.style.color = 'white';
    warningLayer.style.display = 'none';
    warningLayer.style.flexDirection = 'column';
    warningLayer.style.justifyContent = 'center';
    warningLayer.style.alignItems = 'center';
    warningLayer.style.zIndex = '999999';
    warningLayer.innerHTML = '<h1 style="font-size: 40px; font-weight: bold;">🚨 마우스 이탈 감지! 🚨</h1><p style="font-size: 20px; margin-top: 20px;">마우스를 즉시 이 화면 안으로 가져오세요!</p>';
    document.body.appendChild(warningLayer);

    // 3. 마우스가 웹 화면 밖으로 나갔을 때 실행 (mouseleave)
    document.addEventListener('mouseleave', () => {
        audio.play().catch(e => console.log("오디오 재생 제한 유도"));
        warningLayer.style.display = 'flex';
    });

    // 4. 마우스가 다시 웹 화면 안으로 들어왔을 때 실행 (mouseenter)
    document.addEventListener('mouseenter', () => {
        audio.pause();
        audio.currentTime = 0;
        warningLayer.style.display = 'none';
    });
</script>
"""

# HTML 스크립트 실행 (iframe의 크기를 키워 감지 영역을 넓힙니다)
components.html(iframe_lock_script, height=300)

# 안내 문구
st.error("### 🔒 마우스 잠금 감지기 가동 중")
st.markdown("""
💡 **팀원 행동 규칙:**
1. 이 웹페이지를 모니터 한쪽에 띄워둡니다.
2. **마우스 커서를 반드시 이 앱 화면(아래 회색 영역 근처)에 올려두어야 합니다.**
3. 메신저를 켜거나 유튜브를 틀기 위해 마우스를 이 화면 밖으로 던지는 순간 **즉시 강력한 사이렌**이 울립니다.
""")

st.info("⚠️ **지금 테스트해 보세요:** 마우스를 이 창 아래쪽으로 내렸다가, 인터넷 주소창이나 모니터 바탕화면 쪽으로 빠르게 올려서 화면 밖으로 완전히 빼보세요. 바로 작동합니다.")
