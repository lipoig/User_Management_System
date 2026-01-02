# User Management System - Flask Application

A complete user management system built with Flask that allows administrators to create and manage users, while users can maintain their personal profiles.

## Features

### Administrator Features
- Register and login as administrator
- Create new users with username and password
- View list of all users
- View detailed information about each user
- Delete users

### User Features
- Login with credentials provided by administrator
- View and edit personal profile
- Update name, surname, year of birth, and description
- Upload profile photo

## Project Structure

```
project/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── users.db               # SQLite database (created automatically)
│
├── templates/             # HTML templates
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Home page
│   ├── admin_register.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── view_user.html
│   ├── user_login.html
│   └── user_profile.html
│
└── static/
    └── uploads/           # User uploaded photos (created automatically)
```

## Installation & Setup

### 1. Install Python
Make sure you have Python 3.8 or higher installed.

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows**: `venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

The application will be available at: **http://127.0.0.1:5000/**

## Usage Guide

### First Time Setup

1. **Register as Administrator**
   - Go to http://127.0.0.1:5000/
   - Click "Register as Admin"
   - Create your admin account

2. **Login as Administrator**
   - Use your admin credentials to login
   - You'll be redirected to the admin dashboard

3. **Create Users**
   - In the admin dashboard, use the "Create New User" form
   - Enter username and password for new users
   - Users will be created and listed in the table below

4. **User Login**
   - Users can login at http://127.0.0.1:5000/user/login
   - They use credentials created by the administrator
   - After login, users can update their profile information

### Database Management

The database file `users.db` is created automatically when you first run the application. This file contains all user data and can be:
- **Backed up**: Simply copy the `users.db` file
- **Transferred**: Move the file to another location with the project
- **Reset**: Delete the file and restart the app to create a fresh database

To export the database:
```bash
# The database file is located at: users.db
# Simply copy this file to backup or transfer
```

## Security Notes

⚠️ **Important for Production Use:**
1. Change the `SECRET_KEY` in `app.py` to a strong random string
2. Use environment variables for sensitive configuration
3. Enable HTTPS
4. Implement rate limiting
5. Add CSRF protection
6. Use stronger password requirements
7. Consider using PostgreSQL or MySQL for production

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify the last line in `app.py`:
```python
app.run(debug=True, port=5001)  # Change to any available port
```

### Database Errors
If you encounter database errors, delete `users.db` and restart the application to create a fresh database.

### Upload Folder Issues
Ensure the application has write permissions in the project directory to create the `static/uploads` folder.

## Features Overview

| Feature | Admin | User |
|---------|-------|------|
| Registration | ✓ | ✗ |
| Login | ✓ | ✓ |
| Create Users | ✓ | ✗ |
| View All Users | ✓ | ✗ |
| Delete Users | ✓ | ✗ |
| Edit Own Profile | ✗ | ✓ |
| Upload Photo | ✗ | ✓ |

## Technologies Used
- **Backend**: Flask 3.0
- **Database**: SQLite with SQLAlchemy ORM
- **Security**: Werkzeug password hashing
- **Frontend**: HTML5, CSS3
- **File Upload**: Werkzeug secure filename handling