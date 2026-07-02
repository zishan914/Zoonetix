# ZOONETIX Quick Start Guide

## 🐾 Welcome to ZOONETIX!

ZOONETIX is an AI-powered animal disease detection application with user authentication and mobile-responsive design.

### What's New? ✨

✅ **Login & Signup System**
- Create an account with email and username
- Secure password-based authentication
- One-click logout

✅ **Same-Page Authentication**
- Toggle between login and signup without page reload
- Smooth, professional animations
- No popups or separate windows

✅ **Mobile-Friendly**
- Works perfectly on desktop, tablet, and mobile
- Touch-optimized interface
- Responsive design for all screen sizes

✅ **Branded as ZOONETIX**
- Professional app name with 🐾 paw logo
- Dark theme with teal accent color
- Consistent branding throughout

### Getting Started

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Run the App
```bash
python -m uvicorn app.main:app --reload
```

#### 3. Open in Browser
```
http://localhost:8000
```

#### 4. First Time?
- Click **"Sign Up"** on the auth page
- Enter your email, choose a username, create a password
- Click **"Create Account"**
- You're logged in! Start uploading animal photos

#### 5. Returning User?
- Click **"Login"**
- Enter your email and password
- Click **"Login"**
- Ready to predict diseases!

### Features

#### Authentication
- **Email Verification**: Invalid emails are rejected
- **Strong Passwords**: Minimum 6 characters required
- **Password Confirmation**: Must match your entry
- **Secure Storage**: Passwords hashed with bcrypt

#### App Interface
- **Upload Images**: JPG and PNG formats supported
- **AI Predictions**: Get disease predictions instantly
- **Confidence Score**: See model confidence percentage
- **User Profile**: View username in navbar
- **Easy Logout**: One-click logout button

#### Responsive Design
- **Desktop**: Full-featured interface
- **Tablet**: Optimized layout and touch targets
- **Mobile**: Compact design with readable text

### File Locations

- **Login/Signup Page**: `app/templates/auth.html`
- **Main App**: `app/templates/index.html`
- **Auth Logic**: `app/auth.py`
- **Database Models**: `app/database.py`
- **API Routes**: `app/main.py`
- **Frontend JS**: `app/static/js/` 
- **Styles**: `app/static/css/`

### Database

The app uses SQLite (no setup needed):
- Database file: `zoonetix.db`
- Created automatically on first run
- Stores user accounts and login info

### Tips & Tricks

💡 **Lost password?** Currently, use the same credentials. In future updates, we'll add password reset.

💡 **Multiple accounts?** Create as many as you want! Each with unique email.

💡 **Image upload tips:**
- Use clear, well-lit photos of animals
- JPG or PNG format only
- Larger images = more detail for AI analysis

💡 **Mobile vs Desktop:**
- Mobile: Compact, touch-optimized experience
- Desktop: Full interface with side-by-side panels

### Keyboard Shortcuts

- **Tab**: Navigate between form fields
- **Enter**: Submit forms (when focused on inputs)
- **Eye icon (👁️)**: Toggle password visibility

### Security

🔒 **Your data is safe:**
- Passwords hashed immediately
- Tokens stored securely in cookies
- Never shared with third parties

### Troubleshooting

**Q: Can't sign up?**
A: Make sure your email is valid and username is unique

**Q: Forgot credentials?**
A: Delete `zoonetix.db` and start fresh (loses all data)

**Q: Images not uploading?**
A: Ensure model file exists at `model/my_mobilenet_model.keras`

**Q: App not starting?**
A: Run `pip install -r requirements.txt` to install all dependencies

### Next Steps

- Upload your first animal photo
- Get a disease prediction
- Try different images
- Invite others to create accounts
- Share results

### Support

For issues or questions:
1. Check the full documentation in `AUTH_SETUP.md`
2. Review error messages in browser console (F12)
3. Check server logs in terminal

---

**Enjoy using ZOONETIX! 🐾**

*Making livestock health detection smarter, one image at a time.*
