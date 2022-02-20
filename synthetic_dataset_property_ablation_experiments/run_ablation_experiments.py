#!/usr/bin/python3

from __future__ import annotations

import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICES'] = '1'

import causal_scenario_generation.create_two_agent_convoy_scenario
import causal_discovery_evaluation.evaluate_two_agent_convoy_causal_discovery
import rand
import tcdf
import pcmci

import argparse
import random
import math
import glob
import json

class ValueInterface:
    def get_value(self) -> float:
        raise Exception("This is an interface class not meant to be called")

    def get_string(self) -> str:
        raise Exception("This is an interface class not meant to be called")

class ValueFixed(ValueInterface):
    def __init__(self, value: float):
        self.value = value

    def get_value(self) -> float:
        return self.value

    def get_string(self) -> str:
        return str(self.value)

class ValueRange(ValueInterface):
    def __init__(self, min_value: float, max_value: float):
        self.min_value = min_value
        self.max_value = max_value

    def get_value(self) -> float:
        return random.uniform(self.min_value, self.max_value)

    def get_string(self) -> str:
        return "[" + str(self.min_value) + "-" + str(self.max_value) + "]"

class ValueFlooredRange(ValueInterface):
    def __init__(self, min_value: float, max_value: float):
        self.min_value = min_value
        self.max_value = max_value

    def get_value(self) -> float:
        return math.floor(random.uniform(self.min_value, self.max_value))

    def get_string(self) -> str:
        return "floor[" + str(self.min_value) + "-" + str(self.max_value) + "]"

