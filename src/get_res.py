from collections import Counter
import asyncio
import json
import os

ROOTDIR = "./"

async def get_res(dir: str, video_id: str) -> str:
    print(f'[get_res] Getting resolution for {video_id} in {dir}')
    path = os.path.join(dir, 'AdvertBufferState.txt')
    buff = []
    resolutions = []
    with open(path, 'r') as f:
        state = json.loads(f.read())
        buff = state[video_id]['buffer']
    for item in buff:
        buff, _, recorded_res = item
        resolutions.append(recorded_res)
    return Counter(resolutions).most_common()[0][0].strip()

async def main():
    for (subdir, _, files) in os.walk(ROOTDIR):
        for file in files:
            if file == "stream_details.txt":
                path = os.path.join(subdir, file)
                new_dict: dict = {}
                with open(path, 'r') as f:
                    new_dict = json.loads(f.read())
                    id_list = list(new_dict.keys())
                    for video_id in id_list:
                        if video_id == "Main_Video":
                            continue
                        res = await get_res(subdir, video_id)
                        new_dict[video_id]["Resolution"] = res
                with open(path, 'w') as f:
                    f.write(json.dumps(new_dict, indent=4))
    print("Added Resolutions!")

if __name__ == "__main__":
    asyncio.run(main())
