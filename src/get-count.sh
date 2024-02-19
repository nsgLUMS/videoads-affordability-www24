#! /bin/bash

# Usage:
# Place this script in the folder where you have your dated folders. Before running the script
# extract all sub-folders from the zip archives. 
# Note:
# Every dated folder must have two subdirectories named "trending" and "non-trending". These dated folders
# must be three levels deep at maximum.
# 
# This shell script gives you the total count of trending and non-trending videos contained in the entire dataset
# for a given country.


numberOfWdmFoldersTrending=$(find . -maxdepth 1 -type d -not -path "." | wc -l)
numberOfWdmFoldersNonTrending=$(find . -maxdepth 1 -type d -not -path "." | wc -l)
totalTrendingNonEmpty=$(find . -mindepth 3 -type d -not -path "*/.wdm/*" -not -path "*/non-trending/*" -not -path "." | wc -l)

totalTrendingNonEmpty=$(($totalTrendingNonEmpty - $numberOfWdmFoldersTrending))

totalTrendingEmpty=$(find . -mindepth 3 -type d -empty -not -path "*/.wdm/*" -not -path "*/non-trending/*" -not -path "." | wc -l)
totalNonTrendingNonEmpty=$(find . -mindepth 3 -type d -not -path "*/.wdm/*" -not -path "*/trending/*" -not -path "." | wc -l)

totalNonTrendingNonEmpty=$(($totalNonTrendingNonEmpty - $numberOfWdmFoldersNonTrending))

totalNonTrendingEmpty=$(find . -mindepth 3 -type d -empty -not -path "*/.wdm/*" -not -path "*/trending/*" -not -path "." | wc -l)

echo "==== COUNT ===="
echo "Total trending non-empty: $totalTrendingNonEmpty"
echo "Total trending empty: $totalTrendingEmpty"
echo "Total non-trending non-empty: $totalNonTrendingNonEmpty"
echo "Total non-trending empty: $totalNonTrendingEmpty"
echo "==============="
