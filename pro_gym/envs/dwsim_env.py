""" Core API for Pro GYM """
import warnings
warnings.filterwarnings("ignore")
from pro_gym.envs.utils import dll_settings
from tabulate import tabulate
from pro_gym.envs.utils.utils import get_material_stream_obs, get_heater_obs, get_liquid_separator_obs, \
                get_expander_turbine_obs, get_compressor_obs, get_energy_stream_obs, \
                get_equilibrium_reactor_obs, get_cooler_obs, get_splitter_obs, get_conversion_reactor_obs, \
                get_pump_obs, get_recycle_obs, get_energy_recycle_obs, get_dist_col_obs, get_heat_ex_obs
from pro_gym.envs.utils.utils import set_material_stream_actions, set_heater_actions, set_liquid_separator_actions, \
                        set_expander_turbine_actions, set_compressor_actions, set_energy_stream_actions, \
                        set_equilibrium_reactor_actions, set_cooler_actions, set_splitter_actions, \
                        set_conversion_reactor_actions, set_pump_actions, set_recycle_actions, set_energy_recycle_actions, \
                        set_dist_col_actions, set_heat_ex_actions
from DWSIM.Automation import Automation3

# the functions to process the observation
get_obs_by_type = {"Material Stream": get_material_stream_obs, \
                    "Heater": get_heater_obs, \
                    "Gas-Liquid Separator": get_liquid_separator_obs, \
                    "Expander (Turbine)": get_expander_turbine_obs, \
                    "Compressor": get_compressor_obs, \
                    "Energy Stream": get_energy_stream_obs, \
                    "Equilibrium Reactor": get_equilibrium_reactor_obs, \
                    "Cooler": get_cooler_obs, \
                    "Stream Splitter": get_splitter_obs, \
                    "Conversion Reactor": get_conversion_reactor_obs, \
                    "Pump": get_pump_obs, \
                    "Recycle Block": get_recycle_obs, \
                    "Energy Recycle Block": get_energy_recycle_obs, \
                    "Distillation Column": get_dist_col_obs, \
                    "Heat Exchanger": get_heat_ex_obs
                    }
# the functions to process the actions
set_actions_by_type = {"Material Stream": set_material_stream_actions, \
                        "Heater": set_heater_actions, 
                        "Gas-Liquid Separator": set_liquid_separator_actions, \
                        "Expander (Turbine)": set_expander_turbine_actions, \
                        "Compressor": set_compressor_actions, \
                        "Energy Stream": set_energy_stream_actions, \
                        "Equilibrium Reactor": set_equilibrium_reactor_actions, \
                        "Cooler": set_cooler_actions, \
                        "Stream Splitter": set_splitter_actions, \
                        "Conversion Reactor": set_conversion_reactor_actions, \
                        "Pump": set_pump_actions, \
                        "Recycle Block": set_recycle_actions, \
                        "Energy Recycle Block": set_energy_recycle_actions, \
                        "Distillation Column": set_dist_col_actions, \
                        "Heat Exchanger": set_heat_ex_actions
                        }

# the base class of the environment
class DWSimEnvBase:
    def __init__(self, path):
        # load the files
        self.path = path
        self.interf = Automation3()
        self.sim = self.interf.LoadFlowsheet(path)
        self.sim_objects = self._get_simulation_objects()
        # calibrate the val
        self.interf.CalculateFlowsheet2(self.sim)
        # save xml
        self.init_state = self.sim.GetProcessData()

    def step(self, action):
        """ the step function, input the action and get the next observation, reward, terminate and info """
        raise NotImplementedError
    
    def _exec_actions(self, actions):
        """ set actions in the environment """
        for obj_name in actions.keys():
            type = self.sim_objects[obj_name]["type"]
            # set actions
            set_actions_by_type[type](actions[obj_name], self.sim_objects[obj_name]["obj"])
    
    def reset(self):
        """ reset the envrionment to the intial state """
        self.sim.LoadProcessData(self.init_state)
    
    def close(self):
        """ after the user has finished using of environments, close the code for clean up """
        raise NotImplementedError
    
    def _get_simulation_objects(self):
        """ This function is used to get the simulation components """
        sim_objects = {}
        obj_list = self.sim.get_SimulationObjects()
        for obj in obj_list:
            # get the object
            obj_ = obj.Value.GetAsObject()
            obj_type = obj_.GetDisplayName()
            obj_name = obj.Value.ToString().split(":")[0]
            # if this operational unit is available or not
            avail = True
            if obj_type == "Material Stream":
                editor_state = eval(obj_.EditorState)
                avail = False if len(editor_state) == 0 else True
            sim_objects[obj_name] = {}
            sim_objects[obj_name]["obj"] = obj_
            sim_objects[obj_name]["type"] = obj_type
            sim_objects[obj_name]["avail"] = avail
        return sim_objects
    
    def print_sim_objects(self):
        """ This function is used to display the information of simulation objects """
        headers = ["Unit Names", "Unit Type", "Editable"]
        info = []
        for obj_name in self.sim_objects.keys():
            info.append([obj_name, self.sim_objects[obj_name]["type"], self.sim_objects[obj_name]["avail"]])
        print(tabulate(info, headers=headers, tablefmt="grid"))

    def _get_obs(self):
        """ get all observations from the simulation objects """
        obs = {}
        for obj_name in self.sim_objects.keys():
            obj = self.sim_objects[obj_name]["obj"]
            type = self.sim_objects[obj_name]["type"]
            # get observation according to different type
            # TODO: optimise this part 
            if type in get_obs_by_type.keys():
                obs_ = get_obs_by_type[type](obj)
            # store the observation
            obs[obj_name] = obs_
        return obs