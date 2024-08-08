import json

import argparse
from pathlib import Path
import pytz
from entry import Entry
  
parser = argparse.ArgumentParser()

parser.add_argument("--analyzer", 
                    "-a",
                    action="store", 
                    choices=["sleep"],
                    nargs="*"
)

parser.add_argument("--file", 
                    "-f",
                    action="store", 
                    default="journal.json", 
                    help="Filename or path to the Day One journal .json file",
                    nargs="?"
)

parser.add_argument("--timezone", 
                    "-tz",
                    action="store", 
                    default="America/New_York",
                    nargs="?"
)


args = parser.parse_args()

args.timezone = args.timezone.replace('\\/', '/')
target_file = Path(args.file)

if not target_file.exists():
    print("The target file doesn't exist")
    raise SystemExit(1)

with open(target_file, 'r', errors="ignore") as f:
    print('Loading journal contents...')
    file = json.load(f)
    
journal = file['entries']

entries = []
for entry in journal:
    entries.append(Entry(entry))
    
print('Entries loaded.')