# ZOONETIX Admin Panel Setup

## Creating Admin Account

The admin panel allows you to manage all users and view their predictions.

### Method 1: Database Direct Insert (Recommended for First Admin)

1. **Get Python Shell Access:**
   Open a Python terminal in your project directory:
   ```bash
   python
   ```

2. **Create Admin User:**
   ```python
   from app.database import SessionLocal, User
   from app.auth import hash_password
   
   db = SessionLocal()
   
   # Create admin user
   admin_user = User(
       email="admin@example.com",
       username="admin",
       password_hash=hash_password("admin123"),
       is_admin=True
   )
   
   db.add(admin_user)
   db.commit()
   print("Admin user created successfully!")
   db.close()
   ```

3. **Exit Python:**
   ```python
   exit()
   ```

### Method 2: Via Registration + Database Update

1. Register a regular user through the app
2. Then update the database to make them admin:
   ```python
   from app.database import SessionLocal, User
   
   db = SessionLocal()
   admin = db.query(User).filter(User.email == "your-email@example.com").first()
   admin.is_admin = True
   db.commit()
   db.close()
   ```

## Accessing Admin Panel

1. **Navigate to Admin Login:**
   ```
   http://localhost:8000/admin
   ```

2. **Login with Admin Credentials:**
   - Email: `admin@example.com`
   - Password: `admin123`

## Admin Features

### 👥 User Management
- **View All Users:** See a list of all registered users
- **User Statistics:** Total users and predictions count
- **User Details:** View individual user information and their prediction history
- **Search Users:** Quickly find users by username or email
- **Delete Users:** Remove user accounts and all associated predictions

### 📊 Dashboard
- Total number of registered users
- Total number of predictions made
- User status and activity details

## Admin Panel Routes

- **Admin Login:** `GET /admin` (redirects to login if not authenticated)
- **Admin Dashboard:** `GET /admin` (shows dashboard if authenticated)

## API Endpoints (Admin Only)

All admin endpoints require authentication via `admin_token` cookie.

### Login
```
POST /api/admin/login
Content-Type: application/json

{
    "email": "admin@example.com",
    "password": "admin123"
}
```

### Get All Users
```
GET /api/admin/users
```
Returns: List of all users with prediction counts

### Get User Details
```
GET /api/admin/users/{user_id}
```
Returns: User information with complete prediction history

### Delete User
```
DELETE /api/admin/users/{user_id}
```
Deletes user and all associated predictions

### Admin Logout
```
POST /api/admin/logout
```

## Security Notes

⚠️ **Important:**
- Change default admin password immediately
- Use strong, unique passwords for admin accounts
- Don't share admin credentials with regular users
- Only grant admin access to trusted individuals
- Regularly review user accounts and predictions

## Troubleshooting

### Can't Login to Admin Panel
- Verify the user account has `is_admin = True` in the database
- Check that email and password are correct
- Ensure the app is running

### Admin Token Not Working
- Clear browser cookies: `admin_token`
- Log out and log back in

### Database Errors
- Ensure the SQLite database file exists
- Check database file permissions
- Restart the application

## Next Steps

After setting up your admin account:
1. Access the admin panel at `/admin`
2. Review all registered users
3. Monitor prediction statistics
4. Manage user accounts as needed
