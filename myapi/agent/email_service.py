
# This is just for prototype in production real life settings phone call will and an emergency alert wil be 
# send to supervisor for human escalation for critical matters

import resend
from backend.config import settings

resend.api_key= settings.resend_api_key.get_secret_value()

def send_emergency_alert(patient_phone: str, patient_issue: str):
    try:
        params = {
            "from": "onboarding@resend.dev",
            "to": ["batmanmishra23@gmail.com"],  
            "subject": "Emergency: Patient Alert",
            "html": f"""
            <h3>Dental Emergency Notification</h3>
            <p><strong>Patient Contact Number:</strong> {patient_phone}</p>
            <p><strong>Message/Issue:</strong> {patient_issue}</p>
            <hr>
            <p>Sent via Caps & Crowns AI Assistant</p>
        """,
        }

        response = resend.Emails.send(params)
        print(f"Notified Human Receptionist: {response}")
        return response
    except Exception as e:
        print({f"Error sending emergency email: {e}"})
        return None


def send_cancellation_alert(patient_phone: str, patient_issue: str):
    try:
        params = {
            "from": "onboarding@resend.dev",
            "to": ["batmanmishra23@gmail.com"],  
            "subject": "Canellation: Patient Alert",
            "html": f"""
            <h3>Dental Cancellation Notification</h3>
            <p><strong>Patient Contact Number:</strong> {patient_phone}</p>
            <p><strong>Message/Issue:</strong> {patient_issue}</p>
            <hr>
            <p>Sent via Caps & Crowns AI Assistant</p>
        """,
        }

        response = resend.Emails.send(params)
        print(f"Notified Human Receptionist: {response}")
        return response
    except Exception as e:
        print({f"Error sending emergency email: {e}"})
        return None




