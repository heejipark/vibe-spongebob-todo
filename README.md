# 🧽 SpongeBob Todo App

A playful, full-featured todo application with a SpongeBob SquarePants theme! Built with FastAPI, SQLAlchemy, and modern web technologies.

![SpongeBob Todo App](https://img.shields.io/badge/SpongeBob-Ready%20to%20Party!-yellow?style=for-the-badge&logo=spongebob)

## 🌟 Features

### ✨ Core Functionality
- **User Authentication**: Secure JWT-based login/signup system
- **CRUD Operations**: Create, read, update, and delete todos
- **User Isolation**: Each user sees only their own todos
- **Sorting & Filtering**: Sort by priority, deadline, or creation date
- **Search**: Find todos quickly with text search

### 🎨 SpongeBob Theme
- **Playful Design**: Bright colors and cartoonish styling
- **Animated Background**: Floating waterdrops and SpongeBob-themed icons
- **Responsive Layout**: Works perfectly on desktop and mobile
- **Dark/Light Mode**: Toggle between themes

### 📅 Advanced Features
- **Calendar View**: Visual calendar interface for todo management
- **Priority Levels**: High, Medium, Low priority with color coding
- **Deadline Support**: Optional due dates with visual indicators
- **Icon Support**: Add emojis and custom icons to todos

### 🔧 Technical Features
- **FastAPI Backend**: Modern, fast Python web framework
- **SQLAlchemy ORM**: Robust database management
- **JWT Authentication**: Secure token-based authentication
- **Bootstrap UI**: Clean, responsive interface
- **Jinja2 Templates**: Dynamic HTML rendering

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/heejipark/vibe-spongebob-todo.git
   cd vibe-spongebob-todo
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///./todos.db
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8000`

## 📱 Usage

### Getting Started
1. **Sign up** for a new account or **log in** with existing credentials
2. **Create your first todo** using the "Add New Todo" button
3. **Organize your todos** with priorities, deadlines, and icons
4. **Switch to calendar view** for a different perspective
5. **Search and filter** to find specific todos quickly

### Features Guide
- **Priority Colors**: Red (High), Yellow (Medium), Green (Low)
- **Deadline Indicators**: Visual warnings for overdue items
- **Icon Filter**: Filter todos by their associated icons
- **Bulk Actions**: Select multiple todos for batch operations
- **Responsive Design**: Works seamlessly on all devices

## 🛠️ Configuration

### Customization
- **Theme Colors**: Modify CSS variables in `static/style.css`
- **Database**: Change `DATABASE_URL` in `.env` for different databases
- **Security**: Update `SECRET_KEY` for production deployment

## 🏗️ Project Structure

```
vibe-spongebob-todo/
├── main.py                 # FastAPI application entry point
├── auth.py                 # Authentication and JWT handling
├── crud.py                 # Database CRUD operations
├── database.py             # Database connection and session
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas
├── requirements.txt        # Python dependencies
├── static/
│   └── style.css          # Custom CSS styles
├── templates/
│   ├── base.html          # Base template with SpongeBob theme
│   ├── login.html         # Login page
│   ├── signup.html        # Registration page
│   ├── todos.html         # Main todo interface
│   ├── calendar.html      # Calendar view
│   └── edit_todo.html     # Todo editing form
└── README.md              # This file
```

## 🔒 Security Features

- **Password Hashing**: Secure bcrypt password hashing
- **JWT Tokens**: Stateless authentication with refresh tokens
- **SQL Injection Protection**: Parameterized queries with SQLAlchemy
- **XSS Protection**: Template escaping with Jinja2
- **CSRF Protection**: Built-in FastAPI security features

## 🎯 API Endpoints

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Todos
- `GET /` - Main todo interface
- `POST /todos/` - Create new todo
- `GET /todos/{todo_id}` - Get specific todo
- `PUT /todos/{todo_id}` - Update todo
- `DELETE /todos/{todo_id}` - Delete todo
- `GET /calendar` - Calendar view

## 📬 Automated Daily Summary Emails (AI & Zapier)

You can now request the AI assistant to send daily summary emails to all users at any time. Just ask the AI to "send the daily summary email" and it will:
- Fetch the latest summary data from `/api/zapier-daily-summary`
- Generate and send summary emails to each user using their registered email address

**You do not need to set up Zapier automations for daily/weekly emails anymore unless you want to.**

### Manual Email Sending Example
- "Send the daily summary email to all users."
- "Send a summary email to [user] for today."

### API Endpoint
- `GET /api/zapier-daily-summary` — Returns, for each user:
  - Tasks due today
  - Tasks due within the next 7 days
  - Total todos
  - Completed todos
  - Completion rate

### Example API Response
```json
{
  "success": true,
  "data": [
    {
      "user_id": 1,
      "user_name": "heejipark",
      "email": "user@example.com",
      "date": "2025-07-05",
      "tasks_due_today": [
        {"id": 1, "title": "Study Vibe Coding", "deadline": "2025-07-05", "completed": false},
        {"id": 2, "title": "Go to the Trader Joe's", "deadline": "2025-07-05", "completed": true}
      ],
      "tasks_due_soon": [
        {"id": 3, "title": "Take photo", "deadline": "2025-07-11", "completed": false}
      ],
      "total_todos": 3,
      "completed_todos": 1,
      "completion_rate": 33.3
    }
  ],
  "date": "2025-07-05"
}
```

### Privacy Note
> This app sends summary emails to users using their registered email addresses. No email addresses or summary data are shared with third parties except for the configured email provider (e.g., Gmail via Zapier MCP).

### How to Use with Zapier (Optional)
1. **Expose your app to the internet** (if running locally, use [ngrok](https://ngrok.com/)):
   ```bash
   ngrok http 8000
   ```
2. **In Zapier:**
   - Trigger: "Schedule by Zapier" (every day)
   - Action: "Webhooks by Zapier" (GET your `/api/zapier-daily-summary` endpoint)
   - Action: "Looping by Zapier" (for each user in the response)
   - Action: "Gmail/Email by Zapier" (send summary to each user)

### Example Email Format
```
Subject: ToDo Summary - {date}

Hi {user_name},

Here is your ToDo summary for {date}:

✅ Tasks due today:
- ...

📅 Tasks due within 7 days:
- ... (due ...)

📊 Summary:
- Total ToDos: ...
- Completed: ...
- Completion rate: ...%

Keep up the good work!

— Your ToDo Assistant
```

See `ZAPIER_SETUP.md` for a full step-by-step guide.

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Ensure the database directory is writable
chmod 755 .
```

**Port Already in Use**
```bash
# Change the port in main.py or kill the existing process
lsof -ti:8000 | xargs kill -9
```

**Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SpongeBob SquarePants** for the inspiration
- **FastAPI** for the amazing web framework
- **Bootstrap** for the responsive UI components
- **SQLAlchemy** for the robust ORM

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/heejipark/vibe-spongebob-todo/issues) page
2. Create a new issue with detailed information
3. Include your Python version and error messages

---

**Ready to get organized with SpongeBob? Let's make some todos! 🧽✨** 