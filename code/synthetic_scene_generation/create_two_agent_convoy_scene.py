#!/usr/bin/python3

import os
import random
import csv
import argparse
import math
import json

def create_two_agent_convoy_scene_config_file(
output_file_path,
number_of_convoy_actions,
number_of_independent_actions,
variable = "acceleration",
minimum_convoy_distance = 10, # m
maximum_convoy_distance = 100, # m
K_p = 1.0,
K_i = 0.0,
K_d = 0.0,
frequency = 10, # Hz
duration = 240, # s
min_action_interval = 1, # s
min_velocity = 0, # 0 mph in m/s, this does mean reversing is impossible, but this would not be legal on a main road anyway
max_velocity = 44.7, # 100 mph in m/s
min_start_velocity = 4.47, # 10 mph in m/s
max_start_velocity = 26.8, # 60 mph in m/s
min_acceleration = -6.56, # 60 mph to 0 mph over 180 feet in m/s^2
max_acceleration = 3.5, # m/s^2
safe_distance_over_velocity = 2.24, # s
reaction_time = 0.5, # s
fixed_actuary_noise = 0.0, # m/s^2
proportional_actuary_noise = 0.0,
fixed_sensory_noise = 0.0, # m
proportional_sensory_noise = 0.0
):
    output_file_path_dir, _ = os.path.split(output_file_path)
    if not os.path.isdir(output_file_path_dir):
        raise ValueError(f"Output file path parent directory {output_file_path_dir} is not a valid directory")

    config = {
        "number_of_convoy_actions": str(number_of_convoy_actions),
        "number_of_independent_actions": str(number_of_independent_actions),
        "variable": str(variable),
        "minimum_convoy_distance": str(minimum_convoy_distance),
        "maximum_convoy_distance": str(maximum_convoy_distance),
        "K_p": str(K_p),
        "K_i": str(K_i),
        "K_d": str(K_d),
        "frequency": str(frequency),
        "duration": str(duration),
        "min_action_interval": str(min_action_interval),
        "min_velocity": str(min_velocity),
        "max_velocity": str(max_velocity),
        "min_start_velocity": str(min_start_velocity),
        "max_start_velocity": str(max_start_velocity),
        "min_acceleration": str(min_acceleration),
        "max_acceleration": str(max_acceleration),
        "safe_distance_over_velocity": str(safe_distance_over_velocity),
        "reaction_time": str(reaction_time),
        "fixed_actuary_noise": str(fixed_actuary_noise),
        "proportional_actuary_noise": str(proportional_actuary_noise),
        "fixed_sensory_noise": str(fixed_sensory_noise),
        "proportional_sensory_noise": str(proportional_sensory_noise)
    }

    with open(output_file_path, 'w') as output_file:
        json.dump(config, output_file)

