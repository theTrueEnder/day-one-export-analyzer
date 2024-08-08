import json
import argparse
from pathlib import Path
from entry import Entry
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument(
    "--analyzer", 
    "-a",
    action="store", 
    choices=["completed", "created"],
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
print('Entries loaded.')

# generate completed or created time graphs
if 'completed' or 'created' in args.analyzer:
    if 'completed' in args.analyzer:
        print('Analyzing entry completion data...')
        etimes = [entry.get_completed_time() for entry in entries]
    elif 'created' in args.analyzer:
        print('Analyzing entry creation data...')
        etimes = [entry.get_created_time() for entry in entries]
    
    # Extract dates and times
    dates = [dt.date() for dt in etimes]
    times = [dt.time() for dt in etimes]

    # Convert times to a format suitable for plotting
    times_in_seconds = [t.hour * 3600 + t.minute * 60 + t.second for t in times]

    
    # Group data by year
    data_by_year = {}
    for dt, t in zip(etimes, times_in_seconds):
        year = dt.year
        if year not in data_by_year:
            data_by_year[year] = {'dates': [], 'times': []}
        date_within_year = datetime(2020, dt.month, dt.day).date()
        data_by_year[year]['dates'].append(date_within_year)
        data_by_year[year]['times'].append(t)

    print('Generating plot...')
    plt.figure(figsize=(10, 6))
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']
    for i, (year, data) in enumerate(data_by_year.items()):
        plt.scatter(data['dates'], 
                    data['times'], 
                    alpha=0.5, 
                    color=colors[i % len(colors)], 
                    label=str(year),
                    linewidth=0,
                    s=20,
                    )

    # format x axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14))
    
    # there's probably a reason why these numbers are the way they are (most likely string values) but these specific numbers make it 01-02 to 12-31 on the graph
    plt.xlim(18_256,18_628)
    
    # format y axis
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x//3600):02}:{int((x%3600)//60):02}:{int(x%60):02}"))

    # controls number of ticks on y axis
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    
    # added an extra thousand seconds to not cut off the circles of points at the top
    plt.ylim(0, 87_400)
    
    plt.xlabel('Date (year-agnostic)')
    plt.ylabel('Time of Day')
    plt.title('Journal Entry Times: Date vs Time of Day')
    plt.xticks(rotation=55)
    plt.legend()
    plt.tight_layout()

    plt.show()