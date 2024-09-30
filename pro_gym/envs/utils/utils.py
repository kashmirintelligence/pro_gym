""" API to get observation and control the operational units """

# material stream
def get_material_stream_obs(obj):
    """ This function is used to get the energy stream's outputs """
    # state specifications
    temp = obj.GetTemperature()
    pressure = obj.GetPressure()
    enthalpy = obj.GetMassEnthalpy()
    entropy = obj.GetMassEntropy()
    # flow specification
    mass_flow = obj.GetMassFlow()
    molar_flow = obj.GetMolarFlow()
    vol_flow = obj.GetVolumetricFlow()
    properties = {"Temperature": temp, "Pressure": pressure, "Enthalpy": enthalpy, "Entropy": entropy, "MassFlow": mass_flow, \
                "MolarFlow": molar_flow, "VolumetricFlow": vol_flow}
    comps_molar = get_material_compositions(obj, mode="Molar")
    comps_mass = get_material_compositions(obj, mode="Mass")
    # combine two observations
    obs = {**properties, **comps_molar, **comps_mass}
    return obs

def get_material_compositions(obj, mode):
    """ This function is used to get composition outputs """
    composition_names_init = obj.GetCompoundNames()
    composition_names = []
    for name_ in composition_names_init:
        composition_names.append("{} ({})".format(name_, mode))
    assert len(composition_names_init) == len(composition_names)
    if mode == "Molar":
        composition_values_ = obj.GetOverallComposition()
    elif mode == "Mass":
        composition_values_ = obj.GetOverallMassComposition()
    else:
        raise NotImplementedError
    composition_values = [val for val in composition_values_]
    mixture_composition = dict(zip(composition_names, composition_values))
    return mixture_composition

# Heater 
def get_heater_obs(obj):
    """ this function is used to get observation from heater """
    # property of heater
    efficiency = obj.get_Efficiency()
    pressure_drop = obj.get_PressureDrop()
    outlet_temp = obj.get_OutletTemperature()
    heat_added = obj.get_HeatDuty()
    obs = {"OutletTemperature": outlet_temp, "PressureDrop": pressure_drop, "HeatAdded": heat_added, "Efficiency": efficiency}
    return obs

# separator
def get_liquid_separator_obs(obj):
    """ this function is used to get observation from separator """
    temp = obj.get_FlashTemperature()
    pressure = obj.get_FlashPressure()
    obs = {"SeparationPressure": pressure, "SeparationTemperature": temp}
    return obs

# expander
def get_expander_turbine_obs(obj):
    """ this function is used to get observation from expander """
    speed = obj.get_Speed()
    pressure_drop = obj.get_PressureDrop()
    outlet_pressure = obj.get_POut()
    power_generated = obj.get_HeatDuty()
    adiabatic_efficiency = obj.get_AdiabaticEfficiency()
    polytropic_efficiency = obj.get_PolytropicEfficiency()
    adiabatic_head = obj.get_AdiabaticHead()
    polytropic_head = obj.get_PolytropicHead()
    pressure_ratio = obj.get_PressureRatio()
    obs = {"RotationSpeed": speed, "PressureDecrease": pressure_drop, "OutletPressure": outlet_pressure, \
            "PowerGenerated": power_generated, "AdiabaticEfficiency": adiabatic_efficiency, "PolytropicEfficiency": polytropic_efficiency, \
            "AdiabaticHead": adiabatic_head, "PolytropicHead": polytropic_head, "PressureRatio": pressure_ratio}
    return obs

# compressor
def get_compressor_obs(obj):
    """ this function is used to get observation from compressor """
    speed = obj.get_Speed()
    pressure_increase = obj.get_PressureIncrease()
    outlet_pressure = obj.get_POut()
    power_required = obj.get_HeatDuty()
    adiabatic_efficiency = obj.get_AdiabaticEfficiency()
    polytropic_efficiency = obj.get_PolytropicEfficiency()
    adiabatic_head = obj.get_AdiabaticHead()
    polytropic_head = obj.get_PolytropicHead()
    obs = {"RotationSpeed": speed, "PressureIncrease": pressure_increase, "OutletPressure": outlet_pressure, \
            "PowerRequired": power_required, "AdiabaticEfficiency": adiabatic_efficiency, "PolytropicEfficiency": polytropic_efficiency, \
            "AdiabaticHead": adiabatic_head, "PolytropicHead": polytropic_head}
    return obs