def create_two_agent_convoy_scene_config_file_with_action_range(
output_file_path,
minimum_number_of_convoy_actions = 24,
maximum_number_of_convoy_actions = 40,
variable = "acceleration",
minimum_number_of_independent_actions = 0,
maximum_number_of_independent_actions = 80,
minimum_convoy_distance = 10, # m
maximum_convoy_distance = 100, # m
K_p = 1.0,
K_i = 0.0,
K_d = 0.0,
frequency = 10, # Hz
duration = 240, # s
min_action_interval = 1, # s
min_velocity = 0, # 0 mph in m/s, this does mean reversing is impossible, but this would not be legal on a main road anyway
max_velocity = 44.7, # 100 mph in m/s
min_start_velocity = 4.47, # 10 mph in m/s
max_start_velocity = 26.8, # 60 mph in m/s
min_acceleration = -6.56, # 60 mph to 0 mph over 180 feet in m/s^2
max_acceleration = 3.5, # m/s^2
safe_distance_over_velocity = 2.24, # s
reaction_time = 0.5, # s
fixed_actuary_noise = 0.0, # m/s^2
proportional_actuary_noise = 0.0,
fixed_sensory_noise = 0.0, # m
proportional_sensory_noise = 0.0
):
    create_two_agent_convoy_scene_config_file(
        output_file_path,
        "[" + str(minimum_number_of_convoy_actions) + "-" + str(maximum_number_of_convoy_actions) + "]",
        "[" + str(minimum_number_of_independent_actions) + "-" + str(maximum_number_of_independent_actions) + "]",
        variable=variable,
        minimum_convoy_distance=minimum_convoy_distance,
        maximum_convoy_distance=maximum_convoy_distance,
        K_p=K_p,
        K_i=K_i,
        K_d=K_d,
        frequency=frequency,
        duration=duration,
        min_action_interval=min_action_interval,
        min_velocity=min_velocity,
        max_velocity=max_velocity,
        min_start_velocity=min_start_velocity,
        max_start_velocity=max_start_velocity,
        min_acceleration=min_acceleration,
        max_acceleration=max_acceleration,
        safe_distance_over_velocity=safe_distance_over_velocity,
        reaction_time=reaction_time,
        fixed_actuary_noise=fixed_actuary_noise,
        proportional_actuary_noise=proportional_actuary_noise,
        fixed_sensory_noise=fixed_sensory_noise,
        proportional_sensory_noise=proportional_sensory_noise
    )

def create_two_agent_convoy_scene(
output_file_path,
number_of_convoy_actions,
number_of_independent_actions,
variable = "acceleration",
minimum_convoy_distance = 10, # m
maximum_convoy_distance = 100, # m
K_p = 1.0,
K_i = 0.0,
K_d = 0.0,
frequency = 10, # Hz
duration = 240, # s
min_action_interval = 1, # s
min_velocity = 0, # 0 mph in m/s, this does mean reversing is impossible, but this would not be legal on a main road anyway
max_velocity = 44.7, # 100 mph in m/s
min_start_velocity = 4.47, # 10 mph in m/s
max_start_velocity = 26.8, # 60 mph in m/s
min_acceleration = -6.56, # 60 mph to 0 mph over 180 feet in m/s^2
max_acceleration = 3.5, # m/s^2
safe_distance_over_velocity = 2.24, # s
reaction_time = 0.5, # s
fixed_actuary_noise = 0.0, # m/s^2
proportional_actuary_noise = 0.0,
fixed_sensory_noise = 0.0, # m
proportional_sensory_noise = 0.0
):
    create_two_agent_convoy_scene_with_action_range(
        output_file_path,
        minimum_number_of_convoy_actions=number_of_convoy_actions,
        maximum_number_of_convoy_actions=number_of_convoy_actions,
        variable=variable,
        minimum_number_of_independent_actions=number_of_independent_actions,
        maximum_number_of_independent_actions=number_of_independent_actions,
        minimum_convoy_distance=minimum_convoy_distance,
        maximum_convoy_distance=maximum_convoy_distance,
        K_p=K_p,
        K_i=K_i,
        K_d=K_d,
        frequency=frequency,
        duration=duration,
        min_action_interval=min_action_interval,
        min_velocity=min_velocity,
        max_velocity=max_velocity,
        min_start_velocity=min_start_velocity,
        max_start_velocity=max_start_velocity,
        min_acceleration=min_acceleration,
        max_acceleration=max_acceleration,
        safe_distance_over_velocity=safe_distance_over_velocity,
        reaction_time=reaction_time,
        fixed_actuary_noise=fixed_actuary_noise,
        proportional_actuary_noise=proportional_actuary_noise,
        fixed_sensory_noise=fixed_sensory_noise,
        proportional_sensory_noise=proportional_sensory_noise
    )

