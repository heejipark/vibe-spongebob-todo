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
- **Google Calendar Sync**: Integrate with your Google Calendar

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

### Google Calendar Integration
To enable Google Calendar sync:

1. Follow the setup guide in `GOOGLE_CALENDAR_SETUP.md`
2. Add your Google Calendar credentials to the `.env` file
3. Enable sync in the app settings

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
├── google_calendar.py      # Google Calendar integration
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