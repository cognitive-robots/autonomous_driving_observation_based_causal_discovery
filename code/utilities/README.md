# Utilities

## Resample CSV Data
Resamples CSV data via interpolation in order to produce data that reflects a new frame capture frequency.

    usage: resample_csv_data.py [-h] input_file_path input_frequency output_file_path output_frequency
    
Parameters:
* input_file_path: File path specifying input CSV file.
* input_frequency: Specifies the frame capture frequency of the input CSV file.
* output_file_path: File path specifying desired output CSV file location.
* output_frequency: Specifies the desired frame capture frequency of the output CSV file.
* -h: Displays the help message for the script.

## Scene Length Statistics
Provides statistics regarding the length of scenes specified by the wildcard supplied.

    usage: scene_length_stats.py [-h] [--sampling-frequency SAMPLING_FREQUENCY] scene_file_path_wildcard

Parameters:
* scene_file_path_wildcard: Specifies a file path wildcard that dictates which files will be considered when calculating the scene length statistics.
* -h: Displays the help message for the script.
* --sampling-frequency: Specifies the expected sampling rate for the specified scenes.
