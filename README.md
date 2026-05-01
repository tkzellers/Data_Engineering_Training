# Data_Engineering_Training

#Amplitude Project

# Amplitude Export Script

## Summary

This script connects to the Amplitude Export API, downloads event data for a range of dates, unzips it, and converts that data into JSON.

## In More Detail

### 1. The Connection to the Amplitude Export API

1. Uses the `requests` Python library ([link to docs](https://pypi.org/project/requests/))
2. Currently configured only for the **EU Residency Server**
3. Uses a set of API keys specific to The Information Lab
4. See the documentation for more details: [Export API | Amplitude](https://amplitude.com/docs/apis/analytics/export#)

### 2. Downloading the Data

1. Currently hardcoded to produce event data for the **past 24 hours**
2. Will print an error and stop if the connection is not successful
3. Raw data is downloaded and written into memory, not to disk

### 3. Unzipping and Formatting the Data

1. The raw data is unzipped into a directory called `amplitude_data` (automatically created).
2. The raw data comes in the form of a zipped folder, which contains gzipped files of lines of JSON.
   1. Note: the folder is named `100011471`, which is specific to The Information Lab. This directory is **hard-coded** in the script for now.
3. Each gzipped `.json` file contains lines of JSON (one line for each object).
4. These lines of JSON are converted into a single JSON array.
5. This JSON array is then written to a file, with a name corresponding to the date+hour as indicated by the filename as it came out of the Amplitude API.
   1. So each file contains an array of event objects for a particular hour on a particular day.
6. These files are **written into that same `amplitude_data` directory for now**.

## Planned Improvements

1. Add logging for better debugging and monitoring
2. Make date selection dynamic
3. Make the API base URL dynamic in case someone wants to use this outside the EU
4. Unpack the zipped folder and avoid hard-coding the directory path with TIL’s ID
5. Add code to instead put these files into an S3 bucket (loading!)
