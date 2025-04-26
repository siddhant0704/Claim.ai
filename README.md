# Claim.ai

Smart Document Understanding and Reasoning Engine for Healthcare Claims

Dev URL: https://claim-ai.onrender.com/

---

## Overview

**Claim.ai** is an intelligent platform designed to streamline the intake, processing, and review of healthcare insurance claims. It leverages OCR, NLP, and AI (OpenAI GPT) to extract, classify, and summarize information from uploaded documents (PDFs, images, audio), providing insurance companies with structured, actionable data for rapid claim assessment.

---

## Features

- 📄 **Multi-format Upload:** Supports PDFs, images (JPG, PNG), and audio files.
- 🏷️ **Automatic Document Classification:** Detects document type (e.g., Medical Record, Prescription, Lab Report).
- 🧠 **AI-Powered Extraction:** Uses GPT to extract and summarize key patient and claim information.
- ❌ **Missing Document Detection:** Identifies missing or incomplete information for each claim.
- 📊 **Dashboard:** Visualizes all patient claims, statuses, and summaries in a clean, interactive table.
- 👤 **Patient Profile:** Detailed, structured view of each patient’s claim, uploaded docs, and extracted info.
- 🔄 **Status Management:** Easily update claim status (Pending, Submitted for Approval, Requested Additional Info).
- ✅ **Modern UI:** Built with Dash and Bootstrap for a responsive, user-friendly experience.

---

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/siddhant0704/Claim.ai.git
cd Claim.ai
```

### 2. Install Requirements

```sh
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the App

```sh
python app.py
```

The app will be available at [http://127.0.0.1:8050](http://127.0.0.1:8050).

---

## Project Structure

```
Claim.ai/
│
├── app.py                  # Main Dash app entry point
├── requirements.txt        # Python dependencies
├── utils.py                # Core logic for extraction, classification, GPT calls
├── callbacks/              # Dash callback logic (dashboard, upload, patient profile)
├── pages/                  # Layouts for dashboard, upload, and patient profile
├── assets/
│   └── styles.css          # Custom CSS for styling
├── instance/
│   └── claims.db           # (Optional) Database for persistent storage
└── README.md               # This file
```

---

## Usage

1. **Add Patient:** Click "Add Patient" on the dashboard to upload claim documents.
2. **Process Claim:** Upload PDFs, images, or audio files. The app extracts and summarizes key info.
3. **Review & Submit:** View structured patient profiles, preview uploaded docs, and update claim status.
4. **Dashboard:** Monitor all claims, their status, and summaries at a glance.

---

## Requirements

- Python 3.8+
- [OpenAI API Key](https://platform.openai.com/)
- Tesseract OCR (for image extraction)
- [Git LFS](https://git-lfs.github.com/) (if using large files)

---

## Customization

- **Document Types:** Update `utils.py` to add or modify document classification logic.
- **UI/UX:** Edit `assets/styles.css` and layouts in `pages/` for branding or workflow changes.
- **Database:** Integrate with your own DB in `instance/` for persistent claim storage.

---

## License

MIT License

---

## Acknowledgements

- [Dash by Plotly](https://dash.plotly.com/)
- [OpenAI GPT](https://platform.openai.com/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [pdfminer.six](https://github.com/pdfminer/pdfminer.six)

---

*For questions or contributions, please open an issue or pull request!*
