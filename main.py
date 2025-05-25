from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from neo4j import GraphDatabase
from collections import defaultdict
from questions import QUESTIONS
from datetime import datetime, timedelta
import secrets
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Constants
MAX_QUESTIONS = 20
CONFIDENCE_THRESHOLD = 0.25
MANDATORY_TAGS = ["price_range", "review_score_range", "popularity_threshold"]

# Neo4j Configuration
class Gaminator:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "neo4j+s://c14f5bac.databases.neo4j.io",
            auth=("neo4j", "VX0KIEY0nrvKihZ4T_pQJPXnbjY_sjtZc8Q3OwHR2uY"))
    
    def _execute_query(self, query, **params):
        with self.driver.session() as session:
            result = session.run(query, **params)
            return result.data() if "RETURN" in query else None
    
    # User Management
    def create_user(self, username: str, email: str, password: str, is_admin: bool = False):
        user_id = str(uuid.uuid4())
        self._execute_query("""
            CREATE (u:User {
                id: $user_id,
                username: $username,
                email: $email,
                password: $password,
                is_admin: $is_admin,
                created_at: datetime()
            })
            RETURN u
        """, user_id=user_id, username=username, email=email, 
            password=password, is_admin=is_admin)
        return user_id
    
    def get_user(self, username: str = None, email: str = None, user_id: str = None):
        if user_id:
            result = self._execute_query("""
                MATCH (u:User {id: $user_id})
                RETURN u
            """, user_id=user_id)
        elif username:
            result = self._execute_query("""
                MATCH (u:User {username: $username})
                RETURN u
            """, username=username)
        else:
            result = self._execute_query("""
                MATCH (u:User {email: $email})
                RETURN u
            """, email=email)
        return result[0]["u"] if result else None
    
    def create_session(self, user_id: str):
        session_id = secrets.token_hex(16)
        expires_at = (datetime.now() + timedelta(days=7)).isoformat()
        self._execute_query("""
            MATCH (u:User {id: $user_id})
            CREATE (s:Session {
                id: $session_id,
                expires_at: $expires_at
            })-[:BELONGS_TO]->(u)
        """, user_id=user_id, session_id=session_id, expires_at=expires_at)
        return session_id
    
    def validate_session(self, session_id: str):
        result = self._execute_query("""
            MATCH (s:Session {id: $session_id})-[:BELONGS_TO]->(u:User)
            WHERE datetime() < datetime(s.expires_at)
            RETURN u
        """, session_id=session_id)
        return result[0]["u"] if result else None
    
    def delete_session(self, session_id: str):
        self._execute_query("""
            MATCH (s:Session {id: $session_id})
            DETACH DELETE s
        """, session_id=session_id)
    
    # Game Recommendations
    def score_tags(self, answers):
        tag_scores = defaultdict(float)
        for answer, question in answers:
            for tag, weight in question["tags"].items():
                tag_scores[tag] += answer * weight
        return [{"tag": tag, "score": score} for tag, score in sorted(tag_scores.items(), key=lambda x: -x[1])]
    
    def rank_games(self, tag_scores, filters):
        result = self._execute_query("""
            UNWIND $tag_scores AS ts
            MATCH (g:Game)-[:HAS_TAG]->(t:Tag)
            WHERE t.name = ts.tag
            WITH g, SUM(ts.score) AS tag_relevance
            WHERE
              ($min_price IS NULL OR g.price >= $min_price) AND
              ($max_price IS NULL OR g.price <= $max_price) AND
              ($min_score IS NULL OR g.review_score >= $min_score) AND
              ($max_score IS NULL OR g.review_score <= $max_score) AND
              ($min_popularity IS NULL OR g.popularity >= $min_popularity) AND
              ($min_year IS NULL OR g.release_date >= date($min_year + '-01-01')) AND
              ($max_year IS NULL OR g.release_date <= date($max_year + '-12-31'))
            RETURN g.name AS name, tag_relevance, g.price, g.review_score, g.popularity
            ORDER BY tag_relevance DESC
            LIMIT 5
        """, tag_scores=tag_scores, **filters)
        return result if result else []
    
    # Game History & Archetypes
    def add_played_game(self, user_id: str, game_name: str, rating: int):
        self._execute_query("""
            MATCH (u:User {id: $user_id})
            MERGE (g:Game {name: $game_name})
            MERGE (u)-[r:PLAYED {rating: $rating, played_at: datetime()}]->(g)
        """, user_id=user_id, game_name=game_name, rating=rating)
    
    def get_game_history(self, user_id: str):
        return self._execute_query("""
            MATCH (u:User {id: $user_id})-[r:PLAYED]->(g:Game)
            RETURN g.name AS game_name, r.rating AS rating, r.played_at AS played_at
            ORDER BY r.played_at DESC
            LIMIT 10
        """, user_id=user_id)
    
    def get_gamer_archetype(self, user_id: str):
        result = self._execute_query("""
            MATCH (u:User {id: $user_id})-[r:PLAYED]->(g:Game)
            WITH g, r.rating AS rating
            ORDER BY rating DESC LIMIT 5
            MATCH (g)-[:HAS_TAG]->(t:Tag)
            WITH t.name AS tag, COUNT(*) AS freq
            ORDER BY freq DESC LIMIT 5
            WITH COLLECT(tag) AS top_tags
            RETURN 
                CASE
                    WHEN ANY(t IN top_tags WHERE t IN ['RPG', 'Character Customization']) 
                        THEN {name: 'The Roleplayer', description: 'You love deep stories and character progression', traits: ['Story-driven', 'Character-focused', 'Immersive']}
                    WHEN ANY(t IN top_tags WHERE t IN ['Competitive', 'PvP']) 
                        THEN {name: 'The Competitor', description: 'You thrive on challenge and player vs player combat', traits: ['Skilled', 'Strategic', 'Leaderboard-climber']}
                    WHEN ANY(t IN top_tags WHERE t IN ['Exploration', 'Open World']) 
                        THEN {name: 'The Explorer', description: 'You enjoy discovering new places and hidden secrets', traits: ['Curious', 'Adventurous', 'Completionist']}
                    ELSE {name: 'The Balanced Gamer', description: 'You enjoy a variety of gaming experiences', traits: ['Adaptable', 'Versatile', 'Well-rounded']}
                END AS archetype
        """, user_id=user_id)
        return result[0]["archetype"] if result else None
    
    # Admin Functions
    def get_all_users(self):
        return self._execute_query("""
            MATCH (u:User)
            RETURN u.id AS id, u.username AS username, 
                   u.email AS email, u.created_at AS created_at
            ORDER BY u.created_at DESC
        """)

