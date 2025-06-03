import base64
from neo4j import GraphDatabase

# Helper function to simulate image base64 encoding
def get_dummy_base64(image_name):
    return base64.b64encode(f"{image_name} fake image data".encode()).decode()

class ArchetypeMigrator:
    def __init__(self, driver):
        self.driver = driver

    def migrate_archetypes(self):
        archetypes = [
            {
                "name": "The Roleplayer",
                "description": "You love deep stories and character progression",
                "image_base64": get_dummy_base64("roleplayer.png"),
                "traits": [
                    {
                        "name": "Story-driven",
                        "description": "Prefers narrative-rich experiences",
                        "preferences": [
                            {"name": "Story Rich", "weight": 1.0},
                            {"name": "Choices Matter", "weight": 0.9},
                            {"name": "Character Customization", "weight": 0.8}
                        ]
                    },
                    {
                        "name": "Character-focused",
                        "description": "Enjoys developing character abilities",
                        "preferences": [
                            {"name": "RPG", "weight": 1.0},
                            {"name": "Skill Trees", "weight": 0.9},
                            {"name": "Dialogue Heavy", "weight": 0.7}
                        ]
                    }
                ]
            },
            {
                "name": "The Competitor",
                "description": "You thrive on challenge and player vs player combat",
                "image_base64": get_dummy_base64("competitor.png"),
                "traits": [
                    {
                        "name": "Skilled",
                        "description": "Enjoys mastering game mechanics",
                        "preferences": [
                            {"name": "Competitive", "weight": 1.0},
                            {"name": "PvP", "weight": 0.9},
                            {"name": "Precision", "weight": 0.8}
                        ]
                    }
                ]
            },
            {
                "name": "The Explorer",
                "description": "You seek vast worlds and hidden secrets",
                "image_base64": get_dummy_base64("explorer.png"),
                "traits": [
                    {
                        "name": "Curious",
                        "description": "Loves discovering new areas",
                        "preferences": [
                            {"name": "Open World", "weight": 1.0},
                            {"name": "Exploration", "weight": 0.9},
                            {"name": "Collectibles", "weight": 0.7}
                        ]
                    }
                ]
            },
            {
                "name": "The Strategist",
                "description": "You excel at planning and outsmarting opponents",
                "image_base64": get_dummy_base64("strategist.png"),
                "traits": [
                    {
                        "name": "Tactical",
                        "description": "Enjoys strategy and decision-making",
                        "preferences": [
                            {"name": "Turn-Based", "weight": 1.0},
                            {"name": "RTS", "weight": 0.9},
                            {"name": "Base Building", "weight": 0.8}
                        ]
                    }
                ]
            },
            {
                "name": "The Casual Gamer",
                "description": "You enjoy relaxing and stress-free gameplay",
                "image_base64": get_dummy_base64("casual.png"),
                "traits": [
                    {
                        "name": "Relaxed",
                        "description": "Prefers simple and peaceful games",
                        "preferences": [
                            {"name": "Casual", "weight": 1.0},
                            {"name": "Puzzle", "weight": 0.8},
                            {"name": "Simulation", "weight": 0.7}
                        ]
                    }
                ]
            }
        ]

        with self.driver.session() as session:
            # Clear existing nodes
            session.run("MATCH (a:Archetype) DETACH DELETE a")
            session.run("MATCH (t:Trait) DETACH DELETE t")
            session.run("MATCH (gp:GamePreference) DETACH DELETE gp")

            for archetype in archetypes:
                # Create Archetype with base64 image
                session.run("""
                    CREATE (a:Archetype {
                        name: $name,
                        description: $desc,
                        image_base64: $image_base64
                    })
                """, name=archetype["name"], desc=archetype["description"], image_base64=archetype["image_base64"])

                for trait in archetype["traits"]:
                    # Create Trait node and link to Archetype
                    session.run("""
                        MATCH (a:Archetype {name: $archetype_name})
                        MERGE (t:Trait {name: $trait_name})
                        ON CREATE SET t.description = $trait_desc
                        CREATE (a)-[:HAS_TRAIT]->(t)
                    """, archetype_name=archetype["name"],
                         trait_name=trait["name"],
                         trait_desc=trait["description"])

                    for pref in trait["preferences"]:
                        # Create GamePreference and relationships
                        session.run("""
                            MATCH (t:Trait {name: $trait_name})
                            MERGE (gp:GamePreference {name: $pref_name})
                            ON CREATE SET gp.weight = $weight
                            CREATE (t)-[:AFFECTS]->(gp)

                            MERGE (tag:Tag {name: $pref_name})
                            CREATE (gp)-[:MAPS_TO]->(tag)
                        """, trait_name=trait["name"],
                             pref_name=pref["name"],
                             weight=pref["weight"])


if __name__ == "__main__":
    uri = "neo4j+s://c14f5bac.databases.neo4j.io"
    user = "neo4j"
    password = "VX0KIEY0nrvKihZ4T_pQJPXnbjY_sjtZc8Q3OwHR2uY"  # Replace with your actual Neo4j password
    driver = GraphDatabase.driver(uri, auth=(user, password))

    migrator = ArchetypeMigrator(driver)
    migrator.migrate_archetypes()
    driver.close()

    print("✅ Archetypes migrated successfully.")
