import os
import json
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

class GoogleCalendarManager:
    def __init__(self):
        self.creds = None
        self.service = None
        
    def authenticate(self):
        """Authenticate with Google Calendar API"""
        # The file token.json stores the user's access and refresh tokens
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                # You'll need to create credentials.json from Google Cloud Console
                if os.path.exists('credentials.json'):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    self.creds = flow.run_local_server(port=0)
                else:
                    return False, "credentials.json not found. Please set up Google Calendar API credentials."
            
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        
        try:
            self.service = build('calendar', 'v3', credentials=self.creds)
            return True, "Authentication successful"
        except Exception as e:
            return False, f"Authentication failed: {str(e)}"
    
    def create_event(self, todo):
        """Create a Google Calendar event from a todo"""
        if not self.service:
            success, message = self.authenticate()
            if not success:
                return False, message
        
        try:
            # Prepare event details
            event = {
                'summary': f"{todo.icon or '📝'} {todo.title}",
                'description': todo.description or '',
                'start': {
                    'date': todo.deadline,
                    'timeZone': 'UTC',
                },
                'end': {
                    'date': todo.deadline,
                    'timeZone': 'UTC',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 30},
                    ],
                },
            }
            
            # Create the event
            event_result = self.service.events().insert(
                calendarId='primary', body=event
            ).execute()
            
            return True, event_result['id']
            
        except HttpError as error:
            return False, f"An error occurred: {error}"
    
    def update_event(self, todo):
        """Update a Google Calendar event"""
        if not todo.google_calendar_id:
            return self.create_event(todo)
        
        if not self.service:
            success, message = self.authenticate()
            if not success:
                return False, message
        
        try:
            event = {
                'summary': f"{todo.icon or '📝'} {todo.title}",
                'description': todo.description or '',
                'start': {
                    'date': todo.deadline,
                    'timeZone': 'UTC',
                },
                'end': {
                    'date': todo.deadline,
                    'timeZone': 'UTC',
                },
            }
            
            event_result = self.service.events().update(
                calendarId='primary',
                eventId=todo.google_calendar_id,
                body=event
            ).execute()
            
            return True, event_result['id']
            
        except HttpError as error:
            if error.resp.status == 404:
                # Event not found, create new one
                return self.create_event(todo)
            return False, f"An error occurred: {error}"
    
    def delete_event(self, google_calendar_id):
        """Delete a Google Calendar event"""
        if not google_calendar_id:
            return True, "No event to delete"
        
        if not self.service:
            success, message = self.authenticate()
            if not success:
                return False, message
        
        try:
            self.service.events().delete(
                calendarId='primary',
                eventId=google_calendar_id
            ).execute()
            
            return True, "Event deleted successfully"
            
        except HttpError as error:
            if error.resp.status == 404:
                return True, "Event already deleted"
            return False, f"An error occurred: {error}"
    
    def get_auth_url(self):
        """Get authentication URL for Google Calendar"""
        if os.path.exists('credentials.json'):
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            auth_url, _ = flow.authorization_url(prompt='consent')
            return auth_url
        return None

# Global instance
calendar_manager = GoogleCalendarManager() 