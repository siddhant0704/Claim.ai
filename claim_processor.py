import os
from dotenv import load_dotenv
import pytesseract
from PIL import Image
from pdfminer.high_level import extract_text
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Set up the OpenAI client
client = OpenAI(api_key=api_key)

# --- Text Extraction ---
def extract_text_from_pdf(file_path):
    return extract_text(file_path)

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)

def transcribe_audio(audio_path):
    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=f)
    return transcript.text

# --- GPT Utility ---
def gpt_call(prompt, model="gpt-3.5-turbo", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content

# --- Document Classification + Info Extraction ---
def classify_and_extract(text):
    prompt = f"""
You are an expert assistant. First, classify the document into one of the following categories:
- Medical Record
- Insurance Claim
- Personal Document
- Prescription
- Lab Report

Then, extract key information in structured JSON format.

Document:
\"\"\"
{text}
\"\"\"
    """
    return gpt_call(prompt)

# --- Generate Claim Summary ---
def generate_claim_summary(combined_info):
    prompt = f"""
You are an expert insurance analyst. Given the extracted document information below, determine:

1. Whether this is a valid claim or not (Yes/No).
2. Justify the decision.
3. Highlight any missing information required for processing.

Extracted Info:
\"\"\"
{combined_info}
\"\"\"

Respond in the following format:

{{
  "Claim Valid": "Yes/No",
  "Reasoning": "...",
}}
    """
    return gpt_call(prompt)

# --- Suggest Missing Documents ---
def suggest_missing_documents(combined_info):
    prompt = f"""
You are a healthcare insurance assistant. Based on the extracted claim data:

\"\"\"
{combined_info}
\"\"\"

Suggest what key documents or information are missing that could help strengthen the claim (e.g., prescription, diagnosis, billing codes, test results).

    """
    return gpt_call(prompt)

# --- 🧠 Final Pipeline ---
def process_claim_case(documents):
    """
    documents = list of tuples like: [("path/to/file1.pdf", "pdf"), ("image1.png", "image")]
    """
    all_extracted_info = []
    combined_text = ""

    for file_path, file_type in documents:
        if file_type == "pdf":
            text = extract_text_from_pdf(file_path)
        elif file_type == "image":
            text = extract_text_from_image(file_path)
        elif file_type == "audio":
            text = transcribe_audio(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        extracted_info = classify_and_extract(text)
        all_extracted_info.append(extracted_info)
        combined_text += f"\n--- Document: {file_path} ---\n{text}"

    combined_info = "\n\n".join(all_extracted_info)

    claim_summary = generate_claim_summary(combined_info)
    missing_docs = suggest_missing_documents(combined_info)

    return {
        "combined_info": combined_info,
        "claim_summary": claim_summary,
        "missing_documents": missing_docs,
        "combined_text": combined_text
    }
