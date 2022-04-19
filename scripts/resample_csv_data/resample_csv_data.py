#!/usr/bin/python3

import os
import csv
import math
import argparse

arg_parser = argparse.ArgumentParser(description="Resamples the data in the supplied file to a difference frequency")
arg_parser.add_argument("input_file_path")
arg_parser.add_argument("input_frequency", type=float)
arg_parser.add_argument("output_file_path")
arg_parser.add_argument("output_frequency", type=float)
args = arg_parser.parse_args()

if not os.path.isfile(args.input_file_path):
    raise Exception(f"Input file path '{args.input_file_path}' does not describe a valid file")

if args.input_frequency <= 0.0:
    raise Exception(f"Input frequency '{args.input_frequency} Hz' is invalid")

output_file_path_dir, _ = os.path.split(args.output_file_path)
if not os.path.isdir(output_file_path_dir):
    raise Exception(f"Output file path directory '{args.output_file_path_dir}' does not describe a valid directory")

if args.input_frequency <= 0.0:
    raise Exception(f"Output frequency '{args.output_frequency} Hz' is invalid")

m = args.input_frequency / args.output_frequency

with open(args.input_file_path, "r") as input_file:
    csv_reader = csv.DictReader(input_file)
    output_rows = []
    input_counter = 0.0
    output_counter = m
    previous_row = None
    variables = []
    for row in csv_reader:
        if previous_row is not None:
            while input_counter + 1.0 > output_counter:
                alpha = output_counter - input_counter
                new_row = {}
                for variable in row:
                    new_row[variable] = alpha * float(row[variable]) + (1 - alpha) * float(previous_row[variable])
                output_rows.append(new_row)
                output_counter += m
            input_counter += 1.0
        else:
            for variable in row:
                variables.append(variable)
            output_rows.append(row)
        previous_row = row

    print(f"{int(input_counter) + 1} Frames -> {len(output_rows)} Frames")

    with open(args.output_file_path, 'w') as output_file:
        csv_writer = csv.DictWriter(output_file, variables)
        csv_writer.writeheader()
        for row in output_rows:
            csv_writer.writerow(row)
