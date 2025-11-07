
#
import os
import re
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

# Optional imports guarded for graceful UI load
try:
    import google.generativeai as genai
except Exception:  # pragma: no cover
    genai = None  # type: ignore

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.units import inch
except Exception:  # pragma: no cover
    A4 = None  # type: ignore


# --------------------------
# Environment & Config
# --------------------------
load_dotenv()

def get_api_key() -> str:
    return os.getenv("GEMINI_API_KEY", "")


def configure_gemini(api_key: str) -> None:
    if genai is None:
        raise RuntimeError("google-generativeai is not installed. Please install dependencies.")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set. Add it to your .env or environment.")
    genai.configure(api_key=api_key)


SUMMARY_PROMPT = (
    "You are a text summarizer. Read the given text and summarize it in a clear, "
    "concise, and informative way within 200–250 words. Use bullet points for key takeaways if suitable.\n\nText:\n\n"
)


def generate_gemini_summary(input_text: str) -> str:
    model = genai.GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(SUMMARY_PROMPT + input_text)
    return getattr(response, "text", "")


def convert_markdown_to_html(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
    text = text.replace("\n", "<br/>")
    text = text.replace("•", "&bull;")
    return text


# --------------------------
# 🎨 Stylish PDF Export
# --------------------------
def save_summary_as_pdf(summary_text: str) -> str:
    if A4 is None:
        raise RuntimeError("ReportLab is not installed. Install dependencies to export PDF.")

    from reportlab.lib.colors import HexColor

    filename = f"AI_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            leftMargin=60, rightMargin=60, topMargin=80, bottomMargin=60)

    styles = getSampleStyleSheet()

    # --- Styles ---
    title_style = ParagraphStyle(
        "Title",
        fontSize=22,
        leading=26,
        alignment=1,
        textColor=HexColor("#1E3A8A"),
        spaceAfter=12,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        fontSize=13,
        leading=18,
        alignment=1,
        textColor=HexColor("#334155"),
        spaceAfter=18,
    )
    body_style = ParagraphStyle(
        "Body",
        fontSize=12,
        leading=18,
        textColor=HexColor("#0F172A"),
        spaceAfter=10,
    )
    footer_style = ParagraphStyle(
        "Footer",
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=HexColor("#6B7280"),
    )

    # --- Header Bar ---
    header_data = [["🧠 AI Text Summarizer", "Gemini 2.5 Pro | AI Generated Summary"]]
    header_table = Table(header_data, colWidths=[3.5 * inch, 3.0 * inch])
    header_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#2563EB")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("ALIGN", (0, 0), (0, 0), "LEFT"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 13),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    # --- Content Card ---
    formatted = convert_markdown_to_html(summary_text)
    card = Table(
        [[Paragraph(formatted, body_style)]],
        colWidths=[6.0 * inch],
    )
    card.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#EFF6FF")),
            ("BOX", (0, 0), (-1, -1), 0.75, HexColor("#93C5FD")),
            ("INNERPADDING", (0, 0), (-1, -1), 14),
        ])
    )

    # --- Layout Build ---
    content = []
    content.append(header_table)
    content.append(Spacer(1, 0.35 * inch))
    content.append(Paragraph("✨ Executive Summary", title_style))
    content.append(Paragraph("Clean • Concise • Insightful", subtitle_style))
    content.append(card)
    content.append(Spacer(1, 0.4 * inch))

    footer_text = (
        f"<b>Generated on:</b> {datetime.now().strftime('%B %d, %Y - %I:%M %p')}  |  "
        f"<b>Word Count:</b> {len(summary_text.split())}<br/>"
        f"<font color='#9CA3AF'>Made with ❤️ using Streamlit & Gemini</font>"
    )
    content.append(Paragraph(footer_text, footer_style))

    doc.build(content)
    return filename


# --------------------------
# Streamlit UI
# --------------------------
st.set_page_config(
    page_title="AI Summarizer",
    page_icon="🧠",
    layout="wide",
)

