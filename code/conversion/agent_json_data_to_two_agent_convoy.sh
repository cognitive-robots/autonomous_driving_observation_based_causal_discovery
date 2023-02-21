#!/bin/bash

SCRIPT_DIR_PATH=$1
INPUT_DIR_PATH=$2
OUTPUT_DIR_PATH=$3

echo "Script Directory Path: $SCRIPT_DIR_PATH"
echo "Input Directory Path: $INPUT_DIR_PATH"
echo "Output Directory Path: $OUTPUT_DIR_PATH"

for input_scene_command_file in scene_commands/*.sh;
do
	eval $(<$input_scene_command_file)
done