# energy stream
def get_energy_stream_obs(obj):
    """ this function is used to get observation from energy stream """
    heat_flow = obj.GetEnergyFlow()
    obs = {"HeatFlow": heat_flow}
    return obs

# equilibrium
def get_equilibrium_reactor_obs(obj):
    """ this function is used to get observation from reactor """
    outlet_temp = obj.get_OutletTemperature()
    pressure_drop = 0.0 if obj.get_DeltaP() is None else obj.get_DeltaP()
    obs = {"OutletTemperature": outlet_temp, "PressureDrop": pressure_drop}
    return obs

# cooler
def get_cooler_obs(obj):
    """ this function is used to get observation from cooler """
    pressure_drop = obj.get_PressureDrop()
    outlet_temp = obj.get_OutletTemperature()
    heat_removed = obj.get_DeltaQ()
    efficiency = obj.get_Efficiency()
    obs = {"PressureDrop": pressure_drop, "OutletTemperature": outlet_temp, "HeatRemoved": heat_removed, \
            "Efficiency": efficiency}
    return obs

# splitter
def get_splitter_obs(obj):
    """ this function is used to get observation from the splitter """
    split_ratio1 = obj.GetPropertyValue("SR1")
    split_ratio2 = obj.GetPropertyValue("SR2")
    split_ratio3 = obj.GetPropertyValue("SR3")
    s1_flow = obj.GetPropertyValue("PROP_SP_1")
    s2_flow = obj.GetPropertyValue("PROP_SP_2")
    obs = {"SplitRatioStream1": split_ratio1, "SplitRatioStream2": split_ratio2, "SplitRatioStream3": split_ratio3, \
            "S1Flow": s1_flow, "S2Flow": s2_flow}
    return obs

def get_conversion_reactor_obs(obj):
    """ this function is used to get observation from the reactor """
    outlet_temp = obj.get_OutletTemperature()
    pressure_drop = 0.0 if obj.get_DeltaP() is None else obj.get_DeltaP()
    obs = {"OutletTemperature": outlet_temp, "PressureDrop": pressure_drop}
    return obs

def get_pump_obs(obj):
    """ this function is used to get observation from the pump """
    pressure_increase = obj.get_PressureIncrease()
    outlet_pressure = obj.get_Pout()
    efficiency = obj.get_Efficiency()
    power = obj.get_HeatDuty()
    npshr = obj.get_CurveNPSHr()
    npsha = obj.get_NPSH()
    obs = {"PressureIncrease": pressure_increase, "OutletPressure": outlet_pressure, "Efficiency": efficiency, "Power": power, "NPSHR": npshr, "NPSHA": npsha}
    return obs

def get_recycle_obs(obj):
    """ this function is used to get observation from the recycle """
    max_iterations = obj.get_MaximumIterations()
    smoothing_factor = obj.get_SmoothingFactor()
    mass_flow_toler = obj.GetPropertyValue("PROP_RY_1")
    temp_toler = obj.GetPropertyValue("PROP_RY_2")
    pressure_toler = obj.GetPropertyValue("PROP_RY_3")
    obs = {"MaxIteration": max_iterations, "SmoothingFactor": smoothing_factor, "MassFlowTolerance": mass_flow_toler, \
            "TemperatureTolerance": temp_toler, "PressureTolerance": pressure_toler}
    return obs

def get_energy_recycle_obs(obj):
    """ this function is used to get observation from the energy recycle block """
    max_iterations = obj.get_MaximumIterations()
    energy_flow_toler = obj.GetPropertyValue("PROP_ER_1")
    obs = {"MaxIteration": max_iterations, "EnergyFlowTolerance": energy_flow_toler}
    return obs

def get_dist_col_obs(obj):
    """ this function is used to get observation from the distillation column """
    condenser_spec = obj.GetPropertyValue("Condenser_Specification_Value")
    reboiler_spec = obj.GetPropertyValue("Reboiler_Specification_Value")
    obs = {"CondenserSpec": condenser_spec, "ReboilerSpec": reboiler_spec}
    return obs