def run_ablation_experiment(
output_dir_path: str,
scenario_count: int,
skip_existing: bool,
run_rand: bool,
run_pcmci: bool,
run_tcdf: bool,
frequency_value: ValueInterface,
duration_value: ValueInterface,
convoy_action_count_value: ValueInterface,
independent_action_count_value: ValueInterface,
fixed_actuary_noise_value: ValueInterface,
proportional_actuary_noise_value: ValueInterface,
fixed_sensory_noise_value: ValueInterface,
proportional_sensory_noise_value: ValueInterface
):
    working_dir = output_dir_path

    if working_dir[0] != '/':
        working_dir = os.path.abspath(working_dir)

    if not os.path.isdir(working_dir):
        raise ValueError(f"Output directory path {working_dir} is not a valid directory")

    root_dir_name = "two_agent_convoy-" + \
        frequency_value.get_string() + "_" + \
        duration_value.get_string() + "_" + \
        convoy_action_count_value.get_string() + "_" + \
        independent_action_count_value.get_string() + "_" + \
        fixed_actuary_noise_value.get_string() + "_" + \
        proportional_actuary_noise_value.get_string() + "_" + \
        fixed_sensory_noise_value.get_string() + "_" + \
        proportional_sensory_noise_value.get_string()

    working_dir = os.path.join(working_dir, root_dir_name)
    if not os.path.isdir(working_dir):
        os.mkdir(working_dir)

    working_dir = os.path.join(working_dir, "scenarios")
    if not os.path.isdir(working_dir):
        os.mkdir(working_dir)

    for i in range(scenario_count):
        output_file_path = os.path.join(working_dir, f"scene-{i}.csv")
        if not skip_existing or not os.path.isfile(output_file_path):
            causal_scenario_generation.create_two_agent_convoy_scenario.create_two_agent_convoy_scenario(
                output_file_path,
                convoy_action_count_value.get_value(),
                independent_action_count_value.get_value(),
                frequency=frequency_value.get_value(),
                duration=duration_value.get_value(),
                fixed_actuary_noise=fixed_actuary_noise_value.get_value(),
                proportional_actuary_noise=proportional_actuary_noise_value.get_value(),
                fixed_sensory_noise=fixed_sensory_noise_value.get_value(),
                proportional_sensory_noise=proportional_sensory_noise_value.get_value()
            )
        else:
            print(f"Skipped work on file '{output_file_path}' as it already exists, and --skip-existing is in use")
    output_file_path = os.path.join(working_dir, "config.json")
    if not skip_existing or not os.path.isfile(output_file_path):
        causal_scenario_generation.create_two_agent_convoy_scenario.create_two_agent_convoy_scenario_config_file(
            output_file_path,
            convoy_action_count_value.get_string(),
            independent_action_count_value.get_string(),
            frequency=frequency_value.get_string(),
            duration=duration_value.get_string(),
            fixed_actuary_noise=fixed_actuary_noise_value.get_string(),
            proportional_actuary_noise=proportional_actuary_noise_value.get_string(),
            fixed_sensory_noise=fixed_sensory_noise_value.get_string(),
            proportional_sensory_noise=proportional_sensory_noise_value.get_string()
        )
    else:
        print(f"Skipped work on file '{output_file_path}' as it already exists, and --skip-existing is in use")

    working_dir, _ = os.path.split(working_dir)

    if run_rand:
        working_dir = os.path.join(working_dir, "discovered")
        if not os.path.isdir(working_dir):
            os.mkdir(working_dir)
        working_dir = os.path.join(working_dir, "rand")
        if not os.path.isdir(working_dir):
            os.mkdir(working_dir)

        working_dir, _ = os.path.split(working_dir)
        working_dir, _ = os.path.split(working_dir)
        for i in range(scenario_count):
            output_file_path = os.path.join(working_dir, f"discovered/rand/scene-{i}.json")
            if not skip_existing or not os.path.isfile(output_file_path):
                rand.runRAND(os.path.join(working_dir, f"scenarios/scene-{i}.csv"), output_file_path)
            else:
                print(f"Skipped work on file '{output_file_path}' as it already exists, and --skip-existing is in use")
        output_file_path = os.path.join(working_dir, "discovered/rand/config.json")
        if not skip_existing or not os.path.isfile(output_file_path):
            rand.create_RAND_config_file(output_file_path)
        else:
            print(f"Skipped work on file '{output_file_path}' as it already exists, and --skip-existing is in use")

    if run_tcdf:
        working_dir = os.path.join(working_dir, "discovered")
        if not os.path.isdir(working_dir):
            os.mkdir(working_dir)
        working_dir = os.path.join(working_dir, "tcdf")
        if not os.path.isdir(working_dir):
            os.mkdir(working_dir)

        working_dir, _ = os.path.split(working_dir)
        working_dir, _ = os.path.split(working_dir)
        for i in range(scenario_count):
            output_file_path = os.path.join(working_dir, f"discovered/tcdf/scene-{i}.json")
            if not skip_existing or not os.path.isfile(output_file_path):
                tcdf.runTCDF({ os.path.join(working_dir, f"scenarios/scene-{i}.csv"): "" }, False, output_file_path, hidden_layers=2, nrepochs=5000, cuda=True)
            else:
                print(f"Skipped work on file '{output_file_path}' as it already exists, and --skip-existing is in use")
        output_file_path = os.path.join(working_dir, "discovered/tcdf/config.json")
        if not skip_existing or not os.path.isfile(output_file_path):
            tcdf.create_TCDF_config_file(output_file_path, hidden_layers=2, nrepochs=5000, cuda=True)
        else:
            print(f"Skipped work on file '{output_file_path}' as it already exists, and --skip-existing is in use")

    if run_pcmci:
        working_dir = os.path.join(working_dir, "discovered")
        if not os.path.isdir(working_dir):
            os.mkdir(working_dir)
        working_dir = os.path.join(working_dir, "pcmci")
        if not os.path.isdir(working_dir):
            os.mkdir(working_dir)

        working_dir, _ = os.path.split(working_dir)
        working_dir, _ = os.path.split(working_dir)
        for i in range(scenario_count):
            output_file_path = os.path.join(working_dir, f"discovered/pcmci/scene-{i}.json")
            if not skip_existing or not os.path.isfile(output_file_path):
                pcmci.runPCMCI(os.path.join(working_dir, f"scenarios/scene-{i}.csv"), output_file_path, timeout=79)
            else:
                print(f"Skipped work on file '{output_file_path}' as it already exists, and --skip-existing is in use")
        output_file_path = os.path.join(working_dir, f"discovered/pcmci/config.json")
        if not skip_existing or not os.path.isfile(output_file_path):
            pcmci.create_PCMCI_config_file(output_file_path, timeout=79)
        else:
            print(f"Skipped work on file '{output_file_path}' as it already exists, and --skip-existing is in use")

    # NOTE: Result generation is never skipped, because it should be fast and deterministic

    if run_rand:
        working_dir = os.path.join(working_dir, "results")
        if not os.path.isdir(working_dir):
            os.mkdir(working_dir)
        working_dir = os.path.join(working_dir, "rand")
        if not os.path.isdir(working_dir):
            os.mkdir(working_dir)

        working_dir, _ = os.path.split(working_dir)
        working_dir, _ = os.path.split(working_dir)
        causal_discovery_evaluation.evaluate_two_agent_convoy_causal_discovery.evaluate_scenario_causal_discovery(os.path.join(glob.escape(working_dir), "discovered/rand/scene-*.json"), os.path.join(working_dir, "results/rand/results.csv"))

        working_dir = os.path.join(working_dir, "results")
        working_dir = os.path.join(working_dir, "rand")
        causal_discovery_evaluation.evaluate_two_agent_convoy_causal_discovery.aggregate_evaluation_results(os.path.join(working_dir, "results.csv"), os.path.join(working_dir, "aggregated_results.json"))

        working_dir, _ = os.path.split(working_dir)
        working_dir, _ = os.path.split(working_dir)

    if run_tcdf:
        working_dir = os.path.join(working_dir, "results")
        if not os.path.isdir(working_dir):
            os.mkdir(working_dir)
        working_dir = os.path.join(working_dir, "tcdf")
        if not os.path.isdir(working_dir):
            os.mkdir(working_dir)

        working_dir, _ = os.path.split(working_dir)
        working_dir, _ = os.path.split(working_dir)
        causal_discovery_evaluation.evaluate_two_agent_convoy_causal_discovery.evaluate_scenario_causal_discovery(os.path.join(glob.escape(working_dir), "discovered/tcdf/scene-*.json"), os.path.join(working_dir, "results/tcdf/results.csv"))

        working_dir = os.path.join(working_dir, "results")
        working_dir = os.path.join(working_dir, "tcdf")
        causal_discovery_evaluation.evaluate_two_agent_convoy_causal_discovery.aggregate_evaluation_results(os.path.join(working_dir, "results.csv"), os.path.join(working_dir, "aggregated_results.json"))

        working_dir, _ = os.path.split(working_dir)
        working_dir, _ = os.path.split(working_dir)

    if run_pcmci:
        working_dir = os.path.join(working_dir, "results")
        if not os.path.isdir(working_dir):
            os.mkdir(working_dir)
        working_dir = os.path.join(working_dir, "pcmci")
        if not os.path.isdir(working_dir):
            os.mkdir(working_dir)

        working_dir, _ = os.path.split(working_dir)
        working_dir, _ = os.path.split(working_dir)
        causal_discovery_evaluation.evaluate_two_agent_convoy_causal_discovery.evaluate_scenario_causal_discovery(os.path.join(glob.escape(working_dir), "discovered/pcmci/scene-*.json"), os.path.join(working_dir, "results/pcmci/results.csv"))

        working_dir = os.path.join(working_dir, "results")
        working_dir = os.path.join(working_dir, "pcmci")
        causal_discovery_evaluation.evaluate_two_agent_convoy_causal_discovery.aggregate_evaluation_results(os.path.join(working_dir, "results.csv"), os.path.join(working_dir, "aggregated_results.json"))

        working_dir, _ = os.path.split(working_dir)
        working_dir, _ = os.path.split(working_dir)
    return working_dir

