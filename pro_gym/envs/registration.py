""" this module is used to register the environment """
import importlib

registry = {}

def register(id, entry_point):
    """ this function is used to register the environment """
    global registry
    registry[id] = entry_point

def make(id):
    """ this function is used to create the environment """
    if id not in registry.keys():
        raise NotImplementedError("Environment: {} has not been founded!".format(id))
    env_creator = load_env_creator(registry[id])
    return env_creator()

def load_env_creator(name):
    """ load the environment """
    mod_name, attr_name = name.split(":")
    mod = importlib.import_module(mod_name)
    fn = getattr(mod, attr_name)
    return fn