#! /bin/bash

for folder in "$PWD"/*-*/; do
    cd "$folder/trending"
    for subfolder in *; do
        if [ "$subfolder" == ".wdm" ]; then
            rm -rf "$subfolder"
        fi
        newname=$(uuidgen)
        if [ "$subfolder" != ".wdm" ]; then
            mv "$subfolder" "$newname"
        fi
    done
    cp -r * "/media/harris-ahmad/36e3f217-e34c-4138-8628-41f4ef8b5f33/work/Germany/trending"
    cd ..
    cd "non-trending"
    for subfolder in *; do
        if [ "$subfolder" == ".wdm" ]; then
            rm -rf "$subfolder"
        fi
        newname=$(uuidgen)
        if [ "$subfolder" != ".wdm" ]; then
            mv "$subfolder" "$newname"
        fi
    done
    cp -r * "/media/harris-ahmad/36e3f217-e34c-4138-8628-41f4ef8b5f33/work/Germany/non-trending"
    cd ..
done

cd ..

cd "/media/harris-ahmad/36e3f217-e34c-4138-8628-41f4ef8b5f33/work/Germany/trending"
find . -maxdepth 1 -type f -not -name "*.py" -not -name "*.sh" -delete

for i in $(seq 1 10)
do
    mkdir "trend-$i"
done

i=0
for dir in *; do
    if [ "$dir" != "trend-1" ] && [ "$dir" != "trend-2" ] && [ "$dir" != "trend-3" ] && [ "$dir" != "trend-4" ] && [ "$dir" != "trend-5" ] && [ "$dir" != "trend-6" ] && [ "$dir" != "trend-7" ] && [ "$dir" != "trend-8" ] && [ "$dir" != "trend-9" ] && [ "$dir" != "trend-10" ]; then
        i=$((i+1))
        trending_dir_index=$((i%10))
        if [ "$trending_dir_index" -eq 0 ]; then
            trending_dir_index=10
        fi
        cp -r "$dir" "trend-$trending_dir_index"
    fi
done

# loop through the 10 trending directories, and copy the "cleanup.py", "get_bytes.py", "get_res.py", and "add_time.py" scripts to each of them
for i in $(seq 1 10)
do
  cd "trend-$i"
  cp "/media/harris-ahmad/36e3f217-e34c-4138-8628-41f4ef8b5f33/work/CSVs/Germany/cleanup.py" .
  cp "/media/harris-ahmad/36e3f217-e34c-4138-8628-41f4ef8b5f33/work/CSVs/Germany/get_bytes.py" .
  cp "/media/harris-ahmad/36e3f217-e34c-4138-8628-41f4ef8b5f33/work/CSVs/Germany/get_res.py" .
  cp "/media/harris-ahmad/36e3f217-e34c-4138-8628-41f4ef8b5f33/work/CSVs/Germany/add_time.py" .
  cp "/media/harris-ahmad/36e3f217-e34c-4138-8628-41f4ef8b5f33/work/CSVs/Germany/rename.py" .
  cd ..
done

# spwan 10 processes to run the cleanup.py script on each of the 10 trending directories
for i in $(seq 1 10)
do
  cd "trend-$i"
  python3 cleanup.py &
  pid=$!
  ps -p $pid
  wait $pid
  cd ..
done

for i in $(seq 1 10)
do
  gnome-terminal --tab --title="trend-$i" -- bash -c "cd trend-$i; python3 add_time.py; exec bash"
done

for i in $(seq 1 10)
do
    echo "trend-$i"
    cd "trend-$i"
    rm -rf .wdm
    cd ..
done

for i in $(seq 1 10)
do
  gnome-terminal --tab --title="trend-$i" -- bash -c "cd trend-$i; python3 get_res.py; exec bash"
done

for i in $(seq 1 10)
do
  gnome-terminal --tab --title="trend-$i" -- bash -c "cd trend-$i; python3 get_bytes.py; exec bash"
done

echo "Non-Trending"
cd "/media/harris-ahmad/36e3f217-e34c-4138-8628-41f4ef8b5f33/work/Germany/non-trending"

find . -maxdepth 1 -type f -not -name ".py" -not -name ".sh" -delete

for i in $(seq 1 10)
do
    mkdir "non-trend-$i"
done

i=0
for dir in *; do
    if [ "$dir" != "non-trend-1" ] && [ "$dir" != "non-trend-2" ] && [ "$dir" != "non-trend-3" ] && [ "$dir" != "non-trend-4" ] && [ "$dir" != "non-trend-5" ] && [ "$dir" != "non-trend-6" ] && [ "$dir" != "non-trend-7" ] && [ "$dir" != "non-trend-8" ] && [ "$dir" != "non-trend-9" ] && [ "$dir" != "non-trend-10" ]; then
        i=$((i+1))
        nontrending_dir_index=$((i%10))
        if [ "$nontrending_dir_index" -eq 0 ]; then
            nontrending_dir_index=10
        fi
        cp -r "$dir" "non-trend-$nontrending_dir_index"
    fi
done

# loop through the 10 trending directories, and copy the "cleanup.py", "get_bytes.py", "get_res.py", and "add_time.py" scripts to each of them
for i in $(seq 1 10)
do
  cd "non-trend-$i"
  cp "/media/harris-ahmad/36e3f217-e34c-4138-8628-41f4ef8b5f33/work/CSVs/Germany/cleanup.py" .
  cp "/media/harris-ahmad/36e3f217-e34c-4138-8628-41f4ef8b5f33/work/CSVs/Germany/get_bytes.py" .
  cp "/media/harris-ahmad/36e3f217-e34c-4138-8628-41f4ef8b5f33/work/CSVs/Germany/get_res.py" .
  cp "/media/harris-ahmad/36e3f217-e34c-4138-8628-41f4ef8b5f33/work/CSVs/Germany/add_time.py" .
  cp "/media/harris-ahmad/36e3f217-e34c-4138-8628-41f4ef8b5f33/work/CSVs/Germany/rename.py" .
  cd ..
done

# spwan 10 processes to run the cleanup.py script on each of the 10 trending directories
for i in $(seq 1 10)
do
  cd "non-trend-$i"
  python3 cleanup.py &
  pid=$!
  ps -p $pid
  wait $pid
  cd ..
done

for i in $(seq 1 10)
do
  gnome-terminal --tab --title="non-trend-$i" -- bash -c "cd non-trend-$i; python3 add_time.py; exec bash"
done

for i in $(seq 1 10)
do
    echo "non-trend-$i"
    cd "non-trend-$i"
    rm -rf .wdm
    cd ..
done

for i in $(seq 1 10)
do
  gnome-terminal --tab --title="non-trend-$i" -- bash -c "cd non-trend-$i; python3 get_res.py; exec bash"
done

for i in $(seq 1 10)
do
  gnome-terminal --tab --title="non-trend-$i" -- bash -c "cd non-trend-$i; python3 get_bytes.py; exec bash"
done