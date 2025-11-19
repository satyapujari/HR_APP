"""Custom UI components for Streamlit RAG application."""
import streamlit as st
from datetime import datetime
from pathlib import Path


def metric_card(title: str, value: str, icon: str = "📊", color: str = "#667eea"):
    """Display a metric card with gradient background."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color} 0%, {color}dd 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        <div style="font-size: 2rem;">{icon}</div>
        <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">{value}</div>
        <div style="font-size: 0.9rem; opacity: 0.9;">{title}</div>
    </div>
    """, unsafe_allow_html=True)


def progress_card(title: str, progress: float, color: str = "#4CAF50"):
    """Display a progress card."""
    percentage = int(progress * 100)
    st.markdown(f"""
    <div style="
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    ">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: 600;">{title}</span>
            <span style="color: {color};">{percentage}%</span>
        </div>
        <div style="
            width: 100%;
            height: 8px;
            background: #f0f0f0;
            border-radius: 4px;
            overflow: hidden;
        ">
            <div style="
                width: {percentage}%;
                height: 100%;
                background: {color};
                transition: width 0.3s ease;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def info_card(title: str, content: str, icon: str = "ℹ️", color: str = "#2196F3"):
    """Display an information card."""
    st.markdown(f"""
    <div style="
        background: {color}10;
        border-left: 4px solid {color};
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    ">
        <div style="display: flex; align-items: start;">
            <div style="font-size: 1.5rem; margin-right: 0.75rem;">{icon}</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; color: {color}; margin-bottom: 0.25rem;">{title}</div>
                <div style="color: #666;">{content}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def document_card(filename: str, size: int, date: str, page_count: int = None):
    """Display a document card with metadata."""
    size_kb = size / 1024
    size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb / 1024:.1f} MB"

    page_info = f"<span>📄 {page_count} pages</span>" if page_count else ""

    st.markdown(f"""
    <div style="
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: box-shadow 0.3s ease;
    " onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'"
       onmouseout="this.style.boxShadow='none'">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 2rem;">📄</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; color: #1e3a8a; margin-bottom: 0.25rem;">
                    {filename}
                </div>
                <div style="display: flex; gap: 1rem; font-size: 0.85rem; color: #666;">
                    <span>💾 {size_str}</span>
                    <span>🕒 {date}</span>
                    {page_info}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def chat_message(role: str, content: str, timestamp: str = None):
    """Display a chat message."""
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")

    if role == "user":
        icon = "🙋"
        bg_color = "#e3f2fd"
        border_color = "#2196F3"
        align = "right"
    else:
        icon = "🤖"
        bg_color = "#f1f8e9"
        border_color = "#4CAF50"
        align = "left"

    st.markdown(f"""
    <div style="
        background: {bg_color};
        border-left: 4px solid {border_color};
        padding: 1rem;
        border-radius: 8px;
        margin: 0.75rem 0;
        animation: slideIn 0.3s ease;
    ">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
            <span style="font-weight: 600; color: {border_color};">
                {icon} {role.title()}
            </span>
            <span style="font-size: 0.75rem; color: #999;">{timestamp}</span>
        </div>
        <div style="color: #333; line-height: 1.6;">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)


def source_document_card(source: str, page: int, content: str, relevance_score: float = None):
    """Display a source document card."""
    filename = Path(source).name
    preview = content[:300] + "..." if len(content) > 300 else content

    score_badge = ""
    if relevance_score is not None:
        score_pct = int(relevance_score * 100)
        score_color = "#4CAF50" if score_pct > 70 else "#FF9800" if score_pct > 40 else "#F44336"
        score_badge = f"""
        <span style="
            background: {score_color};
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        ">{score_pct}% Match</span>
        """

    st.markdown(f"""
    <div style="
        background: #f8f9fa;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <div style="font-weight: 600; color: #1e3a8a;">
                📄 {filename} <span style="color: #666; font-weight: normal;">(Page {page})</span>
            </div>
            {score_badge}
        </div>
        <div style="
            color: #555;
            font-size: 0.9rem;
            line-height: 1.5;
            background: white;
            padding: 0.75rem;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        ">
            {preview}
        </div>
    </div>
    """, unsafe_allow_html=True)


def status_badge(status: str, message: str = ""):
    """Display a status badge."""
    config = {
        "success": {"color": "#4CAF50", "icon": "✅", "bg": "#4CAF5015"},
        "warning": {"color": "#FF9800", "icon": "⚠️", "bg": "#FF980015"},
        "error": {"color": "#F44336", "icon": "❌", "bg": "#F4433615"},
        "info": {"color": "#2196F3", "icon": "ℹ️", "bg": "#2196F315"},
    }

    cfg = config.get(status, config["info"])

    st.markdown(f"""
    <div style="
        display: inline-flex;
        align-items: center;
        background: {cfg['bg']};
        border: 1px solid {cfg['color']};
        color: {cfg['color']};
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        gap: 0.5rem;
    ">
        <span style="font-size: 1.2rem;">{cfg['icon']}</span>
        <span>{message or status.title()}</span>
    </div>
    """, unsafe_allow_html=True)


def loading_animation(message: str = "Processing..."):
    """Display a loading animation."""
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 2rem;
    ">
        <div style="
            display: inline-block;
            width: 50px;
            height: 50px;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        "></div>
        <div style="
            margin-top: 1rem;
            color: #667eea;
            font-weight: 600;
        ">{message}</div>
    </div>
    <style>
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """, unsafe_allow_html=True)


def feature_card(icon: str, title: str, description: str):
    """Display a feature card."""
    st.markdown(f"""
    <div style="
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 16px rgba(0,0,0,0.1)'"
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
        <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
        <div style="font-weight: 600; color: #1e3a8a; margin-bottom: 0.5rem; font-size: 1.1rem;">
            {title}
        </div>
        <div style="color: #666; font-size: 0.9rem; line-height: 1.5;">
            {description}
        </div>
    </div>
    """, unsafe_allow_html=True)