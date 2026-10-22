**🔬 Interactive Academic Research Proposal Dashboard**

An advanced agentic AI workflow built with **Flask**, **CrewAI**, and **Ollama (qwen2.5-coder:7b)** that enables researchers and students to iteratively construct full academic research proposals section-by-section with real-time web research integration.

---

 ✨ Features

- **User-Guided Section Generation:** Select specific sections (Abstract, Methodology, Literature Review, etc.) iteratively via a web dashboard.
- **Real-Time Web Search Context:** Integrates live search context into the agent prompt pipeline for up-to-date literature and research data.
- **Visual Chart & Flow Integration:** Generates structured visual elements and diagrams for timelines, methodology, and budgets.
- **Persistent Document Assembly:** Automatically aggregates generated sections in session storage.
- **One-Click Word Export (`.docx`):** Download the fully compiled proposal as a properly structured Microsoft Word document.

---

 **🛠️ Tech Stack**

- **Backend:** Python, Flask
- **Agent Orchestration:** CrewAI
- **LLM:** Ollama (`qwen2.5-coder:7b`)
- **Search Tooling:** LangChain `DuckDuckGoSearchRun`
- **Document Processing:** `python-docx`
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API)

---

**🚀 Getting Started
**
Prerequisites

1. Install **Python 3.10+**.
2. Install **Ollama** and pull the local LLM model:
   ```bash
   ollama pull qwen2.5-coder:7b
