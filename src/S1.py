# !/usr/bin/python
# -*- coding: utf-8 -*-

# IMPORTING LIBRARIES
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException
import os
import time
import itertools
import argparse
import sys
import random
import json
from typing import List, Dict
import requests
import subprocess


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

        self.chrome_ser: str = ""
        self.chrome_service: ChromeService = None
        self.driver: webdriver.Chrome = None

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

    def run(self) -> None:
        self.chrome_ser = self.install()
        self.chrome_service = ChromeService(
            executable_path=self.chrome_ser)
        self.driver = webdriver.Chrome(
            service=self.chrome_service, options=self.chrome_options)


class TrendingScraper(InstallDriver):
    '''
    This class scrapes the trending videos from YouTube
    '''

    def __init__(self) -> None:
        '''
        This method sets the options for the Chrome Driver and initializes the Chrome Driver.
        It also sets the number of times the page should be scrolled and initializes the lists
        to store the trending videos.

        :param self: The object itself
        :type self: TrendingScraper
        :return: None
        '''
        super().__init__()
        InstallDriver.run(self)
        # Setting the number of times the page should be scrolled
        self.SCROLL_NUMBER: int = 20
        # Data structures to store and process the trending videos
        self.final_videos: List[List[str]] = []
        self.trending_videos: List[List[List[str]]] = []
        self.trending_videos_final: List[str] = []
        self.trending_videos_dict: Dict[str, float] = {}
        self.trending_videos_longer_than_hour: Dict[str, float] = {}
        self.trending_videos_shorter_than_hour: Dict[str, float] = {}

    def __get_video_duration(self) -> float:
        '''
        This method returns the duration of the video

        :param self: The object itself
        :type self: TrendingScraper
        :return: The duration of the video
        :rtype: float
        '''
        try:
            return self.driver.execute_script( 
                'return document.getElementById("movie_player").getDuration()'
            ) 
        except WebDriverException:
            return 0

    def __accept_cookies(self) -> None:
        '''
        This method accepts the cookies on the YouTube page. 

        :param self: The object itself
        :type self: TrendingScraper
        :return: None
        '''
        try:
            self.driver.find_element( 
                by=By.XPATH, value='/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[2]/div/div/button').click()
        except:
            pass

    def __categorize_by_duration(self) -> None:
        '''
        This method takes the trending videos and categorizes them by duration

        :param self: The object itself
        :type self: TrendingScraper
        :return: None
        '''

        # Iterating over the trending videos
        for video in self.trending_videos_final:
            try:
                # Open the video in the browser
                self.driver.get(video)
                time.sleep(2)
                try:
                    # Accept the cookies
                    if self.driver.find_element(by=By.XPATH, value="//*[@id=\"button\"]/yt-button-renderer/yt-button-shape").is_displayed(): 
                        continue
                except:
                    pass
                try:
                    # Mute the video
                    self.driver.execute_script( 
                        "document.getElementsByClassName('video-stream html5-main-video')[0].volume=0"
                    )
                    duration: float = 0.0
                    # Try to get the duration of the video
                    i = 0
                    # Try 10 times to get the duration of the video
                    while i < 10:
                        try:
                            # Get the duration of the video
                            duration = self.__get_video_duration()
                            # If the duration is not 0, break out of the loop
                            if duration:
                                break
                        except:
                            # If the duration is 0, increment the counter and try again
                            i += 1
                    # If the duration is 0, continue to the next video
                    if not duration:
                        print(f'Could not get duration for video: {video}')
                        continue

                    # Print the video and its duration to the console
                    print(f'Video: {video} | Duration: {duration}')
                    # Add the video and its duration to the dictionary for further processing
                    self.trending_videos_dict[video] = duration
                except Exception as e:
                    # If there is an exception, print it and continue to the next video
                    print(e)
                    continue
            except Exception as e:
                # If there is an exception, print it and continue to the next video
                print(e)
                continue

        # Categorize the videos by duration (longer than an hour and shorter than an hour)
        self.trending_videos_longer_than_hour = {
            k: v for k, v in self.trending_videos_dict.items() if v >= 3600.0}
        self.trending_videos_shorter_than_hour = {
            k: v for k, v in self.trending_videos_dict.items() if v < 3600.0}

        # Shuffle the videos to remove any bias
        trending_longer_keys = list(
            self.trending_videos_longer_than_hour.keys())
        random.shuffle(trending_longer_keys)
        trending_longer_shuffled = {
            key: self.trending_videos_longer_than_hour[key] for key in trending_longer_keys}
        self.trending_videos_longer_than_hour = trending_longer_shuffled

        # Shuffle the videos to remove any bias
        trending_shorter_keys = list(
            self.trending_videos_shorter_than_hour.keys())
        random.shuffle(trending_shorter_keys)
        trending_shorter_shuffled = {
            key: self.trending_videos_shorter_than_hour[key] for key in trending_shorter_keys}
        self.trending_videos_shorter_than_hour = trending_shorter_shuffled

    def __len__(self) -> int:
        '''
        This method returns the length of the trending videos dictionary

        :param self: The object itself
        :type self: TrendingScraper
        :return: The length of the trending videos dictionary
        :rtype: int
        '''
        return len(self.trending_videos_dict.keys())

    def __run(self) -> None:
        '''
        This method runs the scraper

        :param self: The object itself
        :type self: TrendingScraper
        :return: None
        '''
        # Open the file with the trending categories
        with open('trending_categories.txt', 'r') as file:
            # Read the lines of the file
            lines: List[str] = file.readlines()
            # Iterate over the lines
            for link in lines:
                try:
                    # Scrape the videos from the link
                    self.trending_videos.append(self.__scrape(link))
                except Exception as e:
                    # If there is an exception, print it and continue to the next link
                    print(e)
                    continue

    def __scrape(self, url: str) -> List[List[str]]:
        '''
        This method scrapes the videos from the given url and adds them to the trending videos list. 

        :param self: The object itself
        :type self: TrendingScraper
        :param url: The url to scrape the videos from

        :type url: str
        :return: None
        '''

        # Open the YouTube video in the browser
        self.driver.get(url)
        # Sleep for 2 seconds to let the page load
        time.sleep(2)
        try:
            # Accept the cookies
            self.__accept_cookies()
        except:
            # If there is an exception (meaning the accept button cookies did not appear), pass
            pass
        time.sleep(2)

        # Scroll down the page to load more videos
        for i in range(self.SCROLL_NUMBER):
            # Print the scroll number to the console
            print(f'Scroll number: {i}')

            # Scroll down the page by pressing the PAGE_DOWN key
            html: WebElement = self.driver.find_element( 
                by=By.TAG_NAME, value='html')
            html.send_keys(Keys.PAGE_DOWN) 
            # Using XPath, get all the videos on the page and add them to the list of videos
            # The videos are filtered to remove any videos that are not actual videos (e.g. playlists, channels, shorts, etc.)
            
            videos = self.driver.find_elements( 
                by=By.XPATH, value="//a[@href[contains(., 'watch?v=') and not(contains(., '&list=')) and not(contains(., 'channel')) and not(contains(., 'user')) and not(contains(., 'playlist'))  and not(contains(., 'shorts')) and not(contains(., '&pp='))]]")
            # Get the href attribute of each video
            videos = [video.get_attribute('href') for video in videos] 
            # Add the videos to the list of videos
            videos = [video for video in videos if '&pp=' not in video]
            # Add the videos to the list of videos
            self.final_videos.append(videos)

        return self.final_videos

    def __process(self) -> None:
        '''
        This method processes the videos and writes them to the file

        :param self: The object itself
        :type self: TrendingScraper
        :return: None
        '''
        # Flatten the list of lists of videos
        trending_videos = list(
            itertools.chain(*self.final_videos))
        # Remove any duplicates
        trending_videos = list(set(trending_videos))
        # Remove any empty strings
        trending_videos = list(
            filter(None, trending_videos))
        # If there are no trending videos, raise an exception
        self.trending_videos_final = trending_videos
        if not trending_videos:
            raise Exception("Trending videos are not found")

    def __write_to_file(self) -> None:
        '''
        This method writes the trending videos to the file as per the requirements (duration, etc.)

        :param self: The object itself
        :type self: TrendingScraper
        :return: None
        '''
        try:
            # Open the file to write the trending videos to
            with open('trending_videos.txt', 'w') as file:
                for video in self.trending_videos_final:
                    file.write('%s\n' % video)
        except OSError as e:
            # If there is an exception, print it
            print('Could not open file: %s' % e)
        try:
            # Open the file to write the trending videos longer than an hour to
            with open('trending_videos_longer_than_hour.txt', 'w') as file:
                videos = list(self.trending_videos_longer_than_hour.keys())
                # Iterate over the videos
                for video in videos:
                    file.write('%s\n' % video)
        except OSError as e:
            # If there is an exception, print it
            print('Could not open file: %s' % e)
        try:
            # Open the file to write the trending videos shorter than an hour to
            with open('trending_videos_shorter_than_hour.txt', 'w') as file:
                videos = list(self.trending_videos_shorter_than_hour.keys())
                # Iterate over the videos
                for video in videos:
                    file.write('%s\n' % video)
        except OSError as e:
            # If there is an exception, print it
            print('Could not open file: %s' % e)

    def __dump(self) -> None:
        '''
        This method dumps the trending videos to the JSON file

        :param self: The object itself
        :type self: TrendingScraper
        :return: None
        '''
        try:
            # Open the file to write the trending videos to as JSON
            with open('trending_videos_longer_than_hour.json', 'w') as file:
                # Dump the trending videos longer than an hour to the file
                json.dump(self.trending_videos_longer_than_hour,
                          file, indent=4)
        except Exception as e:
            # If there is an exception, print it
            print(f"Error: {e}")

        try:
            # Open the file to write the trending videos to as JSON
            with open('trending_videos_shorter_than_hour.json', 'w') as file:
                # Dump the trending videos shorter than an hour to the file
                json.dump(self.trending_videos_shorter_than_hour,
                          file, indent=4)
        except Exception as e:
            # If there is an exception, print it
            print(f"Error: {e}")

    def __del__(self) -> None:
        '''
        This method closes the driver
        '''
        try:
            # Close the driver
            self.driver.close()
        except Exception:
            pass

    def main(self) -> None:
        '''
        This method runs the program

        :param self: The object itself
        :type self: TrendingScraper
        :return: None
        '''
        # Run the scraper to get the trending videos
        self.__run()
        # Process the videos
        self.__process()
        # Categorize the videos by duration
        self.__categorize_by_duration()
        # Write the videos to the file
        self.__write_to_file()
        # Dump the videos to the JSON file
        self.__dump()
        print(f'Total vidoes without live: {len(self)}')


