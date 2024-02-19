# Uncovering the Hidden Data Costs of Mobile YouTube Video Ads

This file provides essential information about the source code used in the research paper. 

Here's a holistic tree directory structure of the repository to help you navigate the source code:

## Directory Structure

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
└── src
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

To access the scraper for non trending vidoes, type the following in the terminal:

```bash
python S1.py -n
```

## Instructions to run the data collection script

```bash
python S2.py list_of_urls.txt
```