def get_heat_ex_obs(obj):
    """ this function is used to get the heat exchanger observation """
    hot_pressure_drop = obj.get_HotSidePressureDrop()
    cold_pressure_drop = obj.get_ColdSidePressureDrop()
    hot_temp = obj.get_HotSideOutletTemperature()
    cold_temp = obj.get_ColdSideOutletTemperature()
    htc = obj.get_OverallCoefficient()
    area = obj.get_Area()
    heat_ex = obj.get_Q()
    efficiency = obj.get_Efficiency()
    return {"HotPressureDrop": hot_pressure_drop, "ColdPressureDrop": cold_pressure_drop, "HotTemperature": hot_temp, \
            "ColdTemperature": cold_temp, "HTC": htc, "HeatExArea": area, "HeatEx": heat_ex, "Efficiency": efficiency}

"""
belows are the functions to set actions by type in the simulator
"""
def assign_vals(actions, func_mappings):
    """ this function is used to map the actions to the simulator """
    for act_type in actions.keys():
        act_ = actions[act_type]
        if act_type in func_mappings.keys():
            func_mappings[act_type](act_)
        else:
            raise NotImplementedError

# start to set actions
def set_material_stream_actions(actions, obj):
    """ set the material stream actions """ 
    methods_mapping = {"MassFlow": obj.SetMassFlow, \
                        "MolarFlow": obj.SetMolarFlow, \
                        "VolumetricFlow": obj.SetVolumetricFlow, \
                        "Temperature": obj.SetTemperature, \
                        "Pressure": obj.SetPressure,\
                        "Enthalpy": obj.SetMassEnthalpy, \
                        "Entropy": obj.SetMassEntropy, \
                        "Compositions": obj.SetOverallComposition, 
                        }
    # execute actions
    assign_vals(actions, methods_mapping)

def set_heater_actions(actions, obj):
    """ set the material heater actions """ 
    methods_mapping = {"PressureDrop": obj.set_PressureDrop,\
                        "OutletTemperature": obj.set_OutletTemperature, \
                        "Efficiency": obj.set_Efficiency, \
                        "HeatAdded": obj.set_HeatDuty}
    # execute actions
    assign_vals(actions, methods_mapping)


def set_liquid_separator_actions(actions, obj):
    """ set the separator actions """
    methods_mapping = {"SeparationPressure": obj.set_FlashTemperature, \
                        "SeparationTemperature": obj.set_FlashTemperature}
    # execute actions
    assign_vals(actions, methods_mapping)

def set_expander_turbine_actions(actions, obj):
    """ set the expander actions """
    methods_mapping = {"PressureDecrease": obj.set_PressureDrop, \
                        "OutletPressure": obj.set_POut, \
                        "PowerGenerated": obj.set_HeatDuty, \
                        "AdiabaticEfficiency": obj.set_AdiabaticEfficiency, \
                        "PolytropicEfficiency": obj.set_PolytropicEfficiency, \
                        "AdiabaticHead": obj.set_AdiabaticHead, \
                        "PolytropicHead": obj.set_PolytropicHead, \
                        "PressureRatio": obj.set_PressureRatio}
    if "RotationSpeed" in actions.keys():
        act_ = actions["RotationSpeed"]
        obj.SetPropertyValue("RotationSpeed", act_)
        del actions['RotationSpeed']
    # execute actions
    assign_vals(actions, methods_mapping)

def set_compressor_actions(actions, obj):
    """ set the compressor actions """
    methods_mapping = {"PressureIncrease": obj.set_PressureIncrease, \
                        "OutletPressure": obj.set_POut, \
                        "PowerRequired": obj.set_HeatDuty, \
                        "AdiabaticEfficiency": obj.set_AdiabaticEfficiency, \
                        "PolytropicEfficiency": obj.set_PolytropicEfficiency, \
                        "AdiabaticHead": obj.set_AdiabaticHead, \
                        "PolytropicHead": obj.set_PolytropicHead}
    if "RotationSpeed" in actions.keys():
        act_ = actions["RotationSpeed"]
        obj.SetPropertyValue("RotationSpeed", act_)
        del actions['RotationSpeed']
    # execute actions
    assign_vals(actions, methods_mapping)

