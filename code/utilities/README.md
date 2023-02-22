# CSV Resampling Scripts
## Resample CSV Data
Resamples CSV data via interpolation in order to produce data that reflects a new frame capture frequency.

    usage: resample_csv_data.py [-h] input_file_path input_frequency output_file_path output_frequency
    
Parameters:
* input_file_path: File path specifying input CSV file.
* input_frequency: Specifies the frame capture frequency of the input CSV file.
* output_file_path: File path specifying desired output CSV file location.
* output_frequency: Specifies the desired frame capture frequency of the output CSV file.
* -h: Displays the help message for the script.
