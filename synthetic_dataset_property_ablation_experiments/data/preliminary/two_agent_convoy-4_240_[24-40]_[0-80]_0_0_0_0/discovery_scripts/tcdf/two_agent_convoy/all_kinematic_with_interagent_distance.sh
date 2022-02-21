#!/bin/bash

if [ "$#" -eq 4 ]
then
	SCRIPT_DIR_PATH=$1
	INPUT_DIR_PATH=$2
	OUTPUT_DIR_PATH=$3
else
	SCRIPT_DIR_PATH=/home/rhoward/development/python/TCDF
	INPUT_DIR_PATH=/home/rhoward/development/datasets/synthetic/4_240_24_40_0_80/scenario/two_agent_convoy/all_kinematic_with_interagent_distance
	OUTPUT_DIR_PATH=/home/rhoward/development/datasets/synthetic/4_240_24_40_0_80/discovered/tcdf/two_agent_convoy/all_kinematic_with_interagent_distance
fi

echo "Script Directory Path: $SCRIPT_DIR_PATH"
echo "Input Directory Path: $INPUT_DIR_PATH"
echo "Output Directory Path: $OUTPUT_DIR_PATH"

for input_scenario_file in $(ls $INPUT_DIR_PATH);
do
	$SCRIPT_DIR_PATH/runTCDF.py --data "$INPUT_DIR_PATH/$input_scenario_file" --output-file-path "$OUTPUT_DIR_PATH/${input_scenario_file/.csv/.json}" --hidden_layers 2 --epochs 5000
done
