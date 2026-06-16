import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="딴짓차단기", page_icon="🚫")
st.title("🚫 딴짓차단기")

# 브라우저 알림 + 이탈 감지 스크립트
detection_script = """
<script>
    // 페이지 로드 시 알림 권한 요청
    if (Notification.permission !== "granted") {
        Notification.requestPermission();
    }

    document.addEventListener("visibilitychange", () => {
        if (document.hidden) {
            // 이탈 시 시스템 알림 발송
            if (Notification.permission === "granted") {
                new Notification("딴짓차단기", {
                    body: "⚠️ 즉시 화면으로 돌아오세요! 딴짓 감지됨.",
                    icon: "https://cdn-icons-png.flaticon.com/512/1828/1828665.png"
                });
            }
        }
    });
</script>
"""
components.html(detection_script, height=0)

st.markdown("### 🔒 보안 알림 활성화됨")
st.write("브라우저의 **알림 권한을 허용**해주셔야 이탈 즉시 시스템 알림을 받을 수 있습니다.")
st.warning("화면을 나가면 브라우저 상단/우측에 경고 알림이 즉시 나타납니다.")
