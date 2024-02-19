# !/usr/bin/python3

from yt_dlp import YoutubeDL
import os
import json
import asyncio

ROOTDIR = "./"
count = 0

async def get_duration(vid_id: str):
    ydl_opts = {
        'quiet': False,
        'simulate': True,
        'dump_single_json': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(vid_id, download=False)
            return float(info_dict['duration'])
    except Exception as e:
        print(e)
        return 0
    
async def main():
    global count
    for (subdir, _, files) in os.walk(ROOTDIR):
        for file in files:
            if file == "stream_details.txt":
                path = os.path.join(subdir, file)
                new_dict = {}
                with open(path) as f:
                    new_dict: dict = json.load(f)
                    id_list = list(new_dict.keys())
                    for id in id_list:
                        if id == "Main_Video":
                            continue
                        new_id = id.strip()
                        try:
                            time_in_seconds = await get_duration(new_id)
                            print(f'Found duration for {new_id} in {subdir}')
                        except Exception as e:
                            print(e)
                            print(f'Could not find duration for {new_id} in {subdir}')
                            continue
                        new_dict[id]["Duration"] = time_in_seconds
                with open(path, 'w') as f:
                    f.write(json.dumps(new_dict, indent=4))
                count += 1
                print(f'Finished {count} files')
    print('Added Time!')

if __name__ == "__main__":
    asyncio.run(main())