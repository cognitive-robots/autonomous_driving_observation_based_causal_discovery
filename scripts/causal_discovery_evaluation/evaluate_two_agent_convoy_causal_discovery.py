#!/usr/bin/python3

import argparse
import glob
import json
import csv
import os
import numpy as np

def aggregate_evaluation_results(input_file_path, output_file_path):
    if not os.path.isfile(input_file_path):
        raise ValueError(f"Input file path {input_file_path} does not specify a valid file")

    output_file_path_dir, _ = os.path.split(output_file_path)
    if not os.path.isdir(output_file_path_dir):
        raise ValueError(f"Output file path parent directory {output_file_path_dir} is not a valid directory")

    with open(input_file_path, 'r') as input_file:
        csv_reader = csv.DictReader(input_file)

        aggregate_results = {}

        for row in csv_reader:
            for col in row:
                if aggregate_results.get(col) is None:
                    aggregate_results[col] = { "list": [] }

                aggregate_results[col]["list"].append(float(row[col]))

        for col in aggregate_results:
            array = np.array(aggregate_results[col]["list"])
            aggregate_results[col]["mean"] = np.mean(array)
            aggregate_results[col]["sd"] = np.std(array)
            del aggregate_results[col]["list"]

        with open(output_file_path, 'w') as output_file:
            json.dump(aggregate_results, output_file)


def evaluate_scenario_causal_discovery(discoveries_file_path, output_file_path):
    output_file_path_dir, _ = os.path.split(output_file_path)
    if not os.path.isdir(output_file_path_dir):
        raise ValueError(f"Output file path parent directory {output_file_path_dir} is not a valid directory")

    variable_count = 3
    columns = ["tp", "fp", "tn", "fn", "precision", "recall", "f1_score", "runtime"]
    rows = []

    for discovery_file_path in glob.glob(discoveries_file_path):
        row = { "tp": 0, "fp": 0, "tn": 0, "fn": 0 }

        with open(discovery_file_path, "r") as discovery_file:
            json_data = json.load(discovery_file)
            variables = json_data["variables"]

            for variable in variables:
                discovered_parents = variables[variable]["parents"]
                discovered_parent_count = len(discovered_parents)

                if variable in discovered_parents:
                    discovered_parent_count -= 1

                if variable in ["c0.a", "i0.a"]:
                    row["fp"] += discovered_parent_count
                    row["tn"] += (variable_count - 1) - discovered_parent_count
                elif variable == "c1.a":
                    valid_parents = set(["c0.a"])
                    valid_parent_count = len(valid_parents)
                    valid_discovered_parent_count = len(set(discovered_parents) & valid_parents)

                    if valid_discovered_parent_count > 0:
                        row["tp"] += valid_discovered_parent_count
                        row["fp"] += discovered_parent_count - valid_discovered_parent_count
                        row["tn"] += (variable_count - 1) - discovered_parent_count
                    else:
                        row["fp"] += discovered_parent_count
                        row["tn"] += ((variable_count - 1) - discovered_parent_count) - valid_parent_count
                        row["fn"] += valid_parent_count
                else:
                    raise Exception(f"Variable '{variable}' should not be present")

            row["runtime"] = json_data["runtime"]

        row["precision"] = row["tp"] / (row["tp"] + row["fp"]) if row["tp"] + row["fp"] != 0 else 0
        row["recall"] = row["tp"] / (row["tp"] + row["fn"]) if row["tp"] + row["fn"] != 0 else 0
        row["f1_score"] = row["tp"] / (row["tp"] + 0.5 * (row["fp"] + row["fn"])) if (row["tp"] + 0.5 * (row["fp"] + row["fn"])) != 0 else 0

        rows.append(row)

    with open(output_file_path, 'w') as output_file:
        csv_writer = csv.DictWriter(output_file, fieldnames=columns)
        csv_writer.writeheader()
        for row in rows:
            csv_writer.writerow(row)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Evaluates the performance of casual discovery in a two agent convey scenario")
    arg_parser.add_argument("discoveries_file_path")
    arg_parser.add_argument("output_file_path")
    args = arg_parser.parse_args()

    evaluate_scenario_causal_discovery(args.discoveries_file_path, args.output_file_path)