# Initialize database connection
db = Gaminator()

# Helper Functions
def extract_filters(answers):
    filters = {
        "min_price": None, "max_price": None,
        "min_score": None, "max_score": None,
        "min_popularity": None,
        "min_year": None, "max_year": None,
    }
    for answer, q in answers:
        scale = answer / 5.0
        if "price_range" in q:
            min_p, *max_p = q["price_range"]
            filters["min_price"] = max(filters["min_price"] or 0, int(min_p * scale))
            filters["max_price"] = min(filters["max_price"] or 9999, int((max_p[0] if max_p else 9999) * scale))
        if "review_score_range" in q:
            min_r, max_r = q["review_score_range"]
            filters["min_score"] = max(filters["min_score"] or 0, int(min_r * scale))
            filters["max_score"] = min(filters["max_score"] or 100, int(max_r * scale))
        if "popularity_threshold" in q:
            filters["min_popularity"] = max(filters["min_popularity"] or 0, int(q["popularity_threshold"] * scale))
        if "release_year_range" in q:
            filters["min_year"] = max(filters["min_year"] or 1900, q["release_year_range"][0])
            filters["max_year"] = min(filters["max_year"] or 2100, q["release_year_range"][-1])
    return filters

def question_info_gain(question, tag_weights):
    total = 0.0
    for tag, weight in question["tags"].items():
        importance = tag_weights.get(tag, 0)
        uncertainty = 1.0 - min(importance, 1.0)
        total += uncertainty * weight
    return total

def has_answered_mandatory(answered, key):
    for _, q in answered:
        if key in q:
            return True
    return False

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = db.validate_session(request.cookies.get("session_id"))
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

# Add to main.py
@app.get("/quiz", response_class=HTMLResponse)
async def quiz_start(request: Request):
    user = db.validate_session(request.cookies.get("session_id"))
    if not user:
        return RedirectResponse(url="/login?next=/quiz", status_code=status.HTTP_303_SEE_OTHER)
    
    # Reset quiz progress for new session
    db._execute_query("""
        MATCH (u:User {id: $user_id})
        REMOVE u.current_quiz_index, u.quiz_answers
    """, user_id=user["id"])
    
    return templates.TemplateResponse("quiz_start.html", {
        "request": request,
        "user": user,
        "total_questions": len(QUESTIONS)
    })

@app.get("/quiz/next", response_class=HTMLResponse)
async def quiz_next(request: Request):
    try:
        # Validate session
        session_id = request.cookies.get("session_id")
        if not session_id:
            return RedirectResponse(url="/login", status_code=303)
        
        # Get user with progress
        result = db._execute_query("""
            MATCH (s:Session {id: $session_id})-[:BELONGS_TO]->(u:User)
            WHERE datetime() < datetime(s.expires_at)
            RETURN u.id AS id, 
                   u.username AS username,
                   COALESCE(u.current_quiz_index, 0) AS current_index,
                   u.is_guest IS NOT NULL AS is_guest
        """, session_id=session_id)
        
        if not result:
            return RedirectResponse(url="/login", status_code=303)
        
        user_data = result[0]
        current_index = int(user_data["current_index"])
        
        # Check if quiz is complete
        if current_index >= min(MAX_QUESTIONS, len(QUESTIONS)):
            return RedirectResponse(url="/quiz/results", status_code=303)
        
        # Get current question
        question = QUESTIONS[current_index]
        
        return templates.TemplateResponse("quiz_question.html", {
            "request": request,
            "user": {
                "id": user_data["id"],
                "username": user_data["username"],
                "is_guest": user_data["is_guest"]
            },
            "question": question,
            "question_num": current_index + 1,
            "total_questions": min(MAX_QUESTIONS, len(QUESTIONS))
        })
        
    except Exception as e:
        print(f"Error in /quiz/next: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/quiz/answer")