class NonTrending(InstallDriver):
    '''
    This class scrapes the non-trending videos and writes them to the file
    after categorizing them by duration and cleaning them up
    '''

    def __init__(self):
        '''
        This method initializes the object. It also sets the URL and the scroll number

        :param self: The object itself
        :type self: NonTrending
        :return: None
        '''
        # call the super class constructor
        super().__init__()
        InstallDriver.run(self)
        # Set the URL and the scroll number
        self.SCROLL_NUMBER: int = 40
        self.URL: str = 'https://www.youtube.com/'
        # Set the lists and dictionaries for processing
        self.list_videos: list = []
        self.homepage_videos: list = []
        self.random_sample: list = []
        self.max_duration_trending: float = 0.0
        self.nontrending_videos: Dict[str, float] = {}
        self.nontrending_videos_longer_than_hour: Dict[str, float] = {}
        self.nontrending_videos_shorter_than_hour: Dict[str, float] = {}
        self.nontrending_videos_shorter_than_max_duration: Dict[str, float] = {
        }

    def __get_video_duration(self) -> float:
        '''
        This method gets the duration of the video

        :param self: The object itself
        :type self: NonTrending
        :return: The duration of the video
        :rtype: float
        '''
        duration = float(self.driver.execute_script( 
            'return document.getElementById("movie_player").getDuration()'
        ))

        return duration

    def __accept_cookies_homepage(self) -> None:
        '''
        This method accepts the cookies on the homepage (if they exist)

        :param self: The object itself
        :type self: NonTrending
        :return: None
        '''
        try:
            # Accept the cookies
            self.driver.find_element( 
                by=By.XPATH, value="//*[@id=\"content\"]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button").click()
        except Exception:
            # If there is an exception, pass
            pass

    def __get_max_duration(self) -> None:
        '''
        This method gets the maximum duration of the trending videos

        :param self: The object itself
        :type self: NonTrending
        :return: None
        '''

        # Open the file to read the trending videos from
        with open('trending_videos_longer_than_hour.json', 'r') as file:
            # Load the trending videos
            trending_videos: Dict[str, int] = json.load(file)

        # Set the max duration to 0
        max_duration: float = 0.0
        # Iterate through the trending videos
        for _, duration in trending_videos.items():
            # If the duration is greater than the max duration, set the max duration to the duration
            if duration > max_duration:
                max_duration = duration

        # Set the max duration
        self.max_duration_trending = max_duration

    def __scrape(self) -> None:
        '''
        This method scrapes the non-trending videos

        :param self: The object itself
        :type self: NonTrending
        :return: None
        '''
        # Sleep for 5 seconds after navigating to the homepage
        time.sleep(5)
        # Set the scroll number
        scroll_number: int = self.SCROLL_NUMBER
        # Scroll through the page
        for i in range(scroll_number):
            # Scroll down the page by pressing the page down key
            html = self.driver.find_element(by=By.TAG_NAME, value='html') 
            html.send_keys(Keys.PAGE_DOWN) 
            # Get the videos on the page and append them to the list of videos. This removes any short videos or live videos
            videos = self.driver.find_elements( 
                by=By.XPATH, value="//a[@href[contains(., 'watch?v=') and not(contains(., '&list=')) and not(contains(., 'channel')) and not(contains(., 'user')) and not(contains(., 'playlist'))  and not(contains(., 'shorts')) and not(contains(., '&pp='))]]")
            # Get the href attribute of the videos
            videos = [video.get_attribute('href') for video in videos] 
            for video in videos:
                if '&pp=' in video:
                    videos.remove(video)
            # Append the videos to the list of videos
            self.list_videos.append(videos) 
            # Print the scroll number
            print(f'Scroll number: {i}')

    def __process(self) -> None:
        '''
        This method processes the videos

        :param self: The object itself
        :type self: NonTrending
        :return: None
        '''

        # Iterate through the list of videos
        self.homepage_videos = list(set(itertools.chain(*self.list_videos))) 
        # Iterate through the list of videos
        self.homepage_videos = [
            video
            for video in self.homepage_videos 
            if video in self.homepage_videos 
        ]

    def __write_to_file(self) -> None:
        '''
        This method writes the videos to a file for processin. 

        :param self: The object itself
        :type self: NonTrending
        :return: None
        '''
        # Get the links of the videos that are shorter than an hour
        videos_shorter_than_hour: List[str] = list(
            self.nontrending_videos_shorter_than_hour.keys())
        # Get the links of the videos that are shorter than the max duration of the trending videos
        videos_shorter_than_max_duration: List[str] = list(
            self.nontrending_videos_shorter_than_max_duration.keys())
        # Write the videos to a file
        self.__write_to_file_helper(
            videos_shorter_than_hour, 'non_trending_shorter_than_hour.txt')
        # Write the videos to a file
        self.__write_to_file_helper(
            videos_shorter_than_max_duration, 'non_trending_shorter_than_max_duration.txt')

    def __write_to_file_helper(self, videos: List[str], file_name: str) -> None:
        '''
        This method writes the videos to a file

        :param self: The object itself
        :type self: NonTrending
        :param videos: The list of videos
        :type videos: List[str]
        :param file_name: The name of the file
        :type file_name: str
        :return: None
        '''
        try:
            # Open the file
            with open(file_name, 'w') as f:
                # Iterate through the videos
                for video in videos:
                    f.write('%s\n' % video)
        except OSError as e:
            # Print the error
            print(f'Error: {e}')

    def __dump(self) -> None:
        '''
        This method dumps the videos to a json file

        :param self: The object itself
        :type self: NonTrending
        :return: None
        '''
        try:
            # Dump the videos to a json file
            with open('nontrending_videos_shorter_than_hour.json', 'w') as file:
                # Dump the videos to a json file
                json.dump(self.nontrending_videos_shorter_than_hour,
                          file, indent=4)
            # Dump the videos to a json file
            with open('nontrending_videos_shorter_than_max_duration.json', 'w') as file:
                # Dump the videos to a json file
                json.dump(self.nontrending_videos_shorter_than_max_duration,
                          file, indent=4)
        except Exception as e:
            # Print the error
            print(e)

    def __len__(self) -> int:
        '''
        This method returns the length of the list of non-trending videos

        :param self: The object itself
        :type self: NonTrending
        :return: The length of the list of non-trending videos
        :rtype: int
        '''
        return len(self.homepage_videos)

    def __remove_trending(self) -> None:
        '''
        This method removes the trending videos from the sample

        :param self: The object itself
        :type self: NonTrending
        :return: None
        '''
        try:
            # Open the file containing the trending videos streamed immediately before the non-trending videos
            with open('trending_videos.txt', 'r') as file:
                # Get the lines of the file
                lines = file.readlines()
            # Iterate through the lines (trending videos)
            for line in lines:
                # Remove the trending videos from the sample
                if line in self.homepage_videos: 
                    self.homepage_videos.remove(line) 
        except FileNotFoundError as e:
            # Print the error if the file (trending_videos.txt) is not found
            print('Could not open the file: ', e)
        except Exception as e:
            # Print the error
            print(f'Unknown error: {e}')

    def __remove_live(self) -> None:  # remove live videos from the sample
        '''
        This method removes the live videos from the sample by checking if the video is live or not.
        It does so by checking if the video has a live badge or not.

        :param self: The object itself
        :type self: NonTrending
        :return: None
        '''
        # Iterate through the sample
        for video in self.random_sample: 
            # Get the video
            self.driver.get(video) 
            # Wait for the page to load
            time.sleep(3)
            try:
                # Check if there is an accept cookies button
                if self.driver.find_element(by=By.XPATH, value="//*[@id=\"app\"]/div[1]/ytm-watch/div[1]/div/ytm-player-error-message-renderer/div[3]/ytm-button-renderer").is_displayed(): 
                    continue
            except:
                pass
            try:
                # Mute the video
                self.driver.execute_script( 
                    "document.getElementsByClassName('video-stream html5-main-video')[0].volume=0"
                )
                # Variable to store the live badge
                live: str = ""
                i = 0
                # Keep trying to get the live badge for 5 times
                while i < 5:
                    try:
                        # Get the live badge
                        live = self.driver.execute_script(
                            "return document.getElementsByClassName(\"ytp-chrome-bottom\")[0].children[1].children[0].children[4].children[3].textContent")
                        # If the video is live, break out of the loop
                        if live:
                            break
                    except:
                        # Increment the counter and try again
                        i += 1
                # If the video is live, remove it from the sample
                print(f'live: {live}')
                if live == 'Watch live stream':
                    print(f'Removing live video: {video}')
                    self.random_sample.remove(video)
                    print(
                        f'New sample size: {len(self.random_sample)}\n Continuing to next video!')
                    continue

                # Get the duration of the video
                duration: float = 0.0
                i = 0
                # Keep trying to get the duration for 5 times
                while i < 5:
                    try:
                        # Get the duration
                        duration = self.__get_video_duration()
                        # If the duration is found, break out of the loop
                        if duration:
                            break
                    except:
                        # Increment the counter and try again
                        i += 1

                # If the duration is not found, continue to the next video
                if not duration:
                    print(f'Could not get duration for video: {video}')
                    continue

                # Print the video and its duration to the console
                print(f'video: {video} | duration: {duration}')
                # Add the video and its duration to the dictionary
                self.nontrending_videos[video] = duration
            except:
                pass

    def __categorize_by_duration(self) -> None:
        '''
        This method categorizes the videos by duration by separating the videos into two dictionaries:
        1. Videos longer than an hour
        2. Videos shorter than an hour

        :param self: The object itself
        :type self: NonTrending
        :return: None
        '''
        try:
            # Get the videos longer than an hour
            self.nontrending_videos_longer_than_hour = {
                k: v for k, v in self.nontrending_videos.items() if v >= 3600.0}
            # Get the videos shorter than an hour
            self.nontrending_videos_shorter_than_hour = {
                k: v for k, v in self.nontrending_videos.items() if v < 3600.0}
        except (AttributeError, TypeError):
            # If the dictionary is empty or any key is missing, set the dictionaries to empty
            self.nontrending_videos_longer_than_hour = {}
            self.nontrending_videos_shorter_than_hour = {}
        try:
            # Get the max duration of the trending videos
            self.__get_max_duration()
        except Exception as e:
            # Print the error
            print(f'Could not get max duration: {e}')

        # Get the videos shorter than the max duration of the trending videos
        self.nontrending_videos_shorter_than_max_duration = dict(
            filter(lambda elem: elem[1] <= self.max_duration_trending, self.nontrending_videos_longer_than_hour.items()))

        # The keys of the dictionaries are the YouTube video URLs
        nontrending_shorter_keys = list(
            self.nontrending_videos_shorter_than_hour.keys())
        # Shuffle the keys (YouTube video URLs) to remove bias
        random.shuffle(nontrending_shorter_keys)
        # Create a new dictionary with the shuffled keys
        nontrending_shorter_shuffled = {
            key: self.nontrending_videos_shorter_than_hour[key] for key in nontrending_shorter_keys}
        self.nontrending_videos_shorter_than_hour = nontrending_shorter_shuffled

        # The keys of the dictionaries are the YouTube video URLs
        nontrending_shorter_max_duration = list(
            self.nontrending_videos_shorter_than_max_duration.keys())
        # Shuffle the non trending videos
        random.shuffle(nontrending_shorter_max_duration)
        nontrending_shorter_max_duration_shuffled = {
            key: self.nontrending_videos_shorter_than_max_duration[key] for key in nontrending_shorter_max_duration}
        self.nontrending_videos_shorter_than_max_duration = nontrending_shorter_max_duration_shuffled

    def __random_sample(self) -> None:
        '''
        This method creates a random sample of the non trending videos.
        '''
        # Check if the trending videos file exists
        if not os.path.exists('trending_videos.txt'):
            # If the file does not exist, raise an error
            raise FileNotFoundError(
                'trending_videos.txt not found. Scrape trending videos first')

        # Check if the trending videos file is empty
        if os.stat('trending_videos.txt').st_size == 0:
            # If the file is empty, raise an error
            raise ValueError('trending_videos.txt is empty')

        # Read the trending videos file
        with open('trending_videos.txt', 'r') as file:
            # Get the trending videos
            trending_videos = file.read().splitlines()

        # Choose a random sample of trending videos.
        # If the length of the trending videos is greater than the length of the homepage videos,
        if len(self.homepage_videos) < len(trending_videos):
            # Set the random sample to the homepage videos
            self.random_sample = self.homepage_videos
        else:
            # Set the random sample to a random sample of the trending videos
            self.random_sample = random.sample(
                self.homepage_videos, len(trending_videos))
        # Print the length of the random sample
        print(f'Length of random sample: {len(self.random_sample)}')

    def __prepare_dataset(self) -> None:
        '''
        This method prepares the non trending videos list for the dataset.

        :param self: The object itself
        :type self: NonTrending
        :return: None
        '''
        # Remove the trending videos from the random sample of non trending videos
        self.__remove_trending()
        # Remove the live videos from the random sample of non trending videos
        self.__random_sample()
        # Remove the live videos from the random sample of non trending videos
        self.__remove_live()
        # Categorize the non trending videos by duration
        self.__categorize_by_duration()
        # Write the non trending videos to a file
        self.__write_to_file()
        # Dump the non trending videos to a JSON file
        self.__dump()

    def __del__(self) -> None:
        '''
        This method closes the browser.

        :param self: The object itself
        :type self: NonTrending
        :return: None
        '''
        self.driver.quit()

    def main(self) -> None:
        '''
        This method is the main method of the class that calls all the other methods (starts the non-trending scraper).

        :param self: The object itself
        :type self: NonTrending
        :return: None
        '''
        # Get the URL
        self.driver.get(self.URL)
        # Wait for 2 seconds
        time.sleep(2)
        try:
            # Accept the cookies
            self.__accept_cookies_homepage()
        except:
            pass
        # Scrape the URLs form the homepage
        self.__scrape()
        # Process the URLs
        self.__process()
        # Prepare the final list of non trending videos and
        # write the non trending videos to their respective files
        self.__prepare_dataset()


# The main method (Driver Code)
if __name__ == '__main__':
    try:
        # Create an argument parser
        parser = argparse.ArgumentParser()
        # Add the arguments
        parser.add_argument(
            '-t', '--trending', help='Scrape trending videos', action='store_true')
        parser.add_argument(
            '-n', '--non-trending', help='Scrape non trending videos', action='store_true')
        args: argparse.Namespace = parser.parse_args()
        # Check if the trending argument is passed
        if args.trending:
            # Scrape the trending videos
            TrendingScraper().main()
        # Check if the non trending argument is passed
        elif args.non_trending:
            # Scrape the non trending videos
            NonTrending().main()
        else:
            # Print the help message
            parser.print_help()
    except KeyboardInterrupt:
        # If the user presses CTRL+C, exit the program
        print('KeyboardInterrupt')
        sys.exit(0)
