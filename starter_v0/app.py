from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any
import yaml

import streamlit as st

# Load project modules
from env_loader import load_lab_env
from providers import make_provider
from providers.base import ToolCall
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version
from chat import (
    assistant_tool_message, 
    execute_tool_call, 
    tool_results_message, 
    trim_history, 
    safe_slug, 
    now_iso, 
    write_transcript
)

# Page Setup
st.set_page_config(
    page_title="Research Agent UI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="auto"
)

# Load environment variables
ROOT = Path(__file__).parent
load_lab_env(ROOT)

# Custom CSS for Gemini LIGHT theme and hiding sidebar
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600&display=swap');

/* Custom Sidebar Style */
[data-testid="stSidebar"] {
    background-color: #f8f9fa !important;
    border-right: 1px solid #dadce0 !important;
}
.st-emotion-cache-1dp555f {
    display: none !important;
}

/* Base style overrides - Light Theme */
.stApp {
    background: linear-gradient(180deg, #f0f4f9 0%, #f7f9fc 35%, #ffffff 100%) !important;
    color: #1f1f1f !important;
    font-family: 'Outfit', sans-serif;
}

/* Custom header */
.header-container {
    text-align: center;
    padding: 1.5rem 0 1rem 0;
}

.gradient-title {
    background: linear-gradient(90deg, #4285f4 0%, #9b51e0 35%, #e05194 70%, #f4b400 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Outfit', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.gradient-subtitle {
    color: #5f6368;
    font-size: 1.1rem;
    font-weight: 400;
    margin-bottom: 1rem;
}

/* Chat bubble styling - Light mode */
div[data-testid="stChatMessage"] {
    background-color: #ffffff !important;
    border: 1px solid #dadce0 !important;
    border-radius: 20px !important;
    padding: 16px 20px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
    color: #1f1f1f !important;
}

div[data-testid="stChatMessage"]:hover {
    border-color: rgba(66, 133, 244, 0.4) !important;
    box-shadow: 0 4px 12px rgba(66, 133, 244, 0.08);
}

/* Accent user chat bubble */
div[data-testid="stChatMessage"][data-testid*="user"] {
    background-color: #f0f4f9 !important;
    border-color: #d2e3fc !important;
}

/* Accent assistant chat bubble */
div[data-testid="stChatMessage"][data-testid*="assistant"] {
    background-color: #ffffff !important;
    border-left: 4px solid #1a73e8 !important;
}

/* Custom layout helper */
.chat-width {
    max-width: 850px;
    margin: 0 auto;
}

/* Styling for Status Box */
.stStatus {
    background-color: #ffffff !important;
    border: 1px solid #dadce0 !important;
    border-radius: 12px !important;
    color: #1f1f1f !important;
}

/* Expander styling for tool calling rounds */
.stExpander {
    background-color: #f8f9fa !important;
    border: 1px solid #dadce0 !important;
    border-radius: 12px !important;
    margin-bottom: 12px;
}

.stExpander summary {
    font-weight: 500;
    color: #1a73e8 !important;
}

/* Streamlit code and json override */
code {
    font-family: 'Space Grotesk', monospace !important;
    background-color: #f1f3f4 !important;
    color: #202124 !important;
    border-radius: 6px;
    padding: 2px 6px;
    border: 1px solid #e0e0e0;
}

/* Custom form for clarification questions */
.clarification-card {
    background: rgba(244, 180, 0, 0.05) !important;
    border: 1px solid rgba(244, 180, 0, 0.3) !important;
    border-left: 5px solid #f4b400 !important;
    border-radius: 16px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    color: #1f1f1f !important;
}

.clarification-title {
    color: #b06000;
    font-weight: 600;
    font-size: 1.1rem;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Chat Input Styling */
div[data-testid="stChatInput"] {
    border-radius: 28px !important;
    border: 1px solid #dadce0 !important;
    background-color: #ffffff !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05) !important;
    padding: 4px 12px !important;
    transition: all 0.3s ease;
}

div[data-testid="stChatInput"]:focus-within {
    border-color: #1a73e8 !important;
    box-shadow: 0 2px 15px rgba(26, 115, 232, 0.15) !important;
}

div[data-testid="stChatInput"] textarea {
    color: #1f1f1f !important;
}

/* Button overrides */
.stButton>button {
    border-radius: 20px !important;
    background: linear-gradient(90deg, #1a73e8 0%, #34a853 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    border: none !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.3s ease !important;
}

.stButton>button:hover {
    transform: scale(1.03) !important;
    box-shadow: 0 4px 10px rgba(26, 115, 232, 0.25) !important;
}

/* Hide streamlit standard branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -----------------
# Hardcoded Configurations (Removed Sidebar UI)
# -----------------
provider_name = "openrouter"
selected_model = "openai/gpt-4o-mini"
version_input = "v0"
max_tool_rounds = 4
history_window = 5
system_prompt_path = "artifacts/system_prompt.md"
tools_path = "artifacts/tools.yaml"

# Resolve absolute paths
sys_prompt_file = ROOT / system_prompt_path
tools_file = ROOT / tools_path

# Load prompt and tools
if not sys_prompt_file.exists():
    system_prompt = "You are a helpful research assistant."
else:
    system_prompt = sys_prompt_file.read_text(encoding="utf-8")

if not tools_file.exists():
    openai_tools = []
else:
    try:
        tool_declarations = load_tool_declarations(tools_file)
        openai_tools = to_openai_tools(tool_declarations)
    except Exception as e:
        openai_tools = []

# Setup provider
try:
    provider = make_provider(provider_name)
except Exception as e:
    st.error(f"Lỗi khởi tạo model provider: {str(e)}")
    st.stop()

# -----------------
# Thread Management
# -----------------
THREADS_FILE = ROOT / "data" / "chat_threads.json"

def load_threads():
    if not THREADS_FILE.exists():
        return {}
    try:
        with open(THREADS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_threads(threads):
    THREADS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(THREADS_FILE, "w", encoding="utf-8") as f:
        json.dump(threads, f, ensure_ascii=False, indent=2)

def generate_thread_id():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# Initialize session state variables
if "threads" not in st.session_state:
    st.session_state.threads = load_threads()

if "current_thread_id" not in st.session_state:
    if st.session_state.threads:
        st.session_state.current_thread_id = list(st.session_state.threads.keys())[-1]
    else:
        st.session_state.current_thread_id = generate_thread_id()
        st.session_state.threads[st.session_state.current_thread_id] = {
            "title": "Cuộc trò chuyện mới",
            "history": [],
            "chat_history": []
        }
        save_threads(st.session_state.threads)

if "history" not in st.session_state:
    thread_data = st.session_state.threads.get(st.session_state.current_thread_id, {})
    st.session_state.history = thread_data.get("history", [])
if "chat_history" not in st.session_state:
    thread_data = st.session_state.threads.get(st.session_state.current_thread_id, {})
    st.session_state.chat_history = thread_data.get("chat_history", [])
if "waiting_for_clarification" not in st.session_state:
    st.session_state.waiting_for_clarification = False
if "clarification_data" not in st.session_state:
    st.session_state.clarification_data = None
if "transcript" not in st.session_state:
    st.session_state.transcript = None

# Set up transcripts log
if st.session_state.transcript is None:
    try:
        artifact_version = build_artifact_version(version_input, sys_prompt_file, tools_file)
    except Exception:
        artifact_version = None
        
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join([
        safe_slug(version_input),
        safe_slug(provider_name),
        timestamp,
    ])
    
    transcript_path = ROOT / "transcripts" / f"{transcript_id}.transcript.json"
    
    st.session_state.transcript = {
        "transcript_id": transcript_id,
        "artifact_version": artifact_version.artifact_version if artifact_version else version_input,
        "prompt_hash": artifact_version.prompt_hash if artifact_version else "",
        "tools_hash": artifact_version.tools_hash if artifact_version else "",
        "version": version_input,
        "provider": provider_name,
        "model": selected_model,
        "system_prompt": str(sys_prompt_file),
        "tools": str(tools_file),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }
    st.session_state.transcript_path = transcript_path

# -----------------
# UI Rendering
# -----------------

# Sidebar UI cho lịch sử
with st.sidebar:
    st.markdown("### Lịch sử trò chuyện")
    
    if st.button("➕ Cuộc trò chuyện mới", key="new_chat_btn", use_container_width=True):
        new_id = generate_thread_id()
        st.session_state.threads[new_id] = {
            "title": "Cuộc trò chuyện mới",
            "history": [],
            "chat_history": []
        }
        st.session_state.current_thread_id = new_id
        st.session_state.history = []
        st.session_state.chat_history = []
        st.session_state.waiting_for_clarification = False
        st.session_state.clarification_data = None
        st.session_state.transcript = None
        save_threads(st.session_state.threads)
        st.rerun()
        
    st.markdown("---")
    
    for thread_id in reversed(list(st.session_state.threads.keys())):
        thread_title = st.session_state.threads[thread_id].get("title", "Chat")
        is_active = thread_id == st.session_state.current_thread_id
        
        button_label = f"💬 {thread_title}"
        if is_active:
            button_label = f"🔵 {thread_title}"
            
        if st.button(button_label, key=f"btn_{thread_id}", use_container_width=True):
            if thread_id != st.session_state.current_thread_id:
                st.session_state.current_thread_id = thread_id
                st.session_state.history = st.session_state.threads[thread_id].get("history", [])
                st.session_state.chat_history = st.session_state.threads[thread_id].get("chat_history", [])
                st.rerun()

st.markdown('<div class="header-container"><h1 class="gradient-title">Research Agent</h1><p class="gradient-subtitle">Trợ lý nghiên cứu đa tác vụ</p></div>', unsafe_allow_html=True)
# Render conversation history
for idx, message in enumerate(st.session_state.chat_history):
    with st.chat_message(message["role"]):
        # If assistant and has tool runs, show them in a collapsed expander
        if message["role"] == "assistant" and message.get("rounds"):
            num_rounds = len(message["rounds"])
            with st.expander(f"🔧 Các công cụ đã được thực thi ({num_rounds} lượt gọi)", expanded=False):
                for rnd in message["rounds"]:
                    st.markdown(f"**Vòng {rnd['round']}**")
                    if rnd.get("tool_calls"):
                        for tc in rnd["tool_calls"]:
                            st.code(f"Call: {tc['name']}({json.dumps(tc['args'], ensure_ascii=False)})", language="python")
                    if rnd.get("tool_results"):
                        for tr in rnd["tool_results"]:
                            st.markdown(f"*Kết quả của `{tr['tool']}`:*")
                            st.json(tr["result"])
                    st.markdown("---")
        
        st.markdown(message["content"])

# Inline Clarification Input
if st.session_state.waiting_for_clarification and st.session_state.clarification_data:
    clar_data = st.session_state.clarification_data
    question = clar_data["question"]
    resp_type = clar_data.get("response_type", "text")
    options = clar_data.get("options", [])
    
    st.markdown(
        f"""
        <div class="clarification-card">
            <div class="clarification-title">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
                </svg>
                Yêu cầu làm rõ thông tin từ Agent
            </div>
            <div>{question}</div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Inline form
    with st.form("clarification_form"):
        user_response = ""
        if resp_type == "choice" and options:
            user_choice = st.radio("Chọn một trong các phương án sau:", options=options)
            user_response = user_choice
        else:
            user_text_response = st.text_input("Nhập câu trả lời của bạn:")
            user_response = user_text_response
            
        submit_btn = st.form_submit_button("Gửi thông tin bổ sung")
        
        if submit_btn:
            if not user_response.strip():
                st.warning("Vui lòng nhập hoặc chọn câu trả lời trước khi gửi!")
            else:
                # Add turns to history
                st.session_state.history.append({"role": "user", "content": user_response})
                st.session_state.chat_history.append({"role": "user", "content": user_response})
                
                # Save to thread
                st.session_state.threads[st.session_state.current_thread_id]["history"] = st.session_state.history
                st.session_state.threads[st.session_state.current_thread_id]["chat_history"] = st.session_state.chat_history
                save_threads(st.session_state.threads)
                
                # Clear clarification state
                st.session_state.waiting_for_clarification = False
                st.session_state.clarification_data = None
                
                st.rerun()

# -----------------
# Chat Loop Logic
# -----------------

# Standard Chat Input (disabled if waiting for clarification)
user_prompt = st.chat_input(
    "Hỏi tôi bất cứ điều gì...", 
    disabled=st.session_state.waiting_for_clarification
)

if user_prompt:
    # Render user message immediately
    with st.chat_message("user"):
        st.markdown(user_prompt)
        
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    
    if st.session_state.threads[st.session_state.current_thread_id]["title"] == "Cuộc trò chuyện mới":
        st.session_state.threads[st.session_state.current_thread_id]["title"] = user_prompt[:30] + ("..." if len(user_prompt) > 30 else "")
        save_threads(st.session_state.threads)
    
    # Assemble messages history for completion
    # We load completed history and append the current user prompt
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.history, history_window),
        {"role": "user", "content": user_prompt},
    ]
    
    # Run the model tool loop
    with st.chat_message("assistant"):
        # Setup status container to log tool rounds in real-time
        status_placeholder = st.empty()
        
        working_messages = list(messages)
        rounds: list[dict[str, Any]] = []
        all_tool_events: list[dict[str, Any]] = []
        
        loop_status = "answered"
        assistant_text = ""
        
        with status_placeholder.container():
            for round_index in range(1, max_tool_rounds + 1):
                with st.status(f"⚙️ Đang xử lý - Vòng {round_index}/{max_tool_rounds}...", expanded=True) as status_box:
                    status_box.write("Đang gửi yêu cầu...")
                    try:
                        response = provider.complete(
                            working_messages, 
                            openai_tools, 
                            model=selected_model, 
                            temperature=0.0
                        )
                    except Exception as e:
                        status_box.update(label="Lỗi kết nối Provider!", state="error")
                        st.error(f"Lỗi khi gọi API qua OpenRouter: {str(e)}")
                        loop_status = "provider_error"
                        assistant_text = f"Lỗi Provider: {str(e)}"
                        break
                    
                    calls = response.tool_calls
                    round_record = {
                        "round": round_index,
                        "assistant_text": response.text,
                        "tool_calls": [{"name": call.name, "args": call.args} for call in calls],
                        "tool_results": [],
                    }
                    
                    if not calls:
                        status_box.update(label="Hoàn tất suy nghĩ!", state="complete", expanded=False)
                        rounds.append(round_record)
                        loop_status = "answered"
                        assistant_text = response.text or ""
                        break
                    
                    status_box.write(f"Kích hoạt công cụ: `{[call.name for call in calls]}`")
                    working_messages.append(assistant_tool_message(response.text, calls))
                    non_clarification_events = []
                    
                    # Execute each tool call
                    for call in calls:
                        status_box.write(f"▶️ Chạy `{call.name}` với đối số:")
                        status_box.json(call.args)
                        
                        event = execute_tool_call(call)
                        round_record["tool_results"].append(event)
                        all_tool_events.append(event)
                        
                        result = event.get("result", {})
                        status_box.write("◀️ Kết quả:")
                        status_box.json(result)
                        
                        # Clarification logic check
                        if isinstance(result, dict) and result.get("awaiting_user"):
                            question = result.get("question") or call.args.get("question") or "Vui lòng nhập thêm thông tin làm rõ."
                            status_box.update(label="Tạm dừng - Chờ phản hồi làm rõ từ người dùng...", state="complete", expanded=False)
                            rounds.append(round_record)
                            loop_status = "waiting_for_user"
                            assistant_text = question
                            
                            # Save clarification details to session state
                            st.session_state.waiting_for_clarification = True
                            st.session_state.clarification_data = {
                                "question": question,
                                "response_type": result.get("response_type", "text"),
                                "options": result.get("options", [])
                            }
                            break
                        
                        non_clarification_events.append(event)
                    
                    if loop_status == "waiting_for_user":
                        break
                        
                    status_box.update(label=f"Hoàn thành vòng {round_index}", state="complete", expanded=False)
                    rounds.append(round_record)
                    working_messages.append(tool_results_message(non_clarification_events))
            
            else:
                loop_status = "max_tool_rounds"
                assistant_text = f"Đã dừng sau {max_tool_rounds} vòng gọi công cụ."
        
        # Clear status block before writing final output to keep chat clean
        status_placeholder.empty()
        
        # Re-render tools called expander for the current response
        if rounds:
            with st.expander(f"🔧 Các công cụ đã được thực thi ({len(rounds)} lượt gọi)", expanded=False):
                for rnd in rounds:
                    st.markdown(f"**Vòng {rnd['round']}**")
                    if rnd.get("tool_calls"):
                        for tc in rnd["tool_calls"]:
                            st.code(f"Call: {tc['name']}({json.dumps(tc['args'], ensure_ascii=False)})", language="python")
                    if rnd.get("tool_results"):
                        for tr in rnd["tool_results"]:
                            st.markdown(f"*Kết quả của `{tr['tool']}`:*")
                            st.json(tr["result"])
                    st.markdown("---")
        
        # Display the final assistant text
        st.markdown(assistant_text)
        
        # Append turns to history
        st.session_state.history.append({"role": "user", "content": user_prompt})
        st.session_state.history.append({"role": "assistant", "content": assistant_text})
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": assistant_text,
            "rounds": rounds,
            "status": loop_status
        })
        
        # Save to thread
        st.session_state.threads[st.session_state.current_thread_id]["history"] = st.session_state.history
        st.session_state.threads[st.session_state.current_thread_id]["chat_history"] = st.session_state.chat_history
        save_threads(st.session_state.threads)
        
        # Save transcript log
        turn_index = len(st.session_state.history) // 2
        turn_record = {
            "turn_index": turn_index,
            "started_at": now_iso(),
            "user": user_prompt,
            "status": loop_status,
            "assistant_text": assistant_text,
            "rounds": rounds,
            "tool_events": all_tool_events,
            "ended_at": now_iso()
        }
        
        st.session_state.transcript["turns"].append(turn_record)
        try:
            write_transcript(st.session_state.transcript_path, st.session_state.transcript)
        except Exception as e:
            pass
            
        st.rerun()
