# Game Recommender

A personalized game recommendation system that suggests games based on user preferences. Built using Neo4j and FastAPI, this project provides intelligent, data-driven recommendations through an interactive and modern interface.

## Overview

This system was developed as part of a group project for the **Database Systems (DB)** course at **International University of Sarajevo (IUS)**. The goal was to create a functional application that leverages graph database technology to provide meaningful game recommendations to users.

---

## Features

- **Smart Question-Based Recommendation Engine**  
  Users answer a series of questions about their gaming preferences, and the system intelligently recommends suitable games.

- **Modern, Responsive User Interface with Interactive Game Cards**  
  A clean and visually appealing UI that presents game suggestions in a card layout, optimized for various screen sizes.

- **Match Percentage Scoring**  
  Each recommended game is accompanied by a match percentage, giving users transparency into how well the suggestion aligns with their preferences.

- **Multiple Fallback Mechanisms**  
  Ensures that the system always returns relevant results, even when user input is limited or ambiguous.

- **High Performance with Neo4j Graph Queries**  
  Utilizes the power of Neo4j's graph querying capabilities to deliver fast and efficient recommendations.

---

## Technology Stack

- **Backend**: Python with FastAPI
- **Database**: Neo4j (Graph Database)
- **Frontend**: HTML5, CSS3, JavaScript
- **Hosting**: Render (or alternative hosting platforms)

---

## Prerequisites

Before setting up the project, ensure you have the following:

- Python 3.9 or newer
- Neo4j Aura DB account (a free tier is available)
- Node.js (optional, for frontend build tasks if extended)

---

## Installation Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/game-recommender.git
cd game-recommender
```

### 2. Set Up the Python Environment

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
.\venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

### 3. Configure Neo4j Connection

Sign up for a free Neo4j Aura DB instance and update your connection details in the `.env` file:

```env
NEO4J_URI=neo4j+s://your-database-id.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
```

### 4. Import Game Data

Run the import script to populate your Neo4j database with game data:

```bash
python scripts/import_data.py
```

---

## Conclusion

This project demonstrates how graph databases can be effectively used for recommendation systems. As a team effort for the DB course at IUS, it showcases practical applications of database theory and modern web development techniques in a real-world context.