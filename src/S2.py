
# IMPORT LIBRARIES
import time
import warnings
import orjson
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from collections import Counter
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
import sys
from typing import *
import subprocess
import requests
import contextlib

# GLOBAL VARIABLES

# for mobile emulation
mobile_emulation = {
    "deviceMetrics": {"width": 720, "height": 1280, "pixelRatio": 10.0},
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
}

# setting these parameters to ignore any code deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# setting up the chrome driver
chrome_options = webdriver.ChromeOptions()
# enabling mobile emulation by setting up the device metrics and user agent
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

# Setting the headless parameter to False so we can see the browser in action in real time and manually verify the results
chrome_options.headless = False

# this list keeps track of all the errors that occur during the data collection process
error_list = []

# to control if the autoplay toggle is on or off
auto_play_toggle = False


def most_frequent(List: list):
    '''
    This function returns the most frequent element in a list

    :param List: list of elements
    :return: most frequent element in the list
    '''
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]


def to_seconds(timestr: str) -> int:
    '''
    This function converts a time string to seconds

    :param timestr: time string in the format HH:MM:SS
    :return: time in seconds
    :rtype: int
    '''
    seconds = 0
    for part in timestr.split(":"):
        seconds = seconds * 60 + int(part, 10)
    return seconds


def accept_cookies(driver: webdriver.Chrome) -> None:
    '''
    This function accepts the cookies on the youtube website

    :param driver: chrome driver
    :return: None
    '''
    with contextlib.suppress(NoSuchElementException):
        for _ in range(3):
            # Scroll down to bottom
            driver.find_element(
                by=By.XPATH, value="/html/body/div[2]/ytm-consent-bump-v2-renderer/div/div[3]/ytm-button-renderer/button").click()
    # click on the accept cookies button
    driver.find_element(
        by=By.XPATH, value="/html/body/div[2]/ytm-consent-bump-v2-renderer/div/div[2]/div[3]/ytm-button-renderer[1]/button").click()

def change_resolution(driver: webdriver.Chrome):
    """
    change_resolution function.

    This function takes a Chrome WebDriver instance as input and executes JavaScript code to change the resolution of the video being played.

    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.

    Returns:
        None.
    """
    if os.path.isfile("./res.js"):
        try:
            with open("./res.js", "r") as f:
                    js_code: str = f.read()
            driver.execute_script(js_code)
        except Exception as e:
            print(e)

def enable_stats_for_nerds(driver: webdriver.Chrome) -> None:
    """
    Enables the "Stats for Nerds" feature in the YouTube video player.

    Args:
        driver: The Chrome WebDriver instance used to interact with the web page.

    Returns:
        None

    Raises:
        Exception: If the "Stats for Nerds" option is not available.

    Examples:
        enable_stats_for_nerds(driver)
    """
    # click on the settings button
    settings = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH,
             "/html/body/ytm-app/ytm-mobile-topbar-renderer/header/div/button[2]")
        )
    )
    settings.click()

    # click on the playback settings button
    playback_settings = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH,
             "/html/body/ytm-app/bottom-sheet-container/bottom-sheet-layout/div/div[2]/div/div/div/ytm-menu-item[3]")
        )
    )
    playback_settings.click()

    try:
        # click on the stats for nerds button
        stats_for_nerds = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/dialog/div[2]/ytm-menu-item[2]")
            )
        )
        stats_for_nerds.click()
    except Exception:
        try:
            # if the stats for nerds option is not showing up via XML path, then try to click on it via javascript
            stats_for_nerds = driver.execute_script(
                "document.getElementsByClassName('menu-item-button')[1].click()"
            )
        except Exception as e:
            # if the stats for nerds option is not showing up via javascript, then raise an exception
            raise e

    # click on the exit button to exit the settings menu
    exit_dialog = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable(
            (By.XPATH,
             "/html/body/div[2]/dialog/div[3]/c3-material-button/button")
        )
    )
    exit_dialog.click()


