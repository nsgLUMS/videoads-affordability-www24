[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10680861.svg)](https://doi.org/10.5281/zenodo.10680861)

# Uncovering the Hidden Data Costs of Mobile YouTube Video Ads

This file provides essential information about the source code used in the research paper. 

Here's a holistic tree directory structure of the repository to help you navigate the source code:

## Directory Structure & File Descriptions  

```txt
.
├── data/
│   ├── developed/
│   │   ├── canada/
│   │   │   ├── CanadaNonTrending.csv ~> Non-trending videos streamed using Canada's VPN
│   │   │   └── CanadaTrending.csv ~> Trending videos streamed using Canada's VPN
│   │   ├── germany/
│   │   │   ├── GermanyNonTrending.csv ~> Non-trending videos streamed using Germany's VPN
│   │   │   └── GermanyTrending.csv ~> Trending videos streamed using Germany's VPN
│   │   ├── japan/
│   │   │   ├── JapanNonTrending.csv ~> Non-trending videos streamed using Japan's VPN
│   │   │   └── JapanTrending.csv ~> Trending videos streamed using Japan's VPN
│   │   ├── README.md
│   │   └── usa/
│   │       ├── USANonTrending.csv ~> Non-trending videos streamed using USA's VPN
│   │       └── USATrending.csv ~> Trending videos streamed using USA's VPN
│   ├── developing/
│   │   ├── brazil/
│   │   │   ├── BrazilNonTrending.csv ~> Non-trending videos streamed using Brazil's VPN
│   │   │   └── BrazilTrending.csv ~> Trending videos streamed using Brazil's VPN
│   │   ├── indonesia/
│   │   │   ├── IndonesiaNonTrending.csv ~> Non-trending videos streamed using Indonesia's VPN
│   │   │   └── IndonesiaTrending.csv ~> Trending videos streamed using Indonesia's VPN
│   │   ├── mexico/
│   │   │   ├── MexicoNonTrending.csv ~> Non-trending videos streamed using Mexico's VPN
│   │   │   └── MexicoTrending.csv ~> Trending videos streamed using Mexico's VPN
│   │   ├── pakistan/
│   │   │   ├── PakistanNonTrending.csv ~> Non-trending videos streamed using Pakistan's VPN
│   │   │   └── PakistanTrending.csv ~> Trending videos streamed using Pakistan's VPN
│   │   └── README.md
│   ├── README.md
│   └── resolution_experiment/
│       ├── bitrates.csv ~> Data about video bitrates across main-video resolutions
│       ├── README.md ~> README describing the features of each CSV file.
│       ├── resolution_360p.csv ~> Main dataset generated with respect to main-videos streamed at 360p
│       └── resolution_720p.csv ~> Main dataset generated with respect to main-videos streamed at 720p
├── README.md
└── src/ 
    ├── add_time.py
    ├── analysis.ipynb
    ├── bitrate.py
    ├── cleanup.py
    ├── data-collection.sh
    ├── get_bytes.py
    ├── get-count.sh
    ├── get_res.py
    ├── make-csv.ipynb
    ├── make-csv-nontrending.sh
    ├── make-csv.sh
    ├── make-csv-trending.sh
    ├── README.md
    ├── requirements.txt
    ├── res.js
    ├── S1.py
    ├── S2.py
    └── trending_categories.txt

14 directories, 42 files
```

## Instructions to run the scraper (`S1.py`)

```bash
usage: S1.py [-h] [-t] [-n]

options:
  -h, --help          show this help message and exit
  -t, --trending      Scrape trending videos
  -n, --non-trending  Scrape non trending videos
```

The script automatically configures the data retrieval process using your preferred parameters. The `InstallDriver` class (inherited by the `FetchDriverVersion` class) in `S1.py` makes an API call to the relevant endpoint, fetches the latest/ suitable chromdriver's version and begins the data scraping process. The `FetchDriverVersion`

For Ubuntu/ Debian based devices, we used the following code to init the OS version: `linux64`. 

### Caution

Make sure to have `trending_videos.txt` file in your working directory before scraping non trending videos.

### Trending Scraper

To access the trending scraper, type the following in the terminal:

```bash
python S1.py -t
```

### NonTrending Scraper

To access the scraper for non trending videos, type the following in the terminal:

```bash
python S1.py -n
```

## Instructions to run the data collection script (`S2.py`)

```bash
python S2.py list_of_urls.txt
```

**Note** that this `list_of_urls.txt` is generated by `S1.py`. This could be either  a list of trending videos or non-trending videos. 

## Instructions to run the data collection pipeline

1. Run `S1.py` using any one of the flags mentioned above (`t` for trending videos and `n` for non-trending videos). It is important to note that you cannot scrape non-trending videos without collecting the trending-video URLs. First scrape the trending video URLs, and then collect the non-trending ones. 
`S1.py` sorts the video URLs and distributes them in multiple files as per the video duration in seconds. Shorter videos (< 60 mins) are written in separate text files and longer ones (> 60 mins) in others. 
2. Once the scraping process is complete, run the following command to enable `data-collection.sh` for execution: `chmod +x data-collection.sh` to facilitate URL distribution. 
3. Next, run the `data-collection.sh` script. This script has an option of running the scraper (`S1.py`) as well allowing you to skip the first step. 
4. Once all folders have been created and the URL text files have been generated, you're all set to start the data collection process.
5. The bash script `data-collection.sh` automatically starts running the `S2.py` in each of the trending and non-trending data folders created in step 3. 
6. In a single iteration, you're expected to have **one** dated folder, in which you will have one `trending` and one `non-trending` folder. In each of these folders, there will be 4 further subdirectories, each having their share of URLs to be streamed by `S2.py`. 