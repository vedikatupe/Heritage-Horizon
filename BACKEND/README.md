# Heritage Horizon Backend - Setup Instructions

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_db.py
```

### 3. Run Backend Server
```bash
python app.py
```

The backend will start at `http://127.0.0.1:5000`

---

## API Endpoints

### Authentication
- **POST** `/register` - Register new user
- **POST** `/login` - User login

### User Profile
- **GET** `/user/<user_id>` - Get user profile
- **PUT** `/user/<user_id>` - Update user profile

### Games
- **GET** `/games` - Get all available games
- **GET** `/game/<game_id>` - Get specific game details

### Scores & Progress
- **POST** `/save-score` - Save game score
- **GET** `/user-scores/<user_id>` - Get all user scores
- **GET** `/user-high-scores/<user_id>` - Get highest score per game
- **GET** `/dashboard/<user_id>` - Get complete dashboard data

### Leaderboards
- **GET** `/leaderboard` - Global leaderboard
- **GET** `/leaderboard/<game_id>` - Game-specific leaderboard

### Statistics
- **GET** `/stats/user/<user_id>` - Get user statistics

### Health
- **GET** `/` - Health check
- **GET** `/health` - Detailed health check

---

## Sample API Requests

### Register User
```json
POST /register
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "student"
}
```

### Login
```json
POST /login
{
  "email": "john@example.com",
  "password": "password123"
}
```

### Save Score
```json
POST /save-score
{
  "user_id": 1,
  "game_id": 1,
  "score": 85,
  "level": 2,
  "completion_time": 120
}
```

### Get Dashboard
```
GET /dashboard/1
```

### Get Leaderboard
```
GET /leaderboard?limit=10
```

---

## Database Schema

### users
- user_id (PRIMARY KEY)
- name
- email (UNIQUE)
- password (hashed)
- role (student/admin)
- created_at

### games
- game_id (PRIMARY KEY)
- game_name
- game_type
- section
- max_score

### scores
- score_id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- game_id (FOREIGN KEY)
- score
- level
- completion_time
- date_completed

---

## Testing

Use Postman, VS Code REST Client, or curl to test endpoints:

```bash
# Test health
curl http://127.0.0.1:5000/health

# Test login
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'
```

---

## Features

✅ User Authentication (Register/Login with hashed passwords)
✅ Game Management
✅ Score Tracking with timestamps
✅ User Profiles
✅ Leaderboards (Global & Per-Game)
✅ User Statistics
✅ Dashboard with game progress
✅ Error Handling
✅ CORS enabled for frontend integration

---

## Notes

- Database file `game_scores.db` is created automatically
- All passwords are hashed using Werkzeug security
- CORS is enabled for frontend access
- Default admin credentials after init:
  - Email: admin@example.com
  - Password: admin123