def start_playing_video(driver: webdriver.Chrome) -> None:
    """
    start_playing_video function.

    This function takes a Chrome WebDriver instance as input and starts playing the video if it is not already playing.

    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.

    Returns:
        None.
    """

    # get the player state of the video
    player_state = driver.execute_script(
        "return document.getElementById('movie_player').getPlayerState()"
    )
    print(f'player state: {player_state}')

    # if the player state is 5, meaning the video is not playing already
    if player_state == 5:
        # play the video by clicking on the large red play button
        driver.execute_script(
            "document.getElementsByClassName('ytp-large-play-button ytp-button')[0].click()"
        )

    # if the video is already playing, then do nothing
    if player_state == 1:
        return


def play_video_if_not_playing(driver: webdriver.Chrome) -> None:
    """
    play_video_if_not_playing function.

    This function takes a Chrome WebDriver instance as input and plays the video if it is not currently playing.

    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.

    Returns:
        None.
    """

    # get the player state of the video by executing javascript in the browser
    player_state = driver.execute_script(
        "return document.getElementById('movie_player').getPlayerState()"
    )
    # if the player state is 0, meaning the video has ended, then do nothing
    # and return.
    if player_state == 0:
        return

    # if the player state is -1, the video hasn't started playing yet.
    if player_state == -1:
        driver.execute_script(
            "document.getElementsByClassName('video-stream html5-main-video')[0].play()"
        )
    # if there is any other player state, it implies that the video is not playing currently.
    # play the video.
    if player_state != 1:
        driver.execute_script(
            "document.getElementsByClassName('video-stream html5-main-video')[0].play()"
        )


def record_ad_buffer(driver: webdriver.Chrome, movie_id: str) -> Tuple[List, List, Dict, List]:
    """
    record_ad_buffer function.

    This function takes a Chrome WebDriver instance and a movie ID as input. It records the buffer size, skippable status, and other related information for an ad that is currently playing.

    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.
        movie_id (str): The ID of the movie.

    Returns:
        Tuple[List, List, Dict, List]: A tuple containing the ad IDs, skippable status, ad buffer information, and skip duration.
    """
    # get the length of the ad playing. If the ad is playing there will be some true value
    # stored in the variable.
    ad_playing = driver.execute_script(
        "return document.getElementsByClassName('ad-showing').length"
    )
    # stores the ad buffer related information
    ad_buffer_list = {}
    # stores the ad id related information
    ad_id = []
    # stores the ad skippable related information
    ad_skippable = {}
    # stores all other related information
    all_numbers = {}
    # records if the ad is skippable or not
    both_skippable = []
    # fetches the skippable duration of the ad (time-to-skip)
    skip_dur = []

    # Loop until the ad is playing
    while ad_playing:
        # get the ad buffer (read-ahead) and convert it to float
        ad_buffer = float(
            driver.execute_script(
                'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[10].children[1].textContent.split(" ")[1]'
            )
        )
        # get the resolution of the ad
        res = driver.execute_script(
            'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[2].children[1].textContent.replace(" ","").split("/")[0]'
        )

        # Check for a number of tries if the ad is has recently played or not
        current_time_retry = 0
        while current_time_retry < 10:
            try:
                ad_played = float(
                    driver.execute_script(
                        "return document.getElementsByClassName('video-stream html5-main-video')[0].currentTime"
                    )
                )
                break
            except Exception:
                current_time_retry += 1

        with contextlib.suppress(Exception):
            # get the ad id
            ad_id_temp = driver.execute_script(
                'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[0].children[1].textContent.replace(" ","").split("/")[0]'
            )
            if (
                str(ad_id_temp).strip() != movie_id.strip() \
                and str(ad_id_temp).strip() not in ad_id
            ):
                ad_id.append(str(ad_id_temp).strip())
                ad_skippable[str(ad_id_temp).strip()] = []
                all_numbers[str(ad_id_temp).strip()] = []
                ad_buffer_list[str(ad_id_temp).strip()] = []

        try:
            # if the ad is skippable, then get the time-to-skip duration (fixed to 5 seconds)
            skip_duration = driver.execute_script(
                'return document.getElementsByClassName("ytp-ad-text ytp-ad-preview-text")[0].innerText'
            )
            numba = int(skip_duration.split(" ")[-1])
            if len(ad_id) == 1:
                all_numbers[ad_id[0]].append(numba)
            if len(ad_id) == 2:
                all_numbers[ad_id[1]].append(numba)
        except Exception:
            if len(ad_id) == 1:
                all_numbers[ad_id[0]].append(-2)
            if len(ad_id) == 2:
                all_numbers[ad_id[1]].append(-2)

        ad_played_in_seconds = ad_played
        # Buffer, Seconds Played, Res
        if len(ad_id) == 1:
            ad_buffer_list[ad_id[0]].append(
                (ad_buffer, ad_played_in_seconds, res))
        if len(ad_id) == 2:
            ad_buffer_list[ad_id[1]].append(
                (ad_buffer, ad_played_in_seconds, res))

        # check if the ad is currently playing
        ad_playing = driver.execute_script(
            "return document.getElementsByClassName('ad-showing').length"
        )
        # if so, check whether the ad is skippable or not
        skippable = int(driver.execute_script(
            "return document.getElementsByClassName('ytp-ad-skip-button-container').length"
        ))

        if len(ad_id) == 1:
            ad_skippable[ad_id[0]].append(skippable)
        if len(ad_id) == 2:
            ad_skippable[ad_id[1]].append(skippable)

        # play the main video if not playing
        play_video_if_not_playing(driver)

    if len(ad_id) == 2:
        both_skippable = [most_frequent(
            ad_skippable[ad_id[0]]),  most_frequent(ad_skippable[ad_id[1]])]
        skip_dur = [max(all_numbers[ad_id[0]]), max(all_numbers[ad_id[1]])]

    if len(ad_id) == 1:
        both_skippable = [most_frequent(ad_skippable[ad_id[0]])]
        skip_dur = [max(all_numbers[ad_id[0]])]

    return ad_id, both_skippable, ad_buffer_list, skip_dur


