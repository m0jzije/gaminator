from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from neo4j import GraphDatabase
from contextlib import asynccontextmanager
from typing import Dict, List
import random

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Neo4j Connection Info
URI = "URI"
AUTH = ("username", "password")

# Question configuration
QUESTION_POOL = [
    {"type": "tag", "key": "singleplayer", "text": "Do you prefer singleplayer games?", "emoji": "👤"},
    {"type": "tag", "key": "multiplayer", "text": "Do you enjoy multiplayer experiences?", "emoji": "👥"},
    {"type": "tag", "key": "story_rich", "text": "Do you value a rich story?", "emoji": "📖"},
    {"type": "tag", "key": "action", "text": "Do you like action-packed gameplay?", "emoji": "💥"},
    {"type": "tag", "key": "relaxing", "text": "Do you prefer relaxing games?", "emoji": "😌"},
    {"type": "tag", "key": "challenging", "text": "Do you enjoy a good challenge?", "emoji": "🏆"},
    {"type": "tag", "key": "open_world", "text": "Do you like exploring open worlds?", "emoji": "🗺️"},
    {"type": "tag", "key": "puzzle", "text": "Do you enjoy solving puzzles?", "emoji": "🧩"},
    {"type": "tag", "key": "horror", "text": "Do you like horror games?", "emoji": "👻"},
    {"type": "tag", "key": "fantasy", "text": "Do you prefer fantasy settings?", "emoji": "🧙"},
    {"type": "tag", "key": "sci_fi", "text": "Do you like sci-fi themes?", "emoji": "🚀"},
    {"type": "tag", "key": "indie", "text": "Do you enjoy indie games?", "emoji": "🎨"},
]

# Function to run Cypher queries
def run_query(query: str, parameters: Dict = None) -> List[Dict]:
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

# Create FastAPI app
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/start")
async def start_game():
    return {"message": "Ready to recommend games!"}

@app.post("/get_question")
async def get_question():
    # Return a random question from the pool
    question = random.choice(QUESTION_POOL)
    return {"question": question}

@app.post("/get_recommendations")
async def get_recommendations(request: Request):
    data = await request.json()
    answers = data.get("answers", [])
    
    # Build query based on user answers
    query = """
    MATCH (g:Game)
    WHERE 1=1
    """
    
    params = {}
    must_conditions = []
    should_conditions = []
    
    for idx, answer in enumerate(answers):
        if answer["type"] == "tag":
            if answer["value"] == "yes":
                must_conditions.append(f"(g)-[:HAS_TAG]->(:Tag {{name: '{answer['key'].replace('_', ' ').title()}'}})")
            elif answer["value"] == "no":
                must_conditions.append(f"NOT (g)-[:HAS_TAG]->(:Tag {{name: '{answer['key'].replace('_', ' ').title()}'}})")
    
    if must_conditions:
        query += " AND " + " AND ".join(must_conditions)
    
    query += """
    OPTIONAL MATCH (g)-[:HAS_TAG]->(t)
    WITH g, count(t) AS match_score
    RETURN g.name AS name, g.steam_link AS steam_link, match_score
    ORDER BY match_score DESC, g.popularity DESC
    LIMIT 5
    """
    
    result = run_query(query, params)
    
    recommendations = []
    for game in result:
        steam_id = game["steam_link"].split("/")[-1] if game["steam_link"] else None
        cover_url = f"https://cdn.akamai.steamstatic.com/steam/apps/{steam_id}/header.jpg" if steam_id else None
        
        recommendations.append({
            "name": game["name"],
            "cover_url": cover_url,
            "match_score": game["match_score"]
        })
    
    # If no matches, return popular games
    if not recommendations:
        result = run_query("""
        MATCH (g:Game)
        RETURN g.name AS name, g.steam_link AS steam_link
        ORDER BY g.popularity DESC
        LIMIT 5
        """)
        
        for game in result:
            steam_id = game["steam_link"].split("/")[-1] if game["steam_link"] else None
            cover_url = f"https://cdn.akamai.steamstatic.com/steam/apps/{steam_id}/header.jpg" if steam_id else None
            
            recommendations.append({
                "name": game["name"],
                "cover_url": cover_url,
                "match_score": 0,
                "is_fallback": True
            })
    
    return {"recommendations": recommendations}