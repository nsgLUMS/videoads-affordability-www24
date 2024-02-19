# Uncovering the Hidden Data Costs of Mobile YouTube Video Ads

This file provides essential information about the source code used in the research paper. The source code accompanies the paper and is being submitted to the conference for review.

## Instructions to run the scraper

```bash
usage: S1.py [-h] [-t] [-n]

options:
  -h, --help          show this help message and exit
  -t, --trending      Scrape trending videos
  -n, --non-trending  Scrape non trending videos
```

If you want to configure the script manually using your preferred parameters, navigate to the InstallDriver class and modify the line 65 of the S1.py file using any of the following acceptable os_type values:

- Ubuntu/ Server: linux64

However, we fetch the version using the chromdriver API and retrieve the accurate version for you:

```python
class FetchDriverVersion:
    def __init__(self) -> None:
        self.version: str = subprocess.check_output(
            "google-chrome --version", shell=True).decode("utf-8")
        self.chromedriver_ver: str = requests.get(
            "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_" + self.version.split(" ")[2].split(".")[0]).text
        self.os_type: str = sys.platform + str(sys.maxsize.bit_length() + 1)


class InstallDriver(FetchDriverVersion):
    '''
    This class installs the Chrome Driver and sets the options for the driver
    '''

    def __init__(self) -> None:
        '''
        This method sets the options for the Chrome Driver

        :param self: The object itself
        :type self: InstallDriver
        :return: None
        '''
        # Using super() to call the parent class constructor
        super().__init__()
        self.chrome_options: Options = Options()
        self.chrome_options.add_argument("--start-maximized")  
        self.chrome_options.add_argument("--disable-gpu")  
        self.chrome_options.set_capability(  
            "loggingPrefs", {'performance': 'ALL'})

    def install(self) -> str:
        '''
        This method installs the Chrome Driver

        :param self: The object itself
        :type self: InstallDriver
        :return: The path to the Chrome Driver
        '''
        try:
            return ChromeDriverManager(
                version=self.chromedriver_ver,  name='chromedriver', os_type=self.os_type, path=os.getcwd()
            ).install()
        except:
            raise Exception("Could not install Chrome Driver!")
```
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