def create_two_agent_convoy_scene_with_action_range(
output_file_path,
minimum_number_of_convoy_actions = 24,
maximum_number_of_convoy_actions = 40,
variable = "acceleration",
minimum_number_of_independent_actions = 0,
maximum_number_of_independent_actions = 80,
minimum_convoy_distance = 10, # m
maximum_convoy_distance = 100, # m
K_p = 1.0,
K_i = 0.0,
K_d = 0.0,
frequency = 10, # Hz
duration = 240, # s
min_action_interval = 1, # s
min_velocity = 0, # 0 mph in m/s, this does mean reversing is impossible, but this would not be legal on a main road anyway
max_velocity = 44.7, # 100 mph in m/s
min_start_velocity = 4.47, # 10 mph in m/s
max_start_velocity = 26.8, # 60 mph in m/s
min_acceleration = -6.56, # 60 mph to 0 mph over 180 feet in m/s^2
max_acceleration = 3.5, # m/s^2
safe_distance_over_velocity = 2.24, # s
reaction_time = 0.5, # s
fixed_actuary_noise = 0.0, # m/s^2
proportional_actuary_noise = 0.0,
fixed_sensory_noise = 0.0, # m
proportional_sensory_noise = 0.0
):

    output_file_path_dir, _ = os.path.split(output_file_path)
    if not os.path.isdir(output_file_path_dir):
        raise ValueError(f"Output file path parent directory {output_file_path_dir} is not a valid directory")

    independent_frames = generate_agent_variables_from_scratch("i0", minimum_number_of_independent_actions, maximum_number_of_independent_actions,
        K_p=K_p, K_i=K_i, K_d=K_d, frequency=frequency, duration=duration, min_action_interval=min_action_interval, min_velocity=min_velocity, max_velocity=max_velocity, min_start_velocity=min_start_velocity, max_start_velocity=max_start_velocity, min_acceleration=min_acceleration,
        max_acceleration=max_acceleration, reaction_time=reaction_time, fixed_actuary_noise=fixed_actuary_noise, proportional_actuary_noise=proportional_actuary_noise, fixed_sensory_noise=fixed_sensory_noise,
        proportional_sensory_noise=proportional_sensory_noise)
    convoy_head_frames = generate_agent_variables_from_scratch("c0", minimum_number_of_convoy_actions, maximum_number_of_convoy_actions,
        K_p=K_p, K_i=K_i, K_d=K_d, frequency=frequency, duration=duration, min_action_interval=min_action_interval, min_velocity=min_velocity, max_velocity=max_velocity, min_start_velocity=min_start_velocity, max_start_velocity=max_start_velocity, min_acceleration=min_acceleration,
        max_acceleration=max_acceleration, reaction_time=reaction_time, fixed_actuary_noise=fixed_actuary_noise, proportional_actuary_noise=proportional_actuary_noise, fixed_sensory_noise=fixed_sensory_noise,
        proportional_sensory_noise=proportional_sensory_noise)
    convoy_tail_frames = generate_agent_variables_from_convoy("c1", "c0", convoy_head_frames, minimum_convoy_distance, maximum_convoy_distance,
        K_p=K_p, K_i=K_i, K_d=K_d, frequency=frequency, duration=duration, min_velocity=min_velocity, max_velocity=max_velocity, min_start_velocity=min_start_velocity, max_start_velocity=max_start_velocity, min_acceleration=min_acceleration,
        max_acceleration=max_acceleration, safe_distance_over_velocity=safe_distance_over_velocity, reaction_time=reaction_time, fixed_actuary_noise=fixed_actuary_noise, proportional_actuary_noise=proportional_actuary_noise, fixed_sensory_noise=fixed_sensory_noise,
        proportional_sensory_noise=proportional_sensory_noise)

    combined_frames = []

    for independent_frame, convoy_head_frame, convoy_tail_frame in zip(independent_frames, convoy_head_frames, convoy_tail_frames):
        combined_frame = { **independent_frame, **convoy_head_frame, **convoy_tail_frame}
        combined_frames.append(combined_frame)

    if variable == "acceleration":
        columns = ["time_index", "c0.a", "c1.a", "i0.a"]
    elif variable == "velocity":
        columns = ["time_index", "c0.v", "c1.v", "i0.v"]
    else:
        raise ValueError("Variable parameter does not correspond to an applicable parameter")
    rows = []

    for (i, combined_frame) in enumerate(combined_frames):
        row = { "time_index": i }
        for column in columns:
            if column == "time_index":
                continue
            row[column] = combined_frame[column]
        rows.append(row)

    with open(output_file_path, 'w') as output_file:
        csv_writer = csv.DictWriter(output_file, fieldnames=columns)
        csv_writer.writeheader()
        for row in rows:
            csv_writer.writerow(row)

