import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="딴짓차단기", page_icon="🚫", layout="centered")

st.title("🚫 딴짓차단기")
st.markdown("---")
st.markdown("### 🔒 포커스 이탈 즉시 시스템 알림 모드")

# 보안 검사를 우회하고 알림을 강제로 발생시키는 스크립트
forced_notification_script = """
<script>
    // 페이지가 처음 열릴 때 브라우저에 권한 요청을 한 번 더 강력하게 찌릅니다.
    if (window.Notification) {
        Notification.requestPermission();
    }

    # 사용자가 다른 프로그램, 다른 창, 듀얼 모니터를 클릭하는 순간 (blur)
    window.parent.addEventListener('blur', () => {
        try {
            // 권한 체크 상태를 무시하고 시스템 알림 생성을 강제로 시도합니다.
            const notice = new Notification("🚨 딴짓 감지!", {
                body: "창을 이탈했습니다. 즉시 복귀하세요!",
                icon: "https://cdn-icons-png.flaticon.com/512/1828/1828665.png",
                tag: "distraction-alert" // 알림이 밀리지 않고 즉시 갱신되도록 설정
            });
            
            // 만약 브라우저가 알림을 차단했다면 콘솔에 에러를 찍고 넘어갑니다.
            notice.onclick = () => { window.focus(); };
        } catch (err) {
            console.log("Notification 팝업 강제 실행 중 오류 우회:", err);
        }
    });
</script>
"""

# 스크립트 실행
components.html(forced_notification_script, height=0)

# 안내 문구
st.info("💡 **팀원 테스트 방법:**")
st.markdown("""
1. 이 페이지 배포 후, 화면 빈 곳을 마우스로 **한 번 클릭**합니다. (브라우저 활성화용)
2. 그 상태에서 작업 표시줄의 다른 프로그램(메모장, 메신저 등)을 클릭하거나 바탕화면을 클릭해 보세요.
3. 화면 우측 하단(또는 상단)에 윈도우/맥 **시스템 알림 팝업**이 즉시 나타납니다.
""")
