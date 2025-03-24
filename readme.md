# Scholarship Portal

A web application designed to help students discover, track, and apply for scholarships. The platform includes an AI-powered assistant to provide guidance and answer questions about scholarships.

## Features

- **User Authentication**
    - Email/password registration and login
    - Google OAuth integration
    - Secure password storage

- **Scholarship Management**
    - Browse available scholarships
    - View detailed scholarship information
    - Filter scholarships by various criteria

- **AI Assistant**
    - Gemini-powered chatbot for scholarship guidance
    - Personalized recommendations
    - Application assistance

## Technologies Used

- **Backend**
    - Flask
    - SQLAlchemy
    - Flask-Login
    - Flask-Mail
    - Flask-Migrate

- **Frontend**
    - HTML/CSS
    - Bootstrap 5
    - JavaScript
    - Font Awesome

- **Database**
    - SQLite (development)
    - PostgreSQL (production)

- **AI Integration**
    - Google Gemini API

## Installation and Setup

1. Clone the repository:
     ```
     git clone https://github.com/yourusername/scholarship-portal.git
     cd scholarship-portal
     ```

2. Create and activate a virtual environment:
     ```
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```

3. Install dependencies:
     ```
     pip install -r requirements.txt
     ```

4. Set up environment variables:
     Create a `.env` file in the root directory with the required configurations (see Environment Variables section below).

5. Initialize the database:
     ```
     flask db init
     flask db migrate -m "Initial migration"
     flask db upgrade
     ```

6. Run the application:
     ```
     python main.py
     ```

## Environment Variables

Configure the following environment variables in your `.env` file:

```
# Flask Configuration
SECRET_KEY=your_secret_key
SESSION_SECRET=your_session_secret

# Database Configuration
DATABASE_URL=sqlite:///app.db

# Email Configuration
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key

# Deployment Configuration (Optional)
REPLIT_DEV_DOMAIN=your-replit-domain.replit.dev
```

## Usage

1. Register for an account or sign in with Google.
2. Browse available scholarships on the dashboard.
3. Use the AI assistant to ask questions about scholarships.
4. Click on individual scholarships to view detailed information.

## Project Structure

```
scholarship-portal/
├── app.py            # Main Flask application
├── main.py           # Entry point
├── models.py         # Database models
├── forms.py          # Form definitions
├── routes.py         # Main routes
├── auth.py           # Authentication routes
├── google_auth.py    # Google OAuth integration
├── chatbot.py        # Gemini AI integration
├── templates/        # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── login.html
│   └── signup.html
├── static/           # Static assets
│   ├── css/
│   │   └── custom.css
│   └── js/
│       └── main.js
└── .env              # Environment variables
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.