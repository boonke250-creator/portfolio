# Portfolio Admin Dashboard with Python Backend

A secure portfolio management system with a Flask backend and beautiful UI.

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `.env` file to change the admin password:

```env
ADMIN_PASSWORD=your_secure_password_here
```

### 3. Start the Flask Backend

```bash
python app.py
```

The backend will start on `http://localhost:5000`

### 4. Open the Portfolio

In another terminal, start a simple HTTP server:

```bash
# PowerShell
python -m http.server 8000

# Or use Python 3
python3 -m http.server 8000
```

Then open: `http://localhost:8000/boonke.html`

## Accessing the Admin Dashboard

### Method 1: Keyboard Shortcut
Press `Ctrl + Shift + A` anywhere on the site

### Method 2: Direct URL
Navigate to: `http://localhost:8000/boonke.html#admin`

### Method 3: Password Prompt
Either method will prompt you for the admin password (default: `admin123`)

## Features

✅ Secure password authentication  
✅ Token-based session management  
✅ Database storage (SQLite)  
✅ Edit hero section, stats, experience, skills, education, languages  
✅ Add/remove items dynamically  
✅ Save changes to database  
✅ Load previously saved data  

## File Structure

```
├── app.py              # Flask backend server
├── boonke.html         # Portfolio frontend
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (passwords, config)
├── .gitignore          # Git ignore file
├── portfolio.db        # SQLite database (auto-created)
└── README.md           # This file
```

## Security Notes

- Passwords are hashed using SHA-256
- Session tokens expire after 24 hours
- All API calls require proper authentication
- Password stored in `.env` is never exposed to frontend
- Never commit `.env` file to version control

## Deployment

For production deployment:

1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up HTTPS/SSL
3. Use a proper database (PostgreSQL, MySQL)
4. Change default password immediately
5. Set `FLASK_ENV=production`
6. Use environment variables for sensitive data

## Troubleshooting

**"Connection error" when accessing admin:**
- Ensure Flask backend is running: `python app.py`
- Check if it's on `http://localhost:5000`
- Check CORS settings if running on different domains

**Changes not saving:**
- Verify admin token is valid
- Check browser console for errors
- Ensure backend has write permissions

**Database errors:**
- Delete `portfolio.db` and restart to recreate
- Check file permissions in the folder
