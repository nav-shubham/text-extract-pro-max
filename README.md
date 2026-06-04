# 🔮 TextExtract Pro Max v7.0 (Upgraded Version)

Welcome to the **TextExtract Pro Max v7.0**! This is a state-of-the-art PDF segment extraction, paragraph cleaning, and multi-cloud LLM routing application designed with a premium, high-fidelity dark-mode glassmorphic user interface.

It has been built and isolated in this folder (`upgraded/`) using the fast, modern **`uv` python project manager** to ensure zero interference with your existing parent project.

---

## ✨ Features Upgraded & Introduced

### 1. Premium Dark-Mode Glassmorphism UI
- **Outfit & Inter Typography**: Styled using professional Google Fonts (`Outfit` for bold modern headings, `Inter` for highly readable body text).
- **Glassmorphic Cards**: Beautiful translucent, frosted-glass panels (`backdrop-filter: blur(8px)`) with subtle borders, glowing box-shadows, and smooth hover animations.
- **Indigo/Indigo Gradients**: Futuristic dark elements accented with neon glowing badges and action cards.
- **Customized UI Controls**: Native Streamlit sliders, tabs, buttons, and metrics completely styled to feel like an enterprise SaaS portal.

### 2. High-Performance Dual PDF Ingestion Engine
- **PyMuPDF (fitz) Core**: Upgraded from `PyPDF2` to `PyMuPDF` which processes documents **10x to 50x faster** and extracts page layout elements with high layout fidelity.
- **PyPDF2 Fallback**: Built-in automatic safety fallback imports. If `PyMuPDF` is not available, the app automatically falls back to `PyPDF2` so it never crashes.
- **PDF Metadata Analytics**: Visual dashboard metrics showing characters, words, estimated reading time, and character density per page in real-time.

### 3. Flexible Boundary Extraction Modes
- **Single Boundary Block**: Instantly extract text between unique start/end words/phrases.
- **Dynamic Multi-Block Synthesis**: Add/remove multiple extraction blocks dynamically. Use it to merge non-contiguous sections of a book (e.g. page 5 section + page 12 section) into a single unified notes page.
- **Fuzzy Live Validation**: The UI updates in real-time as you type, showing exactly how many occurrences of start and end markers exist downstream.

### 4. Advanced Multi-Cloud LLM Broker Router
- **Expanded Model Suite**:
  - **Google Gemini**: Gemini 2.5 Flash, Gemini 2.5 Pro, Gemini 1.5 Pro, Gemini 1.5 Flash.
  - **Anthropic Claude**: Claude 3.5 Sonnet, Claude 3.5 Haiku.
  - **Meta LLaMA**: LLaMA 3.3 70B (Groq), LLaMA 3.1 8B (Groq).
  - **DeepSeek Suite**: Local DeepSeek-R1 (1.5B/8B via Ollama), Cloud DeepSeek V3.
- **Dynamic Study Presets**: Select format presets that instantly update the system instructions:
  - 📚 **ICAI CA Exam Notes**: Formatted pointwise with exam-ready headings, technical keywords, and ultra-short revision notes.
  - 📝 **Executive Brief & Summary**: Structure key facts, numbers, and recommendations.
  - 🃏 **Active Recall Flashcards**: Converts textbook segments into interactive conceptual Q&A flashcards.
  - 🔍 **Conceptual ELI5 Deep-Dive**: Simplifies hard terminology into plain concepts with simple analogies.

### 5. Persistent Chronological Session Vault
- **Master Study Vault**: All extracted and synthesized pages are saved chronologically in frosted glass panels.
- **In-App Live Editor**: Click to expand any note and **edit the text directly** inside the Vault.
- **In-Vault Regeneration**: Regenerate any card's summary in-place using a different prompt preset or a different model entirely.
- **Multi-Format Exports**: Download your compiled revision notes as:
  - ⬇️ **Markdown (.md)**: Clean structured document.
  - ⬇️ **Print-ready HTML**: Stylized template with a print stylesheet.
  - ⬇️ **Raw JSON (.json)**: Export full session structures.

### 6. Interactive Live Highlighter Viewer
- Enter any search query while reading the raw text, and it dynamically highlights matches in real-time with a glowing background.
- Shows live match count statistics and paragraph flows.

---

## 🚀 How to Run the Upgraded Project

To run this upgraded version using the **`uv`** package manager (which is fully configured and ready in this directory):

1. Open your terminal or powershell and navigate to the project directory:
   ```powershell
   cd D:\PythonTools\text_extract_pro
   ```
2. Run the dedicated batch runner script:
   ```powershell
   .\upgraded\run_app.bat
   ```
   *Alternatively, run the streamlit application manually using `uv`:*
   ```powershell
   cd upgraded
   uv run streamlit run main.py
   ```

3. The application will launch in your browser at `http://localhost:8501`.

---

## 📁 File Structure Created

All upgraded modifications have been safely confined inside the `upgraded/` subfolder:
- 📄 `upgraded/main.py`: The core premium application code.
- 📄 `upgraded/run_app.bat`: Windows executable runner to launch the server inside the virtual environment.
- 📄 `upgraded/pyproject.toml`: The isolated python package declaration managing all upgraded dependencies.
- 📄 `upgraded/README.md`: Upgraded project guide (this document).
