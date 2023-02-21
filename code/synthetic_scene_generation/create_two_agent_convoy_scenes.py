#!/usr/bin/python3

import os
import random
import argparse
import create_two_agent_convoy_scenario

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

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Generates a collection of two agent convoy scenarios")
    arg_parser.add_argument("output_dir_path")
    arg_parser.add_argument("--variable", default="acceleration")
    arg_parser.add_argument("--scenario_count", default=100)
    args = arg_parser.parse_args()

    working_dir = args.output_dir_path

    if working_dir[0] != '/':
        working_dir = os.path.abspath(working_dir)

    if not os.path.isdir(working_dir):
        raise ValueError(f"Output directory path {working_dir} is not a valid directory")

    frequency_value = ValueFixed(10)
    duration_value = ValueRange(50, 70)
    convoy_actions_value = ValueFixed(12)
    independent_actions_value = ValueFixed(12)
    fixed_actuary_noise_value = ValueRange(0.1, 1.6)
    proportional_actuary_noise_value = ValueRange(0.1, 1.6)
    fixed_sensory_noise_value = ValueRange(0.01, 0.16)
    proportional_sensory_noise_value = ValueRange(0.005, 0.08)

    for i in range(args.scenario_count):
        output_file_path = os.path.join(working_dir, f"scene-{i}.csv")
        create_two_agent_convoy_scenario.create_two_agent_convoy_scenario(
            output_file_path,
            convoy_actions_value.get_value(),
            independent_actions_value.get_value(),
            args.variable,
            frequency=frequency_value.get_value(),
            duration=duration_value.get_value(),
            fixed_actuary_noise=fixed_actuary_noise_value.get_value(),
            proportional_actuary_noise=proportional_actuary_noise_value.get_value(),
            fixed_sensory_noise=fixed_sensory_noise_value.get_value(),
            proportional_sensory_noise=proportional_sensory_noise_value.get_value()
        )
    output_file_path = os.path.join(working_dir, "config.json")
    create_two_agent_convoy_scenario.create_two_agent_convoy_scenario_config_file(
        output_file_path,
        convoy_actions_value.get_string(),
        independent_actions_value.get_string(),
        args.variable,
        frequency=frequency_value.get_string(),
        duration=duration_value.get_string(),
        fixed_actuary_noise=fixed_actuary_noise_value.get_string(),
        proportional_actuary_noise=proportional_actuary_noise_value.get_string(),
        fixed_sensory_noise=fixed_sensory_noise_value.get_string(),
        proportional_sensory_noise=proportional_sensory_noise_value.get_string()
    )
