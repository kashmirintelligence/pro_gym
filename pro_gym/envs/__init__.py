from pro_gym.envs.registration import register
""" register the environment """

# Natural Gas Processing
register(
    id="NaturalGasProcessing-v0",
    entry_point="pro_gym.envs.ngp:NaturalGasProcess",
)

# PSD
register(
    id="PSD-v0",
    entry_point="pro_gym.envs.psd:PSD",
)

# automation pump
register(
    id="AutomationPump-v0",
    entry_point="pro_gym.envs.pump:AutomationPump",
)