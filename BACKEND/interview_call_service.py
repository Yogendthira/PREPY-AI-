"""
Twilio Integration for PREPY AI Interview System
Makes congratulatory calls to high-performing candidates (>80% score)
"""
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

class InterviewCallService:
    """Handles automated calls to candidates based on interview performance"""
    
    def __init__(self):
        """Initialize Twilio client"""
        try:
            self.client = Client(
                os.environ.get('TWILIO_ACCOUNT_SID'),
                os.environ.get('TWILIO_AUTH_TOKEN')
            )
            self.from_number = os.environ.get('TWILIO_PHONE_NUMBER')
            # Try CANDIDATE_PHONE_NUMBER first, then YOUR_PHONE_NUMBER (fallback)
            self.to_number = os.environ.get('CANDIDATE_PHONE_NUMBER') or os.environ.get('YOUR_PHONE_NUMBER')
            
            # Verify connection
            account = self.client.api.accounts(os.environ.get('TWILIO_ACCOUNT_SID')).fetch()
            print(f"✅ Twilio connected: {account.friendly_name}")
            
        except Exception as e:
            print(f"⚠️ Twilio initialization failed: {e}")
            self.client = None
    
    def create_congratulations_call(self, candidate_name="Candidate", overall_score=0, job_role=""):
        """
        Create a congratulatory call for high-performing candidates
        
        Args:
            candidate_name: Name of the candidate
            overall_score: Overall interview score (0-100)
            job_role: Position they interviewed for
        """
        
        if not self.client:
            print("❌ Twilio not configured. Call cannot be made.")
            return None
        
        # Generate personalized TwiML with simplified script
        twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" rate="medium">
        Hello {candidate_name}, this is Sarah from the HR team at PREPY Private Limited. Am I speaking with you now?
    </Say>
    <Pause length="2"/>
    
    <Say voice="alice" rate="medium">
        Great! I’m calling to share some wonderful news — you have been selected for the {job_role} position. Congratulations!
    </Say>
    <Pause length="1"/>
    
    <Say voice="alice" rate="medium">
        You performed really well in the interview, and the team is excited to have you onboard.
    </Say>
    <Pause length="1"/>
    
    <Say voice="alice" rate="medium">
        I’ll be sending your offer letter and onboarding details to your email shortly. Kindly review and let us know if you have any questions.
    </Say>
    <Pause length="1"/>
    
    <Say voice="alice" rate="medium">
        Goodbye!
    </Say>
</Response>'''
        
        try:
            print(f"\n📞 Making congratulatory call to {self.to_number}...")
            print(f"📊 Score: {overall_score}%")
            
            call = self.client.calls.create(
                twiml=twiml,
                to=self.to_number,
                from_=self.from_number,
                timeout=60
            )
            
            print(f"✅ Call initiated successfully!")
            print(f"📱 Call SID: {call.sid}")
            print(f"🔔 Candidate will receive call shortly...")
            
            return {
                'success': True,
                'call_sid': call.sid,
                'message': 'Congratulatory call initiated'
            }
            
        except Exception as e:
            print(f"❌ Call failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_feedback_call(self, candidate_name="Candidate", overall_score=0):
        """
        Create a feedback call for candidates who didn't meet the threshold
        
        Args:
            candidate_name: Name of the candidate
            overall_score: Overall interview score (0-100)
        """
        
        if not self.client:
            print("❌ Twilio not configured. Call cannot be made.")
            return None
        
        twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" rate="medium">
        Hello! This is PREPY Private Limited calling.
    </Say>
    <Pause length="1"/>
    
    <Say voice="alice" rate="medium">
        Thank you for taking the time to interview with us. Your score was {overall_score} percent.
    </Say>
    <Pause length="1"/>
    
    <Say voice="alice" rate="medium">
        While we won't be moving forward at this time, we encourage you to keep developing your skills and reapply in the future.
    </Say>
    <Pause length="1"/>
    
    <Say voice="alice" rate="medium">
        Best of luck in your job search. Goodbye!
    </Say>
</Response>'''
        
        try:
            print(f"\n📞 Making feedback call to {self.to_number}...")
            
            call = self.client.calls.create(
                twiml=twiml,
                to=self.to_number,
                from_=self.from_number,
                timeout=60
            )
            
            print(f"✅ Feedback call initiated!")
            print(f"📱 Call SID: {call.sid}")
            
            return {
                'success': True,
                'call_sid': call.sid,
                'message': 'Feedback call initiated'
            }
            
        except Exception as e:
            print(f"❌ Call failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def test_connection(self):
        """Test Twilio connection"""
        if not self.client:
            return False
        
        try:
            account = self.client.api.accounts(os.environ.get('TWILIO_ACCOUNT_SID')).fetch()
            print(f"✅ Twilio connection successful: {account.friendly_name}")
            return True
        except Exception as e:
            print(f"❌ Twilio connection failed: {e}")
            return False


def make_interview_call(overall_score, candidate_name="Candidate", job_role="", prep_type="interview"):
    """
    Main function to trigger interview result call
    
    Args:
        overall_score: Overall interview score (0-100)
        candidate_name: Name of the candidate
        job_role: Position interviewed for
        prep_type: Type of prep (interview/hackathon)
    
    Returns:
        dict: Call result with success status
    """
    
    call_service = InterviewCallService()
    
    # Only make calls for interview mode (not hackathon)
    if prep_type != "interview":
        print(f"ℹ️ Calls only enabled for interview mode (current: {prep_type})")
        return {'success': False, 'message': 'Calls only for interview mode'}
    
    # Threshold: 80% for congratulatory call
    if overall_score >= 80:
        print(f"\n🎉 HIGH SCORE DETECTED: {overall_score}%")
        print("=" * 60)
        return call_service.create_congratulations_call(
            candidate_name=candidate_name,
            overall_score=overall_score,
            job_role=job_role
        )
    else:
        print(f"\nℹ️ Score {overall_score}% below threshold (80%). No call triggered.")
        return {'success': False, 'message': 'Score below threshold'}


# Test function
if __name__ == "__main__":
    print("🧪 Testing Twilio Interview Call Service")
    print("=" * 60)
    
    # Test connection
    service = InterviewCallService()
    
    if service.test_connection():
        print("\n📞 Test Call Options:")
        print("1. High score call (90%)")
        print("2. Threshold call (80%)")
        print("3. Below threshold (75%)")
        print("4. Exit")
        
        choice = input("\nChoose option (1-4): ").strip()
        
        if choice == "1":
            make_interview_call(90, "John Doe", "Software Engineer", "interview")
        elif choice == "2":
            make_interview_call(80, "Jane Smith", "Data Scientist", "interview")
        elif choice == "3":
            make_interview_call(75, "Bob Johnson", "Developer", "interview")
        elif choice == "4":
            print("👋 Goodbye!")
    else:
        print("\n⚠️ Please configure Twilio credentials in .env file:")
        print("  - TWILIO_ACCOUNT_SID")
        print("  - TWILIO_AUTH_TOKEN")
        print("  - TWILIO_PHONE_NUMBER")
        print("  - CANDIDATE_PHONE_NUMBER")
