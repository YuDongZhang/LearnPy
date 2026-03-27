# 4. Streamlit/Gradio前端

## Streamlit

Python原生的Web框架，写Python就能出页面，AI应用首选。

### 核心组件
- `st.chat_input()` — 聊天输入框
- `st.chat_message()` — 聊天气泡
- `st.sidebar` — 侧边栏（设置、历史）
- `st.session_state` — 会话状态管理
- `st.write_stream()` — 流式输出

### 运行
```bash
streamlit run app.py
```

## Gradio

专为ML模型设计的前端框架，组件更丰富。

### 核心组件
- `gr.ChatInterface()` — 一行代码搞定聊天界面
- `gr.Blocks()` — 自定义布局
- `gr.File()` — 文件上传（RAG场景）

### 运行
```python
demo = gr.ChatInterface(fn=chat_fn)
demo.launch()
```

## Streamlit vs Gradio

| 特性 | Streamlit | Gradio |
|------|-----------|--------|
| 上手难度 | 很低 | 很低 |
| 自定义程度 | 中 | 中 |
| 聊天界面 | 好 | 很好 |
| 文件上传 | 支持 | 更方便 |
| 部署 | Streamlit Cloud | HuggingFace Spaces |
| 适用 | 通用AI应用 | 模型Demo |

## 会话状态管理

聊天应用需要维护对话历史：
```python
if "messages" not in st.session_state:
    st.session_state.messages = []
```

## 与后端对接

前端通过HTTP请求调用后端API：
```python
import httpx
response = httpx.post("http://localhost:8080/chat", json={"message": user_input})
```
