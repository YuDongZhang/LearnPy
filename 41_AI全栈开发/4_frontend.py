"""
4. Streamlit前端 - 代码示例
一个完整的聊天界面，支持流式输出。

运行: streamlit run 4_frontend.py
"""

import streamlit as st
import httpx

API_BASE = "http://localhost:8080"

st.set_page_config(page_title="AI聊天助手", page_icon="🤖")
st.title("🤖 AI聊天助手")

# ========== 侧边栏设置 ==========
with st.sidebar:
    st.header("设置")
    model = st.selectbox("模型", ["qwen2.5:7b", "llama3.1:8b"])
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7)
    if st.button("清空对话"):
        st.session_state.messages = []
        st.rerun()

# ========== 会话状态 ==========
if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== 显示历史消息 ==========
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ========== 用户输入 ==========
if prompt := st.chat_input("输入你的问题..."):
    # 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 调用后端API
    with st.chat_message("assistant"):
        try:
            response = httpx.post(
                f"{API_BASE}/chat",
                json={"message": prompt},
                timeout=60,
            )
            answer = response.json()["answer"]
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"请求失败: {e}\n请确认后端已启动")
