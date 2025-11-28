import requests
import json

def analyze_session(history, job_role="Candidate"):
    """
    Analyzes the interview/hackathon session history and generates a performance report.
    """
    
    # Format history for the prompt
    conversation_text = ""
    background_context = ""

    for msg in history:
        role = "Interviewer" if msg['role'] == 'assistant' else "Candidate"
        content = msg['content']
        
        # Check if this message contains the injected context
        if role == "Candidate" and "Context from uploaded file:" in content:
            parts = content.split("User's response:")
            if len(parts) > 1:
                # Extract the context (resume/project info)
                if not background_context:
                    background_context = parts[0].replace("Context from uploaded file:", "").strip()
                
                # The actual user response is the second part
                content = parts[1].strip()
            else:
                # Fallback if format is unexpected
                content = content.replace("Context from uploaded file:", "[Background Info Provided]").strip()

        conversation_text += f"{role}: {content}\n"

    system_prompt = f"""
    You are a STRICT Interview Evaluator. You are NOT helpful. You are NOT polite. You are a critical grader.
    
    CONTEXT (RESUME/PROJECTS) - FOR REFERENCE ONLY:
    {background_context}
    
    ACTUAL INTERVIEW TRANSCRIPT (EVALUATE THIS ONLY):
    {conversation_text}
    
    ⚠️ SCORING RULES (READ CAREFULLY):
    1. **IGNORE THE RESUME FOR SCORING.** A good resume with a bad interview = 0 SCORE.
    2. **AUTOMATIC FAIL CONDITIONS (Score 0-20):**
       - If the candidate says "hi", "hello", "how are you", "bby" instead of answering the question.
       - If the candidate gives one-line or one-word answers.
       - If the candidate ignores the technical question asked by the AI.
       - If the candidate's total word count in the transcript is low.
    
    3. **SCORING SCALE:**
       - 0-30: Irrelevant, rude, or very short answers. (e.g., "I don't know", "hi", "good")
       - 31-50: Vague attempts, poor English, or dodging the question.
       - 51-70: Decent answer but lacks depth.
       - 71-100: Detailed, technical, and professional answer.

    4. **MANDATORY:** If the transcript shows the candidate just said "{conversation_text.strip().splitlines()[-1] if conversation_text.strip() else 'nothing'}" or similar short text, the OVERALL SCORE MUST BE UNDER 20.

    Evaluate the candidate on:
    1. English Communication
    2. Technical Skills
    3. Communication Skills
    4. Team Collaboration
    5. Soft Skills
    6. Project Quality

    Return ONLY JSON:
    {{
        "scores": {{
            "english": 0,
            "technical": 0,
            "communication": 0,
            "teamwork": 0,
            "soft_skills": 0,
            "project": 0,
            "overall": 0
        }},
        "feedback": {{
            "strengths": "None observed.",
            "improvements": "Candidate failed to answer questions.",
            "english_assessment": "Insufficient data.",
            "recommendations": "Please take the interview seriously and answer the questions."
        }}
    }}
    """

    try:
        # Use the chat endpoint which is more reliable for instruction following
        response = requests.post('http://localhost:11434/api/chat', json={
            "model": "phi3:3.8b", 
            "messages": [
                {"role": "system", "content": system_prompt}
            ],
            "stream": False,
            "options": {
                "temperature": 0.2, # Lower temperature for more consistent JSON
                "num_predict": 1000
            }
        })
        
        if response.status_code == 200:
            result = response.json()
            response_text = result['message']['content']
            try:
                # clean up potential markdown code blocks if the model adds them
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0]
                
                return json.loads(response_text.strip())
            except json.JSONDecodeError:
                print("Error parsing JSON from AI response")
                print(f"Raw response: {response_text}")
                return None
        else:
            print(f"Ollama API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Analysis Error: {e}")
        return None