def driver_code(driver: webdriver.Chrome, filename: str) -> None:
    """
    driver_code function.

    This function takes a Chrome WebDriver instance and a filename as input. It reads the file and stores the URLs in a list. Then, it iterates over each URL, initializes various variables, and performs data collection related to video playback, ads, buffer size, and resolution changes.

    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.
        filename (str): The name of the file containing the URLs.

    Returns:
        None.
    """
    # read the file and store the urls in a list
    with open(filename, "r") as f:
        list_of_urls = f.read().splitlines()

    # iterate over each url in the list of urls
    for index, url in enumerate(list_of_urls):
        # initialize all the global variables
        global error_list  # used for any error logging
        global auto_play_toggle  # used to check if the autoplay is on or off
        video_info_details = {}  # used to store the video information
        ad_buffer_information = {}  # used to store the ad buffer information
        error_list = []  # used to store any errors
        unique_add_count = 0  # used to count the number of unique ads
        ad_just_played = False  # used to check if an ad has just played
        buffer_list = []  # used to store the buffer information
        actual_buffer_reads = []  # used to store the actual buffer reads
        buffer_size_with_ad = []  # used to store the buffer size with ad
        vid_res_at_each_second = []  # used to store the video resolution at each second
        main_res_all = []  # used to store the main video resolution
        previous_ad_id = url.split("=")[1]  # used to store the previous ad id
        movie_id = url.split("=")[1]  # used to store the movie id
        filename = str(filename)  # used to store the filename
        folder_name = filename.split('.')  # used to store the folder name
        # used to store the new directory
        new_dir = "./" + str(folder_name[0]) + "-" + str(index + 1)

        driver.get(url) # open the url in the browser
        time.sleep(2)  # sleep for 2 seconds
        try:
            # check if there is a constraint on playing the video and we need to
            # sign in
            error_container: bool
            try:
                error_container = driver.find_element(
                    by=By.XPATH, value="//*[@id=\"app\"]/div[1]/ytm-watch/div[1]/div/ytm-player-error-message-renderer").is_displayed()
            except:
                error_container = False
            if error_container:
                # if there is any, skip the video
                print("PROBLEMATIC URL! Moving to next URL...")
                continue
            try:
                # check if there is an accept cookies button (germany)
                accept_cookies(driver)
            except:
                pass

            # enable stats for nerds after 5 retries
            retry_count = 0
            while retry_count < 5:
                try:
                    # enable
                    enable_stats_for_nerds(driver)
                    break
                except:
                    retry_count += 1

            # Start Playing Video
            start_playing_video(driver)

            # Check If ad played at start
            ad_playing = driver.execute_script(
                "return document.getElementsByClassName('ad-showing').length"
            )
            print("Playing Video: ", movie_id)

            # get the duration of main-video in seconds
            video_duration_in_seconds = driver.execute_script(
                'return document.getElementById("movie_player").getDuration()'
            )

            # create a new folder to store the video data
            Path(new_dir).mkdir(parents=False, exist_ok=True)

            # check if the video is playing by checking the player state
            video_playing = driver.execute_script(  
                "return document.getElementById('movie_player').getPlayerState()"
            )
            # Turning off Autoplay
            if not auto_play_toggle:
                try:
                    driver.execute_script(
                        "document.getElementsByClassName('ytm-autonav-toggle-button-container')[0].click()"
                    )
                    auto_play_toggle = True
                except:
                    pass

            # Turning off Volumne.
            try:
                driver.execute_script(
                    "document.getElementsByClassName('video-stream html5-main-video')[0].volume=0"
                )
            except:
                pass

            if not ad_playing:
                change_resolution(driver)
            
            # main data collection starts here
            while True:
                # play the video if it is not playing
                play_video_if_not_playing(driver)
                # get the player state
                video_playing = driver.execute_script(
                    "return document.getElementById('movie_player').getPlayerState()"
                )

                # check if the ad is playing
                ad_playing = driver.execute_script(
                    "return document.getElementsByClassName('ad-showing').length"
                )
                
                # get the current time of the video in seconds
                video_played_in_seconds = driver.execute_script(
                    'return document.getElementById("movie_player").getCurrentTime()'
                )

                # if the ad appeared at the start of the main-video

                if ad_playing:
                    ad_just_played = True # set it to true
                    print("Ad Playing") # print ad playing

                    # get the buffer-related details of the advert
                    ad_id_list, skippable, ad_buf_details, skip_duration = record_ad_buffer(
                        driver, movie_id
                    )
                    
                    # remove any empty_video ad ids from the list
                    ad_id_list = [
                        ad for ad in ad_id_list if ad != "empty_video"]

                    # iterate through the ad ids
                    for ad_id in range(len(ad_id_list)):
                        if not (skippable[ad_id]):
                            skip_duration[ad_id] = 999 # non-skippable ads have a skip duration of 999 (hardcoded)

                        # print a confirmation message
                        print(
                            "Ad ID: ",
                            ad_id_list[ad_id],
                            "Skippable? ",
                            skippable[ad_id],
                            " Skip Duration: ",
                            skip_duration[ad_id],
                        )
                        
                        # if the ad id is not the movie id, it means this is a unique ad
                        if (str(ad_id_list[ad_id]).strip()) != (str(movie_id).strip()):
                            if ad_id_list[ad_id] != previous_ad_id:
                                # printing the ad id
                                print("Ad id is: ", ad_id_list[ad_id])
                                previous_ad_id = ad_id_list[ad_id] # set the previous ad id to the current ad id

                             # if the ad id is not in the ad buffer information dictionary
                            if len(actual_buffer_reads) >= 1:
                                # append the ad id, buffer size and video played in seconds to the buffer size with ad list
                                buffer_size_with_ad.append(
                                    [
                                        ad_id_list[ad_id],
                                        actual_buffer_reads[-1],
                                        video_played_in_seconds,
                                    ]
                                )
                            else:
                                # append the ad id, buffer size and video played in seconds to the buffer size (0.0) with ad list
                                buffer_size_with_ad.append(
                                    [ad_id_list[ad_id], 0.0,
                                        video_played_in_seconds]
                                )
                            # if the ad id is not in the video info details dictionary meaning it is a unique ad
                            if ad_id_list[ad_id] not in video_info_details.keys():
                                unique_add_count += 1 # increment the unique ad count
                                # add the ad id to the video info details dictionary
                                video_info_details[ad_id_list[ad_id]] = {
                                    "Count": 1,
                                    "Skippable": skippable[ad_id],
                                    "SkipDuration": skip_duration[ad_id],
                                }
                                to_write = {
                                    "buffer": ad_buf_details[ad_id_list[ad_id]],
                                }
                                # add the ad id and buffer information to the ad buffer information dictionary
                                ad_buffer_information[ad_id_list[ad_id]
                                                      ] = to_write
                                # print the confirmation message that the ad data has been collected
                                print("Advertisement " +
                                      str(unique_add_count) + " Data collected.")
                                change_resolution(driver)
                            else:
                                # if the ad id is already in the video info details dictionary
                                current_value = video_info_details[ad_id_list[ad_id]]["Count"]
                                # increment the current count of the ad id
                                video_info_details[ad_id_list[ad_id]
                                                   ]["Count"] = current_value + 1
                                # add the ad id and buffer information to the ad buffer information dictionary
                                name = (
                                    ad_id_list[ad_id]
                                    + "_"
                                    + str(video_info_details[ad_id_list[ad_id]]["Count"])
                                )
                                to_write = {
                                    "buffer": ad_buf_details[ad_id_list[ad_id]],
                                }
                                # add the ad id and buffer information to the ad buffer information dictionary
                                ad_buffer_information[name] = to_write
                                # print the confirmation message that the ad is a repeated ad
                                # and it's information has been collected
                                print("Repeated Ad! Information Added!")
                # if the video has ended
                elif video_playing == 0:
                    # time to write everything to their respective files
                    file_dir = new_dir + "/stream_details.txt"
                    file_dir_two = new_dir + "/buffer_details.txt"
                    file_dir_three = new_dir + "/error_details.txt"
                    file_dir_four = new_dir + "/ResolutionChanges.txt"
                    file_dir_five = new_dir + "/BufferAdvert.txt"
                    file_dir_six = new_dir + "/AdvertBufferState.txt"
                    Main_res = max(main_res_all, key=main_res_all.count)
                    video_info_details["Main_Video"] = {
                        "Url": url,
                        "Total Duration": video_duration_in_seconds,
                        "UniqueAds": unique_add_count,
                        "Resolution": Main_res,
                    }
                    with open(file_dir, "wb+") as f:
                        f.write(orjson.dumps(video_info_details))

                    with open(file_dir_two, "wb+") as f:
                        f.write(orjson.dumps(actual_buffer_reads))

                    with open(file_dir_three, "wb+") as f:
                        f.write(orjson.dumps(error_list))

                    with open(file_dir_five, "wb+") as f:
                        f.write(orjson.dumps(buffer_size_with_ad))

                    with open(file_dir_six, "wb+") as f:
                        f.write(orjson.dumps(ad_buffer_information))
                    video_info_details = {}
                    unique_add_count = 0
                    print("Video Finished and details written to files!")
                    break
                else:
                    # Video is playing normally
                    # get the resolution of the video at each second
                    res = driver.execute_script(
                        'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[2].children[1].textContent.replace(" ","").split("/")[0]'
                    )
                    # all our videos are streamed at 360p.
                    new_data_point = (res, video_played_in_seconds)
                    main_res_all.append(res) # append the resolution to the main resolution list
                    vid_res_at_each_second.append(new_data_point)

                    # Get Current Buffer Size of the video
                    current_buffer = float(
                        driver.execute_script(
                            'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[10].children[1].textContent.split(" ")[1]'
                        )
                    )
                    # if the ad has just played
                    if ad_just_played:
                        # append the buffer size to the buffer size with ad list
                        for i in range(len(buffer_size_with_ad)):
                            # if the buffer size with ad list is empty i.e. less than or equal to 2
                            if len(buffer_size_with_ad[i]) <= 2:
                                buffer_size_with_ad[i].append(current_buffer)

                        ad_just_played = False # set it back to false for the next iteration

                    # Tuple (Buffer, Video Played in seconds timestamp)
                    actual_buffer_reads.append(
                        (current_buffer, video_played_in_seconds))
                    # Current Buffer/(Video Left)
                    try:
                        buffer_ratio = float(
                            current_buffer
                            / (video_duration_in_seconds - video_played_in_seconds)
                        )
                    except:
                        buffer_ratio = 0
                    # append the buffer ratio to the buffer list
                    buffer_list.append(buffer_ratio)
                    previous_ad_id = url.split("=")[1]

        except Exception as e:
            # if an error occurs while collecting data, move to the next video and print the error
            print(e)
            print("Error occured while collecting data! Moving to next video!")
            print("Video: ", url)
            with open("faultyVideos.txt", "a") as f:
                to_write = str(url) + "\n"
                f.write(to_write)

            continue

