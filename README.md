# 🧪 Chemical Research Agent

The **Chemical Research Agent** is a Streamlit-based web app that allows users to:

- 🔍 Search for chemical compounds by name or CAS number  
- 🖼️ View structure images of the compound (from PubChem/Cactus/Wikidata)  
- 📚 Find and download related research papers (from Semantic Scholar, CrossRef, or arXiv)  
- 🧾 View recent search history  
- 🧠 Use an autocomplete chemical name input (with ChEBI data)

---

## 🚀 Features

- ✅ **Autocomplete search** for chemical names using ChEBI dataset
- 🧬 Automatically retrieves **chemical structure image and PubChem CID**
- 📄 Fetches up to **10 related academic papers**
- ⬇️ One-click **CSV download** of search results
- 🔁 Maintains recent **search history**
- ⚠️ **Gracefully handles unknown chemicals** and provides helpful suggestions

---
## 📦 Project Structure

```
chemical_research_agent/
├── app.py              # Streamlit app entry
├── ui.py               # Streamlit UI layout and logic
├── chemical_lookup.py  # Fetches compound info and structure
├── paper_search.py     # Searches related academic papers
├── database.py         # Stores and loads history from SQLite
├── chebi_names.txt     # Preloaded ChEBI names for autocomplete
├── config.py           # Optional SSL config
├── reset_db.py         # Script to reset DB and apply schema
├── data/
│   └── chemicals.db    # Search history database (auto-generated)
├── output/
│   └── papers_*.csv    # CSV export of paper search
└── README.md           # This file
```

---

## 🛠️ Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/your-username/chemical-research-agent.git
cd chemical_research_agent
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
```

**Activate the environment:**

- On **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- On **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app

```bash
streamlit run app.py
```

---

### ⚙️ SSL Configuration (Optional)

If you're behind a proxy or using a custom SSL certificate, you can configure it in `config.py`:

```python
CUSTOM_CERT_PATH = "path/to/your.pem"
DISABLE_SSL_VERIFY = True  # Not recommended in production
```

---

### 📚 Data Sources

This app integrates with multiple scientific and open-access APIs:

- 🔬 [PubChem](https://pubchem.ncbi.nlm.nih.gov/)
- 📘 [Semantic Scholar](https://www.semanticscholar.org/)
- 📖 [CrossRef](https://www.crossref.org/)
- 📜 [arXiv](https://arxiv.org/)
- 🧪 [ChEBI](https://www.ebi.ac.uk/chebi/)
- ⚙️ [Streamlit](https://streamlit.io/)

---
