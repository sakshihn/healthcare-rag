import sys
import os
sys.path.append('src')

import streamlit as st

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

    
from rag_chain import ask

st.set_page_config(
    page_title="Healthcare RAG Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}
.fade-in {
    animation: fadeIn 0.4s ease forwards;
}
.chat-header {
    background: linear-gradient(135deg, #185FA5 0%, #0F6E56 100%);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    color: white;
}
.chat-header h1 {
    font-size: 22px;
    font-weight: 600;
    margin: 0;
    color: white;
}
.chat-header p {
    font-size: 13px;
    opacity: 0.85;
    margin: 4px 0 0;
    color: white;
}
.stat-card {
    background: #F8FAFF;
    border: 0.5px solid #B5D4F4;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
    text-align: center;
}
.stat-card .val {
    font-size: 22px;
    font-weight: 600;
    color: #185FA5;
}
.stat-card .lbl {
    font-size: 11px;
    color: #5F5E5A;
    margin-top: 2px;
}
.source-pill {
    display: inline-block;
    background: #E1F5EE;
    color: #085041;
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 20px;
    margin: 2px;
    font-family: monospace;
}
.sample-q {
    background: #F1EFE8;
    border-left: 3px solid #185FA5;
    padding: 8px 12px;
    border-radius: 0 8px 8px 0;
    font-size: 13px;
    color: #2C2C2A;
    margin-bottom: 6px;
    cursor: pointer;
    transition: background 0.2s;
}
.sample-q:hover { background: #E6F1FB; }
.thinking-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #185FA5;
    animation: pulse 1.2s ease-in-out infinite;
    margin: 0 2px;
}
.thinking-dot:nth-child(2) { animation-delay: 0.2s; }
.thinking-dot:nth-child(3) { animation-delay: 0.4s; }
.msg-meta {
    font-size: 11px;
    color: #888780;
    margin-top: 6px;
    display: flex;
    gap: 12px;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="chat-header">
  <h1>🏥 Healthcare Research Assistant</h1>
  <p>Answers grounded in real PubMed research — with full source citations</p>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "stats" not in st.session_state:
    st.session_state.stats = []

col1, col2 = st.columns([2.2, 0.8])

with col2:
    st.markdown("### Session stats")

    total_q = len([m for m in st.session_state.messages if m["role"] == "user"])
    avg_lat = 0
    total_tok = 0
    if st.session_state.stats:
        avg_lat = round(sum(s["latency"] for s in st.session_state.stats) / len(st.session_state.stats), 2)
        total_tok = sum(s["tokens"] for s in st.session_state.stats)

    st.markdown(f"""
    <div class="stat-card">
        <div class="val">{total_q}</div>
        <div class="lbl">questions asked</div>
    </div>
    <div class="stat-card">
        <div class="val">{avg_lat}s</div>
        <div class="lbl">avg response time</div>
    </div>
    <div class="stat-card">
        <div class="val">{total_tok}</div>
        <div class="lbl">tokens used</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Try asking:**")
    samples = [
        "What lifestyle changes help diabetes?",
        "What does metformin do?",
        "How does insulin resistance work?",
        "Can diabetes be reversed?",
    ]
    for q in samples:
        st.markdown(f'<div class="sample-q">💬 {q}</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.stats = []
        st.rerun()

with col1:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(
                f'<div class="fade-in">{msg["content"]}</div>',
                unsafe_allow_html=True
            )
            if msg["role"] == "assistant":
                if "sources" in msg and msg["sources"]:
                    with st.expander("📄 View sources"):
                        for line in msg["sources"].split("\n"):
                            if line.strip():
                                st.markdown(
                                    f'<span class="source-pill">{line}</span>',
                                    unsafe_allow_html=True
                                )
                st.markdown(
                    f'<div class="msg-meta">'
                    f'<span>⏱ {msg.get("latency", 0)}s</span>'
                    f'<span>🔢 {msg.get("tokens", 0)} tokens</span>'
                    f'<span>📚 664 chunks searched</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    if question := st.chat_input("Ask a medical research question..."):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(
                f'<div class="fade-in">{question}</div>',
                unsafe_allow_html=True
            )

        with st.chat_message("assistant"):
            thinking = st.empty()
            thinking.markdown(
                '<div style="padding:8px 0">'
                '<span class="thinking-dot"></span>'
                '<span class="thinking-dot"></span>'
                '<span class="thinking-dot"></span>'
                '<span style="font-size:12px;color:#888;margin-left:6px">Searching 664 research papers...</span>'
                '</div>',
                unsafe_allow_html=True
            )

            result = ask(question)
            thinking.empty()

            st.markdown(
                f'<div class="fade-in">{result["answer"]}</div>',
                unsafe_allow_html=True
            )

            with st.expander("📄 View sources"):
                for line in result["sources_formatted"].split("\n"):
                    if line.strip():
                        st.markdown(
                            f'<span class="source-pill">{line}</span>',
                            unsafe_allow_html=True
                        )

            st.markdown(
                f'<div class="msg-meta">'
                f'<span>⏱ {result["latency"]}s</span>'
                f'<span>🔢 {result["tokens"]} tokens</span>'
                f'<span>📚 664 chunks searched</span>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources_formatted"],
            "latency": result["latency"],
            "tokens": result["tokens"]
        })
        st.session_state.stats.append({
            "latency": result["latency"],
            "tokens": result["tokens"]
        })
        st.rerun()