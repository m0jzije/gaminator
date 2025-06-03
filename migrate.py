from neo4j import GraphDatabase
from datetime import datetime
import uuid

QUESTIONS = [
  {"text": "I want a game that keeps me guessing with unpredictable twists.", "tags": {"Narrative": 1.0, "Mystery": 0.9, "Psychological": 0.8}},
  {"text": "Games where I can shape the world through my choices excite me.", "tags": {"Choices Matter": 1.0, "Replay Value": 0.9, "Open World": 0.8}},
  {"text": "I enjoy games that challenge my reflexes with precise platforming.", "tags": {"Precision Platformer": 1.0, "Skill Trees": 0.9, "Fast Paced": 0.8}},
  {"text": "I love managing a team of unique characters with backstories.", "tags": {"Party Based RPG": 1.0, "Character Customization": 0.9, "Tactical": 0.8}},
  {"text": "Games set in space colonies make me feel like a pioneer.", "tags": {"Sci fi": 1.0, "Space": 0.9, "Exploration": 0.8}},
  {"text": "I want to survive harsh environments by crafting everything myself.", "tags": {"Survival": 1.0, "Crafting": 0.9, "Building": 0.8}},
  {"text": "I’m all about brutal melee combat that rewards skill over luck.", "tags": {"Action": 1.0, "Combat": 0.9, "Difficult": 0.8}},
  {"text": "Games with deep lore hidden in books and ruins keep me hooked.", "tags": {"Lore Rich": 1.0, "Exploration": 0.9, "Story Rich": 0.8}},
  {"text": "I want to explore ancient temples filled with deadly traps.", "tags": {"Adventure": 1.0, "Puzzle": 0.9, "Exploration": 0.8}},
  {"text": "I thrive in games that force tough moral decisions.", "tags": {"Choices Matter": 1.0, "Narrative": 0.9, "Drama": 0.8}},
  {"text": "Games that let me build massive armies and conquer lands thrill me.", "tags": {"Strategy": 1.0, "Empire Building": 0.9, "Historical": 0.8}},
  {"text": "I love games where every character feels truly alive and unique.", "tags": {"Strong Characters": 1.0, "Story Rich": 0.9, "Dialogue Heavy": 0.8}},
  {"text": "I want a game that makes me laugh out loud with absurd humor.", "tags": {"Comedy": 1.0, "Funny": 0.9, "Satire": 0.8}},
  {"text": "Games that simulate real-world physics keep me engaged.", "tags": {"Simulation": 1.0, "Physics": 0.9, "Realistic": 0.8}},
  {"text": "I enjoy games that combine rhythm mechanics with fast action.", "tags": {"Rhythm": 1.0, "Arcade": 0.9, "Fast Paced": 0.8}},
  {"text": "I prefer games with hand-crafted levels instead of random generation.", "tags": {"Hand drawn": 1.0, "Artistic": 0.9, "Precision": 0.8}},
  {"text": "Games that blend horror with mystery give me chills.", "tags": {"Horror": 1.0, "Mystery": 0.9, "Psychological Horror": 0.8}},
  {"text": "I want to command massive battles on land, sea, and air.", "tags": {"War": 1.0, "Military": 0.9, "Strategy": 0.8}},
  {"text": "Games that teach real-life skills while being fun? Yes please!", "tags": {"Education": 1.0, "Simulation": 0.9, "Useful": 0.8}},
  {"text": "I love discovering secret paths and hidden areas in games.", "tags": {"Exploration": 1.0, "Metroidvania": 0.9, "Mystery": 0.8}},
  {"text": "I want to pilot mech suits and destroy entire cities.", "tags": {"Mechs": 1.0, "Action": 0.9, "Sci fi": 0.8}},
  {"text": "Games with voice narration guide me through unforgettable stories.", "tags": {"Narration": 1.0, "Story Rich": 0.9, "Atmospheric": 0.8}},
  {"text": "I enjoy building and defending strongholds against waves of enemies.", "tags": {"Tower Defense": 1.0, "Building": 0.9, "Strategy": 0.8}},
  {"text": "Games that use time travel as a core mechanic fascinate me.", "tags": {"Time Travel": 1.0, "Puzzle": 0.9, "Narrative": 0.8}},
  {"text": "I want games that reward exploration with meaningful secrets.", "tags": {"Exploration": 1.0, "Collectibles": 0.9, "Replay Value": 0.8}},
  {"text": "I love games that let me live someone else's life for a while.", "tags": {"Life Sim": 1.0, "Simulation": 0.9, "Immersive": 0.8}},
  {"text": "Games that combine cooking with chaos sound amazing.", "tags": {"Cooking": 1.0, "Casual": 0.9, "Funny": 0.8}},
  {"text": "I want to explore alien worlds teeming with strange lifeforms.", "tags": {"Sci fi": 1.0, "Exploration": 0.9, "Aliens": 0.8}},
  {"text": "Games that require teamwork and coordination bring me joy.", "tags": {"Multiplayer": 1.0, "Team Based": 0.9, "Co op": 0.8}},
  {"text": "I love games that mix genres in unexpected ways.", "tags": {"Experimental": 1.0, "Unique": 0.9, "Innovative": 0.8}},
  {"text": "Games with branching storylines based on morality appeal to me.", "tags": {"Choices Matter": 1.0, "Multiple Endings": 0.9, "Narrative": 0.8}},
  {"text": "I want games that surprise me with clever level design.", "tags": {"Design": 1.0, "Exploration": 0.9, "Creative": 0.8}},
  {"text": "I enjoy playing games with procedurally generated content.", "tags": {"Procedural Generation": 1.0, "Replay Value": 0.9, "Roguelike": 0.8}, "price_range": [0, 30]},
  {"text": "I only play games that support modding communities.", "tags": {"Moddable": 1.0, "Indie": 0.9, "Community Driven": 0.8}, "price_range": [0, 20]},
  {"text": "I'm willing to pay extra for games with full controller support.", "tags": {"Controller": 1.0, "AAA": 0.9, "Comfortable": 0.8}, "price_range": [20, 50]},
  {"text": "I avoid anything without a demo or free trial.", "tags": {"Selective": 1.0, "Bargain Hunter": 0.9, "Risk Taker": 0.7}, "price_range": [0, 40]},
  {"text": "I only buy games if they're on my wishlist for over a month.", "tags": {"Worth It": 1.0, "Selective": 0.9, "Budget Game": 0.8}, "price_range": [0, 30]},
  {"text": "I'll pay more if it means getting early access and shaping the game.", "tags": {"Early Access": 1.0, "Community Driven": 0.9, "Supportive": 0.8}, "price_range": [10, 40]},
  {"text": "I prefer games with high review scores even if they cost more.", "tags": {"Popular": 1.0, "AAA": 0.9, "High Standards": 0.8}, "review_score_range": [85, 100]},
  {"text": "I only trust games with over 50,000 positive reviews.", "tags": {"Popular": 1.0, "Verified": 0.9, "Selective": 0.8}, "popularity_threshold": 50000},
  {"text": "If a game has a score below 70%, I skip it immediately.", "tags": {"High Standards": 1.0, "Selective": 0.9, "Discerning": 0.8}, "review_score_range": [70, 100]},
  {"text": "I only play games released in the last five years.", "tags": {"Up To Date": 1.0, "Modern": 0.9, "New": 0.8}, "release_year_range": [2020, 2025]},
  {"text": "I love retro games from the early 2000s with pixel art charm.", "tags": {"Retro": 1.0, "Pixel Graphics": 0.9, "Nostalgia": 0.8}, "release_year_range": [2000, 2005]},
  {"text": "I want games that push graphical boundaries with ray tracing.", "tags": {"Graphics Focused": 1.0, "AAA": 0.9, "Visuals": 0.8}, "price_range": [40, 60]},
  {"text": "I enjoy indie darlings that fly under most people’s radar.", "tags": {"Indie": 1.0, "Cult Classic": 0.9, "Unique": 0.8}, "price_range": [0, 20]},
  {"text": "I only try games that have at least 10,000 reviews.", "tags": {"Popular": 1.0, "Trusted": 0.9, "Selective": 0.8}, "popularity_threshold": 10000},
  {"text": "I stick to games that are updated regularly post-launch.", "tags": {"Ongoing": 1.0, "Supportive": 0.9, "Quality Assurance": 0.8}, "release_year_range": [2020, 2025]},
  {"text": "I want games that are part of an established series I already love.", "tags": {"Series": 1.0, "Loyal Fan": 0.9, "Sequel": 0.8}, "release_year_range": [2020, 2025]},
  {"text": "I only buy games that come with a roadmap and future updates.", "tags": {"Early Access": 1.0, "Roadmap": 0.9, "Transparency": 0.8}, "price_range": [20, 40]},
  {"text": "I look for games that trend highly on social media platforms.", "tags": {"Trending": 1.0, "Community Driven": 0.9, "Fresh": 0.8}, "release_year_range": [2024, 2025]},
  {"text": "I prefer games that don’t change much from their original release.", "tags": {"Classic": 1.0, "Old School": 0.9, "Conservative": 0.8}, "release_year_range": [2000, 2010]},
  {"text": "I only play games that are actively supported by developers.", "tags": {"Ongoing": 1.0, "Supportive": 0.9, "Community Friendly": 0.8}, "release_year_range": [2020, 2025]},
  {"text": "I value games that offer lifetime updates and no microtransactions.", "tags": {"Value": 1.0, "Premium": 0.9, "No Ads": 0.8}, "price_range": [20, 50]},
  {"text": "I avoid anything that doesn't support mods or user content.", "tags": {"Moddable": 1.0, "Indie": 0.9, "Customizable": 0.8}, "price_range": [0, 30]},
  {"text": "I only consider games with active developer blogs or devlogs.", "tags": {"Community Driven": 1.0, "Transparency": 0.9, "Trustworthy": 0.8}, "release_year_range": [2020, 2025]},
  {"text": "I want games that introduce new mechanics with each update.", "tags": {"Evolving": 1.0, "Innovative": 0.9, "Dynamic": 0.8}, "release_year_range": [2022, 2025]},
  {"text": "I only play games that have clear refund policies.", "tags": {"Risk Taker": 1.0, "Selective": 0.9, "Steam": 0.8}, "price_range": [0, 40]},
  {"text": "I look for games that integrate well with streaming services.", "tags": {"Streaming": 1.0, "Social": 0.9, "Online": 0.8}, "price_range": [0, 30]},
  {"text": "I prefer games that work offline without constant internet checks.", "tags": {"Offline": 1.0, "Singleplayer": 0.9, "Privacy": 0.8}, "price_range": [0, 50]},
  {"text": "I want games that respect my time with no unnecessary grinding.", "tags": {"Time Efficient": 1.0, "Respectful": 0.9, "Balanced": 0.8}, "price_range": [0, 40]},
  {"text": "I only buy games with robust accessibility options.", "tags": {"Accessibility": 1.0, "Inclusive": 0.9, "Supportive": 0.8}, "price_range": [0, 60]},
  {"text": "I value games that support multiple languages and subtitles.", "tags": {"Multilingual": 1.0, "Global": 0.9, "Inclusive": 0.8}, "price_range": [0, 50]},
  {"text": "I avoid games that rely heavily on loot boxes or gacha systems.", "tags": {"Anti Microtransaction": 1.0, "Ethical": 0.9, "Selective": 0.8}, "price_range": [0, 30]}
]
class Neo4jMigrator:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "neo4j+s://c14f5bac.databases.neo4j.io",
            auth=("neo4j", "VX0KIEY0nrvKihZ4T_pQJPXnbjY_sjtZc8Q3OwHR2uY")
        )
    
    def migrate_questions(self):
        with self.driver.session() as session:
            # Clear existing questions (optional - only for fresh imports)
            session.run("MATCH (q:Question) DETACH DELETE q")
            
            # Create constraints for uniqueness
            session.run("CREATE CONSTRAINT unique_question_id IF NOT EXISTS FOR (q:Question) REQUIRE q.id IS UNIQUE")
            session.run("CREATE CONSTRAINT unique_tag_name IF NOT EXISTS FOR (t:Tag) REQUIRE t.name IS UNIQUE")
            
            # Import each question
            for i, question in enumerate(QUESTIONS):
                question_id = str(uuid.uuid4())
                
                # Create the question node
                session.run("""
                    CREATE (q:Question {
                        id: $id,
                        text: $text,
                        index: $index,
                        created_at: datetime()
                    })
                """, id=question_id, text=question["text"], index=i)
                
                # Add any special filter properties
                if "price_range" in question:
                    session.run("""
                        MATCH (q:Question {id: $id})
                        SET q.price_range = $price_range
                    """, id=question_id, price_range=question["price_range"])
                
                if "review_score_range" in question:
                    session.run("""
                        MATCH (q:Question {id: $id})
                        SET q.review_score_range = $review_score_range
                    """, id=question_id, review_score_range=question["review_score_range"])
                
                if "popularity_threshold" in question:
                    session.run("""
                        MATCH (q:Question {id: $id})
                        SET q.popularity_threshold = $popularity_threshold
                    """, id=question_id, popularity_threshold=question["popularity_threshold"])
                
                if "release_year_range" in question:
                    session.run("""
                        MATCH (q:Question {id: $id})
                        SET q.release_year_range = $release_year_range
                    """, id=question_id, release_year_range=question["release_year_range"])
                
                # Create tags and relationships
                for tag_name, weight in question["tags"].items():
                    session.run("""
                        MERGE (t:Tag {name: $tag_name})
                        WITH t
                        MATCH (q:Question {id: $id})
                        CREATE (q)-[r:HAS_TAG {weight: $weight}]->(t)
                    """, id=question_id, tag_name=tag_name, weight=weight)
            
            print(f"Successfully migrated {len(QUESTIONS)} questions to Neo4j")

if __name__ == "__main__":
    migrator = Neo4jMigrator()
    migrator.migrate_questions()