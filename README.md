# Todo App

A modern, feature-rich todo application built with FastAPI, SQLAlchemy, and Bootstrap. This application provides a complete CRUD system for managing todos with user authentication, sorting capabilities, and optional features like priorities and deadlines.

## Features

### Mandatory Features ✅
- **CRUD Operations**: Create, Read, Update, and Delete todos
- **User Authentication**: Secure login/signup system with password hashing
- **Per-User Isolation**: Each user sees only their own todos
- **Landing Page**: Introduction with clear login/signup buttons
- **Sorting**: Sort by creation time (ascending/descending)
- **Login Failure Handling**: Redirects to dedicated login-failed page

### Optional Features ✅
- **Priority System**: P0 (Critical) to P3 (Low) priority levels
- **Deadline Management**: Set and track deadlines for todos
- **Advanced Sorting**: Sort by title (alphabetical), priority, and deadline
- **Modern UI**: Beautiful, responsive design with Bootstrap 5
- **Real-time Updates**: Toggle completion status instantly

## Technology Stack

- **Backend**: FastAPI (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **Frontend**: Bootstrap 5, Font Awesome icons
- **Templates**: Jinja2 templating engine

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the application**:
   Open your browser and navigate to `http://localhost:8000`

## Usage Guide

### Getting Started
1. **Sign Up**: Create a new account with username, email, and password
2. **Login**: Use your credentials to access your personal todo list
3. **Create Todos**: Add new todos with title, description, priority, and deadline
4. **Manage Todos**: Edit, complete, or delete your todos as needed

### Features in Detail

#### Todo Management
- **Create**: Add new todos with optional description, priority, and deadline
- **Read**: View all your todos with sorting and filtering options
- **Update**: Edit todo details or toggle completion status
- **Delete**: Remove todos with confirmation dialog

#### Sorting Options
- **Creation Time**: Sort by when todos were created (newest/oldest first)
- **Title**: Alphabetical sorting (A-Z or Z-A)
- **Priority**: Sort by priority level (P0 → P3 or P3 → P0)
- **Deadline**: Sort by due date (earliest/latest first)

#### Priority System
- **P0**: Critical priority (red badge)
- **P1**: High priority (orange badge)
- **P2**: Medium priority (yellow badge)
- **P3**: Low priority (green badge)

## Project Structure

```
todo-app/
├── main.py              # FastAPI application and routes
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas for validation
├── crud.py              # Database CRUD operations
├── auth.py              # Authentication and security functions
├── database.py          # Database configuration
├── requirements.txt     # Python dependencies
├── templates/           # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── landing.html     # Landing page
│   ├── signup.html      # User registration
│   ├── login.html       # User login
│   ├── login_failed.html # Login failure page
│   ├── todos.html       # Main todos page
│   └── edit_todo.html   # Edit todo form
└── static/              # Static files
    └── style.css        # Custom CSS styles
```

## Security Features

- **Password Hashing**: All passwords are securely hashed using bcrypt
- **JWT Authentication**: Secure token-based authentication
- **User Isolation**: Complete separation of user data
- **Input Validation**: Server-side validation using Pydantic schemas
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## API Endpoints

### Public Routes
- `GET /` - Landing page
- `GET /signup` - Signup page
- `POST /signup` - User registration
- `GET /login` - Login page
- `POST /login` - User authentication
- `GET /login-failed` - Login failure page

### Protected Routes (Require Authentication)
- `GET /todos` - View todos with sorting options
- `POST /todos` - Create new todo
- `POST /todos/{id}/toggle` - Toggle todo completion
- `POST /todos/{id}/delete` - Delete todo
- `GET /todos/{id}/edit` - Edit todo page
- `POST /todos/{id}/edit` - Update todo
- `GET /logout` - User logout

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `hashed_password`: Encrypted password
- `created_at`: Account creation timestamp

### Todos Table
- `id`: Primary key
- `title`: Todo title
- `description`: Optional description
- `completed`: Completion status
- `priority`: Priority level (P0-P3)
- `deadline`: Optional deadline date
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `user_id`: Foreign key to users table

## Customization

### Styling
- Modify `static/style.css` for custom styling
- Update `templates/base.html` for layout changes
- Bootstrap classes can be customized in templates

### Features
- Add new sorting options in `crud.py`
- Extend priority levels in `models.py`
- Add new todo fields in models and schemas

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

2. **Database Issues**: The SQLite database (`todos.db`) will be created automatically on first run

3. **Port Already in Use**: Change the port in `main.py` or use a different port with uvicorn

4. **Authentication Issues**: Clear browser cookies if experiencing login problems

### Development

For development, run with auto-reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application. 