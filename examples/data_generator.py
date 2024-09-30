""" this script is used to generate the data for time forecasting prediction """
import os, csv
import numpy as np
import argparse
from tqdm import tqdm
import pro_gym
from pro_gym.utils.utils import get_action_space, generate_random_actions, \
                    create_csv_headers, generate_row_data, generate_fake_time

# arguments
parser = argparse.ArgumentParser()
parser.add_argument("--env", type=str, default="NaturalGasProcessing-v0", help="define the environment name")
parser.add_argument("--steps", type=int, default=10, help="steps to execute the simulator")
parser.add_argument("--save-dir", type=str, default="saved_csv", help="path to save the csv file")
parser.add_argument("--action-config", type=str, default="config/natural_gas_proc.yaml", help="path to define the action space")
parser.add_argument("--random-range", type=float, default=0.2, help="random range 20 percent +-")
parser.add_argument("--seed", type=int, default=123, help="random seed")

if __name__ == "__main__":
    # get the arguments
    cur_path = os.path.dirname(os.path.abspath(__file__))
    args = parser.parse_args()
    # set the seeds
    np.random.seed(args.seed)
    # start to create the environment
    env = pro_gym.make(args.env)
    # start to generate data
    init_vals = env.get_obs()
    # get the defined action space
    action_space = get_action_space("{}/{}".format(cur_path, args.action_config))
    # create the CSV head
    csv_path = "{}/{}".format(cur_path, args.save_dir)
    if not os.path.exists(csv_path):
        os.makedirs(csv_path, exist_ok=True)
    csv_headers = create_csv_headers(init_vals)
    csv_file = open("{}/{}_{}_{}.csv".format(csv_path, args.env, args.random_range, args.steps), "w")
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(csv_headers)
    # generate fake times
    date_times_str = generate_fake_time(args.steps)
    # generate row vals
    row_data = generate_row_data(init_vals, date_times_str[0])
    # start to generate data
    writer.writerow(row_data)
    for iter in tqdm(range(args.steps)):
        # generate random actions
        random_actions = generate_random_actions(action_space, init_vals, args.random_range)
        # execute the random actions
        obs_next, _, _, _ = env.step(random_actions)
        row_data = generate_row_data(obs_next, date_times_str[iter+1])
        writer.writerow(row_data)
        env.reset()
    csv_file.close()