def output_matrices_to_dir_path_for_method(output_dir_path, method_name, precision_matrix, recall_matrix, f1_matrix, runtime_matrix):
    if not os.path.isdir(output_dir_path):
        raise ValueError(f"Output directory path {output_dir_path} is not a valid directory")

    with open(os.path.join(output_dir_path, f"{method_name}_precision_matrix.csv"), 'w') as precision_matrix_file:
        output_matrix_to_file(precision_matrix_file, precision_matrix)

    with open(os.path.join(output_dir_path, f"{method_name}_recall_matrix.csv"), 'w') as recall_matrix_file:
        output_matrix_to_file(recall_matrix_file, recall_matrix)

    with open(os.path.join(output_dir_path, f"{method_name}_f1_matrix.csv"), 'w') as f1_matrix_file:
        output_matrix_to_file(f1_matrix_file, f1_matrix)

    with open(os.path.join(output_dir_path, f"{method_name}_runtime_matrix.csv"), 'w') as runtime_matrix_file:
        output_matrix_to_file(runtime_matrix_file, runtime_matrix)

def output_matrix_to_file(output_file, output_matrix):
    for i in range(len(output_matrix)):
        for j in range(len(output_matrix[i])):
            if j == len(output_matrix[i]) - 1:
                output_file.write(f"{output_matrix[i][j]}")
            else:
                output_file.write(f"{output_matrix[i][j]},")
        output_file.write("\n")

