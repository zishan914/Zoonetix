# ZOONETIX - Authentication System Setup

## Overview
ZOONETIX is now equipped with a complete user authentication system that includes login and signup pages with mobile-responsive design.

## Features

✅ **User Registration**
- Email validation
- Username uniqueness check
- Password strength requirements (minimum 6 characters)
- Password confirmation matching

✅ **User Login**
- Email-based authentication
- Secure password verification with bcrypt hashing
- JWT token-based sessions

✅ **Same-Page Forms**
- Login and signup forms on the same page
- Easy toggle between forms
- Smooth animations and transitions

✅ **Mobile Responsive**
- Fully responsive design for all screen sizes
- Desktop, tablet, and mobile optimized views
- Touch-friendly interface

✅ **Security**
- Password hashing with bcrypt
- JWT token-based authentication
- Secure cookie storage
- Protected API endpoints

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
python -m uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`

## First Time User Flow

1. **Visit the app** → User lands on authentication page
2. **Create account** → Click "Sign Up" tab and fill the registration form
3. **Login** → After registration, automatically redirected to main app
4. **Use app** → Upload images and get disease predictions

## API Endpoints

### Authentication
- `POST /api/register` - Register a new user
- `POST /api/login` - Login an existing user
- `POST /api/logout` - Logout the current user
- `GET /api/user` - Get current user info

### Disease Prediction
- `POST /predict` - Upload image and get disease prediction (requires authentication)

## Registration Request

```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123",
  "confirm_password": "securepassword123"
}
```

## Login Request

```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

## Database

The app uses SQLite with the following user table:

```
users
├── id (Integer, Primary Key)
├── email (String, Unique)
├── username (String, Unique)
├── password_hash (String)
└── created_at (DateTime)
```

Database file: `zoonetix.db` (created automatically)

## File Structure

```
app/
├── auth.py                     # Authentication utilities (hashing, JWT)
├── database.py                 # Database models and connection
├── main.py                     # FastAPI app with auth routes
├── schemas.py                  # Pydantic schemas for request/response
├── static/
│   ├── css/
│   │   ├── auth.css           # Auth page styles (responsive)
│   │   └── styles.css         # Main app styles
│   └── js/
│       ├── auth.js            # Auth form handling
│       └── app.js             # Main app logic
└── templates/
    ├── auth.html              # Login/Signup page
    └── index.html             # Main disease detection app
```

## Key Features Implemented

### 1. Same-Window Login/Signup
- Toggle buttons switch between forms without page reload
- Smooth transitions and animations
- No popup windows or separate pages

### 2. Mobile Responsive Design
- Breakpoints for mobile (< 400px), tablet (< 600px), desktop
- Touch-friendly buttons and inputs
- Optimized layout for all screen sizes
- Readable fonts and proper spacing

### 3. Form Validation
- Client-side validation with error messages
- Real-time feedback for user inputs
- Password matching verification
- Email format validation

### 4. Branding
- App name: **ZOONETIX** displayed throughout
- Paw emoji 🐾 as visual identifier
- Consistent color scheme (teal accent color)
- Professional dark theme with gradient backgrounds

## Environment Variables (Optional)

Create a `.env` file to customize settings:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./zoonetix.db
```

## User Session Management

- Sessions stored in HTTP-only cookies
- 30-day expiration time
- Automatic logout on token expiration
- Logout button in navbar

## Security Notes

1. **In Production:**
   - Change the `SECRET_KEY` in `app/auth.py`
   - Use HTTPS for secure communications
   - Set `httponly=True` and `secure=True` for cookies
   - Enable CORS with specific origins

2. **Password Policy:**
   - Minimum 6 characters
   - Hashed with bcrypt (rounds=12)
   - Never stored in plain text

## Testing

### Register a new user
```bash
curl -X POST "http://localhost:8000/api/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123",
    "confirm_password": "password123"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

## Troubleshooting

**Issue: "Email already registered"**
- Use a different email address
- Or delete `zoonetix.db` to start fresh

**Issue: "Username already taken"**
- Choose a different username
- Usernames are case-sensitive

**Issue: Login not working**
- Verify email and password are correct
- Check that user account exists
- Clear browser cookies and try again

## Next Steps

- Integrate with your backend database
- Add password reset functionality
- Implement email verification
- Add social login (Google, GitHub, etc.)
- Setup user profiles and preferences

---

**Made with ❤️ for ZOONETIX**
