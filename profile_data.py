import json

with open('thedump.json') as f:
    the_data = json.load(f)

print ([a for a in the_data])