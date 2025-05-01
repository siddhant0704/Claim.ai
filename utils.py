import os
from dotenv import load_dotenv
import pytesseract
from PIL import Image
from pdfminer.high_level import extract_text
from dash import html
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment
api_key = os.getenv("ANTHROPIC_API_KEY")

# Set up the Anthropic client
anthropic_client = Anthropic(api_key=api_key)

# --- Claude Utility ---
def claude_call(prompt, model="claude-3-opus-20240229", temperature=0):
    # Claude expects prompts in a special format
    full_prompt = f"{HUMAN_PROMPT} {prompt}{AI_PROMPT}"
    response = anthropic_client.completions.create(
        prompt=full_prompt,
        model=model,
        max_tokens_to_sample=1024,
        temperature=temperature,
    )
    return response.completion.strip()

# --- Text Extraction ---
def extract_text_from_pdf(file_path):
    return extract_text(file_path)

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)

def transcribe_audio(audio_path):
    # Claude does not support audio transcription; implement with another service if needed
    return "Audio transcription not implemented for Claude-only mode."

# --- Document Classification + Info Extraction ---
def classify_and_extract(text):
    prompt = f"""
You are an expert assistant. First, classify the document into one of the following categories:
- Medical Record
- Insurance Claim
- Personal Document
- Prescription
- Lab Report
- Other

Then, extract key information from each document.

Document:
\"\"\"
{text}
\"\"\"
    """
    return claude_call(prompt)

# --- Generate Claim Summary ---
def generate_claim_summary(combined_info, missing_docs):
    prompt = f"""
You are an expert insurance analyst.

Below is the extracted claim information:

\"\"\"
{combined_info}
\"\"\"

And here is the list of missing documents or important information:

\"\"\"
{missing_docs}
\"\"\"

Based on this:
- If NO missing documents or data are mentioned in the list above, classify the claim as valid.
- If ANY documents or information are mentioned as missing, mark the claim as invalid.

Structure response like this: 

"Claim Valid": "Yes" or "No",

"Reasoning": "...",

    """
    return claude_call(prompt)

# --- Suggest Missing Documents ---
def suggest_missing_documents(combined_info):
    prompt = f"""
You are a healthcare insurance assistant. Based on the extracted claim data:

\"\"\"
{combined_info}
\"\"\"

List down what key documents or information are missing that could help strengthen the claim. For example:
- Prescription
- Diagnosis
- Billing codes
- Test results
- Hospital discharge notes
- Doctor's signature

Only list relevant missing items.
    """
    return claude_call(prompt)

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
        elif file_type in ["image", "png", "jpg", "jpeg"]:  # Accept png as an image type
            text = extract_text_from_image(file_path)
        elif file_type == "audio":
            text = transcribe_audio(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        extracted_info = classify_and_extract(text)
        all_extracted_info.append(extracted_info)
        combined_text += f"\n--- Document: {file_path} ---\n{text}"

    combined_info = "\n\n".join(all_extracted_info)

    # 🔧 FIX: Reorder to generate missing_docs first
    missing_docs = suggest_missing_documents(combined_info)
    claim_summary = generate_claim_summary(combined_info, missing_docs)

    return {
        "combined_info": combined_info,
        "claim_summary": claim_summary,
        "missing_documents": missing_docs,
        "combined_text": combined_text
    }

def generate_patient_summary(combined_info):
    prompt = f"""
Summarize the following patient claim information in 2-3 crisp sentences. Include the patient's name, age, gender, hospital, and a brief mention of their condition or claim reason. Be concise and clear.

Information:
\"\"\"
{combined_info}
\"\"\"
"""
    return claude_call(prompt)

def format_combined_info(combined_info):
    """
    Converts the combined_info string into a structured HTML list for display.
    """
    import re
    if not combined_info:
        return "No information available"

    # Split into lines and filter out empty lines
    lines = [line.strip() for line in combined_info.splitlines() if line.strip()]
    items = []
    for line in lines:
        # Try to split on the first colon for key-value pairs
        if ":" in line:
            key, value = line.split(":", 1)
            items.append(html.Tr([html.Td(html.B(key.strip() + ":")), html.Td(value.strip())]))
        else:
            # If not a key-value, just show the line
            items.append(html.Tr([html.Td(line, colSpan=2)]))
    return html.Table(items, className="table table-sm table-borderless")