import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

# Load environment variables
load_dotenv()

# Twilio credentials from .env file
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
YOUR_PHONE_NUMBER = os.getenv('YOUR_PHONE_NUMBER')

def make_job_offer_call():
    """
    Makes a phone call with a job offer message using Twilio
    """
    try:
        # Initialize Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Create TwiML response with the job offer message
        # Using <break> tags for natural pauses in the conversation
        job_offer_message = """
            <speak>
                Hello, this is calling from the HR team at PREPY A I. Am I speaking with yogendthira now?
                <break time="5s"/>
                Great! I'm calling to share some wonderful news — you have been selected for the Software Engineer position. Congratulations!
                <break time="6s"/>
                You performed really well in the interview, and the team is excited to have you onboard.
                <break time="6s"/>
                I'll be sending your offer letter and onboarding details to your email shortly. Kindly review and let us know if you have any questions.
                <break time="4s"/>
                Once again, congratulations, and welcome to PREPY AI!
            </speak> 
        """
        
        # Make the call with proper TwiML structure
        twiml_response = f"""
        <Response>
            <Say voice="alice">Hello, this is calling from the HR team at PREPY A I. Am I speaking with yogendthira now?</Say>
            <Pause length="5"/>
            <Say voice="alice">Great! I'm calling to share some wonderful news — you have been selected for the Software Engineer position. Congratulations!</Say>
            <Pause length="6"/>
            <Say voice="alice">You performed really well in the interview, and the team is excited to have you onboard.</Say>
            <Pause length="6"/>
            <Say voice="alice">I'll be sending your offer letter and onboarding details to your email shortly. Kindly review and let us know if you have any questions.</Say>
            <Pause length="4"/>
            <Say voice="alice">Once again, congratulations, and welcome to PREPY AI!</Say>
        </Response>
        """
        
        call = client.calls.create(
            twiml=twiml_response,
            to=YOUR_PHONE_NUMBER,
            from_=TWILIO_PHONE_NUMBER
        )
        
        print(f"✅ Call initiated successfully!")
        print(f"📞 Call SID: {call.sid}")
        print(f"📱 Calling: {YOUR_PHONE_NUMBER}")
        print(f"📞 From: {TWILIO_PHONE_NUMBER}")
        print(f"📊 Status: {call.status}")
        print("\n💬 Conversation flow:")
        print("1. Hello, this is calling from the HR team at PREPY A I; Am I speaking with yogendthira now?")
        print("   [3 second pause]")
        print("2. Great! I'm calling to share some wonderful news — you have been selected for the Software Engineer position. Congratulations!")
        print("   [2 second pause]")
        print("3. You performed really well in the interview, and the team is excited to have you onboard.")

        print("4. I'll be sending your offer letter and onboarding details to your email shortly. Kindly review and let us know if you have any questions.")
        print("   [4 second pause]")
        print("5. Once again, congratulations, and welcome to PREPY AI!")

        
        return call.sid
        
    except Exception as e:
        print(f"❌ Error making call: {str(e)}")
        print("\n🔍 Please check:")
        print("1. Your .env file contains all required credentials")
        print("2. Your Twilio account is active and has sufficient balance")
        print("3. The phone numbers are in correct format (E.164)")
        return None

if __name__ == "__main__":
    print("🚀 Starting Twilio Job Offer Call...\n")
    make_job_offer_call()