def run_ablation_experiments(output_dir_path: str, scenario_count: int, skip_existing: bool, run_rand: bool, run_pcmci: bool, run_tcdf: bool):
    working_dir = output_dir_path

    if working_dir[0] != '/':
        working_dir = os.path.abspath(working_dir)

    if not os.path.isdir(working_dir):
        raise ValueError(f"Output directory path {working_dir} is not a valid directory")

    fixed_actuary_noise = ValueRange(0.1, 1.6)
    proportional_actuary_noise = ValueRange(0.1, 1.6)
    fixed_sensory_noise = ValueRange(0.01, 0.16)
    proportional_sensory_noise = ValueRange(0.005, 0.08)

    output_subdir_paths = []



    working_dir = os.path.join(working_dir, "frequency-duration")
    if not os.path.isdir(working_dir):
        os.mkdir(working_dir)

    frequencies = [20, 10, 8, 5, 4, 2]
    durations = [480, 240, 120, 60, 30, 15]
    convoy_actions = ValueFlooredRange(1, 5.999)
    independent_actions = ValueFlooredRange(0, 6.999)

    results_matrix = {}
    precision_matrix = {}
    recall_matrix = {}
    f1_matrix = {}
    runtime_matrix = {}

    for frequency in frequencies:
        results_matrix[f"{frequency} Hz"] = {}
        for duration in durations:
            results_matrix[f"{frequency} Hz"][f"{duration} s"] = {}
            experiment_dir_path = run_ablation_experiment(working_dir, scenario_count, skip_existing, run_rand, run_pcmci, run_tcdf, ValueFixed(frequency), ValueFixed(duration), convoy_actions, independent_actions, fixed_actuary_noise, proportional_actuary_noise, fixed_sensory_noise, proportional_sensory_noise)
            if run_rand:
                with open(os.path.join(experiment_dir_path, "results/rand/aggregated_results.json"), 'r') as rand_results_file:
                    results_matrix[f"{frequency} Hz"][f"{duration} s"]["rand"] = json.load(rand_results_file)

                    if precision_matrix.get("rand") is None:
                        precision_matrix["rand"] = [[results_matrix[f"{frequency} Hz"][f"{duration} s"]["rand"]["precision"]["mean"]]]
                    else:
                        precision_matrix["rand"][-1].append(results_matrix[f"{frequency} Hz"][f"{duration} s"]["rand"]["precision"]["mean"])

                    if recall_matrix.get("rand") is None:
                        recall_matrix["rand"] = [[results_matrix[f"{frequency} Hz"][f"{duration} s"]["rand"]["recall"]["mean"]]]
                    else:
                        recall_matrix["rand"][-1].append(results_matrix[f"{frequency} Hz"][f"{duration} s"]["rand"]["recall"]["mean"])

                    if f1_matrix.get("rand") is None:
                        f1_matrix["rand"] = [[results_matrix[f"{frequency} Hz"][f"{duration} s"]["rand"]["f1_score"]["mean"]]]
                    else:
                        f1_matrix["rand"][-1].append(results_matrix[f"{frequency} Hz"][f"{duration} s"]["rand"]["f1_score"]["mean"])

                    if runtime_matrix.get("rand") is None:
                        runtime_matrix["rand"] = [[results_matrix[f"{frequency} Hz"][f"{duration} s"]["rand"]["runtime"]["mean"]]]
                    else:
                        runtime_matrix["rand"][-1].append(results_matrix[f"{frequency} Hz"][f"{duration} s"]["rand"]["runtime"]["mean"])

            if run_tcdf:
                with open(os.path.join(experiment_dir_path, "results/tcdf/aggregated_results.json"), 'r') as tcdf_results_file:
                    results_matrix[f"{frequency} Hz"][f"{duration} s"]["tcdf"] = json.load(tcdf_results_file)

                    if precision_matrix.get("tcdf") is None:
                        precision_matrix["tcdf"] = [[results_matrix[f"{frequency} Hz"][f"{duration} s"]["tcdf"]["precision"]["mean"]]]
                    else:
                        precision_matrix["tcdf"][-1].append(results_matrix[f"{frequency} Hz"][f"{duration} s"]["tcdf"]["precision"]["mean"])

                    if recall_matrix.get("tcdf") is None:
                        recall_matrix["tcdf"] = [[results_matrix[f"{frequency} Hz"][f"{duration} s"]["tcdf"]["recall"]["mean"]]]
                    else:
                        recall_matrix["tcdf"][-1].append(results_matrix[f"{frequency} Hz"][f"{duration} s"]["tcdf"]["recall"]["mean"])

                    if f1_matrix.get("tcdf") is None:
                        f1_matrix["tcdf"] = [[results_matrix[f"{frequency} Hz"][f"{duration} s"]["tcdf"]["f1_score"]["mean"]]]
                    else:
                        f1_matrix["tcdf"][-1].append(results_matrix[f"{frequency} Hz"][f"{duration} s"]["tcdf"]["f1_score"]["mean"])

                    if runtime_matrix.get("tcdf") is None:
                        runtime_matrix["tcdf"] = [[results_matrix[f"{frequency} Hz"][f"{duration} s"]["tcdf"]["runtime"]["mean"]]]
                    else:
                        runtime_matrix["tcdf"][-1].append(results_matrix[f"{frequency} Hz"][f"{duration} s"]["tcdf"]["runtime"]["mean"])

            if run_pcmci:
                with open(os.path.join(experiment_dir_path, "results/pcmci/aggregated_results.json"), 'r') as pcmci_results_file:
                    results_matrix[f"{frequency} Hz"][f"{duration} s"]["pcmci"] = json.load(pcmci_results_file)

                    if precision_matrix.get("pcmci") is None:
                        precision_matrix["pcmci"] = [[results_matrix[f"{frequency} Hz"][f"{duration} s"]["pcmci"]["precision"]["mean"]]]
                    else:
                        precision_matrix["pcmci"][-1].append(results_matrix[f"{frequency} Hz"][f"{duration} s"]["pcmci"]["precision"]["mean"])

                    if recall_matrix.get("pcmci") is None:
                        recall_matrix["pcmci"] = [[results_matrix[f"{frequency} Hz"][f"{duration} s"]["pcmci"]["recall"]["mean"]]]
                    else:
                        recall_matrix["pcmci"][-1].append(results_matrix[f"{frequency} Hz"][f"{duration} s"]["pcmci"]["recall"]["mean"])

                    if f1_matrix.get("pcmci") is None:
                        f1_matrix["pcmci"] = [[results_matrix[f"{frequency} Hz"][f"{duration} s"]["pcmci"]["f1_score"]["mean"]]]
                    else:
                        f1_matrix["pcmci"][-1].append(results_matrix[f"{frequency} Hz"][f"{duration} s"]["pcmci"]["f1_score"]["mean"])

                    if runtime_matrix.get("pcmci") is None:
                        runtime_matrix["pcmci"] = [[results_matrix[f"{frequency} Hz"][f"{duration} s"]["pcmci"]["runtime"]["mean"]]]
                    else:
                        runtime_matrix["pcmci"][-1].append(results_matrix[f"{frequency} Hz"][f"{duration} s"]["pcmci"]["runtime"]["mean"])

        for method in precision_matrix:
            precision_matrix[method].append([])

        for method in recall_matrix:
            recall_matrix[method].append([])

        for method in f1_matrix:
            f1_matrix[method].append([])

        for method in runtime_matrix:
            runtime_matrix[method].append([])

    with open(os.path.join(working_dir, "results_matrix.json"), 'w') as results_matrix_file:
        json.dump(results_matrix, results_matrix_file)

    if run_rand:
        output_matrices_to_dir_path_for_method(working_dir, "rand", precision_matrix["rand"], recall_matrix["rand"], f1_matrix["rand"], runtime_matrix["rand"])

    if run_tcdf:
        output_matrices_to_dir_path_for_method(working_dir, "tcdf", precision_matrix["tcdf"], recall_matrix["tcdf"], f1_matrix["tcdf"], runtime_matrix["tcdf"])

    if run_pcmci:
        output_matrices_to_dir_path_for_method(working_dir, "pcmci", precision_matrix["pcmci"], recall_matrix["pcmci"], f1_matrix["pcmci"], runtime_matrix["pcmci"])

    output_subdir_paths.append(working_dir)



    working_dir, _ = os.path.split(working_dir)
    working_dir = os.path.join(working_dir, "convoy_actions-independent_actions")
    if not os.path.isdir(working_dir):
        os.mkdir(working_dir)

    frequency = ValueRange(4, 10)
    duration = ValueRange(30, 240)
    convoy_actions_list = [1, 2, 3, 5, 8, 13]
    independent_actions_list = [0, 1, 2, 4, 7, 12]

    results_matrix = {}
    precision_matrix = {}
    recall_matrix = {}
    f1_matrix = {}
    runtime_matrix = {}

    for convoy_actions in convoy_actions_list:
        results_matrix[f"{convoy_actions} convoy actions"] = {}
        for independent_actions in independent_actions_list:
            results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"] = {}
            experiment_dir_path = run_ablation_experiment(working_dir, scenario_count, skip_existing, run_rand, run_pcmci, run_tcdf, frequency, duration, ValueFixed(convoy_actions), ValueFixed(independent_actions), fixed_actuary_noise, proportional_actuary_noise, fixed_sensory_noise, proportional_sensory_noise)
            if run_rand:
                with open(os.path.join(experiment_dir_path, "results/rand/aggregated_results.json"), 'r') as rand_results_file:
                    results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["rand"] = json.load(rand_results_file)

                    if precision_matrix.get("rand") is None:
                        precision_matrix["rand"] = [[results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["rand"]["precision"]["mean"]]]
                    else:
                        precision_matrix["rand"][-1].append(results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["rand"]["precision"]["mean"])

                    if recall_matrix.get("rand") is None:
                        recall_matrix["rand"] = [[results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["rand"]["recall"]["mean"]]]
                    else:
                        recall_matrix["rand"][-1].append(results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["rand"]["recall"]["mean"])

                    if f1_matrix.get("rand") is None:
                        f1_matrix["rand"] = [[results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["rand"]["f1_score"]["mean"]]]
                    else:
                        f1_matrix["rand"][-1].append(results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["rand"]["f1_score"]["mean"])

                    if runtime_matrix.get("rand") is None:
                        runtime_matrix["rand"] = [[results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["rand"]["runtime"]["mean"]]]
                    else:
                        runtime_matrix["rand"][-1].append(results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["rand"]["runtime"]["mean"])

            if run_tcdf:
                with open(os.path.join(experiment_dir_path, "results/tcdf/aggregated_results.json"), 'r') as tcdf_results_file:
                    results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["tcdf"] = json.load(tcdf_results_file)

                    if precision_matrix.get("tcdf") is None:
                        precision_matrix["tcdf"] = [[results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["tcdf"]["precision"]["mean"]]]
                    else:
                        precision_matrix["tcdf"][-1].append(results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["tcdf"]["precision"]["mean"])

                    if recall_matrix.get("tcdf") is None:
                        recall_matrix["tcdf"] = [[results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["tcdf"]["recall"]["mean"]]]
                    else:
                        recall_matrix["tcdf"][-1].append(results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["tcdf"]["recall"]["mean"])

                    if f1_matrix.get("tcdf") is None:
                        f1_matrix["tcdf"] = [[results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["tcdf"]["f1_score"]["mean"]]]
                    else:
                        f1_matrix["tcdf"][-1].append(results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["tcdf"]["f1_score"]["mean"])

                    if runtime_matrix.get("tcdf") is None:
                        runtime_matrix["tcdf"] = [[results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["tcdf"]["runtime"]["mean"]]]
                    else:
                        runtime_matrix["tcdf"][-1].append(results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["tcdf"]["runtime"]["mean"])

            if run_pcmci:
                with open(os.path.join(experiment_dir_path, "results/pcmci/aggregated_results.json"), 'r') as pcmci_results_file:
                    results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["pcmci"] = json.load(pcmci_results_file)

                    if precision_matrix.get("pcmci") is None:
                        precision_matrix["pcmci"] = [[results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["pcmci"]["precision"]["mean"]]]
                    else:
                        precision_matrix["pcmci"][-1].append(results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["pcmci"]["precision"]["mean"])

                    if recall_matrix.get("pcmci") is None:
                        recall_matrix["pcmci"] = [[results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["pcmci"]["recall"]["mean"]]]
                    else:
                        recall_matrix["pcmci"][-1].append(results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["pcmci"]["recall"]["mean"])

                    if f1_matrix.get("pcmci") is None:
                        f1_matrix["pcmci"] = [[results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["pcmci"]["f1_score"]["mean"]]]
                    else:
                        f1_matrix["pcmci"][-1].append(results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["pcmci"]["f1_score"]["mean"])

                    if runtime_matrix.get("pcmci") is None:
                        runtime_matrix["pcmci"] = [[results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["pcmci"]["runtime"]["mean"]]]
                    else:
                        runtime_matrix["pcmci"][-1].append(results_matrix[f"{convoy_actions} convoy actions"][f"{independent_actions} independent actions"]["pcmci"]["runtime"]["mean"])

        for method in precision_matrix:
            precision_matrix[method].append([])

        for method in recall_matrix:
            recall_matrix[method].append([])

        for method in f1_matrix:
            f1_matrix[method].append([])

        for method in runtime_matrix:
            runtime_matrix[method].append([])

    with open(os.path.join(working_dir, "results_matrix.json"), 'w') as results_matrix_file:
        json.dump(results_matrix, results_matrix_file)

    if run_rand:
        output_matrices_to_dir_path_for_method(working_dir, "rand", precision_matrix["rand"], recall_matrix["rand"], f1_matrix["rand"], runtime_matrix["rand"])

    if run_tcdf:
        output_matrices_to_dir_path_for_method(working_dir, "tcdf", precision_matrix["tcdf"], recall_matrix["tcdf"], f1_matrix["tcdf"], runtime_matrix["tcdf"])

    if run_pcmci:
        output_matrices_to_dir_path_for_method(working_dir, "pcmci", precision_matrix["pcmci"], recall_matrix["pcmci"], f1_matrix["pcmci"], runtime_matrix["pcmci"])

    output_subdir_paths.append(working_dir)



    return output_subdir_paths





if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Carries out ablation experiments on casual discovery in a two agent convey scenario")
    arg_parser.add_argument("output_file_path")
    arg_parser.add_argument("--skip-existing", action="store_true")
    arg_parser.add_argument("--rand", action="store_true")
    arg_parser.add_argument("--pcmci", action="store_true")
    arg_parser.add_argument("--tcdf", action="store_true")
    args = arg_parser.parse_args()

    run_ablation_experiments(args.output_file_path, 100, args.skip_existing, args.rand, args.pcmci, args.tcdf)
