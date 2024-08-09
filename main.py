import json
import argparse
from pathlib import Path
from analyzer import Analyzer
from entry import Entry
from journal import Journal

parser = argparse.ArgumentParser()

parser.add_argument(
    "--analyzer", 
    "-a",
    action="store", 
    choices=["completed", "created", "filter"],
    nargs="*"
)

parser.add_argument(
    "--file", 
    "-f",
    action="store", 
    default="journal.json", 
    help="Filename or path to the Day One journal .json file",
    nargs="?"
)

args = parser.parse_args()

# check target file existence
target_file = Path(args.file)
if not target_file.exists():
    print("The target file doesn't exist")
    raise SystemExit(1)

# load json file contents
with open(target_file, 'r', errors="ignore") as f:
    print('Loading journal contents...')
    file = json.load(f)
    
journal = file['entries']
entries = [Entry(entry) for entry in journal]
journal = Journal(entries)

a = Analyzer(journal, args.analyzer)
a.analyze()