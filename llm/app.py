import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel
import time

# Page Configuration
st.set_page_config(
    page_title="Neural Summarizer", 
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with Inter font, icons, and navbar
st.markdown("""
<style>
    /* Import Inter Font & Font Awesome Icons */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Custom Loading Animation */
    @keyframes loading-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes loading-pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.85; transform: scale(0.98); }
    }
    
    @keyframes loading-glow {
        0%, 100% { box-shadow: 0 0 20px rgba(138, 43, 226, 0.3); }
        50% { box-shadow: 0 0 40px rgba(138, 43, 226, 0.5); }
    }
    
    @keyframes text-shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    
    .custom-loader {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px 40px;
        background: linear-gradient(135deg, rgba(138, 43, 226, 0.1) 0%, rgba(0, 0, 0, 0.4) 50%, rgba(138, 43, 226, 0.05) 100%);
        border: 2px solid rgba(138, 43, 226, 0.4);
        border-radius: 25px;
        margin: 50px auto;
        max-width: 500px;
        animation: loading-pulse 2s ease-in-out infinite, loading-glow 2s ease-in-out infinite;
    }
    
    .loader-spinner {
        width: 70px;
        height: 70px;
        border: 4px solid rgba(138, 43, 226, 0.2);
        border-top: 4px solid #8a2be2;
        border-right: 4px solid #9932cc;
        border-bottom: 4px solid #8a2be2;
        border-radius: 50%;
        animation: loading-spin 0.8s linear infinite;
        margin-bottom: 30px;
    }
    
    .loader-text {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.3rem;
        background: linear-gradient(90deg, #8a2be2, #d8b4fe, #ffffff, #d8b4fe, #8a2be2);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: text-shimmer 2s linear infinite;
        letter-spacing: 1px;
        text-align: center;
    }
    
    .loader-subtext {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 0.9rem;
        color: #888;
        margin-top: 12px;
        letter-spacing: 0.5px;
    }
    
    .loader-icon {
        font-size: 2.5rem;
        color: #8a2be2;
        margin-bottom: 25px;
        animation: loading-pulse 1.5s ease-in-out infinite;
    }
    
    /* Custom star cursor */
    *, *::before, *::after {
        cursor: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><polygon points="12,2 15,9 22,9 16,14 18,21 12,17 6,21 8,14 2,9 9,9" fill="%238a2be2"/></svg>') 8 8, auto !important;
    }
    
    /* Hide sidebar completely */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    
    /* Main background - solid black */
    .stApp {
        background: #000000;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 0 !important;
        position: relative;
        z-index: 1;
        max-width: 1200px;
    }
    
    /* Navbar styling */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 40px;
        background: #0a0a0a;
        border-bottom: 1px solid rgba(138, 43, 226, 0.3);
        margin: -1rem -1rem 30px -1rem;
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .nav-brand i {
        font-size: 1.8rem;
        color: #8a2be2;
    }
    
    .nav-brand span {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 1.4rem;
        color: #fff;
        letter-spacing: 1px;
    }
    
    .nav-links {
        display: flex;
        gap: 40px;
        align-items: center;
    }
    
    .nav-link {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.95rem;
        color: #888;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-link:hover { color: #8a2be2; }
    .nav-link i { font-size: 1rem; }
    
    .nav-tag {
        background: #8a2be2;
        padding: 8px 16px;
        border-radius: 20px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.85rem;
        color: #fff;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Title styling */
    .cyber-title {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #ffffff 0%, #d8b4fe 25%, #8a2be2 50%, #d8b4fe 75%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0;
        letter-spacing: -1px;
    }
    
    .cyber-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 400;
        text-align: center;
        color: #666;
        margin-top: 10px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* Line separator */
    .neon-line {
        height: 1px;
        background: linear-gradient(90deg, transparent, #8a2be2, transparent);
        margin: 30px auto;
        width: 60%;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background: #0a0a0a !important;
        border: 1px solid rgba(138, 43, 226, 0.4) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
        padding: 20px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #8a2be2 !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #444 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Button styling */
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
        padding: 16px 40px !important;
        border-radius: 12px !important;
        border: none !important;
        background: #8a2be2 !important;
        color: #fff !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: #9932cc !important;
        transform: translateY(-2px) !important;
    }
    
    /* Section title styling */
    .section-title {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        color: #8a2be2;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-title i { font-size: 1.1rem; }
    
    /* Stats styling */
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin: 20px 0;
    }
    .stat-item { text-align: center; }
    .stat-value {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.5rem;
        color: #8a2be2;
    }
    .stat-value.accent { color: #9932cc; }
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.8rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }
    
    /* Result box */
    .result-box {
        background: rgba(138, 43, 226, 0.05);
        border: 1px solid rgba(138, 43, 226, 0.4);
        border-radius: 12px;
        padding: 25px;
        margin: 20px 0;
    }
    .result-box p {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 1.1rem;
        color: #fff;
        line-height: 1.8;
        margin: 0;
    }
    
    /* Warning box */
    .warning-box {
        background: rgba(138, 43, 226, 0.05);
        border: 1px solid rgba(138, 43, 226, 0.4);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
    }
    .warning-box p {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 1rem;
        color: #8a2be2;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }
    
    /* Progress text */
    .progress-text {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #8a2be2;
        font-size: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }
    
    /* Result stats */
    .result-stats {
        display: flex;
        justify-content: center;
        gap: 50px;
        margin: 25px 0;
    }
    .result-stat {
        text-align: center;
        padding: 15px 25px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        border: 1px solid rgba(138, 43, 226, 0.3);
    }
    .result-stat.accent { border-color: rgba(138, 43, 226, 0.5); }
    .result-stat-value {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.8rem;
        color: #8a2be2;
    }
    .result-stat.accent .result-stat-value { color: #9932cc; }
    .result-stat-label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.75rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 5px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        color: #444;
        font-size: 0.85rem;
        letter-spacing: 1px;
        margin-top: 20px;
    }
    .footer i { color: #8a2be2; margin: 0 5px; }
    
    /* Custom Spinner Animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .stSpinner {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 40px 0 !important;
    }
    
    .stSpinner > div {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 20px !important;
    }
    
    .stSpinner > div > div {
        width: 50px !important;
        height: 50px !important;
        border: 3px solid rgba(138, 43, 226, 0.2) !important;
        border-top: 3px solid #8a2be2 !important;
        border-radius: 50% !important;
        animation: spin 1s linear infinite !important;
    }
    
    .stSpinner > div > span,
    .stSpinner > div > div:last-child {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        color: #8a2be2 !important;
        letter-spacing: 1px !important;
        animation: pulse 1.5s ease-in-out infinite !important;
    }
    
    /* Override Streamlit's default spinner */
    [data-testid="stSpinner"] {
        background: rgba(138, 43, 226, 0.05) !important;
        border: 1px solid rgba(138, 43, 226, 0.2) !important;
        border-radius: 15px !important;
        padding: 30px !important;
        margin: 20px auto !important;
        max-width: 400px !important;
    }
    
    /* Scrollbar - hidden */
    ::-webkit-scrollbar {
        display: none;
    }
    
    /* Hide scrollbar for Firefox */
    * {
        scrollbar-width: none;
    }
    
    /* Hide scrollbar for IE/Edge */
    * {
        -ms-overflow-style: none;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobile responsive styles */
    @media (max-width: 768px) {
        /* Remove star cursor on mobile */
        *, *::before, *::after {
            cursor: auto !important;
        }
        
        /* Hide Active text on mobile */
        .nav-tag span {
            display: none;
        }
        
        /* Make navbar more compact on mobile */
        .navbar {
            padding: 15px 20px;
        }
        
        .nav-brand span {
            font-size: 1.1rem;
        }
        
        /* Center the button on mobile */
        .stButton {
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
        }
        .stButton > button {
            width: 80% !important;
            max-width: 300px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        
        /* Center button container */
        [data-testid="column"] {
            display: flex !important;
            justify-content: center !important;
        }
        
        /* Adjust title size on mobile */
        .cyber-title {
            font-size: 2rem;
        }
        
        .cyber-subtitle {
            font-size: 0.9rem;
        }
    }
</style>

<!-- Font Awesome CDN -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

# Navbar
st.markdown("""
<div class="navbar">
    <div class="nav-brand">
        <i class="fas fa-bolt"></i>
        <span>NEURAL SUMMARIZER</span>
    </div>
    <div class="nav-links">
        <div class="nav-tag">
            <i class="fas fa-circle" style="font-size: 8px; color: #8a2be2;"></i>
            <span>Active</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div style="text-align: center; padding: 30px 0 10px 0;">
    <h1 class="cyber-title">Intelligent Text Summarization</h1>
    <p class="cyber-subtitle">Powered by Transformer Architecture</p>
</div>
<div class="neon-line"></div>
""", unsafe_allow_html=True)

# Load Model Function
@st.cache_resource
def load_trained_model():
    base_model_name = "t5-small"
    adapter_path = "."  # Adapter files are in the current directory
    
    tokenizer = AutoTokenizer.from_pretrained(adapter_path)
    base_model = AutoModelForSeq2SeqLM.from_pretrained(base_model_name)
    
    # Load LoRA weights into base model
    model = PeftModel.from_pretrained(base_model, adapter_path)
    return tokenizer, model

# Check if model is already cached
if 'model_loaded' not in st.session_state:
    # Custom loading display
    loading_placeholder = st.empty()
    loading_placeholder.markdown("""
    <div class="custom-loader">
        <i class="fas fa-brain loader-icon"></i>
        <div class="loader-spinner"></div>
        <div class="loader-text">Initializing Neural Networks</div>
        <div class="loader-subtext">Loading T5 Transformer with LoRA Adapters...</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load the model
    tokenizer, model = load_trained_model()
    st.session_state.model_loaded = True
    
    # Small delay to show loading animation
    time.sleep(0.5)
    
    # Clear loading display
    loading_placeholder.empty()
else:
    # Model already loaded, just get it from cache
    tokenizer, model = load_trained_model()

# Fixed settings
max_length = 150
num_beams = 4

# Main Content Area
col1, col2, col3 = st.columns([1, 8, 1])

with col2:
    # Input Section
    st.markdown("""
    <div class="section-title">
        <i class="fas fa-arrow-down"></i>
        Input Your Text
    </div>
    """, unsafe_allow_html=True)
    
    text_to_summarize = st.text_area(
        "",
        height=220,
        placeholder="Paste your article, document, or any long text here...\n\nThe AI will analyze and generate a concise summary capturing the key points.",
        label_visibility="collapsed"
    )
    
    # Character count
    if text_to_summarize:
        word_count = len(text_to_summarize.split())
        char_count = len(text_to_summarize)
        
        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-value">{word_count}</div>
                <div class="stat-label">Words</div>
            </div>
            <div class="stat-item">
                <div class="stat-value accent">{char_count}</div>
                <div class="stat-label">Characters</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Summarize Button
    if st.button("GENERATE SUMMARY"):
        if text_to_summarize:
            # Progress animation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            stages = [
                ("fa-search", "Analyzing text structure..."),
                ("fa-brain", "Processing through neural network..."),
                ("fa-bolt", "Applying LoRA transformations..."),
                ("fa-sparkles", "Generating summary...")
            ]
            
            for i, (icon, stage) in enumerate(stages):
                status_text.markdown(f"""
                <div class="progress-text">
                    <i class="fas {icon}"></i>
                    {stage}
                </div>
                """, unsafe_allow_html=True)
                progress_bar.progress((i + 1) * 25)
                time.sleep(0.3)
            
            # Prepare Input
            input_text = "summarize: " + text_to_summarize
            inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
            
            # Generate
            outputs = model.generate(
                input_ids=inputs["input_ids"], 
                max_new_tokens=max_length, 
                num_beams=num_beams
            )
            summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            progress_bar.empty()
            status_text.empty()
            
            # Display Results
            st.markdown("""
            <div class="neon-line"></div>
            <div class="section-title" style="justify-content: center; color: #8a2be2;">
                <i class="fas fa-check-circle"></i>
                Summary Generated
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="result-box">
                <p>{summary}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Summary stats
            summary_words = len(summary.split())
            compression = round((1 - summary_words / word_count) * 100, 1) if word_count > 0 else 0
            
            st.markdown(f"""
            <div class="result-stats">
                <div class="result-stat">
                    <div class="result-stat-value">{summary_words}</div>
                    <div class="result-stat-label">Words</div>
                </div>
                <div class="result-stat accent">
                    <div class="result-stat-value">{compression}%</div>
                    <div class="result-stat-label">Compression</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.markdown("""
            <div class="warning-box">
                <p>
                    <i class="fas fa-exclamation-triangle"></i>
                    Please enter some text to summarize
                </p>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="neon-line" style="margin-top: 50px;"></div>
<div class="footer">
    Built by Arun Ulagappan
</div>
""", unsafe_allow_html=True)