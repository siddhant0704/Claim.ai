# ClaimPal.ai

Smart Document Understanding and Reasoning Engine for Healthcare Claims

Dev URL: https://claim-ai.onrender.com/

---

## Overview

**ClaimPal.ai** is an intelligent, agentic platform designed to streamline the intake, processing, and review of healthcare insurance claims. It leverages OCR, NLP, and AI to extract, classify, and summarize information from uploaded documents (PDFs, images, audio), providing insurance companies and hospital admins with structured, actionable data for rapid claim assessment and communication.

---

## Features

- 📄 **Multi-format Upload:** Supports PDFs, images (JPG, PNG), and audio files.
- 🏷️ **Automatic Document Classification:** Detects document type (e.g., Medical Record, Prescription, Lab Report) and only processes healthcare-related docs.
- 🧠 **AI-Powered Extraction:** Uses LLMs to extract and summarize key patient and claim information.
- ❌ **Missing Document Detection:** Identifies missing or incomplete information for each claim.
- 🤖 **Agentic Clarification:** If info is missing, the AI generates a ready-to-send clarification email template for the admin to send to the patient/hospital.
- 📧 **Gmail Integration:** Send clarification emails directly from the app using your Gmail account (App Password required).
- 📊 **Dashboard:** Visualizes all patient claims, statuses, and summaries in a clean, interactive table.
- 🗑️ **Bulk Edit & Delete:** Edit mode with checkboxes for selecting and deleting multiple patient entries at once.
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

Create a `.env` file in the root directory and add your keys:

```
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GMAIL_SENDER_EMAIL=your_gmail@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password   # See below for setup
```

#### Gmail App Password Setup

- Enable 2-Step Verification on your Google account.
- Create an [App Password](https://myaccount.google.com/apppasswords) for "Mail".
- Use this app password for `GMAIL_APP_PASSWORD`.

### 4. Install Tesseract OCR

```sh
sudo apt-get install tesseract-ocr
# or use the apt.txt file if deploying on a service that supports it
```

### 5. Run the App

```sh
python app.py
```

The app will be available at [http://0.0.0.0:8050](http://0.0.0.0:8050).

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
2. **Process Claim:** Upload PDFs, images, or audio files. The app extracts and summarizes key info, and classifies document type.
3. **Review & Submit:** View structured patient profiles, preview uploaded docs, and update claim status.
4. **Agentic Clarification:** If documents/info are missing, click "Reach Out to Patient" to generate and send a clarification email directly from the app.
5. **Dashboard:** Monitor all claims, their status, and summaries at a glance. Use "Edit" to select and delete multiple entries.

---

## Requirements

- Python 3.8+
- [OpenAI API Key](https://platform.openai.com/)
- [Google OAuth Credentials](https://console.cloud.google.com/apis/credentials) (for login)
- [Gmail App Password](https://myaccount.google.com/apppasswords) (for sending emails)
- Tesseract OCR (for image extraction)
- [Git LFS](https://git-lfs.github.com/) (if using large files)

---

## Customization

- **Document Types:** Update `utils.py` to add or modify document classification logic.
- **UI/UX:** Edit `assets/styles.css` and layouts in `pages/` for branding or workflow changes.
- **Database:** Integrate with your own DB in `instance/` for persistent claim storage.

---

## Security Notes

- Never commit your `.env` file or credentials to version control.
- For production, consider using the Gmail API with OAuth2 for more robust email sending.

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