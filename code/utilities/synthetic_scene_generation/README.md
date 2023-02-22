# Synthetic Scene Generation

## Create Two Agent Convoy Scene
Generates a synthetic two agent convoy scenario scenes based upon a configurable number of convoy and independent actions (actions correspond to speed goal changes), with agent behaviour determined by PID controllers.

    usage: create_two_agent_convoy_scene.py [-h] output_file_path
    
Parameters:
* output_file_path: File path to output generated scenes to.
* -h: Displays the help message for the script.

## Create Two Agent Convoy Scenes
Creates a batch of synthetic two agent convoy scenario scenes utilising the script described above.

    usage: create_two_agent_convoy_scenes.py [-h] [--variable VARIABLE] [--scene_count SCENE_COUNT] output_dir_path
    
Parameters:
* output_dir_path: Directory path to output generated scenes to.
* -h: Displays the help message for the script.
* --variable: Variable to base the scenarios upon. Supports "acceleration" or "velocity".
* --scene_count: Specifies the number of scenes to be generated.
