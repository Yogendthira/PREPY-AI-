# Prepy AI Backend

## Setup Instructions

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Open `app.py` and replace `YOUR_API_KEY_HERE` with your actual OpenRouter API key:
```python
OPENROUTER_API_KEY = 'your-actual-api-key-here'
```

### 3. Run the Server
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### 1. Upload File
**POST** `/api/upload`
- **Form Data:**
  - `file`: PDF or PPT file
  - `type`: 'interview' or 'hackathon'
  - `mode`: 'superman', 'batman', or 'hulk'
- **Response:** Initial AI evaluation message

### 2. Chat
**POST** `/api/chat`
- **JSON Body:**
  ```json
  {
    "message": "user message",
    "history": [...conversation history...],
    "system_prompt": "system prompt from session"
  }
  ```
- **Response:** AI response message

### 3. Health Check
**GET** `/api/health`
- **Response:** Server status

## Features

- ✅ PDF text extraction
- ✅ PowerPoint text extraction
- ✅ OpenRouter API integration (DeepSeek R1 model)
- ✅ Difficulty-based prompts (Superman/Batman/Hulk)
- ✅ Interview vs Hackathon mode prompts
- ✅ Conversation history management
- ✅ CORS enabled for frontend

## File Structure
```
BACKEND/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── uploads/           # Temporary file storage (auto-created)
```

## Notes
- Uploaded files are automatically deleted after processing
- Maximum file size: 16MB
- Supported formats: PDF, PPT, PPTX
