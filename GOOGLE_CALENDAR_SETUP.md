# Google Calendar Integration Setup

This guide will help you set up Google Calendar integration for your Todo app.

## Prerequisites

1. A Google account
2. Access to Google Cloud Console

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click on it and press "Enable"

## Step 2: Create Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Desktop application" as the application type
4. Give it a name (e.g., "Todo App Calendar Integration")
5. Click "Create"
6. Download the JSON file and rename it to `credentials.json`
7. Place `credentials.json` in your project root directory

## Step 3: Install Dependencies

```bash
source venv/bin/activate.fish
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Step 4: First Authentication

1. Start your todo app
2. Create a todo with a deadline
3. The app will automatically open a browser window for Google authentication
4. Sign in with your Google account and grant permissions
5. The authentication token will be saved as `token.json`

## Step 5: Test the Integration

1. Create a new todo with a deadline
2. Check your Google Calendar - you should see the event
3. Edit the todo - the calendar event should update
4. Delete the todo - the calendar event should be removed

## Features

- **Automatic Sync**: Todos with deadlines are automatically synced to Google Calendar
- **Event Details**: Todo title, description, and icon are included in calendar events
- **Reminders**: Calendar events include email and popup reminders
- **Bidirectional**: Changes in the app update the calendar, and calendar changes can be reflected back

## Troubleshooting

### "credentials.json not found"
- Make sure you downloaded the credentials file and placed it in the project root
- Verify the file is named exactly `credentials.json`

### Authentication errors
- Delete `token.json` and restart the app to re-authenticate
- Make sure you have the correct Google account permissions

### Calendar sync not working
- Check that the Google Calendar API is enabled in your Google Cloud project
- Verify your Google account has calendar permissions
- Check the console logs for error messages

## Security Notes

- Keep `credentials.json` and `token.json` secure and don't commit them to version control
- Add them to your `.gitignore` file
- The tokens contain sensitive authentication information

## File Structure

```
todo-app/
├── credentials.json    # Google API credentials (you create this)
├── token.json         # Authentication tokens (auto-generated)
├── google_calendar.py # Integration module
└── ...
```

## Optional: Custom Calendar

You can sync to a specific calendar instead of the primary one by modifying the `calendarId` parameter in `google_calendar.py`:

```python
# Change from 'primary' to your calendar ID
calendarId='your-calendar-id@group.calendar.google.com'
```

To find your calendar ID, go to Google Calendar settings and look for the calendar ID in the calendar details. 