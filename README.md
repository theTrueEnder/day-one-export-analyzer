# Day One Export Analyzer
*A tool to examine statistics and trends of metadata for exports of the [Day One](https://dayoneapp.com/) journaling app.*

This tool was created entirely for fun and for my own benefit, primarily to see a graph of when I went to sleep over the past three years. If anyone else actually uses this or wants a certain feature, contact me and I'll be happy to take a look or just hear that anyone actually used it!

I love Python.

---

## How to use this thing

It's pretty simple. Make sure you already have Python installed, as well as `matplotlib`, `datetime`, and `pytz`.
```c
analyzer.py [-h] --a {completed,created} [--f [FILE]]

options:
  -h, --help            show this help message and exit
  --analyzer {completed,created}, -a {completed,created}
                        sets the mode of the analyzer
  --file [FILE], -f [FILE]
                        filename or path to the Day One journal .json file
```

In other words, run `python analyzer.py -a completed -f journal.py` (or whatever you named your journal export). Change the analyzer mode to your heart's desire. My heart desires to see how late I've stayed up over the past few years. Make sure you extracted your journal if you exported it using the `.zip` option.

---

## To-Do
- [ ] Import and parse the journal data
- [ ] Add argparse abilities
- [ ] Make a working graph
- [X] Adjust for local time zones
- [ ] Shift the completed/created graph 12h vertically (much more intuitive)
- [ ] Add general statistics about completed/created times
- [ ] Add a map function (similar to what exists in the app)
- [ ] Get weather information from a certain day
- [ ] Get weather informatiom from a range of days
- [ ] GUI?
- [ ] Add a selection pane with different specificities:
  - [ ] Add ability to select range of entry dates for all functionalities
  - [ ] Select only pinned entries
  - [ ] Select only starred entries
  - [ ] Grab text/richtext of groups of entries
  - [ ] Select only entries that contain a word/phrase
  - [ ] Select only entries done on a certain device
  - [ ] Select only entries from a certain country
  - [ ] Select only entries from a certain locality
  - [ ] Select only entries from a certain address (placeName)
  - [ ] Select entries by tag

> **Disclaimer:** Day One was not involved in any form with the creation of this tool, nor does it endorse or recognize its existence.
