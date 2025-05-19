# scripts/tag_splitter.py

import csv
import ast

INPUT_FILE = '../data/export.csv'
GAMES_OUTPUT = '../data/games.csv'
TAGS_OUTPUT = '../data/game_tags.csv'

with open(INPUT_FILE, 'r', encoding='utf-8') as infile, \
     open(GAMES_OUTPUT, 'w', newline='', encoding='utf-8') as gfile, \
     open(TAGS_OUTPUT, 'w', newline='', encoding='utf-8') as tfile:

    reader = csv.reader(infile)
    games_writer = csv.writer(gfile)
    tags_writer = csv.writer(tfile)

    # Write headers
    games_writer.writerow(['id', 'name', 'url'])
    tags_writer.writerow(['game_id', 'tag'])

    next(reader)  # Skip header row if exists
    for row in reader:
        if len(row) < 8:
            continue  # skip malformed rows

        game_id = row[0]
        name = row[1]
        url = row[7]

        try:
            tags = ast.literal_eval(row[6])  # safely parse list string
        except (SyntaxError, ValueError):
            tags = []

        games_writer.writerow([game_id, name, url])
        for tag in tags:
            tags_writer.writerow([game_id, tag.strip()])