def generate_agent_variables_from_scratch(
id,
min_actions,
max_actions,
K_p = 1.0,
K_i = 0.0,
K_d = 0.0,
frequency = 10, # Hz
duration = 240, # s
min_action_interval = 1, # s
min_velocity = 0, # 0 mph in m/s, this does mean reversing is impossible, but this would not be legal on a main road anyway
max_velocity = 44.7, # 100 mph in m/s
min_start_velocity = 4.47, # 10 mph in m/s
max_start_velocity = 26.8, # 60 mph in m/s
min_acceleration = -6.56, # 60 mph to 0 mph over 180 feet in m/s^2
max_acceleration = 3.5, # m/s^2
reaction_time = 0.5, # s
fixed_actuary_noise = 0.0, # m/s^2
proportional_actuary_noise = 0.0,
fixed_sensory_noise = 0.0, # m
proportional_sensory_noise = 0.0
):
    frame_count = int(frequency * duration)
    time_step = 1 / frequency
    reaction_frame_difference = int(math.ceil(reaction_time / time_step))

    starting_velocity = random.uniform(min_start_velocity, max_start_velocity)
    actions = { 0 : starting_velocity }

    while True:
        for i in range(frame_count):
            if not (len(actions.keys()) >= max_actions or any(map(lambda x : abs(i - x) * time_step < min_action_interval, actions.keys()))):
                if random.random() < (((max_actions + min_actions) / 2) / frame_count):
                    actions[i] = random.uniform(min_velocity, max_velocity)

        #print(f"{len(actions.keys())}, {min_actions}, {max_actions}")
        if len(actions.keys()) >= min_actions:
            break

    frames = []

    distance_travelled = 0
    velocity = starting_velocity
    acceleration = 0

    accumulated_velocity_error = 0
    previous_velocity_error = None

    steps_til_reaction = 0

    for i in range(frame_count):
        if i != 0:
            perturbated_acceleration = acceleration * (1.0 + random.uniform(-proportional_actuary_noise, proportional_actuary_noise)) + random.uniform(-fixed_actuary_noise, fixed_actuary_noise)
            new_velocity = min(max(velocity + perturbated_acceleration * time_step, min_velocity), max_velocity)
            additional_distance_travelled = 0.5 * (new_velocity + velocity) * time_step
            velocity = new_velocity
            distance_travelled += additional_distance_travelled

        # This relies upon i = 0 being first in order to initialise the velocity goal
        if actions.get(i) is not None:
            velocity_goal = actions[i]

        if steps_til_reaction <= 0:
            steps_til_reaction = reaction_frame_difference

            velocity_error = velocity_goal - velocity

            accumulated_velocity_error += velocity_error

            if previous_velocity_error is None:
                velocity_error_delta = 0
            else:
                velocity_error_delta = velocity_error - previous_velocity_error

            desired_acceleration = K_p * velocity_error + K_i * accumulated_velocity_error + K_d * (velocity_error_delta / time_step)

            # First line enforces acceleration restrictions, second line forgoes them
            acceleration = min(max(desired_acceleration, min_acceleration), max_acceleration)
            #acceleration = desired_acceleration

            previous_velocity_error = velocity_error
        else:
            steps_til_reaction -= 1

        frame = { f"{id}.a": acceleration, f"{id}.vg": velocity_goal, f"{id}.v": velocity, f"{id}.p": distance_travelled }
        frames.append(frame)

    return frames

