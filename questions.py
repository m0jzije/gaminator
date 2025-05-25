QUESTIONS = [
    # ———————— Genre & Gameplay Mechanics ————————
    {"text": "I'd rather hack-n-slash my way through hordes than think twice about it.", "tags": {"Hack and Slash": 1.0, "Action": 0.9, "Combat": 0.8}},
    {"text": "I want every button press to mean something in fast-paced chaos.", "tags": {"Fast Paced": 1.0, "Precision": 0.9, "Arcade": 0.8}},
    {"text": "I get a thrill out of sneaking past enemies like a ghost.", "tags": {"Stealth": 1.0, "Tactical": 0.9, "Infiltration": 0.8}},
    {"text": "I love building things from scratch and watching them grow.", "tags": {"Building": 1.0, "Sandbox": 0.9, "Crafting": 0.8}},
    {"text": "Exploring every nook and cranny of a world gives me joy.", "tags": {"Exploration": 1.0, "Open World": 0.9, "Adventure": 0.8}},
    {"text": "I enjoy managing complex systems like economies or colonies.", "tags": {"Management": 1.0, "Simulation": 0.9, "Strategy": 0.8}},
    {"text": "I live for turn-based tactical battles where every move counts.", "tags": {"Turn Based Strategy": 1.0, "Tactical": 0.9, "Chess": 0.8}},
    {"text": "I thrive in chaotic multiplayer deathmatches with friends.", "tags": {"Multiplayer": 1.0, "PvP": 0.9, "Competitive": 0.8}},
    {"text": "I want to fight aliens with a plasma cannon while floating in space.", "tags": {"Sci fi": 1.0, "Space": 0.9, "Shooter": 0.8}},
    {"text": "I enjoy deep character progression and skill trees.", "tags": {"RPG": 1.0, "Character Customization": 0.9, "Level Up": 0.8}},

    # ———————— Setting & Theme ————————
    {"text": "I’m obsessed with ancient magic and dragons ruling the land.", "tags": {"Fantasy": 1.0, "Magic": 0.9, "Medieval": 0.8}},
    {"text": "I want to explore post-apocalyptic wastelands alone with just a backpack.", "tags": {"Post apocalyptic": 1.0, "Survival": 0.9, "Horror": 0.8}},
    {"text": "Farming life in a cozy valley sounds perfect for me.", "tags": {"Farming Sim": 1.0, "Relaxing": 0.9, "Cozy": 0.8}},
    {"text": "I’d die for a game set during WWII with realistic military tactics.", "tags": {"Historical": 1.0, "World War II": 0.9, "Military": 0.8}},
    {"text": "I dream of exploring alien worlds with strange creatures and ruins.", "tags": {"Aliens": 1.0, "Space": 0.9, "Exploration": 0.8}},
    {"text": "I want to solve mysteries in a noir city full of secrets.", "tags": {"Noir": 1.0, "Mystery": 0.9, "Detective": 0.8}},
    {"text": "A steampunk city ruled by inventors and mad scientists? Yes please!", "tags": {"Steampunk": 1.0, "Sci fi": 0.9, "Immersive": 0.8}},
    {"text": "I'm all about pirate ships and treasure hunts across open seas.", "tags": {"Pirates": 1.0, "Naval": 0.9, "Adventure": 0.8}},
    {"text": "I want to build an empire from scratch in a fantasy realm.", "tags": {"Strategy": 1.0, "Empire Building": 0.9, "Fantasy": 0.8}},
    {"text": "I'm dying to explore a cursed castle filled with traps and ghosts.", "tags": {"Horror": 1.0, "Mystery": 0.9, "Exploration": 0.8}},

    # ———————— Narrative & Style ————————
    {"text": "Every choice I make should change the story forever.", "tags": {"Choices Matter": 1.0, "Multiple Endings": 0.9, "Story Rich": 0.8}},
    {"text": "I prefer stories told without dialogue—just pure vibes.", "tags": {"Atmospheric": 1.0, "Walking Simulator": 0.9, "Silent Protagonist": 0.8}},
    {"text": "I want to be emotionally crushed by a deeply personal story.", "tags": {"Emotional": 1.0, "Drama": 0.9, "Narrative": 0.8}},
    {"text": "Dark humor and absurd situations crack me up every time.", "tags": {"Funny": 1.0, "Dark Humor": 0.9, "Satire": 0.8}},
    {"text": "I need a strong protagonist who kicks butt and takes names.", "tags": {"Strong Characters": 1.0, "Female Protagonist": 0.9, "Hero Shooter": 0.8}},
    {"text": "I want cinematic cutscenes that feel like a movie.", "tags": {"Cinematic": 1.0, "FMV": 0.9, "Visual Novel": 0.8}},
    {"text": "Games that mess with time and memory really intrigue me.", "tags": {"Time Manipulation": 1.0, "Psychological": 0.9, "Mystery": 0.8}},
    {"text": "I love reading lore books and uncovering hidden backstories.", "tags": {"Lore Rich": 1.0, "Fantasy": 0.9, "Story Rich": 0.8}},
    {"text": "I want a game that makes me cry like a baby.", "tags": {"Emotional": 1.0, "Drama": 0.9, "Romance": 0.8}},
    {"text": "I prefer stories that let me imagine my own version of events.", "tags": {"Ambient": 1.0, "Atmospheric": 0.9, "Walking Simulator": 0.8}},

    # ———————— Visuals & Presentation ————————
    {"text": "I crave pixel art so good it hurts my eyes in the best way.", "tags": {"Pixel Graphics": 1.0, "Retro": 0.9, "Indie": 0.8}},
    {"text": "I want ultra-realistic graphics that blur the line between game and film.", "tags": {"Realistic": 1.0, "3D": 0.9, "Cinematic": 0.8}},
    {"text": "Hand-drawn visuals with vibrant colors are what dreams are made of.", "tags": {"Hand drawn": 1.0, "Artistic": 0.9, "Colorful": 0.8}},
    {"text": "I want a game that feels like playing inside a comic book.", "tags": {"Comic Book": 1.0, "Stylized": 0.9, "Superhero": 0.8}},
    {"text": "VR-only experiences that transport me to another dimension.", "tags": {"VR Only": 1.0, "Immersive": 0.9, "3D": 0.8}},
    {"text": "I’m down for anything that looks like it came straight out of the 80s.", "tags": {"1980s": 1.0, "Retro": 0.9, "Synthwave": 0.8}},
    {"text": "Isometric views and retro charm hit just right.", "tags": {"Isometric": 1.0, "Retro": 0.9, "Strategy": 0.8}},
    {"text": "I want everything to look like a beautiful oil painting.", "tags": {"Artistic": 1.0, "Stylized": 0.9, "Atmospheric": 0.8}},
    {"text": "Cartoony animation style with exaggerated expressions is my vibe.", "tags": {"Cartoony": 1.0, "Funny": 0.9, "Family Friendly": 0.8}},
    {"text": "I’m obsessed with games that use lighting and shadows masterfully.", "tags": {"Atmospheric": 1.0, "Psychological": 0.9, "Horror": 0.8}},

    # ———————— Price Sensitivity ————————
    {"text": "I'm willing to break the bank if it means getting the best experience.", "tags": {"Premium": 1.0, "AAA": 0.9, "Cinematic": 0.8}, "price_range": [40, 60]},
    {"text": "I'll pay a little extra for something that lasts 100+ hours.", "tags": {"Replay Value": 1.0, "Long": 0.9, "Singleplayer": 0.8}, "price_range": [20, 40]},
    {"text": "I only buy games under $15 unless they’re legendary.", "tags": {"Indie": 1.0, "Value": 0.9, "Short": 0.8}, "price_range": [0, 15]},
    {"text": "If it's free-to-play but fair, I'm all in.", "tags": {"Free to Play": 1.0, "Multiplayer": 0.9, "Mobile": 0.8}, "price_range": [0]},
    {"text": "I don't care about price as long as it's worth my time.", "tags": {"Worth It": 1.0, "Time Investment": 0.9, "Singleplayer": 0.8}},
    {"text": "I only buy games on sale or when they're dirt cheap.", "tags": {"Bargain Hunter": 1.0, "Indie": 0.9, "Early Access": 0.8}, "price_range": [0, 20]},
    {"text": "I’ll wait for a bundle before buying even a top-rated game.", "tags": {"Bundle Lover": 1.0, "Indie": 0.9, "Steam": 0.8}, "price_range": [0, 10]},
    {"text": "I’d spend more if it meant supporting indie devs directly.", "tags": {"Indie": 1.0, "Supportive": 0.9, "Crowdfunded": 0.8}, "price_range": [10, 30]},
    {"text": "I expect great value even if it’s super cheap.", "tags": {"Budget Game": 1.0, "Good Deal": 0.9, "Short": 0.8}, "price_range": [0, 10]},
    {"text": "Only premium AAA titles are worth paying full price for.", "tags": {"AAA": 1.0, "Cinematic": 0.9, "Graphics Focused": 0.8}, "price_range": [40, 60]},

    # ———————— Review Score & Popularity ————————
    {"text": "I only play games rated higher than 95% on Steam.", "tags": {"AAA": 1.0, "Cinematic": 0.9, "Popular": 0.8}, "review_score_range": [95, 100]},
    {"text": "I want a cult classic that not everyone knows about yet.", "tags": {"Cult Classic": 1.0, "Underground": 0.9, "Indie": 0.8}, "review_score_range": [70, 90]},
    {"text": "If it's got over 100k reviews, it must be worth trying.", "tags": {"Popular": 1.0, "Multiplayer": 0.9, "Massively Multiplayer": 0.8}, "review_score_range": [0, 100], "popularity_threshold": 100000},
    {"text": "I trust games with mixed reviews—they might surprise me.", "tags": {"Experimental": 1.0, "Unique": 0.9, "Risk Taker": 0.8}, "review_score_range": [50, 70]},
    {"text": "I avoid anything with a score below 80%, life’s too short.", "tags": {"Selective": 1.0, "High Standards": 0.9, "AAA": 0.8}, "review_score_range": [80, 100]},

    # ———————— Release Date Preference ————————
    {"text": "I only play modern games from the last 2 years.", "tags": {"Modern": 1.0, "Up To Date": 0.9, "New": 0.8}, "release_year_range": [2023, 2025]},
    {"text": "Give me classics from the 90s that aged like fine wine.", "tags": {"Classic": 1.0, "Nostalgia": 0.9, "Old School": 0.8}, "release_year_range": [1990, 1999]},
    {"text": "I want to try early access games and shape their future.", "tags": {"Early Access": 1.0, "Community Driven": 0.9, "Ongoing": 0.8}, "release_year_range": [2024, 2025]},
    {"text": "I don’t mind waiting for a sequel if the first was amazing.", "tags": {"Sequel": 1.0, "Loyal Fan": 0.9, "Series": 0.8}, "release_year_range": [2020, 2025]},
    {"text": "I want a fresh game that dropped this year.", "tags": {"New": 1.0, "Fresh": 0.9, "Trending": 0.8}, "release_year_range": [2025, 2025]}
]
