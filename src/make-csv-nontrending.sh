cd "$HOME/non-trending"

# get the total count of subdirectories in the "non-trending" folder
num_subdirs=$(ls -l | grep -c ^d)
echo "Number of subdirectories in the non-trending folder: $num_subdirs"

# run the cleanup.py file in non-trending folder
python3 cleanup.py &
pid=$!
ps $pid
wait $pid
if ps -p $pid > /dev/null; then
    kill $pid
fi

# get the updated count of subdirectories in the "non-trending" folder
num_subdirs=$(ls -l | grep -c ^d)
echo "Number of subdirectories in the non-trending folder after cleanup: $num_subdirs"

# now run the add_time.py file in the non-trending folder and wait until the process finishes
python3 add_time.py &
pid=$!
ps $pid
wait $pid
if ps -p $pid > /dev/null; then
    kill $pid
fi

# now run the get_res.py file in the non-trending folder and wait until the process finishes
python3 get_res.py &
pid=$!
ps $pid
wait $pid
if ps -p $pid > /dev/null; then
    kill $pid
fi

# now run the get_bytes.py file in the non-trending folder and wait until the process finishes
python3 get_bytes.py &
pid=$!
ps $pid
wait $pid
if ps -p $pid > /dev/null; then
    kill $pid
fi

echo "Now run the jupyter notebook to create the csv file"