# GGH-TaxEaseAI - Voice-Driven AI Tax Filing
AI Powered Inclusive Tax Assistant

## Project Description
Managing tax filing is often complex, especially for individuals with disabilities such as blindness or limited hand mobility. This AI-powered tax assistant automates tax filing through voice commands, making the process seamless and accessible. It leverages Google’s AI and cloud services to upload, process, and autofill tax documents without requiring manual interaction.

## Tech Stack
- **Python** – Core programming language
- **Google Cloud APIs**
  - Cloud Vision API – Extracts text from documents
  - Google Drive API – Handles file uploads and storage
  - Vertex AI & Gemini API – Generates autofilled tax forms using AI
- **SpeechRecognition** – Captures and processes voice commands
- **dotenv** – Loads environment variables securely
- **requests** – Handles API calls

## Installation
Ensure you have Python installed (preferably Python 3.8+). Then, install the required dependencies:

```sh
pip install speechrecognition google-auth google-auth-oauthlib google-auth-httplib2 google-auth-transport-requests google-api-python-client google-cloud-vision google-generativeai python-dotenv requests
```

## Configuration: Setting Up API Keys & Credentials
To use this project, you need API keys and JSON credentials from Google Cloud.

### Steps to Obtain API Credentials
1. **Enable Required APIs:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable **Google Drive API**, **Cloud Vision API**, and **Vertex AI API**.

2. **Generate OAuth Credentials for Google Drive API:**
   - Navigate to **APIs & Services > Credentials**
   - Click **Create Credentials > OAuth Client ID**
   - Select **Desktop App**, then download the `credentials.json` file.
   - Rename it to `latest_credentials.json` and place it in the project directory.

3. **Obtain Google Cloud Vision & Vertex AI Credentials:**
   - Navigate to **IAM & Admin > Service Accounts**
   - Create a new service account and download the JSON key.
   - Set the environment variable:
     ```sh
     export GOOGLE_APPLICATION_CREDENTIALS='path/to/service-account.json'
     ```

4. **Get a Gemini API Key:**
   - Sign up for Gemini API at [Google AI Studio](https://aistudio.google.com/)
   - Obtain the API key and save it in a `.env` file as:
     ```sh
     GEMINI_API_KEY=your_api_key_here
     ```

## Usage & Testing
1. Run the script:
   ```sh
   python TaxAssistant.py
   ```
2. Speak the command:
   ```
   upload filename.ext
   ```
   - The file will be uploaded to Google Drive.
   - It will be parsed using OCR and saved as `parsed_#.txt`.
   - AI will autofill the tax form and save the final document.
   
## Results
- The processed text from the uploaded document is stored in `parsed_#.txt`.
- The AI-generated, autofilled tax form is saved as `tax_form_<timestamp>.txt`.
- Both files are stored in Google Drive and locally in the project directory.

## Potential Impact
- **Accessibility:** Designed specifically for disabled individuals (blind, hand immobility, etc.).
- **Automation:** Eliminates the need for manual tax filing by leveraging AI.
- **User-Friendly:** Voice-driven interaction with no reliance on keyboard/mouse.

## Use of AI Techniques
- **Speech Recognition:** Uses speech_recognition library for capturing and processing voice commands.
- **Optical Character Recognition (OCR):** Cloud Vision API extracts text from documents.
- **Natural Language Processing (NLP):** Gemini API understands and fills tax forms based on extracted data.
- **Machine Learning:** Google Vertex AI enhances document understanding and improves accuracy of AI-generated responses.

## Code Quality
- **Modular Design:** Code follows a structured class-based design (TaxAssistant class).
- **Error Handling:** Includes exception handling for API failures, missing files, and incorrect commands.
- **Scalability:** Designed to integrate additional AI models or extend functionality if required.

## Testing Strategy
- Unit Testing: Individual functions tested for correctness.
- Error Handling Tests: Verified API failures, incorrect voice inputs, and missing files.
- Performance Testing: Ensured seamless execution of voice command to tax form generation.

---
This project ensures seamless, accessible, and secure tax filing using AI and Google Cloud services.

