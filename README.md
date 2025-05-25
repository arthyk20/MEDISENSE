# 🩺 MediSense – AI-Powered Medical Chatbot

**MediSense** is a locally hosted AI chatbot built to provide accurate, real-time answers to medical queries. It uses **LLaMA 2** and the **Gale Encyclopedia of Medicine** as a domain-specific knowledge base. Designed for **educational and research** purposes, MediSense enables natural language interaction with reliable healthcare content.

> ⚠️ *This tool is not intended for clinical use or medical diagnosis.*

---

## 🚀 Features

- 💬 Medical Q&A chatbot powered by **LLaMA 2**
- 📚 Integrated with **Gale Encyclopedia of Medicine** for factual knowledge
- 🔍 Uses **vector search (FAISS/ChromaDB)** for semantic document retrieval
- 🧠 Built using **LangChain** with Retrieval-Augmented Generation (RAG)
- 🎨 Simple UI via **Chainlit**
- 💻 Fully runs on **local CPU** — no API keys or external servers required

---

## 🛠️ Tech Stack

- **Python**
- **LLaMA 2** (TheBloke model from Hugging Face)
- **LangChain** for chaining logic
- **FAISS or ChromaDB** for vector store
- **Chainlit** for front-end chat interface
- **PyMuPDF / PDFMiner** for PDF processing



## 📁 Folder Structure

MEDISENSE/
│
├── dataset/             # Medical encyclopedia PDF files
├── vectorstore/         # Stores generated FAISS vector embeddings
├── model/               # Contains your LLaMA 2 GGML model (.bin file)
├── ingest.py            # Script to load PDFs and create vector DB
├── model.py             # Main chatbot logic + Chainlit interface
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation


---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/arthyk20/MEDISENSE.git
cd MEDISENSE
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare Your Model and Data

* Download the **LLaMA 2** model weights (e.g., from *TheBloke* on Hugging Face)
* Process the medical PDF files and create vector embeddings using `ingest.py`
* Ensure `model.py` points to the correct model path and vector store directory

### 4. Launch the Chatbot

```bash
chainlit run model.py
```

Then open your browser and go to: [http://localhost:8000](http://localhost:8000)

---

## 📌 Use Cases

* 🧪 Research-based medical chatbot experiments
* 🩻 AI-assisted health information queries
* 🧠 NLP applications in biomedical domains
* 🛠️ Offline chatbot solutions for education

---

## 👩‍💻 Developer Info

**Arthy K**
🎓 M.Sc Data Science
🔗 GitHub: [@arthyk20](https://github.com/arthyk20)
💡 Passionate about NLP, Healthcare AI, and open-source development

---

## ⭐ Support the Project

If you found **MediSense** helpful, please consider ⭐ starring the repo and sharing it with others!

````
