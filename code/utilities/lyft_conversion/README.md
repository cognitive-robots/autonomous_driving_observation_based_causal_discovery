# Lyft Conversion
Scripts specific to this paper for converting Lyft scenes from an intermediary data format to two-agent convoy scenario scenes stored in a CSV format.

## Scene Commands
Individual scripts used to convert from intermediary agent data to two agent convoy scenarios that causal discovery can be carried out on.

## Agent JSON Data to Two Agent Convoy
Converts an entire directory of intemediary agent data files to two agent convoy scenario files that causal discovery can be carried out on.

    usage: agent_json_data_to_two_agent_convoy.sh script_dir_path input_dir_path output_dir_path
  
Parameters:
* script_dir_path: Path to directory containing conversion script. Conversion scripts can be found at https://github.com/cognitive-robots/lyft_prediction_dataset_tools/.
* input_dir_path: Path to directory to take input intemediary agent data files from.
* output_dir_path: Path to directory to output two agent convoy scenarios to.