async def quiz_answer(request: Request):
    user = db.validate_session(request.cookies.get("session_id"))
    if not user:
        raise HTTPException(status_code=401)
    
    form_data = await request.form()
    answer = int(form_data.get("answer"))
    question_index = int(form_data.get("question_index"))
    
    # Store answer
    db._execute_query("""
        MATCH (u:User {id: $user_id})
        SET u.current_quiz_index = $next_index,
            u.quiz_answers = coalesce(u.quiz_answers, []) + [$answer]
    """, user_id=user["id"], 
       next_index=question_index + 1,
       answer={"index": question_index, "value": answer})
    
    return RedirectResponse(url="/quiz/next", status_code=303)

@app.get("/quiz/results", response_class=HTMLResponse)
async def quiz_results(request: Request):
    user = db.validate_session(request.cookies.get("session_id"))
    if not user:
        raise HTTPException(status_code=401)
    
    # Get all answers
    result = db._execute_query("""
        MATCH (u:User {id: $user_id})
        RETURN u.quiz_answers AS answers
    """, user_id=user["id"])
    
    answers = [(a["value"], QUESTIONS[a["index"]]) for a in result[0]["answers"]]
    
    tag_scores = db.score_tags(answers)
    filters = extract_filters(answers)
    top_games = db.rank_games(tag_scores, filters)
    
    # Store results for guest users
    if user.get("is_guest", False):
        for game in top_games:
            db.add_played_game(user["id"], game["name"], 5)
    
    archetype = db.get_gamer_archetype(user["id"])
    
    return templates.TemplateResponse("results.html", {
        "request": request,
        "user": user,
        "games": top_games,
        "archetype": archetype
    })

@app.post("/quiz/results")
async def quiz_results(request: Request):
    user = db.validate_session(request.cookies.get("session_id"))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    form_data = await request.form()
    answers = []
    for q_id, answer in form_data.items():
        if q_id.startswith('q_'):
            q_index = int(q_id[2:])
            answer_val = int(answer)
            answers.append((answer_val, QUESTIONS[q_index]))
    
    tag_scores = db.score_tags(answers)
    filters = extract_filters(answers)
    top_games = db.rank_games(tag_scores, filters)
    
    # Record these games as played (for archetype analysis)
    for game in top_games:
        db.add_played_game(user["id"], game["name"], 5)  # Assuming they'll like these
    
    archetype = db.get_gamer_archetype(user["id"])
    
    return templates.TemplateResponse("results.html", {
        "request": request,
        "user": user,
        "games": top_games,
        "archetype": archetype
    })

@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    user = db.validate_session(request.cookies.get("session_id"))
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    archetype = db.get_gamer_archetype(user["id"])
    raw_game_history = db.get_game_history(user["id"])

    # Format the 'played_at' datetime into a string
    formatted_game_history = []
    for entry in raw_game_history:
        played_at = entry["played_at"]
        if hasattr(played_at, "strftime"):  # Check if it's a datetime object
            played_at_str = played_at.strftime("%Y-%m-%d")
        else:
            played_at_str = str(played_at)  # Fallback for unexpected types

        formatted_game_history.append({
            "game_name": entry["game_name"],
            "rating": entry["rating"],
            "played_at": played_at_str
        })

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user,
        "archetype": archetype,
        "game_history": formatted_game_history
    })

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    user = db.validate_session(request.cookies.get("session_id"))
    if not user or not user.get("is_admin", False):
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    users = db.get_all_users()
    
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "user": user,
        "users": users
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, next_url: Optional[str] = None):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "next_url": next_url
    })

@app.post("/login")
async def login(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    next_url = form_data.get("next_url", "/")
    
    user = db.get_user(username=username)
    if not user or user["password"] != password:  # In production, use password hashing
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid username or password",
            "next_url": next_url
        })
    
    session_id = db.create_session(user["id"])
    response = RedirectResponse(url=next_url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return response

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    email = form_data.get("email")
    password = form_data.get("password")
    confirm_password = form_data.get("confirm_password")
    
    if password != confirm_password:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Passwords don't match"
        })
    
    if db.get_user(username=username) or db.get_user(email=email):
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Username or email already exists"
        })
    
    user_id = db.create_user(username, email, password)
    session_id = db.create_session(user_id)
    
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return response

@app.get("/logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        db.delete_session(session_id)
    
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("session_id")
    return response

@app.get("/guest")
async def guest_login(request: Request):
    guest_id = f"guest_{uuid.uuid4()}"
    # Create guest user with is_guest flag
    db._execute_query("""
        CREATE (u:User {
            id: $user_id,
            username: $username,
            email: $email,
            password: 'guest',
            is_guest: true,
            created_at: datetime()
        })
    """, user_id=guest_id, username=f"Guest_{guest_id[:8]}", email=f"{guest_id}@example.com")
    
    session_id = db.create_session(guest_id)
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)