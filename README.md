# BrowserTimelineRecovery-Kaminski-Rhodes
A python tool for analyzing browser artifacts to potentially detect deleted browsing history. Works on Linux and Windows operating systems.
Attempts to recover deleted browsing history based on browsing data such as cookies, cache, etc.


### Usage
```
usage: btr.py [-h] -b {chrome,firefox} [-d {history,cookies,cache}] [-o OUT]
              [-u USER] [-c CONFIG] [-s START] [-e END] [-w WINDOW]

Detects inconsistencies in browsing data or dumps browsing data

optional arguments:
  -h, --help            show this help message and exit
  -b {chrome,firefox}, --browser {chrome,firefox}
                        Select a browser to examine
  -d {history,cookies,cache}, --dump {history,cookies,cache}
                        Dump data in CSV format and quit
  -o OUT, --outfile OUT
                        File to write results
  -u USER, --user USER  Specifiy a user directory to search, default is
                        current user
  -c CONFIG, --config CONFIG
                        Specify YAML configuration file with paths to files
  -s START, --start START
                        Starting time for analysis (epoch/NTFS file time)
  -e END, --end END     Ending time for analysis (epoch/NTFS file time)
  -w WINDOW, --window WINDOW
                        Time window to check for discrepancies between
                        artifacts (e.g. cookies) with history (microseconds).
                        DEFAULT: 5000000 (5s)
```

### Use cases
- Obtain a file containing history/cookie records is a readable format (CSV)
  - Example: ```python btr.py -b firefox -d cookies -o out.csv```
- Recover deleted browsing history by comparing the timestamps of browsing records (such as cookie creation time) to that of a user's search history.
  - Example: ```python btr.py -b chrome -w 10000000```

### Current Condition
Currently, the tool analyzes history or cookie records for Firefox and Chrome, with support on both Linux and Windows. When a user deletes browsing history, modern browsers often delete cache and cookies as well. Future work is needed to parse other browsing artifacts, such as offline website data, form and search history, and active logins, to aid in recovering a user's search history.
