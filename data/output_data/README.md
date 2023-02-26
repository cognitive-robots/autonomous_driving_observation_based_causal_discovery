# Output Data

## Graphs
Contains the graphs produced during the benchmark evaluation for every driving scenario scene. Files are stored based upon the following paths:

    {dataset}/{variable}/{max_time_lag}/{sig_alpha}/{method}_{i}
    
Graphs are stored in the binary format used by the networkx Python package.

## Performance Average
Contains performance statistics from the benchmark evaluation across each combination of parameters. Files are stored based upon the following paths:

    {max_time_lag}/{sig_alpha}/{method}_{dataset}_{variable}

Performance statistics are stored in formatted plaintext.

## Performance Detail
Contains performance details from the benchmark evaluation for every driving scenario scene. Files are stored based upon the following paths:

    {max_time_lag}/{sig_alpha}/{method}_{dataset}_{variable}.csv
    
Performance details are stored in CSV format with each row corresponding to a single scene for the combination of parameters specified by the file path.