def set_energy_stream_actions(actions, obj):
    """ set the energy stream actions """
    methods_mapping = {"HeatFlow": obj.SetEnergyFlow}
    # execute actions
    assign_vals(actions, methods_mapping)

# reactor
def set_equilibrium_reactor_actions(actions, obj):
    """ set the reactor actions """
    methods_mapping = {"OutletTemperature": obj.set_OutletTemperature, \
                        "PressureDrop": obj.set_DeltaP}
    # execute actions
    assign_vals(actions, methods_mapping)

# cooler
def set_cooler_actions(actions, obj):
    """ set the cooler actions """
    methods_mapping = {"PressureDrop": obj.set_PressureDrop, \
                        "OutletTemperature": obj.set_OutletTemperature, \
                        "HeatRemoved": obj.set_DeltaQ, \
                        "Efficiency": obj.set_Efficiency}
    # execute actions
    assign_vals(actions, methods_mapping)

# splitter
def set_splitter_actions(actions, obj):
    """ set the splitter actions """
    for act_type in actions.keys():
        act_ = actions[act_type]
        if act_type == "SplitRatioStream1":
            obj.SetPropertyValue("SR1", act_)
        elif act_type == "SplitRatioStream2":
            obj.SetPropertyValue("SR2", act_)
        elif act_type == "SplitRatioStream3":
            obj.SetPropertyValue("SR3", act_)
        elif act_type == "S1Flow":
            obj.SetPropertyValue("PROP_SP_1", act_)
        elif act_type == "S2Flow":
            obj.SetPropertyValue("PROP_SP_2", act_)

# conversation reactor
def set_conversion_reactor_actions(actions, obj):
    """ set conversion reactor actions """
    methods_mapping = {"OutletTemperature": obj.set_OutletTemperature, \
                        "PressureDrop": obj.set_DeltaP}
    # execute actions
    assign_vals(actions, methods_mapping)

def set_pump_actions(actions, obj):
    """ set pump actions """
    methods_mapping = {"PressureIncrease": obj.set_PressureIncrease, \
                        "OutletPressure": obj.set_Pout, \
                        "Efficiency": obj.set_Efficiency, \
                        "Power": obj.set_HeatDuty}
    # execute actions
    assign_vals(actions, methods_mapping)

def set_recycle_actions(actions, obj):
    """ set recycle actions """
    for act_type in actions.keys():
        act_ = actions[act_type]
        if act_type == "MaxIteration":
            obj.set_MaximumIterations(act_)
        elif act_type == "Smoothing":
            obj.set_SmoothingFactor(act_)
        elif act_type == "MassFlowTolerance":
            obj.SetPropertyValue("PROP_RY_1", act_)
        elif act_type == "TemperatureTolerance":
            obj.SetPropertyValue("PROP_RY_2", act_)
        elif act_type == "PressureTolerance":
            obj.SetPropertyValue("PROP_RY_3", act_)

def set_energy_recycle_actions(actions, obj):
    """ set energy recycle actions """
    for act_type in actions.keys():
        act_ = actions[act_type]
        if act_type == "MaxIteration":
            obj.set_MaximumIterations(act_)
        elif act_type == "EnergyFlowTolerance":
            obj.SetPropertyValue("PROP_ER_1", act_)

def set_dist_col_actions(actions, obj):
    """ set distillation column actions """
    for act_type in actions.keys():
        act_ = actions[act_type]
        if act_type == "CondenserSpec":
            obj.SetCondenserSpec("Reflux Ratio", act_, " ")
        elif act_type == "ReboilerSpec":
            obj.SetReboilerSpec("Product Molar Flow Rate", act_, "kmol/h")

def set_heat_ex_actions(actions, obj):
    """ set heat exchanger actions """
    methods_mapping = {"HotPressureDrop": obj.set_HotSidePressureDrop, \
                        "ColdPressureDrop": obj.set_ColdSidePressureDrop, \
                        "HotTemperature": obj.set_HotSideOutletTemperature, \
                        "ColdTemperature": obj.set_ColdSideOutletTemperature, \
                        "HTC": obj.set_OverallCoefficient, \
                        "HeatExArea": obj.set_Area, \
                        "HeatEx": obj.set_Q, \
                        "Efficiency": obj.set_Efficiency}
    # execute actions
    assign_vals(actions, methods_mapping)