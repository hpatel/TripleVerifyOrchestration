import streamlit as st
import time
from api import run_query, stream_query

st.set_page_config(page_title="AI Agent Chat", layout="wide")

# -------------------------
# Session state
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory_panel" not in st.session_state:
    st.session_state.memory_panel = []

if "tool_logs" not in st.session_state:
    st.session_state.tool_logs = []

# -------------------------
# Sidebar
# -------------------------
st.sidebar.title("🧠 System Panels")

with st.sidebar.expander("Memory", expanded=True):
    for m in st.session_state.memory_panel:
        st.write(m)

with st.sidebar.expander("Tool Logs", expanded=True):
    for t in st.session_state.tool_logs:
        st.json(t)

show_debug = st.sidebar.checkbox("Show Debug Trace")

# -------------------------
# Main UI
# -------------------------
st.title("💬 Multi-Agent Chat System")

# Render chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask anything...")

# -------------------------
# Handle input
# -------------------------
if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            start = time.time()

            payload = {
                "query": user_input,
                "history": st.session_state.messages
            }

            # -------------------------
            # Try streaming first
            # -------------------------
            try:
                for chunk in stream_query(payload):
                    full_response += chunk
                    placeholder.markdown(full_response)
            except Exception:
                # fallback to normal request
                data = run_query(payload)
                full_response = data.get("final_answer", "")
                placeholder.markdown(full_response)

            latency = time.time() - start

            # Save message
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

            # If we used non-streaming, we still need metadata
            try:
                data
            except:
                data = run_query(payload)

            # -------------------------
            # Panels
            # -------------------------
            st.session_state.memory_panel = data.get("memory_used", []) + data.get("memory_written", [])
            st.session_state.tool_logs = data.get("tools_used", [])

            if show_debug:
                st.subheader("🧪 Critic Loop")
                for i, c in enumerate(data.get("critic_history", [])):
                    with st.expander(f"Critic Iter {i+1}"):
                        st.json(c)

                st.subheader("🛡 Safety Loop")
                for i, s in enumerate(data.get("safety_history", [])):
                    with st.expander(f"Safety Iter {i+1}"):
                        st.json(s)

            st.caption(f"⏱ {latency:.2f}s")

        except Exception as e:
            placeholder.error(str(e))