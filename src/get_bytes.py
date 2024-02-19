import os
import asyncio
import json
from yt_dlp import YoutubeDL
from pprint import pprint

ERROR_LOGS = []
new_count = 0
rootdir = "./"
count = len(next(os.walk(rootdir))[1])

async def process_filesizes(filesizes: list):
    if not filesizes:
        raise ValueError("No filesizes found")
    try:
        return float(filesizes[0]) if len(filesizes) == 1 else float(filesizes[2])
    except:
        raise Exception("length of filesizes list is not 1 or 4")

async def get_bytes(url: str, res: str) -> float:
    video_id = url.split("=")[1]
    res = int(res.split("x")[1])
    ops = {
        "format": f"bestvideo[ext=mp4]/best[ext=webm]+bestvideo[height={res}]",
        "outtmpl": f"./{video_id}.mp4",
        "quiet": False,
    }
    filesizes = []
    try:
        with YoutubeDL(ops) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict['formats']
            filesizes.extend(
                f['filesize']
                for f in formats
                if f.get('height', None) == res and f.get('filesize', None)
            )
    except Exception as e:
        print(e)
        ERROR_LOGS.append([e, url, res])
    
    to_return = await process_filesizes(filesizes)
    print(f'[done] {to_return}')
    return to_return
    
async def main():
    global new_count
    for (subdir, _, files) in os.walk(rootdir):
        for file in files:
            if file == "stream_details.txt":
                print(f'In folder {subdir}')
                path = os.path.join(subdir, file)
                new_dict = None
                with open(path) as f:
                    stream_file = json.loads(f.read())
                    for item in stream_file:
                        if item == "Main_Video":
                            url: str = ""
                            res: str = ""
                            try:
                                url = stream_file[item]["Url"]
                                res = stream_file[item]["Resolution"]
                            except AttributeError as e:
                                print(e)
                                continue
                            native: float = 0.0
                            try:
                                native = await get_bytes(url, res)
                                print(f'[done] {native}')
                            except Exception as e:
                                print(e)
                                ERROR_LOGS.append([e, url, res])
                                continue    
                            stream_file["Main_Video"]["Size"] = native
                        else:
                            url = f'https://www.youtube.com/watch?v={item}'
                            res = stream_file[item]["Resolution"]
                            try:
                                native = await get_bytes(url, res)
                                print(f'[done] {native}')
                            except Exception as e:
                                print(e)
                                ERROR_LOGS.append([e, url, res])
            
                            stream_file[item]["Size"] = native
                    new_dict = stream_file
                print("")
                print(f'{new_count}/{count} Done')
                new_count += 1
                if new_dict:
                    with open(path, "w") as f:
                        f.write(json.dumps(new_dict, indent=4))
                else:
                    print("new_dict is None")
                    

if __name__ == "__main__":
    asyncio.run(main())