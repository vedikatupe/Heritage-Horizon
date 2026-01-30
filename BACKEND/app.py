"""
Heritage Horizon Backend - Main Flask Application
Complete API for game management, user authentication, and score tracking
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
DB = "game_scores.db"

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def dict_from_row(row):
    """Convert sqlite3.Row to dictionary"""
    if row is None:
        return None
    return dict(row)

# ==========================================
# TEST & HEALTH ROUTES
# ==========================================

@app.route("/", methods=["GET"])
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "success",
        "message": "Heritage Horizon Backend is running",
        "version": "1.0.0"
    })

@app.route("/health", methods=["GET"])
def health():
    """API health check"""
    try:
        conn = get_db_connection()
        conn.execute("SELECT 1")
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

# ==========================================
# USER AUTHENTICATION ROUTES
# ==========================================

@app.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "student")

        # Validation
        if not all([name, email, password]):
            return jsonify({
                "success": False,
                "message": "Name, email, and password are required"
            }), 400

        # Hash password
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                (name, email, hashed_password, role)
            )
            conn.commit()
            user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            conn.close()

            return jsonify({
                "success": True,
                "message": "Registration successful",
                "user_id": user_id,
                "name": name,
                "email": email
            }), 201

        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({
                "success": False,
                "message": "Email already registered"
            }), 409

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    """Authenticate user and return user info"""
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({
                "success": False,
                "message": "Email and password required"
            }), 400

        conn = get_db_connection()
        user = conn.execute(
            "SELECT user_id, name, email, password, role, created_at FROM users WHERE email=?",
            (email,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            return jsonify({
                "success": True,
                "message": "Login successful",
                "user_id": user["user_id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# ==========================================
# USER PROFILE ROUTES
# ==========================================

@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Get user profile information"""
    try:
        conn = get_db_connection()
        user = conn.execute(
            "SELECT user_id, name, email, role, created_at FROM users WHERE user_id=?",
            (user_id,)
        ).fetchone()
        conn.close()

        if user:
            return jsonify({
                "success": True,
                "user": dict_from_row(user)
            }), 200
        else:
            return jsonify({"success": False, "message": "User not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Update user profile"""
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")

        conn = get_db_connection()
        conn.execute(
            "UPDATE users SET name=?, email=? WHERE user_id=?",
            (name, email, user_id)
        )
        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Profile updated successfully"
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# ==========================================
# GAME MANAGEMENT ROUTES
# ==========================================

@app.route("/games", methods=["GET"])
def get_games():
    """Get all available games"""
    try:
        conn = get_db_connection()
        games = conn.execute(
            "SELECT game_id, game_name, game_type, section, max_score FROM games"
        ).fetchall()
        conn.close()

        return jsonify({
            "success": True,
            "games": [dict_from_row(game) for game in games]
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/game/<int:game_id>", methods=["GET"])
def get_game(game_id):
    """Get specific game details"""
    try:
        conn = get_db_connection()
        game = conn.execute(
            "SELECT * FROM games WHERE game_id=?",
            (game_id,)
        ).fetchone()
        conn.close()

        if game:
            return jsonify({
                "success": True,
                "game": dict_from_row(game)
            }), 200
        else:
            return jsonify({"success": False, "message": "Game not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# ==========================================
# SCORE & GAME PROGRESS ROUTES
# ==========================================

@app.route("/save-score", methods=["POST"])
def save_score():
    """Save or update game score"""
    try:
        data = request.json
        user_id = data.get("user_id")
        game_id = data.get("game_id")
        score = data.get("score")
        level = data.get("level", 1)
        completion_time = data.get("completion_time")

        if not all([user_id, game_id, score is not None]):
            return jsonify({
                "success": False,
                "message": "user_id, game_id, and score are required"
            }), 400

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO scores (user_id, game_id, score, level, completion_time) VALUES (?, ?, ?, ?, ?)",
            (user_id, game_id, score, level, completion_time)
        )
        conn.commit()
        score_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()

        return jsonify({
            "success": True,
            "message": "Score saved successfully",
            "score_id": score_id
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/user-scores/<int:user_id>", methods=["GET"])
def get_user_scores(user_id):
    """Get all scores for a user"""
    try:
        game_id = request.args.get("game_id")

        conn = get_db_connection()
        
        if game_id:
            scores = conn.execute(
                """SELECT s.score_id, s.score, s.level, s.completion_time, s.date_completed,
                        g.game_name, g.game_type
                   FROM scores s
                   JOIN games g ON s.game_id = g.game_id
                   WHERE s.user_id=? AND s.game_id=?
                   ORDER BY s.date_completed DESC""",
                (user_id, game_id)
            ).fetchall()
        else:
            scores = conn.execute(
                """SELECT s.score_id, s.score, s.level, s.completion_time, s.date_completed,
                        g.game_id, g.game_name, g.game_type
                   FROM scores s
                   JOIN games g ON s.game_id = g.game_id
                   WHERE s.user_id=?
                   ORDER BY s.date_completed DESC""",
                (user_id,)
            ).fetchall()

        conn.close()

        return jsonify({
            "success": True,
            "scores": [dict_from_row(score) for score in scores]
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/user-high-scores/<int:user_id>", methods=["GET"])
def get_user_high_scores(user_id):
    """Get highest score for each game by user"""
    try:
        conn = get_db_connection()
        
        high_scores = conn.execute(
            """SELECT g.game_id, g.game_name, g.game_type, g.section,
                      MAX(s.score) as highest_score, COUNT(s.score_id) as attempts
               FROM games g
               LEFT JOIN scores s ON g.game_id = s.game_id AND s.user_id=?
               GROUP BY g.game_id
               ORDER BY g.section""",
            (user_id,)
        ).fetchall()

        conn.close()

        return jsonify({
            "success": True,
            "high_scores": [dict_from_row(score) for score in high_scores]
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# ==========================================
# DASHBOARD ROUTE
# ==========================================

@app.route("/dashboard/<int:user_id>", methods=["GET"])
def dashboard(user_id):
    """Get complete dashboard data for user"""
    try:
        conn = get_db_connection()

        # Get user info
        user = conn.execute(
            "SELECT name, email, role FROM users WHERE user_id=?",
            (user_id,)
        ).fetchone()

        # Get all games with high scores
        games_data = conn.execute(
            """SELECT g.game_id, g.game_name, g.game_type, g.section,
                      COALESCE(MAX(s.score), 0) as high_score,
                      COALESCE(COUNT(s.score_id), 0) as times_played,
                      COALESCE(MAX(s.date_completed), 'Not played') as last_played
               FROM games g
               LEFT JOIN scores s ON g.game_id = s.game_id AND s.user_id=?
               GROUP BY g.game_id
               ORDER BY g.section""",
            (user_id,)
        ).fetchall()

        # Calculate total score
        total_score = conn.execute(
            "SELECT SUM(score) FROM scores WHERE user_id=?",
            (user_id,)
        ).fetchone()[0] or 0

        conn.close()

        return jsonify({
            "success": True,
            "user": dict_from_row(user),
            "total_score": total_score,
            "games": [dict_from_row(game) for game in games_data]
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# ==========================================
# LEADERBOARD ROUTES
# ==========================================

@app.route("/leaderboard", methods=["GET"])
def global_leaderboard():
    """Get global leaderboard across all games"""
    try:
        limit = request.args.get("limit", 10, type=int)

        conn = get_db_connection()
        leaderboard = conn.execute(
            """SELECT u.user_id, u.name, SUM(s.score) as total_score,
                      COUNT(DISTINCT s.game_id) as games_played
               FROM users u
               LEFT JOIN scores s ON u.user_id = s.user_id
               GROUP BY u.user_id
               ORDER BY total_score DESC
               LIMIT ?""",
            (limit,)
        ).fetchall()
        conn.close()

        return jsonify({
            "success": True,
            "leaderboard": [dict_from_row(entry) for entry in leaderboard]
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/leaderboard/<int:game_id>", methods=["GET"])
def game_leaderboard(game_id):
    """Get leaderboard for a specific game"""
    try:
        limit = request.args.get("limit", 10, type=int)

        conn = get_db_connection()
        leaderboard = conn.execute(
            """SELECT u.user_id, u.name, MAX(s.score) as highest_score, COUNT(s.score_id) as attempts
               FROM users u
               LEFT JOIN scores s ON u.user_id = s.user_id AND s.game_id=?
               WHERE s.score IS NOT NULL
               GROUP BY u.user_id
               ORDER BY highest_score DESC
               LIMIT ?""",
            (game_id, limit)
        ).fetchall()
        conn.close()

        return jsonify({
            "success": True,
            "leaderboard": [dict_from_row(entry) for entry in leaderboard]
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# ==========================================
# STATISTICS ROUTES
# ==========================================

@app.route("/stats/user/<int:user_id>", methods=["GET"])
def user_statistics(user_id):
    """Get detailed statistics for a user"""
    try:
        conn = get_db_connection()

        total_games_played = conn.execute(
            "SELECT COUNT(DISTINCT game_id) FROM scores WHERE user_id=?",
            (user_id,)
        ).fetchone()[0]

        total_score = conn.execute(
            "SELECT SUM(score) FROM scores WHERE user_id=?",
            (user_id,)
        ).fetchone()[0] or 0

        average_score = conn.execute(
            "SELECT AVG(score) FROM scores WHERE user_id=?",
            (user_id,)
        ).fetchone()[0] or 0

        best_score = conn.execute(
            "SELECT MAX(score) FROM scores WHERE user_id=?",
            (user_id,)
        ).fetchone()[0] or 0

        total_attempts = conn.execute(
            "SELECT COUNT(*) FROM scores WHERE user_id=?",
            (user_id,)
        ).fetchone()[0]

        conn.close()

        return jsonify({
            "success": True,
            "statistics": {
                "total_games_played": total_games_played,
                "total_score": total_score,
                "average_score": round(average_score, 2),
                "best_score": best_score,
                "total_attempts": total_attempts
            }
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500

# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
