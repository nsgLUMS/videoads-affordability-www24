# !/usr/bin/bash

# Running the trending scraper
echo "Running the trending scraper"

python3 S1.py -t &
pid=$!
ps $pid
wait $pid
if ps -p $pid > /dev/null; then
    kill $pid
fi

# echo "Trending scraper completed"

# Running the non-trending scraper
echo "Running the non-trending scraper"

python3 S1.py -n &
pid=$!
ps $pid
wait $pid
if ps -p $pid > /dev/null; then
    kill $pid
fi
echo "Non-trending scraper completed"

folder_name=$(date +"%d-%m-%Y")

mkdir $folder_name
cd $folder_name

mkdir trending 
mkdir non-trending

cd trending
touch trending-1.txt trending-2.txt trending-3.txt trending-4.txt

# move trending_videos_shorter_than_hour.txt and trending_videos_longer_than_hour.txt to the trending folder
cp ../../trending_videos_shorter_than_hour.txt .
cp ../../trending_videos_longer_than_hour.txt .

echo "Creating files for trending videos"
# calculate the number of lines in the file trending_videos_shorter_than_hour.txt and store it in a variable
num_lines_shorter_than_hour=$(wc -l trending_videos_shorter_than_hour.txt | cut -d " " -f 1)

# check if the number of lines is divisible by 4. if not, then remove the last line from the file
if [ $(($num_lines_shorter_than_hour % 4)) -ne 0 ]
then
    num_lines_shorter_than_hour=$(($num_lines_shorter_than_hour - 1))
fi

# remove the last line from the file
cp trending_videos_shorter_than_hour.txt foo.txt.tmp
sed '$ d' foo.txt.tmp > trending_videos_shorter_than_hour.txt
rm -f foo.txt.tmp

# divide the number of lines by 4 and store it in a variable
num_lines_per_file_shorter_than_hour=$(($num_lines_shorter_than_hour / 4))

# divide the file trending_videos_shorter_than_hour.txt into 4 files with equal number of lines. 
# the first file will have the first $num_lines_per_file_shorter_than_hour lines, the second file will have the next $num_lines_per_file_shorter_than_hour lines and so on.
split -l $num_lines_per_file_shorter_than_hour trending_videos_shorter_than_hour.txt trending-.txt

mv trending-.txtaa trending-1.txt
mv trending-.txtab trending-2.txt
mv trending-.txtac trending-3.txt
mv trending-.txtad trending-4.txt

rm -rf trending-.txt*

# find the number of lines in the file trending_videos_longer_than_hour.txt and store it in a variable
num_lines_longer_than_hour=$(wc -l trending_videos_longer_than_hour.txt | cut -d " " -f 1)

if [ $num_lines_longer_than_hour -lt 4 ]
then
    for i in $(seq 1 $num_lines_longer_than_hour)
    do
        line=$(sed -n "$i p" trending_videos_longer_than_hour.txt)
        echo $line >> trending-$i.txt
    done
else
    if [ $(($num_lines_longer_than_hour % 4)) -ne 0 ]
    then
        num_lines_longer_than_hour=$(($num_lines_longer_than_hour - 1))
    fi

    for i in $(seq 1 4)
    do
        line=$(sed -n "$i p" trending_videos_longer_than_hour.txt)
        echo $line >> trending-$i.txt
    done

    if [ $num_lines_longer_than_hour -gt 4 ]
    then
        for i in $(seq 5 $num_lines_longer_than_hour)
        do
            line=$(sed -n "$i p" trending_videos_longer_than_hour.txt)
            echo $line >> trending-4.txt
        done 
    fi
fi

echo "Trending done!"

echo "Creating files for non-trending videos"

cd ../non-trending
touch non-1.txt non-2.txt non-3.txt non-4.txt

cp ../../non_trending_shorter_than_hour.txt .
cp ../../non_trending_shorter_than_max_duration.txt .

num_lines_shorter_than_hour=$(wc -l non_trending_shorter_than_hour.txt | cut -d " " -f 1)

if [ $(($num_lines_shorter_than_hour % 4)) -ne 0 ]
then
    num_lines_shorter_than_hour=$(($num_lines_shorter_than_hour - 1))
fi

cp non_trending_shorter_than_hour.txt foo.txt.tmp
sed '$ d' foo.txt.tmp > non_trending_videos_shorter_than_hour.txt
rm -f foo.txt.tmp

num_lines_per_file_shorter_than_hour=$(($num_lines_shorter_than_hour / 4))

split -l $num_lines_per_file_shorter_than_hour non_trending_shorter_than_hour.txt non-.txt

mv non-.txtaa non-1.txt
mv non-.txtab non-2.txt
mv non-.txtac non-3.txt
mv non-.txtad non-4.txt

rm -rf non-.txt*

num_lines_longer_than_max_duration_non_trending=$(wc -l non_trending_shorter_than_max_duration.txt | cut -d " " -f 1)

if [ $num_lines_longer_than_max_duration_non_trending -lt 4 ]
then
    for i in $(seq 1 $num_lines_longer_than_max_duration_non_trending)
    do
        line=$(sed -n "$i p" non_trending_shorter_than_max_duration.txt)
        echo $line >> non-$i.txt
    done
else
    if [ $(($num_lines_longer_than_max_duration_non_trending % 4)) -ne 0 ]
    then
        num_lines_longer_than_max_duration_non_trending=$(($num_lines_longer_than_max_duration_non_trending - 1))
    fi

    for i in $(seq 1 4)
    do
        line=$(sed -n "$i p" non_trending_shorter_than_max_duration.txt)
        echo $line >> non-$i.txt
    done

    if [ $num_lines_longer_than_max_duration_non_trending -gt 4 ]
    then
        for i in $(seq 5 $num_lines_longer_than_max_duration_non_trending)
        do
            line=$(sed -n "$i p" non_trending_shorter_than_max_duration.txt)
            echo $line >> non-4.txt
        done 
    fi
fi

echo "Non Trending done!"

echo "Running the Trending Scripts"
# copy the file S2.py from the current directory to both the trending and non-trending directories
cp ../../S2.py .

# navigate to the trending directory
cd ../trending

# copy S2.py to the trending directory
cp ../../S2.py .

trending_files=$(ls -1 trending-*.txt | wc -l)

# run the S2.py script for each trending file
for i in $(seq 1 $trending_files)
do
    file_name=$(ls -1 trending-*.txt | sed -n "$i p")
    gnome-terminal --tab --title="$file_name" -- bash -c "python3 S2.py $file_name; exec bash"
    sleep 4
done

gnome-terminal --tab --title="trending-1.txt" -- bash -c "python3 S2.py trending-1.txt; exec bash"
sleep 4
gnome-terminal --tab --title="trending-2.txt" -- bash -c "python3 S2.py trending-2.txt; exec bash"
sleep 4
gnome-terminal --tab --title="trending-3.txt" -- bash -c "python3 S2.py trending-3.txt; exec bash"
sleep 4
gnome-terminal --tab --title="trending-4.txt" -- bash -c "python3 S2.py trending-4.txt; exec bash"

echo "Running the Non-Trending Scripts"

# navigate to the non-trending directory
cd ../non-trending

# copy S2.py to the non-trending directory
cp ../../S2.py .

nontrending_files=$(ls -1 non-*.txt | wc -l)

# run the S2.py script for each non-trending file
for i in $(seq 1 $nontrending_files)
do
    file_name=$(ls -1 non-*.txt | sed -n "$i p")
    gnome-terminal --tab --title="$file_name" -- bash -c "python3 S2.py $file_name; exec bash"
    sleep 4
done

echo "All done!"