CUSTOM_CSS = """
<style>
  .app-header { margin-top: 8px; }
  .title { font-size: 2rem; font-weight: 700; color: #0F172A; }
  .subtitle { color: #475569; font-size: 0.95rem; }
  .card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 18px 18px 14px 18px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
  }
  .summary-card { background: #F8FAFF; border: 1px solid #E0EAFF; }
  .muted { color: #64748B; }
  .accent { color: #2563EB; }
  .btn-row { margin-top: 6px; }
  textarea { font-size: 15px !important; }
  .footer-note { color: #94A3B8; font-size: 12px; }
  .spacer-8 { height: 8px; }
  .spacer-16 { height: 16px; }
  .spacer-24 { height: 24px; }
  .spacer-32 { height: 32px; }
  .spacer-48 { height: 48px; }
  .pill { background:#EFF6FF; color:#1D4ED8; padding:4px 10px; border-radius:999px; font-size:12px; }
  .label { font-size: 0.9rem; color: #334155; font-weight: 600; }
  .download-row { margin-top: 10px; }
  .icon { margin-right: 6px; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

api_key = get_api_key()

header_col1, header_col2 = st.columns([5, 2])
with header_col1:
    st.markdown(
        """
        <div class="app-header">
          <div class="title"> 🔍GEMINI POWERED  TEXT SUMMARISER📘 </div>
          <div class="subtitle">Paste your content, click <b>Summarise Text</b>, and get a clean, concise summary. Export to a colorful PDF with one click.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with header_col2:
    st.markdown(
        f"<div class='pill'>{'Gemini configured ✅' if api_key else 'Set GEMINI_API_KEY in .env'}</div>",
        unsafe_allow_html=True,
    )

st.markdown("<div class='spacer-16'></div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='label'>📝 Input Text</div>", unsafe_allow_html=True)
    user_text = st.text_area(
        label=" ",
        placeholder="Paste or type your text here...",
        height=260,
        label_visibility="collapsed",
    )

st.markdown("<div class='spacer-8'></div>", unsafe_allow_html=True)

col_a, col_b = st.columns([1, 6])
with col_a:
    summarize_clicked = st.button("🔎 Summarize Text", type="primary", use_container_width=True)
with col_b:
    st.markdown("<span class='muted'>Tip: Keep inputs under a few thousand words for best results.</span>", unsafe_allow_html=True)

st.markdown("<div class='spacer-24'></div>", unsafe_allow_html=True)

if "last_summary" not in st.session_state:
    st.session_state.last_summary = ""

if summarize_clicked:
    if not user_text or not user_text.strip():
        st.warning("Please paste some text to summarize.")
    elif not api_key:
        st.error("GEMINI_API_KEY not set. Add it to your environment or .env, then reload.")
    else:
        try:
            configure_gemini(api_key)
            with st.spinner("Summarizing with Gemini…"):
                summary = generate_gemini_summary(user_text)
                st.session_state.last_summary = summary or "(No content returned)"
        except Exception as e:  # pragma: no cover
            st.error(f"Failed to generate summary: {e}")


if st.session_state.last_summary:
    st.markdown("<div class='label'>📘 Summary</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown(
            "<div class='card summary-card'>" + st.session_state.last_summary.replace("\n", "<br/>") + "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='spacer-16'></div>", unsafe_allow_html=True)

    pdf_col1, pdf_col2 = st.columns([1, 6])
    with pdf_col1:
        if st.button("⬇️ Download PDF", use_container_width=True):
            try:
                filename = save_summary_as_pdf(st.session_state.last_summary)
                with open(filename, "rb") as f:
                    st.download_button(
                        label="Click to save",
                        data=f.read(),
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True,
                    )
            except Exception as e:  # pragma: no cover
                st.error(f"PDF export failed: {e}")
    with pdf_col2:
        st.markdown("<span class='muted'>Your summary PDF includes a stylish blue header, clean typography, and timestamp.</span>", unsafe_allow_html=True)

st.markdown("<div class='spacer-48'></div>", unsafe_allow_html=True)
st.markdown("<div class='footer-note'>Made with ❤️ using Streamlit and Gemini</div>", unsafe_allow_html=True)
