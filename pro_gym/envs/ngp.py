""" Natural Gas Processing Simulated Environment """
import os
from pro_gym.envs.dwsim_env import DWSimEnvBase 

class NaturalGasProcess(DWSimEnvBase):
    def __init__(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        flowsheet_path = "{}/assets/flowsheet/natural_gas_processing.dwxmz".format(cur_path)
        super().__init__(flowsheet_path)

    def get_obs(self):
        obs = self._get_obs()
        return obs

    def step(self, action):
        # take actions
        self._exec_actions(action)
        # step the simulation
        self.interf.CalculateFlowsheet2(self.sim)
        # get the next observation
        obs_next = self.get_obs()
        return obs_next, None, None, None
    
    def reward_func(self):
        """ the reward function of the environment """
        raise NotImplementedError