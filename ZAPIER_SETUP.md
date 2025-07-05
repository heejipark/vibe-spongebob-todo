# 🧽 SpongeBob Todo App - Zapier Integration Guide

## 📧 Daily Summary Email Setup

This guide will help you set up **Zapier** to automatically send daily summary emails to your todo app users.

---

## 🚀 Quick Setup

### 1. **Start Your Todo App**
Make sure your app is running and accessible:
```bash
python main.py
```
Your app will be available at: `http://localhost:8000`

### 2. **Test the API Endpoints**
Before setting up Zapier, test that the API endpoints work:

#### Test All Users Summary:
```bash
curl http://localhost:8000/api/daily-summary
```

#### Test Specific User Summary:
```bash
curl http://localhost:8000/api/daily-summary/1
```

#### Test Users List:
```bash
curl http://localhost:8000/api/users
```

---

## 🔧 Zapier Setup Steps

### Step 1: Create a New Zap

1. **Go to [Zapier.com](https://zapier.com)** and sign in
2. Click **"Create Zap"**
3. Search for **"Schedule"** as your trigger
4. Choose **"Schedule by Zapier"**

### Step 2: Configure the Schedule

1. **Choose Trigger Event:** `Every Day`
2. **Set Time:** Choose when you want emails sent (e.g., 9:00 AM)
3. **Time Zone:** Select your timezone
4. Click **"Continue"**

### Step 3: Add Webhook Action

1. **Search for "Webhooks by Zapier"**
2. Choose **"POST"** action
3. **Configure the webhook:**
   - **URL:** `http://localhost:8000/api/daily-summary`
   - **Payload Type:** `JSON`
   - **Data:** Leave empty (no data needed)

### Step 4: Add Email Action

1. **Search for your email provider** (Gmail, Outlook, etc.)
2. Choose **"Send Email"** action
3. **Configure the email:**
   - **To:** Use data from the webhook response
   - **Subject:** `ToDo Reflection - {{date}}`
   - **Body:** Use the summary data to create a beautiful email

### Step 5: Map the Data

In the email action, map these fields from the webhook response:

```
To: {{data[0].email}}
Subject: ToDo Reflection - {{date}}
Body: 
Hello {{data[0].username}}!

Your daily todo summary:

📊 Completion Rate: {{data[0].summary.completion_rate}}%
✅ Completed: {{data[0].summary.completed_tasks}} of {{data[0].summary.total_tasks}} tasks

📋 Tasks Due Today and Earlier:
{{#each data[0].summary.tasks}}
• {{title}} {{#if completed}}✅{{else}}⏳{{/if}}
{{/each}}

Keep up the great work! 🧽
```

---

## 📊 API Endpoints Reference

### 1. **Get All Users Daily Summary**
```
GET /api/daily-summary
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "user_id": 1,
      "username": "spongebob",
      "email": "spongebob@bikinibottom.com",
      "summary": {
        "total_tasks": 5,
        "completed_tasks": 3,
        "completion_rate": 60.0,
        "tasks": [
          {
            "id": 1,
            "title": "Clean kitchen",
            "description": "Wash dishes and mop floor",
            "completed": true,
            "priority": "P1",
            "deadline": "2024-06-30",
            "icon": "🧽",
            "overdue": false
          }
        ]
      }
    }
  ],
  "date": "2024-06-30",
  "total_users": 1
}
```

### 2. **Get Specific User Summary**
```
GET /api/daily-summary/{user_id}
```

### 3. **Get All Users**
```
GET /api/users
```

---

## 🎨 Email Template Examples

### Simple Text Template:
```
Hello {{username}}!

🧽 Your Daily Todo Summary - {{date}}

📊 Completion Rate: {{completion_rate}}%
✅ Completed: {{completed_tasks}} of {{total_tasks}} tasks

📋 Tasks Due Today and Earlier:
{{#each tasks}}
• {{icon}} {{title}} {{#if completed}}✅{{else if overdue}}⏰ OVERDUE{{else}}⏳{{/if}}
{{/each}}

🌟 Keep up the great work! 🌟
```

### HTML Template (Advanced):
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background: #FFD700; padding: 20px; text-align: center; }
        .stats { background: #f0f0f0; padding: 15px; margin: 10px 0; }
        .task { margin: 5px 0; padding: 5px; }
        .completed { background: #d4edda; }
        .overdue { background: #f8d7da; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧽 ToDo Reflection - {{date}}</h1>
    </div>
    
    <div class="stats">
        <h2>📊 Your Progress</h2>
        <p>Completion Rate: {{completion_rate}}%</p>
        <p>Completed: {{completed_tasks}} of {{total_tasks}} tasks</p>
    </div>
    
    <h3>📋 Tasks Due Today and Earlier:</h3>
    {{#each tasks}}
    <div class="task {{#if completed}}completed{{else if overdue}}overdue{{/if}}">
        {{icon}} {{title}} {{#if completed}}✅{{else if overdue}}⏰ OVERDUE{{else}}⏳{{/if}}
    </div>
    {{/each}}
    
    <p>🌟 Keep up the great work! 🌟</p>
</body>
</html>
```

---

## 🔄 Alternative: Weekly Summaries

To send **weekly summaries** instead of daily:

1. **Change the Schedule trigger** to "Every Week"
2. **Set the day** (e.g., Sunday at 9:00 AM)
3. **Update the email subject** to: `Weekly Todo Reflection - {{date}}`

---

## 🛠️ Troubleshooting

### Common Issues:

1. **"Connection refused" error:**
   - Make sure your todo app is running
   - Check that port 8000 is accessible

2. **"No users found" response:**
   - Create some test users in your app first
   - Make sure users have email addresses

3. **Empty task lists:**
   - Create tasks with deadlines
   - Set deadlines to today or earlier dates

4. **Zapier can't access localhost:**
   - Use a service like **ngrok** to expose your local server:
   ```bash
   ngrok http 8000
   ```
   - Then use the ngrok URL in your Zapier webhook

---

## 🎯 Next Steps

1. **Test the integration** with a few users
2. **Customize the email template** to match your brand
3. **Set up error notifications** in Zapier
4. **Monitor the automation** to ensure it's working correctly

---

## 📞 Support

If you need help with:
- **Zapier setup:** Check Zapier's documentation
- **API issues:** Check the console logs in your todo app
- **Email delivery:** Check your email provider's settings

**Happy automating! 🧽✨** 