# Description of the `src` directory

This directory contains the source code of the project.

## Structure

The `src` directory contains the following scripts:

- `S1.py`: Scrapes trending and non-trending videos from the YouTube's official website (https://www.youtube.com/). Trending video URLs are scraped from the YouTube's trending videos pages (see `trending_categories.txt` for reference), and Non-trending video URLs are taken from YouTube's homepage. 
- `S2.py`: Main data retrieval tool used to collect ad and main-video's byte data. 
- `add_time.py`: Fetches the length (duration in seconds) of a given video (main-video and ad) and updates the raw data files with the video durations. 
- `analysis.ipynb`: Jupyter Notebook containing the code backing all our figures used in the paper - will give you an inside look into the calculations that we computed to generate the plots.
- `bitrate.py`: Makes API calls using a third-party library `yt-dlp` to get the video bit-rates at certain resolutions (360p & 720p).
- `cleanup.py`: Prior to generating the CSV files, run this script to remove any empty raw data directories and renames them to in numerical order and sorts them alphabetically. 
- `data-collection.sh`: A shell script to automate the data collection process (as outlined in section 3 of the paper).
- `get-count.sh`: Gives the total count of trending and non-trending videos contained in the entire dataset of a given country.
- `get_bytes.py`: Makes an API call to a third-party library `yt-dlp` and fetches the size (in bytes) of a given video (main-video and ad) and updates the raw data files with the target video's size.
- `get_res.py`: Updates the raw data files with a given video's (main-video and ad) resolution that was captured by `S2.py` during data retrieval phase.
- `make-csv-nontrending.sh`: Runs the `cleanup.py`, `add_time.py`, `get_res.py`, and `get_bytes.py` file sequentially to facilitate the CSV generation process for non-trending videos of a given country.
- `make-csv-trending.csv`: Runs the `cleanup.py`, `add_time.py`, `get_res.py`, and `get_bytes.py` file sequentially to facilitate the CSV generation process for trending videos of a given country.
- `make-csv.ipynb`: Reads the raw data files sequentially and generates the final CSV file. For further information, navigate to any CSV data file given. Click [here](data/developed/canada/CanadaNonTrending.csv) to access the data file.
-  `res.js`: Manipulates the DOM to configure the resolution of a given video manually on the mobile web version of YouTube (`m.youtube.com`).
-  `trending_categories.txt`: The 4 main trending categories on YouTube's homepage. 

