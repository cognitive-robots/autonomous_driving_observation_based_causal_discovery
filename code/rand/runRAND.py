#!/usr/bin/python3

import os
import argparse
import csv
import json
import random
import time
import numpy as np

link_likelihood = 0.5

def create_RAND_config_file(output_file_path):
    output_file_path_dir, _ = os.path.split(output_file_path)
    if not os.path.isdir(output_file_path_dir):
        raise ValueError(f"Output file path parent directory {output_file_path_dir} is not a valid directory")

    config = {
        "link_likelihood": str(link_likelihood)
    }

    with open(output_file_path, 'w') as output_file:
        json.dump(config, output_file)

def runRAND(scenario_file_path, output_file_path):
    start_time = time.time()

    if not os.path.isfile(scenario_file_path):
        raise ValueError(f"Scenario CSV file path {scenario_file_path} is not a valid file")

    if output_file_path is not None:
        output_file_path_dir, _ = os.path.split(output_file_path)
        if not os.path.isdir(output_file_path_dir):
            raise ValueError(f"Output file path parent directory {output_file_path_dir} is not a valid directory")

    with open(scenario_file_path, "r") as input_file:
        csv_reader = csv.DictReader(input_file)
        data_rows = []
        variables = []
        for row in csv_reader:
            data_row = np.zeros(len(row.keys()))
            for (i, key) in enumerate(row.keys()):
                data_row[i] = row[key]
                if len(data_rows) == 0:
                    variables.append(key)
                    print(f"Data column {i} is variable '{key}'")
            data_rows.append(data_row)
        data = np.stack(data_rows)

        if output_file_path is not None:
            with open(output_file_path, "w") as output_file:
                json_data = { "variables": {}, "runtime": time.time() - start_time }
                for i in range(len(variables)):
                    variable = variables[i]
                    json_data["variables"][variable] = { "parents": [] }
                    for other_variable in variables:
                        if other_variable != variable and random.random() > link_likelihood:
                            json_data["variables"][variable]["parents"].append(other_variable)
                json.dump(json_data, output_file)
                print(f"Output results to file path {output_file_path}")

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Attempts causal discovery on a scenario CSV file")
    arg_parser.add_argument("scenario_file_path")
    arg_parser.add_argument("--output-file-path")
    args = arg_parser.parse_args()

    runRAND(scenario_file_path, output_file_path)
