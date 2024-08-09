from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
# from entry import Entry
from journal import Journal

SUCCESS_CODE = 1
NO_MATCH_CODE = -1

FILTER_MODES = {
    'starred',
    'pinned',
    'country',
    'admin_area',
    'locality',
    'placename',
    'tags',
    'keyword'
}

class Analyzer():
    def __init__(self, journal: Journal, mode: list[str]):
        self.mode = mode
        self.journal = journal
        self.entries = journal.get_entries()
        print('Entries loaded.')
    
    def analyze(self):
        if 'filter' in self.mode:
            self.filter()
        if 'completed' in self.mode:
            print('Analyzing entry completion data...')
            self.time_graph()
        if 'created' in self.mode:
            print('Analyzing entry creation data...')
            self.time_graph()
            
    def filter(self):
        in_loop = True
        neg_filter = False
        overwrite = False
        filter_mode = 'placename' # 'keyword'
        count = self.journal.get_entry_count()
        while in_loop:
            print('Current settings:\t')
            print(f'- Negative filter: {neg_filter}\t')
            print(f'- Overwrite with results: {overwrite}\t')
            print(f'- Filter mode: {filter_mode}\n\t')
            opt = input('Change settings: s | Apply filter: a | Quit: q\n\t> ')
            match (opt):
                case 's':
                    c = input('Negative filter: n | Overwrite with results: o | Filter mode: t\n\t> ')
                    match (c):
                        case 'n':
                            neg_filter != neg_filter
                        case 'o':
                            overwrite != overwrite
                        case 'f':
                            print('Select filter mode from:')
                            [print(f'\t- {fmode}') for fmode in FILTER_MODES]
                            fm = input('\n\t> ')
                            if fm not in FILTER_MODES:
                                print(f'Invalid option: {fm}')
                            else:
                                filter_mode = fm
                        case _:
                            print(f'Invalid option: {c}')
                            
                    continue
                
                case 'a':
                    res = None
                    match(filter_mode):
                        case 'starred':
                            opt = input('Select starred entries? y/n\n\t> ')
                            print('')
                            s = True if opt == 'y' else False if opt == 'n' else None
                            if neg_filter is None:
                                continue
                            res = self.journal.filter_starred(s, overwrite)
                            
                        case 'pinned':
                            opt = input('Select pinned entries? y/n\n\t> ')
                            print('')
                            s = True if opt == 'y' else False if opt == 'n' else None
                            if neg_filter is None:
                                continue
                            res = self.journal.filter_pinned(s, overwrite)
                            
                        case 'country':
                            opt = input('Enter country to select:\n\t> ')
                            print('')
                            res = self.journal.filter_by_country(opt.strip(), neg_filter, overwrite)
                            
                        case 'admin_area':
                            opt = input('Enter administrative area (state) to select:\n\t> ')
                            print('')
                            res = self.journal.filter_by_admin_area(opt, neg_filter, overwrite)
                            
                        case 'locality':
                            opt = input('Enter locality (city/town) to select:\n\t> ')
                            print('')
                            res = self.journal.filter_by_locality(opt, neg_filter, overwrite)
                            
                        case 'placename':
                            opt = input('Enter place-name (address) to select:\n\t> ')
                            print('')
                            res = self.journal.filter_by_placename(opt, neg_filter, overwrite)
                        
                        case 'tags':
                            opt = input('Enter tags (space-separated) to select:\n\t> ')
                            print('')
                            res = self.journal.filter_by_tags(' '.split(opt), neg_filter, overwrite)
                        
                        case 'keyword':
                            opt = input('Enter keyword to select: (case sensitive)\n\t> ')
                            print('')
                            res = self.journal.filter_by_keyword(opt, neg_filter, overwrite)
                        
                        case _:
                            print(f'\n! Invalid filter option: {filter_mode}\n')
                            continue
                        
                    if res['code'] == NO_MATCH_CODE:
                        print(f'\n# {res["msg"]} #\n')
                    
                    if res['code'] == SUCCESS_CODE:
                        print(f'\n# {res["count"]} of {count} entries found that match filter #\n')
                    
                    count = self.journal.get_entry_count()
                    if overwrite:
                        print(f'New entry count: {count}\n')
                        
                case 'q':
                    in_loop = False
                    continue
                    
                case _:
                    print(f'Invalid option: {opt}')
                    continue
            
            
            
        print('Exiting...')
        
    def time_graph(self):
        if 'completed' in self.mode:
            etimes = [entry.get_completed_time() for entry in self.entries]
        elif 'created' in self.mode:
            etimes = [entry.get_created_time() for entry in self.entries]
        
        # Extract dates and times
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
            plt.scatter(
                data['dates'], 
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