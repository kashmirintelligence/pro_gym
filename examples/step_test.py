""" this script is used to demonstrate the step test """
import os
import numpy as np
from tqdm import tqdm
import pro_gym
from pro_gym.utils.utils import get_action_space, generate_random_actions, \
                    create_csv_headers, generate_row_data, generate_fake_time
from matplotlib import pyplot as plt


if __name__ == "__main__":
    cur_path = os.path.dirname(os.path.abspath(__file__))
    # create the environment
    env = pro_gym.make("AutomationPump-v0")
    # initial value
    init_vals = env.get_obs()
    reservoir_vol_flow = init_vals["Reservoir"]["VolumetricFlow"]
    obses = []
    obses.append(init_vals)
    # output var
    output_var = {"Reservoir": ["VolumetricFlow"], "Pump": ["OutletPressure", "Efficiency", "NPSHR", "NPSHA"], "Tank Outlet": ["Pressure"]}
    for _ in range(20):
        reservoir_vol_flow += 0.000085
        action = {"Reservoir": {"VolumetricFlow": reservoir_vol_flow}}
        # execute action in Pro Gym
        obs_next, _, _, _ = env.step(action)
        obses.append(obs_next)
        # reset the environment
        env.reset()
    # start to plot the figures
    collect_vals = {}
    for i in range(len(obses)):
        for op_name in output_var.keys():
            for var_name in output_var[op_name]:
                if i == 0:
                    collect_vals["{}: {}".format(op_name, var_name)] = []
                    collect_vals["{}: {}".format(op_name, var_name)].append(obses[i][op_name][var_name])
                else:
                    collect_vals["{}: {}".format(op_name, var_name)].append(obses[i][op_name][var_name])
    # plot the figure
    plt.figure(figsize=(24, 10))
    for i, param_name in enumerate(collect_vals.keys()):
        plt.subplot(2, 3, i+1)
        val = collect_vals[param_name]
        plt.plot(np.arange(len(val)), val, "-*")
        plt.xlabel("Steps")
        plt.ylabel("Value")
        plt.title(param_name)
        plt.grid()
    plt.tight_layout()
    plt.savefig("{}/pump_step_test.svg".format(cur_path))