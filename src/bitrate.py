import os
import asyncio
import numpy as np
from yt_dlp import YoutubeDL
import pandas as pd

ERROR_LOGS = []
new_count = 0
rootdir = "./"
count = len(next(os.walk(rootdir))[1])
bitrates_720, bitrates_360 = [], []

async def get_urls():
    p360 = pd.read_csv("./360p_cleaned.csv")
    p720 = pd.read_csv("./720p_cleaned.csv")
    urls_720, urls_360 = p720["Main_Video_Url"].tolist(), p360["Main_Video_Url"].tolist()
    return urls_720, urls_360

async def process_bitrates(bitrates: list):
    try:
        return float(bitrates[0]) if len(bitrates) == 1 else float(np.mean(bitrates))
    except Exception:
        return -123

async def get_bitrate(url: str, res: str) -> float:
    video_id = url.split("=")[1]
    ops = {
        "format": f"bestvideo[ext=mp4]/best[ext=webm]+bestvideo[height={res}]",
        "outtmpl": f"./{video_id}.mp4",
        "quiet": False,
    }
    bitrates = []
    try:
        with YoutubeDL(ops) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            formats = info_dict.get("formats", None)                
            bitrates.extend(
                f['vbr']
                for f in formats
                if f["height"] == int(res) and f['vbr']
            )
        print(bitrates)
    except Exception as e:
        print(e)
        ERROR_LOGS.append([e, url, res])

    return await process_bitrates(bitrates)

async def get_bitrates(urls: list, res: str) -> list:
    print(f'Getting bitrates for {res}')
    bitrates = []
    for url in urls:
        bitrate = await get_bitrate(url, res)
        bitrates.append(bitrate)
    return bitrates

async def main():
    urls_720, urls_360 = await get_urls()
    bitrates_720 = await get_bitrates(urls_720, "720")
    bitrates_360 = await get_bitrates(urls_360, "360")
    return bitrates_720, bitrates_360

async def create_csv():
    bitrates_720, bitrates_360 = await main()
    df = pd.DataFrame({"720p": bitrates_720, "360p": bitrates_360})
    df.to_csv("./bitrates.csv", index=False)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(create_csv())
    loop.close()