class InstallError(Exception):
    """
    InstallError class.

    This class represents an exception that is raised when an installation error occurs.

    Attributes:
        message (str): The error message.

    Methods:
        __init__(message: str): Initializes the InstallError object with the given error message.
        __str__(): Returns a string representation of the InstallError object.

    """
    def __init__(self, message: str) -> None:
        """
        __init__ method.

        This method initializes the object with the given error message.

        Args:
            self: The instance of the class.
            message (str): The error message.

        Returns:
            None.
        """
        self.message = message
        super().__init__(self.message)
        
    def __str__(self) -> str:
        """
        __str__ method.

        This method returns a string representation of the object.

        Args:
            self: The instance of the class.

        Returns:
            str: The string representation of the object.
        """
        return f"{self.message}"

class FetchDriverVersion:
    """
    FetchDriverVersion class.

    This class is responsible for fetching the version of the Chrome browser, the corresponding version of the ChromeDriver, and the type of the operating system.

    Attributes:
        version (str): The version of the Chrome browser.
        chromedriver_ver (str): The version of the ChromeDriver.
        os_type (str): The type of the operating system.

    Methods:
        __init__(): Initializes the object and fetches the version of the Chrome browser, the corresponding version of the ChromeDriver, and the type of the operating system.

    """
    def __init__(self) -> None:
        """
        __init__ method.

        This method initializes the object and fetches the version of the Chrome browser, the corresponding version of the ChromeDriver, and the type of the operating system.

        Args:
            self: The instance of the class.

        Returns:
            None.
        """
        self.version: str = subprocess.check_output("google-chrome --version", shell=True).decode("utf-8")
        self.chromedriver_ver: str = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE_" + self.version.split(" ")[2].split(".")[0]).text
        self.os_type: str = sys.platform + str(sys.maxsize.bit_length() + 1)

