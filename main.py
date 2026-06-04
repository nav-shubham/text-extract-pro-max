#--- File: main.py ---
import streamlit as st
import re
import os
import time
import requests
import json
import html
from typing import Tuple, List, Dict, Optional
from dotenv import load_dotenv

# Try to load environment variables from a local .env file
load_dotenv()

# --- PDF ENGINE FALLBACK SYSTEM ---
try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False
    try:
        import PyPDF2
        HAS_PYPDF2 = True
    except ImportError:
        HAS_PYPDF2 = False

# Try to load Google Generative AI
try:
    import google.generativeai as genai
    HAS_GEMINI_API = True
except ImportError:
    HAS_GEMINI_API = False

# 1. Page Configuration with Premium Aesthetics
st.set_page_config(
    page_title="TextExtract Pro Max v7.0",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Premium Theme and Advanced CSS Styling (Glassmorphism + Neon Indigo Accents)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');
    
    /* Global Font Settings */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Container Padding */
    .block-container { 
        padding-top: 2rem; 
        padding-bottom: 2rem; 
        max-width: 95%;
    }
    
    /* Sidebar Styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #0d0f14;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(17, 22, 34, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    /* Glow Accents and Headers */
    .glow-header {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }
    
    .glow-tag {
        display: inline-block;
        padding: 3px 8px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 6px;
        color: #a5b4fc;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    /* Stats Containers */
    .stat-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    
    .stat-val {
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #e2e8f0;
    }
    
    .stat-lbl {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 2px;
    }
    
    /* Streamlit Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        background: rgba(15, 23, 42, 0.3);
        padding: 4px;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 6px;
        padding: 8px 16px;
        color: #94a3b8;
        font-weight: 500;
        transition: all 0.2s ease;
        border: none;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #e2e8f0;
        background: rgba(255, 255, 255, 0.03);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #c7d2fe !important;
        font-weight: 600;
    }
    
    /* Styled Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
        transition: all 0.2s ease;
        width: 100%;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.35);
        border: none;
        color: white;
    }
    
    div.stButton > button:first-child:active {
        transform: translateY(1px);
    }
    
    /* Context & Utility Classes */
    .context-text { 
        color: #64748b; 
        font-size: 0.85em; 
        font-style: italic; 
    }
    
    .success-badge {
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34d399;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    /* Scrollable Text Viewer */
    .document-viewer {
        height: 480px; 
        overflow-y: scroll; 
        padding: 20px; 
        background: #090d16;
        border: 1px solid rgba(255, 255, 255, 0.05); 
        border-radius: 10px; 
        white-space: pre-wrap; 
        font-family: 'Fira Code', monospace, Courier; 
        font-size: 0.9rem;
        line-height: 1.6;
        color: #cbd5e1;
    }
    
    /* Custom Scrollbar */
    .document-viewer::-webkit-scrollbar {
        width: 8px;
    }
    .document-viewer::-webkit-scrollbar-track {
        background: #090d16;
    }
    .document-viewer::-webkit-scrollbar-thumb {
        background: #1e293b;
        border-radius: 4px;
    }
    .document-viewer::-webkit-scrollbar-thumb:hover {
        background: #334155;
    }
</style>
""", unsafe_allow_html=True)

# 3. Session State Initialization
def init_session_state():
    defaults = {
        "raw_text": "",
        "optimized_text": "",
        "file_name": "",
        "num_pages": 0,
        "file_size": 0.0,
        "extraction_history": [],
        "has_result": False,
        "current_result": "",
        "current_ai_summary": "",
        "num_blocks": 1,
        "selected_engine": "Gemini 2.5 Flash",
        "custom_prompt": ""
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()

# --- HELPER FUNCTIONS ---
def get_pdf_metadata(text: str) -> Dict:
    """Calculate interesting stats from text"""
    chars = len(text)
    words = len(text.split())
    reading_time = max(1, round(words / 200)) # Avg reading speed 200 wpm
    density = round(chars / max(1, st.session_state.num_pages))
    return {
        "chars": chars,
        "words": words,
        "reading_time": reading_time,
        "density": density
    }

def clean_paragraphs(text: str) -> str:
    """Heuristic logic to clean unnecessary newlines (e.g. mid-sentence hyphenations/breaks)"""
    # Simple heuristic: remove a newline if the previous character is not punctuation
    cleaned = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    # Fix multiple spaces
    cleaned = re.sub(r' +', ' ', cleaned)
    return cleaned

# --- CORE EXTRACTION ENGINE (PyMuPDF / PyPDF2) ---
def parse_pdf(file_obj) -> Tuple[str, int]:
    """Parse PDF file with PyMuPDF speed, fallback to PyPDF2 if needed"""
    if HAS_PYMUPDF:
        doc = fitz.open(stream=file_obj.read(), filetype="pdf")
        num_pages = len(doc)
        text_list = []
        for page in doc:
            text_list.append(page.get_text() + "\n")
        return "".join(text_list), num_pages
    elif HAS_PYPDF2:
        reader = PyPDF2.PdfReader(file_obj)
        num_pages = len(reader.pages)
        text_list = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text_list.append(t + "\n")
        return "".join(text_list), num_pages
    else:
        raise ImportError("No PDF extraction libraries are available. Install PyMuPDF or PyPDF2.")

def find_boundary_extraction(text: str, start: str, end: str, case_sensitive: bool, regex_mode: bool) -> Tuple[str, Dict]:
    """Search for bounds and return extracted section and status metadata"""
    flags = 0 if case_sensitive else re.IGNORECASE
    
    # Build search patterns
    start_pat = start if regex_mode else re.escape(start)
    end_pat = end if regex_mode else re.escape(end)
    
    start_matches = list(re.finditer(start_pat, text, flags=flags))
    
    if not start_matches:
        return "", {"status": "error", "message": f"Start marker '{start}' not found."}
    
    # Grab the first match index
    start_idx = start_matches[0].start()
    search_start_pos = start_matches[0].end()
    
    end_matches = list(re.finditer(end_pat, text[search_start_pos:], flags=flags))
    if not end_matches:
        return "", {"status": "error", "message": f"End marker '{end}' not found after the start marker."}
    
    true_end_idx = search_start_pos + end_matches[0].end()
    extracted_text = text[start_idx : true_end_idx]
    
    # Extract short context previews
    context_before = text[max(0, start_idx - 60) : start_idx].replace('\n', ' ')
    context_after = text[true_end_idx : min(len(text), true_end_idx + 60)].replace('\n', ' ')
    
    return extracted_text, {
        "status": "success",
        "context_before": context_before,
        "context_after": context_after,
        "start_count": len(start_matches),
        "end_count": len(end_matches)
    }

# --- PROMPT PRESETS ---
PROMPT_PRESETS = {
    "📚 ICAI CA Exam Notes": """Convert the following paragraph into ICAI CA exam-ready notes.

Strict Output Requirements:
1. First line MUST be exactly in this format:
   TOPIC: [Topic Name]
2. Start the answer immediately after the TOPIC line. Do not write any introduction.
3. Use exam-ready point-wise structured format with proper headings.
4. Preserve ICAI technical keywords.
5. Use short sentences suitable for exam writing.
6. IMPORTANT FORMATTING:
   * Use strict Markdown.
   * Leave one blank line between every bullet point.
   * Use only "-" or "1. 2. 3." for lists. Do NOT use A., B., C.
7. Structure:
   * Main Exam Answer (with headings & bold terms)
   * Short Study Note
   * Ultra Short 5-point Revision Summary
8. Output only study content.""",

    "📝 Executive Brief & Summary": """You are an elite research analyst. Convert the following text into a highly polished, professional Executive Brief.

Strict Output Requirements:
1. First line MUST be:
   TOPIC: [Executive Topic Title]
2. Formats:
   * **Executive Summary**: A concise 3-sentence high-level overview.
   * **Core Pillars**: Key themes or facts structured in bullet points.
   * **Strategic Recommendations / Action Items**: Point-wise recommendations.
3. Use clear bolding for critical metrics or numbers.
4. Output only executive notes without introductory chat.""",

    "🃏 Active Recall Flashcards": """Translate the provided text into a series of highly effective Flashcards for Active Recall study.

Strict Output Requirements:
1. First line MUST be:
   TOPIC: [Subject / Topic Name]
2. Create 5-10 structural Q&A cards in this exact markdown pattern:
   ---
   **Q[Number]: [Enter clear, conceptual Question]**
   *Answer*: [Enter comprehensive, exact answer]
3. Include ultra-concise definitions and key facts.
4. Avoid chit-chat or extra words.""",

    "🔍 Conceptual Deep-Dive (ELI5)": """Explain the complex details of the following text as a highly-skilled educator. Break it down so that a curious 10-year-old can understand, without losing technical accuracy.

Strict Output Requirements:
1. First line MUST be:
   TOPIC: [Concept Name]
2. Structure:
   * **The Big Picture**: High-level intuitive explanation.
   * **Simple Analogy**: Use a powerful real-world analogy.
   * **Core Technical Terms**: Define the hard words clearly.
   * **Common Mistakes**: Key points where people get confused.
3. Keep it highly readable and engaging.
4. Return only the educational summary."""
}

# --- LLM CLIENT ROUTER ---
def run_ai_synthesis(api_key: str, model_name: str, system_instructions: str, analyze_text: str, advanced_options: Dict) -> str:
    """Routes the text to the selected LLM provider API"""
    if "Gemini" in model_name:
        if not HAS_GEMINI_API:
            raise ImportError("Google GenerativeAI module not loaded.")
        if not api_key:
            raise ValueError("API Key is missing for Google Gemini.")
            
        genai.configure(api_key=api_key)
        
        # Route between versions
        gemini_model_id = 'gemini-1.5-flash'
        if "2.5 Pro" in model_name:
            gemini_model_id = 'gemini-2.5-pro'
        elif "2.5 Flash" in model_name:
            gemini_model_id = 'gemini-2.5-flash'
        elif "1.5 Pro" in model_name:
            gemini_model_id = 'gemini-1.5-pro'
            
        model = genai.GenerativeModel(gemini_model_id)
        prompt = f"{system_instructions}\n\nTEXT TO ANALYZE:\n{analyze_text}"
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": advanced_options.get("temperature", 0.3),
                "max_output_tokens": 2048
            }
        )
        return response.text.strip()
        
    elif "DeepSeek" in model_name:
        # Local Ollama deepseek routing
        if "Local" in model_name:
            endpoint = advanced_options.get("ollama_endpoint", "http://localhost:11434/api/generate")
            prompt = f"{system_instructions}\n\nTEXT TO ANALYZE:\n{analyze_text}"
            payload = {
                "model": "deepseek-r1:1.5b" if "R1" in model_name else "deepseek-r1:8b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": advanced_options.get("temperature", 0.3)
                }
            }
            res = requests.post(endpoint, json=payload, timeout=300)
            res.raise_for_status()
            raw_text = res.json().get("response", "")
            # Strip deepseek thoughts if present
            raw_text = re.sub(r'<think>.*?</think>', '', raw_text, flags=re.DOTALL).strip()
            return raw_text
        else:
            # Cloud API DeepSeek Router (via OpenRouter or standard API endpoint)
            cloud_endpoint = advanced_options.get("deepseek_endpoint", "https://api.deepseek.com/v1/chat/completions")
            cloud_key = advanced_options.get("deepseek_api_key", "")
            if not cloud_key:
                raise ValueError("DeepSeek Cloud API Key is required.")
            
            headers = {
                "Authorization": f"Bearer {cloud_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "deepseek-chat", # V3 default
                "messages": [
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": f"TEXT TO ANALYZE:\n{analyze_text}"}
                ],
                "temperature": advanced_options.get("temperature", 0.3)
            }
            res = requests.post(cloud_endpoint, json=payload, headers=headers, timeout=120)
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"].strip()
            
    elif "LLaMA" in model_name:
        # Groq Cloud API LLaMA routing
        groq_key = advanced_options.get("groq_api_key", "")
        if not groq_key:
            raise ValueError("Groq API Key is required for LLaMA models.")
            
        endpoint = advanced_options.get("groq_endpoint", "https://api.groq.com/openai/v1/chat/completions")
        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        }
        
        llama_model = "llama-3.3-70b-versatile"
        if "8B" in model_name:
            llama_model = "llama-3.1-8b-instant"
            
        payload = {
            "model": llama_model,
            "messages": [
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": f"TEXT TO ANALYZE:\n{analyze_text}"}
            ],
            "temperature": advanced_options.get("temperature", 0.3)
        }
        res = requests.post(endpoint, json=payload, headers=headers, timeout=120)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"].strip()

    elif "Claude" in model_name:
        # OpenRouter or Anthropic Endpoint Routing
        claude_key = advanced_options.get("claude_api_key", "")
        if not claude_key:
            raise ValueError("Claude API Key is required.")
            
        endpoint = advanced_options.get("claude_endpoint", "https://api.anthropic.com/v1/messages")
        headers = {
            "x-api-key": claude_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        model_id = "claude-3-5-sonnet-20241022" if "Sonnet" in model_name else "claude-3-5-haiku-20241022"
        payload = {
            "model": model_id,
            "max_tokens": 2048,
            "system": system_instructions,
            "messages": [
                {"role": "user", "content": f"TEXT TO ANALYZE:\n{analyze_text}"}
            ],
            "temperature": advanced_options.get("temperature", 0.3)
        }
        res = requests.post(endpoint, json=payload, headers=headers, timeout=120)
        res.raise_for_status()
        return res.json()["content"][0]["text"].strip()
        
    else:
        raise NotImplementedError(f"Model {model_name} is not currently implemented.")

# --- CALLBACK ACTIONS ---
def update_history_item(index: int, new_ai_text: str):
    if 0 <= index < len(st.session_state.extraction_history):
        st.session_state.extraction_history[index]["ai_summary"] = new_ai_text
        st.toast("Vault entry updated successfully!", icon="📝")

def delete_history_item(index: int):
    if 0 <= index < len(st.session_state.extraction_history):
        st.session_state.extraction_history.pop(index)
        st.toast("Entry deleted from vault.", icon="🗑️")

def clear_all():
    st.session_state.extraction_history = []
    st.session_state.has_result = False
    st.session_state.current_result = ""
    st.session_state.current_ai_summary = ""
    st.toast("Session Vault reset.", icon="🧹")

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.markdown('<div class="glow-header" style="font-size: 1.8rem;">🔮 TextExtract Max</div>', unsafe_allow_html=True)
    st.caption("⚡ v7.0 - Ultimate Multi-Engine PDF Synthesizer")
    
    chapter_name = st.text_input("📚 Subject / Vault Session Name", placeholder="e.g., Auditing: Chapter 3", key="session_name")
    
    st.divider()
    
    # Document Engine Status Indicator
    st.subheader("⚙️ PDF Parser Engine")
    if HAS_PYMUPDF:
        st.markdown('<div class="success-badge">✅ PyMuPDF High-Speed Loaded</div>', unsafe_allow_html=True)
    elif HAS_PYPDF2:
        st.info("ℹ️ Using PyPDF2 (Install PyMuPDF for 10x faster performance)")
    else:
        st.error("🚨 No PDF Engine loaded! Run environment setup.")
        
    uploaded_file = st.file_uploader("Ingest Document", type=["pdf"])
    
    if uploaded_file:
        if st.session_state.file_name != uploaded_file.name:
            with st.spinner("🔄 Deep-Parsing PDF..."):
                try:
                    raw, pgs = parse_pdf(uploaded_file)
                    st.session_state.raw_text = raw
                    st.session_state.optimized_text = clean_paragraphs(raw)
                    st.session_state.num_pages = pgs
                    st.session_state.file_size = uploaded_file.size / 1024
                    st.session_state.file_name = uploaded_file.name
                    st.session_state.has_result = False
                    st.toast("PDF processed successfully!", icon="✅")
                except Exception as e:
                    st.error(f"Failed to ingest PDF: {e}")
                    st.stop()
                    
        # Glowing Document Statistics Card
        st.markdown(f"""
        <div class="glass-card" style="padding: 12px; margin-top: 10px;">
            <div style="font-size:0.8rem; font-weight:600; color:#818cf8; margin-bottom:8px;">📊 PARSED METRICS</div>
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="font-size:0.75rem; color:#94a3b8;">File Size:</span>
                <span style="font-size:0.75rem; font-weight:600; color:#cbd5e1;">{st.session_state.file_size:.1f} KB</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="font-size:0.75rem; color:#94a3b8;">Total Pages:</span>
                <span style="font-size:0.75rem; font-weight:600; color:#cbd5e1;">{st.session_state.num_pages}</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="font-size:0.75rem; color:#94a3b8;">Total Characters:</span>
                <span style="font-size:0.75rem; font-weight:600; color:#cbd5e1;">{len(st.session_state.raw_text):,}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    
    st.subheader("🔍 Extraction Settings")
    opt_toggle = st.toggle("✨ Auto-Clean Broken Line breaks", value=False, help="Heuristically repair broken paragraph flow. Recommended for textbook reading.")
    case_toggle = st.toggle("Case Sensitive Search", value=False)
    regex_toggle = st.toggle("Regular Expression Mode", value=False)
    
    st.divider()
    
    st.subheader("🤖 AI Intelligence Routing")
    enable_ai = st.toggle("Activate AI Synthesis Engine", value=True)
    
    # Advanced Intelligence Router Setup
    selected_provider = st.selectbox(
        "Select Intelligence Engine:",
        [
            "Gemini 2.5 Flash", "Gemini 2.5 Pro", "Gemini 1.5 Pro", "Gemini 1.5 Flash",
            "Local DeepSeek-R1 (1.5B)", "Local DeepSeek-R1 (8B)", "Cloud DeepSeek V3",
            "Claude 3.5 Sonnet", "Claude 3.5 Haiku",
            "LLaMA 3.3 70B (Groq)", "LLaMA 3.1 8B (Groq)"
        ]
    )
    
    st.session_state.selected_engine = selected_provider
    
    adv_options = {"temperature": 0.3}
    
    # Conditional API Key Inputs based on selected routing engine
    if "Gemini" in selected_provider:
        gemini_api_key = st.text_input("Gemini API Key", type="password", value=os.environ.get("GEMINI_API_KEY", ""))
    elif "Local" in selected_provider:
        st.info("Ensure Ollama is running (`ollama run deepseek-r1:1.5b`)")
        adv_options["ollama_endpoint"] = st.text_input("Ollama Endpoint", value="http://localhost:11434/api/generate")
    elif "Cloud DeepSeek" in selected_provider:
        adv_options["deepseek_api_key"] = st.text_input("DeepSeek Cloud API Key", type="password", value=os.environ.get("DEEPSEEK_API_KEY", ""))
        adv_options["deepseek_endpoint"] = st.text_input("Endpoint URL", value="https://api.deepseek.com/v1/chat/completions")
    elif "Claude" in selected_provider:
        adv_options["claude_api_key"] = st.text_input("Anthropic Claude API Key", type="password", value=os.environ.get("ANTHROPIC_API_KEY", ""))
        adv_options["claude_endpoint"] = st.text_input("Endpoint URL", value="https://api.anthropic.com/v1/messages")
    elif "LLaMA" in selected_provider:
        adv_options["groq_api_key"] = st.text_input("Groq API Key", type="password", value=os.environ.get("GROQ_API_KEY", ""))
        adv_options["groq_endpoint"] = st.text_input("Groq Endpoint URL", value="https://api.groq.com/openai/v1/chat/completions")
        
    adv_options["temperature"] = st.slider("Model Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.1)
    
    st.divider()
    
    st.subheader("📚 Prompt Guidelines Preset")
    selected_preset = st.selectbox(
        "Choose Preset Format:",
        list(PROMPT_PRESETS.keys())
    )
    
    preset_prompt_content = PROMPT_PRESETS[selected_preset]
    
    ai_instructions = st.text_area(
        "AI Instructions Prompt:",
        value=preset_prompt_content,
        height=320
    )
    
    st.write("")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🧹 Reset Session"):
            clear_all()
    with c2:
        if st.button("🔄 Reset Results"):
            st.session_state.has_result = False
            st.session_state.current_result = ""
            st.session_state.current_ai_summary = ""
            st.toast("Results cleared.", icon="🔄")

# --- MAIN WORKSPACE VIEW ---
if not uploaded_file:
    # Rich high fidelity dashboard landing page when no PDF is uploaded
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem;">
        <div style="font-size: 5rem; margin-bottom: 1rem; animation: pulse 2s infinite;">🔮</div>
        <h1 class="glow-header" style="font-size: 3rem;">TextExtract Pro Max v7.0</h1>
        <p style="color: #94a3b8; font-size: 1.25rem; max-width: 700px; margin: 0 auto 2.5rem auto;">
            Experience state-of-the-art PDF segment extraction, paragraph cleaning, and multi-cloud LLM routing. 
            Extract structured, study-ready notes, active recall flashcards, or briefs from any textbook or document in seconds.
        </p>
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
            <div class="glass-card" style="width: 260px; padding: 25px; text-align: left;">
                <div style="font-size: 2rem; margin-bottom: 10px;">⚡</div>
                <div style="font-weight: 600; font-size: 1.1rem; color: #e2e8f0; margin-bottom: 6px;">Ultra-Fast Fitz</div>
                <div style="color: #64748b; font-size: 0.85rem; line-height: 1.4;">Uses high-performance layout extraction that processes 100+ pages instantly.</div>
            </div>
            <div class="glass-card" style="width: 260px; padding: 25px; text-align: left;">
                <div style="font-size: 2rem; margin-bottom: 10px;">🌐</div>
                <div style="font-weight: 600; font-size: 1.1rem; color: #e2e8f0; margin-bottom: 6px;">Multi-Cloud LLM</div>
                <div style="color: #64748b; font-size: 0.85rem; line-height: 1.4;">Route summaries to Google Gemini, Anthropic Claude, Groq LLaMA, or local DeepSeek.</div>
            </div>
            <div class="glass-card" style="width: 260px; padding: 25px; text-align: left;">
                <div style="font-size: 2rem; margin-bottom: 10px;">📚</div>
                <div style="font-weight: 600; font-size: 1.1rem; color: #e2e8f0; margin-bottom: 6px;">Master Vault</div>
                <div style="color: #64748b; font-size: 0.85rem; line-height: 1.4;">Compile and edit chronological revision notes inside the persistent Session Vault.</div>
            </div>
        </div>
        <div style="margin-top: 3.5rem; background: rgba(99, 102, 241, 0.05); border: 1px dashed rgba(99, 102, 241, 0.2); border-radius: 12px; padding: 15px; display: inline-block;">
            <span style="color: #a5b4fc; font-weight: 600;">👈 Please upload a PDF in the sidebar control panel to begin!</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Layout has 3 core engine tabs
tab_extract, tab_history, tab_source = st.tabs([
    "🎯 Extraction Engine", 
    "📚 Session Master Vault", 
    "📄 Interactive Document View"
])

# --- TAB 1: EXTRACTION ENGINE WORKSPACE ---
with tab_extract:
    st.markdown('<div style="margin-bottom:15px;"><span class="glow-tag">MODE CONFIGURATION</span></div>', unsafe_allow_html=True)
    st.markdown("### 🎯 Bound Segment Extraction")
    st.caption("Instruct the program to scan the document and pull out content lying between boundary markers.")
    
    extract_mode = st.radio("Select Extraction Boundary Mode:", ["Single Boundary Block", "Dynamic Multi-Block Synthesis"], horizontal=True)
    
    text_source = st.session_state.optimized_text if opt_toggle else st.session_state.raw_text
    
    # 1. SINGLE BOUNDARY BLOCK MODE
    if extract_mode == "Single Boundary Block":
        with st.container(border=True):
            col_in1, col_in2 = st.columns(2)
            with col_in1:
                start_marker = st.text_input("Segment Start Marker Words", placeholder="e.g. In auditing cash balances...")
            with col_in2:
                end_marker = st.text_input("Segment End Marker Words", placeholder="e.g. ...verification is complete.")
            
            # Live previews for single block
            st.write("")
            start_found, end_found = False, False
            if start_marker:
                pat = start_marker if regex_toggle else re.escape(start_marker)
                fl = 0 if case_toggle else re.IGNORECASE
                matches = list(re.finditer(pat, text_source, flags=fl))
                if matches:
                    start_found = True
                    st.success(f"✓ Start marker found in document ({len(matches)} occurrences)")
                else:
                    st.error("✗ Start marker NOT found in document")
                    
            if start_marker and end_marker:
                pat_end = end_marker if regex_toggle else re.escape(end_marker)
                fl = 0 if case_toggle else re.IGNORECASE
                # Scan from first start match onward
                if start_found:
                    start_pos = matches[0].end()
                    end_matches = list(re.finditer(pat_end, text_source[start_pos:], flags=fl))
                    if end_matches:
                        end_found = True
                        st.success(f"✓ End marker found downstream ({len(end_matches)} occurrences)")
                    else:
                        st.error("✗ End marker NOT found downstream of start marker")
            
            st.write("")
            extract_run = st.button("🚀 Process Segment Extraction", type="primary")
            
        if extract_run:
            if not start_marker or not end_marker:
                st.warning("Please supply both starting and ending markers.")
            else:
                with st.spinner("Extracting content..."):
                    seg_text, meta = find_boundary_extraction(text_source, start_marker, end_marker, case_toggle, regex_toggle)
                    
                    if meta["status"] == "error":
                        st.error(meta["message"])
                    else:
                        st.session_state.current_result = seg_text
                        st.session_state.has_result = True
                        st.session_state.current_ai_summary = ""
                        
                        # Process AI synthesis
                        if enable_ai:
                            try:
                                with st.spinner(f"🧠 Synthesizing via {selected_provider}..."):
                                    # Setup API keys if not empty
                                    passed_key = ""
                                    if "Gemini" in selected_provider:
                                        passed_key = gemini_api_key
                                    elif "Cloud DeepSeek" in selected_provider:
                                        passed_key = adv_options.get("deepseek_api_key", "")
                                    elif "Claude" in selected_provider:
                                        passed_key = adv_options.get("claude_api_key", "")
                                    elif "LLaMA" in selected_provider:
                                        passed_key = adv_options.get("groq_api_key", "")
                                        
                                    ai_out = run_ai_synthesis(
                                        api_key=passed_key,
                                        model_name=selected_provider,
                                        system_instructions=ai_instructions,
                                        analyze_text=seg_text,
                                        advanced_options=adv_options
                                    )
                                    st.session_state.current_ai_summary = ai_out
                                    
                                    # Parse topic title
                                    lines = ai_out.split('\n')
                                    topic_title = "Extracted Topic"
                                    if lines and ("TOPIC:" in lines[0].upper() or "TOPIC :" in lines[0].upper()):
                                        topic_title = re.sub(r'^[*#\s]*(TOPIC[:\s]*)?', '', lines[0], flags=re.IGNORECASE).strip()
                                        st.session_state.current_ai_summary = "\n".join(lines[1:]).strip()
                                    else:
                                        topic_title = lines[0][:50].replace("#", "").strip() if lines else "Extracted Study Section"
                                        
                                    # Append to vault
                                    st.session_state.extraction_history.append({
                                        "timestamp": time.strftime("%Y-%m-%d %H:%M"),
                                        "source": uploaded_file.name,
                                        "start": start_marker[:35] + "..." if len(start_marker) > 35 else start_marker,
                                        "end": end_marker[:35] + "..." if len(end_marker) > 35 else end_marker,
                                        "text": seg_text,
                                        "ai_summary": st.session_state.current_ai_summary,
                                        "topic": topic_title,
                                        "model": selected_provider
                                    })
                                    st.toast("Extraction & Synthesis complete! Saved to Session Vault.", icon="🚀")
                                    
                            except Exception as e:
                                st.error(f"Intelligence Generation Issue: {e}")
                                st.info("Displaying raw extracted segment instead.")
                        else:
                            st.session_state.extraction_history.append({
                                "timestamp": time.strftime("%Y-%m-%d %H:%M"),
                                "source": uploaded_file.name,
                                "start": start_marker,
                                "end": end_marker,
                                "text": seg_text,
                                "ai_summary": "",
                                "topic": f"Raw Segment: {start_marker[:20]}...",
                                "model": "None"
                            })
                            st.toast("Raw segment extracted and saved to Vault.", icon="✅")

    # 2. MULTI-BLOCK DYNAMIC SYNTHESIS MODE
    else:
        with st.container(border=True):
            st.markdown("#### Dynamic Block Manager")
            st.caption("Construct one consolidated study page from disparate parts of the book.")
            
            blocks = []
            
            # Simple callbacks to add or remove blocks
            def add_mb(): st.session_state.num_blocks += 1
            def remove_mb(): 
                if st.session_state.num_blocks > 1: st.session_state.num_blocks -= 1

            for i in range(st.session_state.num_blocks):
                st.markdown(f"**🔗 Segment Block #{i+1}**")
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    sb_val = st.text_input(f"Block {i+1} Start Marker", key=f"mb_start_{i}", placeholder="Segment start...")
                with col_m2:
                    eb_val = st.text_input(f"Block {i+1} End Marker", key=f"mb_end_{i}", placeholder="Segment end...")
                
                # Check status
                if sb_val and eb_val:
                    chunk, res = find_boundary_extraction(text_source, sb_val, eb_val, case_toggle, regex_toggle)
                    if res["status"] == "success":
                        st.markdown(f"🟢 *Block {i+1} Validated ({len(chunk)} characters found)*")
                        blocks.append({"text": chunk, "start": sb_val, "end": eb_val, "valid": True})
                    else:
                        st.markdown(f"🔴 *Block {i+1} Match Error: {res['message']}*")
                        blocks.append({"text": "", "start": sb_val, "end": eb_val, "valid": False})
                else:
                    blocks.append({"text": "", "start": sb_val, "end": eb_val, "valid": False})
                st.divider()
                
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                st.button("➕ Add Extraction Block", on_click=add_mb, use_container_width=True)
            with col_b2:
                if st.session_state.num_blocks > 1:
                    st.button("➖ Remove Last Block", on_click=remove_mb, use_container_width=True)
                    
            st.write("")
            multi_run = st.button("🚀 Process Consolidated Multi-Block Synthesis", type="primary", use_container_width=True)
            
        if multi_run:
            valid_blocks = [b for b in blocks if b["valid"]]
            if not valid_blocks:
                st.error("No valid blocks have been matched. Verify your boundary text strings.")
            else:
                with st.spinner("Consolidating segment text blocks..."):
                    # Combine all matched texts
                    combined_segment = "\n\n[... CONTINUOUS SYNTHESIS SEGMENT BOUNDARY ...]\n\n".join(b["text"] for b in valid_blocks)
                    st.session_state.current_result = combined_segment
                    st.session_state.has_result = True
                    st.session_state.current_ai_summary = ""
                    
                    if enable_ai:
                        try:
                            with st.spinner(f"🧠 Synthesizing via {selected_provider}..."):
                                passed_key = ""
                                if "Gemini" in selected_provider:
                                    passed_key = gemini_api_key
                                elif "Cloud DeepSeek" in selected_provider:
                                    passed_key = adv_options.get("deepseek_api_key", "")
                                elif "Claude" in selected_provider:
                                    passed_key = adv_options.get("claude_api_key", "")
                                elif "LLaMA" in selected_provider:
                                    passed_key = adv_options.get("groq_api_key", "")
                                    
                                ai_out = run_ai_synthesis(
                                    api_key=passed_key,
                                    model_name=selected_provider,
                                    system_instructions=ai_instructions,
                                    analyze_text=combined_segment,
                                    advanced_options=adv_options
                                )
                                st.session_state.current_ai_summary = ai_out
                                
                                # Parse topic title
                                lines = ai_out.split('\n')
                                topic_title = "Multi-Block Synthesis"
                                if lines and ("TOPIC:" in lines[0].upper() or "TOPIC :" in lines[0].upper()):
                                    topic_title = re.sub(r'^[*#\s]*(TOPIC[:\s]*)?', '', lines[0], flags=re.IGNORECASE).strip()
                                    st.session_state.current_ai_summary = "\n".join(lines[1:]).strip()
                                else:
                                    topic_title = lines[0][:50].replace("#", "").strip() if lines else "Consolidated Notes"
                                    
                                st.session_state.extraction_history.append({
                                    "timestamp": time.strftime("%Y-%m-%d %H:%M"),
                                    "source": uploaded_file.name,
                                    "start": f"{len(valid_blocks)} Block(s) Consolidated",
                                    "end": "N/A",
                                    "text": combined_segment,
                                    "ai_summary": st.session_state.current_ai_summary,
                                    "topic": topic_title,
                                    "model": selected_provider
                                })
                                st.toast("Consolidated Multi-Block synthesis successfully finalized!", icon="🚀")
                                
                        except Exception as e:
                            st.error(f"Synthesis Issue: {e}")
                            st.info("Displaying consolidated raw blocks instead.")
                    else:
                        st.session_state.extraction_history.append({
                            "timestamp": time.strftime("%Y-%m-%d %H:%M"),
                            "source": uploaded_file.name,
                            "start": "Multi-Block Raw",
                            "end": "N/A",
                            "text": combined_segment,
                            "ai_summary": "",
                            "topic": "Consolidated Raw Segments",
                            "model": "None"
                        })
                        st.toast("Consolidated raw segments saved to Vault.", icon="✅")

    # --- RENDER RECENT EXTRACTION RESULTS ---
    if st.session_state.has_result and st.session_state.current_result:
        st.write("")
        st.markdown("### ✨ Current Segment Output")
        
        # Display Glassmorphic Card containing result
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            
            # Show summary tab vs raw tab
            res_tab_ai, res_tab_raw = st.tabs(["🔮 AI Synthesized Output", "📄 Original Extracted Text"])
            
            with res_tab_ai:
                if st.session_state.current_ai_summary:
                    st.markdown(st.session_state.current_ai_summary)
                else:
                    st.info("AI synthesis was disabled or failed. Review the raw segment in the next tab.")
                    
            with res_tab_raw:
                st.text_area("Extracted Context Text String", value=st.session_state.current_result, height=350)
                
            st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: MASTER STUDY VAULT ---
with tab_history:
    st.markdown('<div style="margin-bottom:15px;"><span class="glow-tag">STUDY COMPLIANCE STORAGE</span></div>', unsafe_allow_html=True)
    st.markdown("### 📚 Vault Repository")
    st.caption("Organize, review, live-edit, and export your compiled study materials and revision logs.")
    
    if not st.session_state.extraction_history:
        st.info("📭 Vault is currently empty. Run segment extractions to store notes.")
    else:
        st.markdown(f"**Persistent vault count:** `{len(st.session_state.extraction_history)} topics stored`")
        
        # Chronological reverse display
        for i, item in reversed(list(enumerate(st.session_state.extraction_history))):
            disp_idx = len(st.session_state.extraction_history) - i
            
            # Draw Glassmorphic Card for each entry
            st.markdown(f"""
            <div class="glass-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <div>
                        <span style="font-family:'Outfit'; font-size:1.25rem; font-weight:700; color:#e2e8f0;">{disp_idx}. {item.get('topic', 'Segment Entry')}</span>
                        <span style="font-size:0.75rem; color:#64748b; margin-left:12px;">⏰ {item.get('timestamp')}</span>
                    </div>
                    <span class="glow-tag" style="margin-bottom:0;">🤖 {item.get('model', 'Unknown')}</span>
                </div>
                <div style="font-size:0.8rem; color:#94a3b8; margin-bottom:15px;">
                    📄 Source: <code>{item.get('source', 'Document')}</code> | Markers: <code>Start: {item.get('start')}</code> → <code>End: {item.get('end')}</code>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Sub-contents inside standard streamlit expander attached to the card for neat clean UI
            with st.expander("🛠️ View / Edit Study Summary", expanded=False):
                # Live Editing Area
                current_summary = item.get("ai_summary", "")
                if current_summary:
                    edited_summary = st.text_area("Live Edit Note Summary:", value=current_summary, height=250, key=f"edit_summary_{i}")
                    
                    c_ed1, c_ed2, c_ed3 = st.columns([1, 1, 2])
                    with c_ed1:
                        if st.button("💾 Save Changes", key=f"save_btn_{i}"):
                            update_history_item(i, edited_summary)
                            st.rerun()
                    with c_ed2:
                        if st.button("🗑️ Delete Note", key=f"del_btn_{i}"):
                            delete_history_item(i)
                            st.rerun()
                    with c_ed3:
                        # Re-run synthesis with a different preset/instructions
                        if st.button("🔄 Regenerate Notes", key=f"regen_btn_{i}"):
                            with st.spinner("Regenerating..."):
                                try:
                                    passed_key = ""
                                    if "Gemini" in selected_provider:
                                        passed_key = gemini_api_key
                                    elif "Cloud DeepSeek" in selected_provider:
                                        passed_key = adv_options.get("deepseek_api_key", "")
                                    elif "Claude" in selected_provider:
                                        passed_key = adv_options.get("claude_api_key", "")
                                    elif "LLaMA" in selected_provider:
                                        passed_key = adv_options.get("groq_api_key", "")
                                        
                                    regen_out = run_ai_synthesis(
                                        api_key=passed_key,
                                        model_name=selected_provider,
                                        system_instructions=ai_instructions,
                                        analyze_text=item["text"],
                                        advanced_options=adv_options
                                    )
                                    
                                    # Strip topic name if returned in regenerate
                                    regen_lines = regen_out.split('\n')
                                    if regen_lines and "TOPIC:" in regen_lines[0].upper():
                                        regen_out = "\n".join(regen_lines[1:]).strip()
                                        
                                    st.session_state.extraction_history[i]["ai_summary"] = regen_out
                                    st.session_state.extraction_history[i]["model"] = selected_provider
                                    st.toast("Summary regenerated successfully!", icon="🔮")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Regeneration Failed: {e}")
                                    
                    st.markdown(edited_summary)
                else:
                    st.warning("This record contains only raw segment text (AI summary skipped).")
                    st.text_area("Raw segment content:", value=item.get("text", ""), height=150, disabled=True)
                    if st.button("🗑️ Delete Note", key=f"del_btn_raw_{i}"):
                        delete_history_item(i)
                        st.rerun()
                        
            st.markdown("<br>", unsafe_allow_html=True)
            
        st.divider()
        
        # MASTER BULK EXPORT VAULT BUILDER
        st.markdown("### 📥 Dynamic Vault Exports")
        st.caption("Compile your persistent Session Vault into study guides and download in multiple formats.")
        
        session_title_display = chapter_name if chapter_name else "Master Study Revision Notes"
        
        # 1. MARKDOWN BUILDER
        master_vault_markdown = f"# 📚 {session_title_display}\n\n"
        master_vault_markdown += f"*Compiled session notes from document `{st.session_state.file_name}`*\n"
        master_vault_markdown += f"*Generated: {time.strftime('%Y-%m-%d %H:%M')} | Engine: {st.session_state.selected_engine}*\n\n---\n\n"
        
        for idx, rec in enumerate(st.session_state.extraction_history):
            topic_name = rec.get("topic", "Segment Topic")
            master_vault_markdown += f"## {idx + 1}. {topic_name}\n"
            master_vault_markdown += f"> *Markers: Start: `{rec['start']}` | End: `{rec['end']}`*\n\n"
            
            if rec.get("ai_summary", None):
                master_vault_markdown += f"{rec.get('ai_summary')}\n\n"
            else:
                master_vault_markdown += f"```text\n{rec.get('text')}\n```\n\n"
            master_vault_markdown += "---\n\n"
            
        file_export_slug = chapter_name.lower().replace(" ", "_").replace(":", "") if chapter_name else "study_revision_vault"
        
        # 2. HTML BUILDER (Beautifully stylized print-ready HTML export template)
        master_vault_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{session_title_display}</title>
<style>
    body {{ font-family: -apple-system, system-ui, sans-serif; line-height: 1.6; color: #1e293b; max-width: 800px; margin: 40px auto; padding: 0 20px; }}
    h1 {{ border-bottom: 2px solid #6366f1; padding-bottom: 12px; color: #1e1b4b; }}
    h2 {{ color: #4338ca; margin-top: 30px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }}
    code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.85em; }}
    blockquote {{ border-left: 4px solid #818cf8; padding-left: 15px; color: #475569; margin: 15px 0; background: #faf5ff; padding: 10px; border-radius: 0 8px 8px 0; }}
    hr {{ border: 0; border-top: 1px solid #cbd5e1; margin: 40px 0; }}
</style>
</head>
<body>
    <h1>📚 {session_title_display}</h1>
    <p><em>Generated from {st.session_state.file_name} on {time.strftime('%Y-%m-%d %H:%M')} via TextExtract Pro Max v7.0</em></p>
    <hr>
"""
        for idx, rec in enumerate(st.session_state.extraction_history):
            topic_name = rec.get("topic", "Segment Topic")
            master_vault_html += f"<h2>{idx + 1}. {topic_name}</h2>"
            master_vault_html += f"<p><blockquote><strong>Extraction Markers:</strong> Start: <code>{html.escape(rec['start'])}</code> &rarr; End: <code>{html.escape(rec['end'])}</code></blockquote></p>"
            if rec.get("ai_summary", None):
                # Quick markdown list parsing to html representation (simple regex conversion)
                md_converted = html.escape(rec.get("ai_summary", ""))
                md_converted = md_converted.replace("\n", "<br>")
                master_vault_html += f"<div style='white-space: pre-wrap;'>{rec.get('ai_summary')}</div>"
            else:
                master_vault_html += f"<pre style='background:#f8fafc; padding:15px; border-radius:6px; border:1px solid #e2e8f0; overflow-x:auto;'>{html.escape(rec.get('text'))}</pre>"
            master_vault_html += "<hr>"
            
        master_vault_html += """
</body>
</html>
"""
        
        # 3. JSON BUILDER
        master_vault_json = json.dumps(st.session_state.extraction_history, indent=4)
        
        # Dynamic Export Column buttons
        col_ex1, col_ex2, col_ex3 = st.columns(3)
        with col_ex1:
            st.download_button(
                label="⬇️ Download Markdown (.md)",
                data=master_vault_markdown.encode('utf-8'),
                file_name=f"{file_export_slug}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_ex2:
            st.download_button(
                label="⬇️ Download Print-ready HTML",
                data=master_vault_html.encode('utf-8'),
                file_name=f"{file_export_slug}.html",
                mime="text/html",
                use_container_width=True
            )
        with col_ex3:
            st.download_button(
                label="⬇️ Export Raw JSON (.json)",
                data=master_vault_json.encode('utf-8'),
                file_name=f"{file_export_slug}.json",
                mime="application/json",
                use_container_width=True
            )

# --- TAB 3: INTERACTIVE DOCUMENT VIEW & HIGHLIGHTER ---
with tab_source:
    st.markdown('<div style="margin-bottom:15px;"><span class="glow-tag">REALTIME SEARCH VERIFIER</span></div>', unsafe_allow_html=True)
    st.markdown("### 📄 Live Highlighter Document Viewer")
    st.caption("Use this viewer to scan the raw extracted document content and verify your start/end markers in real-time.")
    
    col_t1, col_t2 = st.columns([1, 2])
    with col_t1:
        view_mode = st.radio("Text Preprocessing View Mode:", ["Raw Document Content", "Optimized Paragraph Layout"], horizontal=True)
    with col_t2:
        search_query = st.text_input("🔍 Dynamic Document Highlighter Search:", placeholder="Type a concept, term, or phrase to highlight below...")
        
    text_display = st.session_state.optimized_text if "Optimized" in view_mode else st.session_state.raw_text
    
    # Calculate stats
    stats = get_pdf_metadata(text_display)
    
    col_st1, col_st2, col_st3, col_st4 = st.columns(4)
    with col_st1:
        st.markdown(f"""<div class="stat-container"><span class="stat-val">{stats['chars']:,}</span><span class="stat-lbl">Characters</span></div>""", unsafe_allow_html=True)
    with col_st2:
        st.markdown(f"""<div class="stat-container"><span class="stat-val">{stats['words']:,}</span><span class="stat-lbl">Words</span></div>""", unsafe_allow_html=True)
    with col_st3:
        st.markdown(f"""<div class="stat-container"><span class="stat-val">{stats['reading_time']} min</span><span class="stat-lbl">Reading Time</span></div>""", unsafe_allow_html=True)
    with col_st4:
        st.markdown(f"""<div class="stat-container"><span class="stat-val">{stats['density']}</span><span class="stat-lbl">Chars / Page</span></div>""", unsafe_allow_html=True)
        
    st.write("")
    
    # Highlight logic
    escaped_display = html.escape(text_display)
    if search_query:
        try:
            # Case insensitive regex highlighting
            flg = re.IGNORECASE
            safe_query = html.escape(search_query)
            re_term = re.escape(safe_query)
            # Replace query terms with custom mark elements
            highlighted_output = re.sub(
                f"({re_term})",
                r"<mark style='background: linear-gradient(120deg, #fef08a 0%, #fde047 100%); color: #0f172a; font-weight: 600; padding: 2px 4px; border-radius: 4px;'>\1</mark>",
                escaped_display,
                flags=flg
            )
            matches_count = len(re.findall(re_term, escaped_display, flags=flg))
            st.markdown(f"<span class='success-badge'>Found <strong>{matches_count}</strong> occurrence(s) for '{search_query}'</span>", unsafe_allow_html=True)
        except Exception:
            highlighted_output = escaped_display
    else:
        highlighted_output = escaped_display
        
    # Render stylized document container
    st.markdown(
        f"""
        <div class="document-viewer">
            {highlighted_output}
        </div>
        """,
        unsafe_allow_html=True
    )

# --- GLOBAL STICKY FOOTER ---
st.divider()
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; opacity:0.75; font-size:0.8rem;">
    <span>🔮 TextExtract Pro Max v7.0 | Designed with High-Aesthetic Glassmorphic UI</span>
    <span>⚡ Multi-Cloud LLM Broker Enabled</span>
</div>
""", unsafe_allow_html=True)
#--- End of main.py ---
