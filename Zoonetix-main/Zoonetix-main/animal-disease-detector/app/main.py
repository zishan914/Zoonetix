from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Depends, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.services.predict_service import predict_animal_disease
from app.schemas import PredictionResponse, UserRegister, UserLogin, TokenResponse, AdminUserResponse
from app.database import get_db, SessionLocal, User, Prediction
from app.auth import hash_password, verify_password, create_access_token, decode_token
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

app = FastAPI(
    title="ZOONETIX - Animal Disease Detection",
    description="AI-based animal disease prediction from photos.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Get current authenticated user from cookie"""
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    payload = decode_token(token)
    if not payload:
        return None
    
    email = payload.get("sub")
    if not email:
        return None
    
    user = db.query(User).filter(User.email == email).first()
    return user


def get_current_admin(current_user: User = Depends(get_current_user)):
    """Ensure the current user is authenticated AND is an admin"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@app.get("/", response_class=HTMLResponse)
def root(request: Request, current_user: User = Depends(get_current_user)):
    if current_user:
        return templates.TemplateResponse(request, "index.html", {
            "request": request,
            "current_user": current_user.username
        })
    else:
        return templates.TemplateResponse(request, "auth.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, current_user: User = Depends(get_current_user)):
    if current_user:
        return templates.TemplateResponse(request, "dashboard.html", {
            "request": request,
            "current_user": current_user.username
        })
    else:
        return templates.TemplateResponse(request, "auth.html", {"request": request})


@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, current_user: User = Depends(get_current_user)):
    if not current_user:
        return templates.TemplateResponse(request, "auth.html", {"request": request})
    if not current_user.is_admin:
        # Non-admins get bounced back to the main app, not the admin page
        return templates.TemplateResponse(request, "index.html", {
            "request": request,
            "current_user": current_user.username
        })
    return templates.TemplateResponse(request, "admin.html", {
        "request": request,
        "current_user": current_user.username
    })

@app.get("/services", response_class=HTMLResponse)
def services(request: Request, current_user: User = Depends(get_current_user)):
    if current_user:
        return templates.TemplateResponse(request, "services.html", {
            "request": request,
            "current_user": current_user.username
        })
    else:
        return templates.TemplateResponse(request, "services.html", {
            "request": request,
            "current_user": "Guest"
        })


@app.get("/creators", response_class=HTMLResponse)
def creators(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse(request, "creators.html", {
        "request": request,
        "current_user": current_user.username if current_user else "Guest"
    })

@app.get("/pricing", response_class=HTMLResponse)
def pricing(request: Request, current_user: User = Depends(get_current_user)):
    if current_user:
        return templates.TemplateResponse(request, "pricing.html", {
            "request": request,
            "current_user": current_user.username
        })
    else:
        return templates.TemplateResponse(request, "pricing.html", {
            "request": request,
            "current_user": "Guest"
        })


@app.post("/api/register")
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    # Validate password match
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Validate password strength
    if len(user_data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_password
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User registration failed")
    
    # Create access token
    access_token = create_access_token(data={"sub": new_user.email})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": new_user.id,
            "email": new_user.email,
            "username": new_user.username
        }
    )


@app.post("/api/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
    )


@app.post("/api/logout")
async def logout(response: Response):
    """Logout user"""
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}


@app.get("/api/user")
async def get_user(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "is_admin": current_user.is_admin
    }


@app.get("/api/admin/users")
async def get_all_users(
    admin_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Return all users with their prediction counts. Admin only."""
    users = db.query(User).order_by(User.created_at.desc()).all()

    result = []
    for u in users:
        count = db.query(Prediction).filter(Prediction.user_id == u.id).count()
        result.append({
            "id": u.id,
            "email": u.email,
            "username": u.username,
            "is_admin": u.is_admin,
            "created_at": u.created_at.isoformat() if u.created_at else None,
            "prediction_count": count
        })
    return result


@app.delete("/api/admin/users/{user_id}")
async def delete_user(
    user_id: int,
    admin_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete a user and all their predictions. Admin only."""
    if user_id == admin_user.id:
        raise HTTPException(status_code=400, detail="You cannot delete your own account")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete their predictions first (foreign key constraint)
    db.query(Prediction).filter(Prediction.user_id == user_id).delete()
    db.delete(user)
    db.commit()

    return {"message": f"User '{user.username}' deleted successfully"}


@app.get("/api/admin/users/{user_id}/predictions")
async def get_user_predictions_admin(
    user_id: int,
    admin_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get a specific user's full prediction history. Admin only."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    predictions = db.query(Prediction).filter(
        Prediction.user_id == user_id
    ).order_by(Prediction.created_at.desc()).all()

    return {
        "username": user.username,
        "predictions": [
            {
                "id": p.id,
                "disease": p.disease,
                "confidence": p.confidence,
                "image_name": p.image_name,
                "created_at": p.created_at.isoformat() if p.created_at else None
            }
            for p in predictions
        ]
    }



@app.get("/api/predictions")
async def get_predictions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's prediction history"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    predictions = db.query(Prediction).filter(
        Prediction.user_id == current_user.id
    ).order_by(Prediction.created_at.desc()).all()
    
    return [
        {
            "id": p.id,
            "disease": p.disease,
            "confidence": p.confidence,
            "image_name": p.image_name,
            "created_at": p.created_at.isoformat() if p.created_at else None
        }
        for p in predictions
    ]


@app.get("/api/stats")
async def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's prediction statistics"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    predictions = db.query(Prediction).filter(
        Prediction.user_id == current_user.id
    ).all()
    
    total = len(predictions)
    healthy = sum(1 for p in predictions if p.disease and p.disease.lower() == "healthy")
    disease = total - healthy
    
    last_prediction = predictions[-1] if predictions else None
    
    return {
        "total": total,
        "healthy": healthy,
        "disease": disease,
        "last_prediction": last_prediction.created_at.isoformat() if last_prediction and last_prediction.created_at else None
    }



@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Predict disease - requires authentication"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated. Please login first.")
    
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Image must be JPEG or PNG")

    image_bytes = await file.read()
    try:
        result = predict_animal_disease(image_bytes)
        
        # Save prediction to database
        new_prediction = Prediction(
            user_id=current_user.id,
            disease=result.disease,
            confidence=result.confidence,
            image_name=file.filename
        )
        db.add(new_prediction)
        db.commit()
        
        return result
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@app.delete("/api/predictions/{prediction_id}")
async def delete_prediction(
    prediction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a prediction"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    prediction = db.query(Prediction).filter(
        Prediction.id == prediction_id,
        Prediction.user_id == current_user.id
    ).first()
    
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    db.delete(prediction)
    db.commit()
    
    return {"message": "Prediction deleted successfully"}
