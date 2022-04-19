# Experiment Scripts
Most scripts have their documentation in their respective directories/repositories with the exception of the synthetic albation experiments script.

## Run Synthetic Ablation Experiments
The central script for running the synthetic data generation parameter ablation experiments. Note that only the approaches specified via flags will be included in the experiments. This can be combined with --skip-existing in order to carry out experimentation with some approaches before others. This can be useful to carry out experiments with the faster approaches first to enable evaluation of these results while waiting for experiments to run with other slower approaches.

    usage: run_synthetic_ablation_experiments.py [-h] [--skip-existing] [--rand] [--pcmci] [--tcdf] output_file_path
    
Parameters:
* output_file_path: Path to directory to output experiment data to.
* -h: Displays the help message for the script.
* --skip-existing: Will check for the presence of files before carrying out experiment steps and skip experiment steps if relevant files have been output already.
* --rand: Include the random causal discovery approach in experiments.
* --pcmci: Include the PCMCI approach in experiments.
* --tcdf: Include the TCDF approach in experiments.