class InstallDriver(FetchDriverVersion):
    """
    InstallDriver class.

    This class extends the FetchDriverVersion class and is responsible for setting the options for the Chrome Driver and installing the Chrome Driver.

    Attributes:
        mobile_emulation (dict): The mobile emulation settings for the Chrome Driver.

    Methods:
        __init__(): Initializes the InstallDriver object and sets the options for the Chrome Driver.
        install(): Installs the Chrome Driver.

    """
    mobile_emulation = {
        "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
    }

    def __init__(self) -> None:
        """
        __init__ method.

        This method initializes the object and sets the options for the Chrome Driver.

        Args:
            self: The instance of the class.

        Returns:
            None.
        """
        super().__init__()
        self.chrome_options: Options = Options()
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.set_capability(
            "loggingPrefs", {'performance': 'ALL'})
        self.chrome_options.add_experimental_option(
            "mobileEmulation", self.mobile_emulation)

    def install(self) -> str:
        """
        install method.

        This method installs the Chrome Driver.

        Args:
            self: The instance of the class.

        Returns:
            str: The path to the Chrome Driver.

        Raises:
            InstallError: If the Chrome Driver installation fails.
        """

        try:
            return ChromeDriverManager(
                version=self.chromedriver_ver,  name='chromedriver', os_type=self.os_type, path=os.getcwd()
            ).install()
        except:
            raise InstallError("Could not install Chrome Driver!")

chrome_opt = InstallDriver().chrome_options
chrome_ser = InstallDriver().install()
driver = webdriver.Chrome(service=ChromeService(
    executable_path=chrome_ser), options=chrome_opt)
filename = sys.argv[1]
driver_code(driver, filename)
driver.quit()
