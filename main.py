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
URI = "neo4j+s://c14f5bac.databases.neo4j.io"
AUTH = ("neo4j", "VX0KIEY0nrvKihZ4T_pQJPXnbjY_sjtZc8Q3OwHR2uY")


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
    {"type": "numeric", "key": "playtime", "text": "Do you prefer short (<10h) or long games?", "emoji": "⏱️"},
    {"type": "genre", "key": "atmosphere", "text": "Do you prefer dark or lighthearted games?", "emoji": "🎭"}
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

def process_results(results):
    recommendations = []
    for game in results:
        steam_id = game["steam_link"].split("/")[-1] if game.get("steam_link") else None
        cover_url = f"https://cdn.akamai.steamstatic.com/steam/apps/{steam_id}/header.jpg" if steam_id else None
        
        recommendations.append({
            "name": game["name"],
            "steam_link": game.get("steam_link"),
            "cover_url": cover_url,
            "match_score": game.get("match_score", 0)  # Added match_score if available
        })
    return recommendations

@app.post("/get_question")
async def get_question(request: Request):
    data = await request.json()
    answered_questions = [q["key"] for q in data.get("answers", [])]
    
    # Filter out already-asked questions
    available_questions = [
        q for q in QUESTION_POOL 
        if q["key"] not in answered_questions
    ]
    
    if not available_questions:
        return {"question": None}  # End if no questions left
    
    # Prioritize questions that best split remaining candidates
    if data.get("candidates"):
        question = find_optimal_question(available_questions, data["candidates"])
    else:
        question = random.choice(available_questions)
    
    return {"question": question}

def find_optimal_question(questions, candidate_ids):
    # Find the question that most evenly splits remaining games
    best_question = None
    best_score = -1
    
    for question in questions:
        if question["type"] == "tag":
            tag = question["key"].replace("_", " ").title()
            result = run_query("""
                MATCH (g:Game)-[:HAS_TAG]->(:Tag {name: $tag})
                WHERE g.id IN $candidates
                RETURN count(g) AS count
                """, {"tag": tag, "candidates": candidate_ids})
            
            yes_count = result[0]["count"] if result else 0
            split_ratio = abs(yes_count / len(candidate_ids) - 0.5)
            
            if split_ratio > best_score:
                best_score = split_ratio
                best_question = question
    
    return best_question or random.choice(questions)

@app.post("/get_recommendations")
async def get_recommendations(request: Request):
    data = await request.json()
    answers = data.get("answers", [])
    
    # Base query
    query = """
    MATCH (g:Game)
    WHERE 1=1
    """
    
    # Apply tag filters
    for answer in answers:
        if answer["type"] == "tag" and answer["value"] == "yes":
            tag = answer["key"].replace("_", " ").title()
            query += f"\nAND (g)-[:HAS_TAG]->(:Tag {{name: '{tag}'}})"
    
    # Add diversity with randomness and popularity
    query += """
    WITH g, rand() AS r
    ORDER BY g.popularity DESC, r
    LIMIT 20
    RETURN g.name AS name, g.steam_link AS steam_link
    """
    
    results = run_query(query)
    return {"recommendations": process_results(results)}
    
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