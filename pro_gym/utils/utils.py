""" provide util functions for generating data """
import yaml
import numpy as np
from datetime import datetime, timedelta

def generate_random_actions(action_space, init_val, random_range=0.2):
    actions = {}
    """ this function is used to generate random actions of the environment """
    for unit_name in action_space.keys():
        actions[unit_name] = {}
        for avail_spec in action_space[unit_name]:
            init_val_ = init_val[unit_name][avail_spec]
            upper = init_val_ * (1 + random_range)
            lower = init_val_ * (1 - random_range)
            sample_val = np.random.uniform(upper, lower)
            # assign values
            actions[unit_name][avail_spec] = sample_val
    return actions

def get_action_space(yaml_path):
    """ this function is used to get the pre-defined action space in yaml file """
    with open(yaml_path, "r") as file:
        action_space = yaml.safe_load(file)
    return action_space["defined_actions"]

def create_csv_headers(init_vals):
    """ this function is used to create csv header """
    headers = ["Timestamp"]
    for unit_name in init_vals.keys():
        for spec in init_vals[unit_name].keys():
            headers.append("{} : {}".format(unit_name, spec))
    return headers

def generate_row_data(data, datetime):
    """ this function is used to generate a row of data with timestamp """
    row_data = []
    row_data.append(datetime)
    for unit_name in data.keys():
        for spec in data[unit_name].keys():
            row_data.append(data[unit_name][spec])
    return row_data
    
def generate_fake_time(steps):
    """ this function is used to generate a fake time data """
    start_date = datetime(2024, 8, 1, 0, 0, 0)
    date_times = [start_date + timedelta(hours=i) for i in range(steps + 1)]
    date_times_str = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in date_times]
    return date_times_str