def generate_agent_variables_from_convoy(
tail_id,
head_id,
head_frames,
min_distance,
max_distance,
K_p = 1.0,
K_i = 0.0,
K_d = 0.0,
frequency = 10, # Hz
duration = 240, # s
min_velocity = 0, # 0 mph in m/s, this does mean reversing is impossible, but this would not be legal on a main road anyway
max_velocity = 44.7, # 100 mph in m/s
min_start_velocity = 4.47, # 10 mph in m/s
max_start_velocity = 26.8, # 60 mph in m/s
min_acceleration = -6.56, # 60 mph to 0 mph over 180 feet in m/s^2
max_acceleration = 3.5, # m/s^2
safe_distance_over_velocity = 2.24, # s
reaction_time = 0.5, # s
fixed_actuary_noise = 0.0, # m/s^2
proportional_actuary_noise = 0.0,
fixed_sensory_noise = 0.0, # m
proportional_sensory_noise = 0.0
):
    frame_count = int(frequency * duration)
    time_step = 1 / frequency
    reaction_frame_difference = int(math.ceil(reaction_time / time_step))

    starting_distance = random.uniform(min_distance, max_distance)
    starting_velocity = random.uniform(min_start_velocity, max_start_velocity)

    frames = []

    distance_travelled = 0
    velocity = starting_velocity
    acceleration = 0
    distance = starting_distance
    perturbated_distance = distance * (1.0 + random.uniform(-proportional_sensory_noise, proportional_sensory_noise)) + random.uniform(-fixed_sensory_noise, fixed_sensory_noise)

    accumulated_distance_error = 0
    previous_distance_error = None

    steps_til_reaction = 0

    for i in range(frame_count):
        head_frame = head_frames[i]

        if i != 0:
            perturbated_acceleration = acceleration * (1.0 + random.uniform(-proportional_actuary_noise, proportional_actuary_noise)) + random.uniform(-fixed_actuary_noise, fixed_actuary_noise)
            new_velocity = min(max(velocity + perturbated_acceleration * time_step, min_velocity), max_velocity)
            additional_distance_travelled = 0.5 * (new_velocity + velocity) * time_step
            velocity = new_velocity
            distance_travelled += additional_distance_travelled
            distance = starting_distance + (head_frame[f"{head_id}.p"] - distance_travelled)
            perturbated_distance = distance * (1.0 + random.uniform(-proportional_sensory_noise, proportional_sensory_noise)) + random.uniform(-fixed_sensory_noise, fixed_sensory_noise)

        if steps_til_reaction <= 0:
            steps_til_reaction = reaction_frame_difference

            distance_goal = safe_distance_over_velocity * velocity

            distance_error = perturbated_distance - distance_goal

            accumulated_distance_error += distance_error

            if previous_distance_error is None:
                distance_error_delta = 0
            else:
                distance_error_delta = distance_error - previous_distance_error

            desired_acceleration = K_p * distance_error + K_i * accumulated_distance_error + K_d * (distance_error_delta / time_step)

            # First line enforces acceleration restrictions, second line forgoes them
            acceleration = min(max(desired_acceleration, min_acceleration), max_acceleration)
            #acceleration = desired_acceleration

            previous_distance_error = distance_error
        else:
            steps_til_reaction -= 1

        frame = { f"{tail_id}.a": acceleration, f"{tail_id}.v": velocity, f"{tail_id}.p": distance_travelled, f"{head_id}-{tail_id}.dg": distance_goal, f"{head_id}-{tail_id}.d": distance }
        frames.append(frame)

    return frames

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Generates synthetic data for a two agent convoy scenario scene")
    arg_parser.add_argument("output_file_path")
    args = arg_parser.parse_args()

    create_two_agent_convoy_scene_with_action_range(args.output_file_path)
