import os
import sys
import time
import speech_recognition as sr
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.cloud import vision
import google.generativeai as genai
from dotenv import load_dotenv
from google.auth.transport.requests import Request  
import requests

# Load environment variables
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "latest_credentials.json" #change this
PROJECT_ID = "xyz" #change this

# Configuration Constants
SCOPES_DRIVE = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_PATH = 'latest_credentials.json' #change this
TOKEN_PATH = 'token.json' #change this
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') #change this
TEMPLATE_PATH = 'sample_tax_form_template.txt' #change this

class TaxAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.drive_service = self.authenticate_google_drive()
        genai.configure(api_key=GEMINI_API_KEY)

    def authenticate_google_drive(self):
        """Authenticate with Google Drive API"""
        creds = None
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES_DRIVE)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES_DRIVE)
                creds = flow.run_local_server(port=0)
            
            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
        
        return build('drive', 'v3', credentials=creds)

    def voice_command_handler(self):
        """Handle voice commands using speech recognition"""
        with sr.Microphone() as source:
            print("Listening for tax command...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, timeout=10)
            
            try:
                command = self.recognizer.recognize_google(audio).lower()
                if "upload" in command:
                    file_name = command.split("upload")[-1].strip()
                    file_name = file_name.replace(" dot ", ".")
                    return file_name
                return None
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Speech service error: {e}")
                return None

    def drive_upload(self, file_path):
        """Upload file to Google Drive"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")
        
        file_metadata = {'name': os.path.basename(file_path)}
        media = MediaFileUpload(file_path)
        
        try:
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            return file['id']
        except Exception as e:
            print(f"Drive upload failed: {e}")
            return None

    def vision_ocr(self, file_path):
        """Process document with Cloud Vision OCR"""
        client = vision.ImageAnnotatorClient()
        
        try:
            with open(file_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            response = client.text_detection(image=image)
            
            if response.error.message:
                raise Exception(f"Vision API Error: {response.error.message}")
            
            return response.text_annotations[0].description if response.text_annotations else ""
        except Exception as e:
            print(f"OCR processing failed: {e}")
            return ""
    
    def generate_tax_form(self, parsed_text):
        """Generate tax form using Vertex AI API"""
        PROJECT_ID = "xyz"  # From GCP Console
        LOCATION = "us-central1"
        
        if not GEMINI_API_KEY:
            print("Missing API Key")
            return ""

        prompt = f"""..."""  

        try:
            vertex_url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/gemini-pro:generateContent"
            
            headers = {
                "Authorization": f"Bearer {GEMINI_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }

            response = requests.post(vertex_url, headers=headers, json=payload)
            response.raise_for_status()
            
            return response.json()['candidates'][0]['content']['parts'][0]['text']
            
        except Exception as e:
            print(f"Vertex AI Error: {str(e)}")
            return ""

    def workflow_manager(self):
        """Main automation workflow"""
        # Step 1: Voice command handling
        file_name = self.voice_command_handler()
        if not file_name:
            print("No valid command received")
            return
        
        # Step 2: Document upload
        upload_id = self.drive_upload(file_name)
        if not upload_id:
            print("Failed to upload document")
            return
        
        # Step 3: Document processing
        parsed_text = self.vision_ocr(file_name)
        if not parsed_text:
            print("Failed to process document")
            return
        
        # Save parsed text
        parsed_filename = f"parsed_{int(time.time())}.txt"
        with open(parsed_filename, 'w') as f:
            f.write(parsed_text)
        self.drive_upload(parsed_filename)
        
        # Step 4: Tax form generation
        filled_form = self.generate_tax_form(parsed_text)
        if not filled_form:
            print("Failed to generate tax form")
            return
        
        # Save final form
        final_filename = f"tax_form_{int(time.time())}.txt"
        with open(final_filename, 'w') as f:
            f.write(filled_form)
        self.drive_upload(final_filename)
        
        print(f"Process completed successfully! Final form: {final_filename}")

if __name__ == "__main__":
    assistant = TaxAssistant()
    assistant.workflow_manager()