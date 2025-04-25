import re

'''
Contents of README file:

EU4 Idea evaluator. Evaluations are designed for semi-competitive multiplayer play. This list is very incorrect for singleplayer or WC.
Values for the modifiers are stored in the .py file, although such values can easily be pulled from a .txt file.
Make sure there is no trailing zeros for the idea names. The EU4 idea .txt in both vanilla and Anbennar (and probably others) are inconsistent with this.
Several mods, like Imperium Universalis, rename such ideas to things like "skirmisher_power = x.yz". No non-vanilla ideas are referenced, so these must be added.
I almost certainly missed some of the lesser ideas, add if you wish.

Developed by Softwarekh
'''
name_value_to_weight = {
    ## Military
    'cavalry_power = 0.05': 0.4,
    'cavalry_power = 0.075': 0.6,
    'cavalry_power = 0.1': 0.8,
    'cavalry_power = 0.15': 1.2,
    'cavalry_power = 0.2': 1.6,
    'cavalry_power = 0.25': 2,
    'cavalry_power = 0.3': 2.4,
    'cavalry_power = 0.33': 2.65,
    'discipline = 0.025': 1,
    'discipline = 0.05': 2,
    'discipline = 0.1': 4,
    'infantry_power = 0.05': 0.5,
    'infantry_power = 0.075': 0.75,
    'infantry_power = 0.1': 1,
    'infantry_power = 0.15': 1.50,
    'infantry_power = 0.2': 2,
    'land_morale = 0.05': 0.50,
    'land_morale = 0.1': 1,
    'land_morale = 0.15': 1.50,
    'land_morale = 0.2': 2,
    'reserves_organisation = 0.1': 0.25,
    'reserves_organisation = 0.15': 0.35,
    'reserves_organisation = 0.2': 0.5,
    'reserves_organisation = 0.25': 0.65,
    'reserves_organisation = 0.3': 0.75,
    'leader_land_shock = 1.0': 0.25,
    'leader_land_shock = 2.0': 0.50,
    'leader_land_fire = 1.0': 0.25,
    'leader_land_fire = 2.0': 0.50,
    'leader_land_siege = 1.0': 0.25,
    'leader_land_siege = 2.0': 0.50,
    'leader_land_manuever = 1.0': 0.25,
    'leader_land_manuever = 2.0': 0.50,
    'hostile_attrition = 1.0': 0.20,
    'hostile_attrition = 2.0': 0.30,
    'manpower_in_own_culture_provinces = 0.1': 0.15,
    'manpower_in_own_culture_provinces = 0.15': 0.35,
    'manpower_in_own_culture_provinces = 0.2': 0.50,
    'manpower_in_own_culture_provinces = 0.25': 0.75,
    'manpower_in_own_culture_provinces = 0.3': 0.95,
    'manpower_in_own_culture_provinces = 0.35': 1.05,
    'manpower_in_true_faith_provinces = 0.1': 0.3,
    'manpower_in_true_faith_provinces = 0.15': 0.70,
    'manpower_in_true_faith_provinces = 0.2': 0.90,
    'manpower_in_true_faith_provinces = 0.25': 1.2,
    'manpower_in_true_faith_provinces = 0.3': 1.4,
    'manpower_in_true_faith_provinces = 0.35': 1.6,
    'manpower_in_culture_group_provinces = 0.1': 0.15,
    'manpower_in_culture_group_provinces = 0.15': 0.35,
    'manpower_in_culture_group_provinces = 0.2': 0.45,
    'manpower_in_culture_group_provinces = 0.25': 0.65,
    'manpower_in_culture_group_provinces = 0.3': 0.75,
    'manpower_in_culture_group_provinces = 0.35': 0.80,
    'manpower_in_accepted_culture_provinces = 0.1': 0.2,
    'manpower_in_accepted_culture_provinces = 0.15': 0.4,
    'manpower_in_accepted_culture_provinces = 0.2': 0.55,
    'manpower_in_accepted_culture_provinces = 0.25': 0.85,
    'manpower_in_accepted_culture_provinces = 0.3': 1,
    'manpower_in_accepted_culture_provinces = 0.33': 1.08,
    'manpower_in_accepted_culture_provinces = 0.35': 1.1,
    'global_manpower_modifier = 0.05': 0.25,
    'global_manpower_modifier = 0.075': 0.5,
    'global_manpower_modifier = 0.1': 0.75,
    'global_manpower_modifier = 0.15': 1,
    'global_manpower_modifier = 0.2': 1.25,
    'global_manpower_modifier = 0.25': 1.5,
    'global_manpower_modifier = 0.3': 1.75,
    'global_manpower_modifier = 0.33': 2,
    'global_manpower_modifier = 0.35': 2,
    'mercenary_discipline = 0.025': 0.75,
    'mercenary_discipline = 0.05': 1.5,
    'mercenary_discipline = 0.075': 2,
    'mercenary_discipline = 0.1': 3,
    'siege_ability = 0.05': 0.25,
    'siege_ability = 0.1': 0.5,
    'siege_ability = 0.15': 0.75,
    'siege_ability = 0.2': 1,
    'movement_speed = 0.05': 0.25,
    'movement_speed = 0.1': 0.5,
    'movement_speed = 0.15': 0.75,
    'movement_speed = 0.2': 1,
    'movement_speed = 0.25': 1.25,
    'war_exhaustion = -0.01': 0.15,
    'war_exhaustion = -0.02': 0.3,
    'war_exhaustion = -0.03': 0.5,
    'war_exhaustion = -0.05': 0.6,
    'shock_damage_received = -0.05': 0.5,
    'shock_damage_received = -0.1': 1,
    'shock_damage_received = -0.15': 1.5,
    'shock_damage_received = -0.2': 2,
    'morale_damage_received = -0.05': 0.25,
    'morale_damage_received = -0.1': 0.5,
    'morale_damage_received = -0.15': 0.75,
    'morale_damage_received = -0.2': 1,
    'mercenary_manpower = 0.1': 0.35,
    'mercenary_manpower = 0.15': 0.50,
    'mercenary_manpower = 0.2': 0.65,
    'mercenary_manpower = 0.25': 0.75,
    'mercenary_manpower = 0.3': 0.9,
    'mercenary_manpower = 0.5': 1.5,
    'defensiveness = 0.05': 0.15,
    'defensiveness = 0.075': 0.2,
    'defensiveness = 0.1': 0.25,
    'defensiveness = 0.15': 0.30,
    'defensiveness = 0.2': 0.35,
    'defensiveness = 0.25': 0.40,
    'land_attrition = -0.1': 0.25,
    'land_attrition = -0.15': 0.40,
    'land_attrition = -0.2': 0.55,
    'land_attrition = -0.25': 0.70,
    'land_attrition = -0.3': 0.85,
    'army_tradition = 0.25': 0.25,
    'army_tradition = 0.5': 0.5,
    'army_tradition = 0.75': 0.75,
    'army_tradition = 0.1': 1,
    'land_forcelimit_modifier = 0.05': 0.2,
    'land_forcelimit_modifier = 0.075': 0.3,
    'land_forcelimit_modifier = 0.1': 0.4,
    'land_forcelimit_modifier = 0.15': 0.5,
    'land_forcelimit_modifier = 0.2': 0.6,
    'land_forcelimit_modifier = 0.25': 0.7,
    'land_forcelimit_modifier = 0.3': 0.8,
    'land_forcelimit_modifier = 0.33': 0.88,
    'cav_to_inf_ratio = 0.1': 0.1,
    'cav_to_inf_ratio = 0.15': 0.15,
    'cav_to_inf_ratio = 0.2': 0.2,
    'cav_to_inf_ratio = 0.25': 0.25,
    'cav_to_inf_ratio = 0.3': 0.3,
    'cav_to_inf_ratio = 0.35': 0.35,
    'cav_to_inf_ratio = 0.4': 0.4,
    'cav_to_inf_ratio = 0.45': 0.45,
    'cav_to_inf_ratio = 0.5': 0.5,
    'shock_damage = 0.05': 0.5,
    'shock_damage = 0.1': 1,
    'shock_damage = 0.15': 1.5,
    'shock_damage = 0.2': 2,
    'garrison_size = 0.1': 0.1,
    'garrison_size = 0.15': 0.15,
    'garrison_size = 0.2': 0.20,
    'garrison_size = 0.25': 0.25,
    'fire_damage = 0.05': 0.5,
    'fire_damage = 0.1': 1,
    'fire_damage = 0.15': 1.5,
    'fire_damage = 0.2': 2,
    'morale_damage = 0.05': 0.25,
    'morale_damage = 0.1': 0.5,
    'morale_damage = 0.15': 0.75,
    'morale_damage = 0.2': 1,
    'artillery_power = 0.05': 0.5,
    'artillery_power = 0.075': 0.75,
    'artillery_power = 0.1': 1,
    'artillery_power = 0.15': 1.5,
    'artillery_power = 0.2': 2,
    'fire_damage_received = -0.05': 0.5,
    'fire_damage_received = -0.1': 1,
    'fire_damage_received = -0.15': 1.5,
    'fire_damage_received = -0.2': 2,
    'infantry_shock = 0.5': 3.2,
    'infantry_shock = 0.15': 1,
    'infantry_shock = 0.1': 0.66,
    'infantry_shock = 0.05': 0.33,
    'infantry_shock = 0.2': 1.33,
    'infantry_fire = 0.15': 1,
    'infantry_fire = 0.1': 0.66,
    'infantry_fire = 0.05': 0.33,
    'infantry_fire = 0.2': 1.33,
    'infantry_fire = 0.5': 3.2,
    'cavalry_shock = 0.1': 0.50,
    'cavalry_shock = 0.15': 0.75,
    'cavalry_shock = 0.2': 1,
    'cavalry_shock = 0.25': 1.25,
    'cavalry_shock = 0.3': 1.5,
    'cavalry_shock = 0.35': 1.75,
    'cavalry_shock = 0.4': 2,
    'cavalry_shock = 0.45': 2.25,
    'cavalry_shock = 0.5': 2.5,
    'cavalry_fire = 0.1': 0.50,
    'cavalry_fire = 0.15': 0.75,
    'cavalry_fire = 0.2': 1,
    'cavalry_fire = 0.25': 1.25,
    'cavalry_fire = 0.3': 1.5,
    'cavalry_fire = 0.35': 1.75,
    'cavalry_fire = 0.4': 2,
    'cavalry_fire = 0.45': 2.25,
    'cavalry_fire = 0.5': 2.5,
    'cavalry_flanking = 0.5': 0.15,
    'cavalry_flanking = 0.25': 0.075,
    'cavalry_flanking = 0.75': 0.22,
    'cavalry_flanking = 1.0': 0.30,
    'artillery_fire = 0.5': 1,
    'artillery_fire = 0.25': 0.5,
    'artillery_fire = 0.3': 0.75,
    'artillery_fire = 0.15': 0.3,
    'artillery_fire = 1.0': 2,
    'manpower_recovery_speed = 0.1': 0.5,
    'manpower_recovery_speed = 0.15': 0.75,
    'manpower_recovery_speed = 0.2': 1,
    'manpower_recovery_speed = 0.25': 1.25,
    'manpower_recovery_speed = 0.3': 1.5,
    'backrow_artillery_damage = 0.1': 0.8,
    'backrow_artillery_damage = 0.15': 1.2,
    'backrow_artillery_damage = 0.2': 1.6,
    'army_tradition_decay = -0.005': 0.1,
    'army_tradition_decay = -0.01': 0.15,
    'army_tradition_decay = -0.015': 0.20,
    'army_tradition_decay = -0.02': 0.25,
    'general_cost = -0.1': 0.10,
    'general_cost = -0.15': 0.15,
    'general_cost = -0.2': 0.20,
    'general_cost = -0.25': 0.25,
    'drill_gain_modifier = 0.1': 0.1,
    'drill_gain_modifier = 0.15': 0.15,
    'drill_gain_modifier = 0.2': 0.2,
    'drill_gain_modifier = 0.25': 0.25,
    'drill_gain_modifier = 0.3': 0.3,
    'drill_gain_modifier = 0.33': 0.33,
    'drill_gain_modifier = 0.4': 0.4,
    'drill_gain_modifier = 0.5': 0.5,
    'drill_decay_modifier = -0.1': 0.1,
    'drill_decay_modifier = -0.15': 0.15,
    'drill_decay_modifier = -0.2': 0.2,
    'drill_decay_modifier = -0.25': 0.25,
    'drill_decay_modifier = -0.3': 0.3,
    'drill_decay_modifier = -0.35': 0.35,
    'drill_decay_modifier = -0.4': 0.40,
    'drill_decay_modifier = -0.45': 0.45,
    'drill_decay_modifier = -0.5': 0.50,
    'yearly_army_professionalism = 0.003': 0.8,
    'yearly_army_professionalism = 0.005': 1.2,
    'allowed_samurai_fraction = 0.15': 0.35,
    'amount_of_banners = 0.15': 0.3,
    'garrison_size = 0.15': 0.05,
    'garrison_size = 0.2': 0.1,
    'garrison_size = 0.25': 0.15,
    'garrison_damage = 0.5': 0.2,
    'military_tactics = 0.1': 1,
    'max_general_fire = 1.0': 1,
    'max_general_shock = 1.0': 1,
    'max_hostile_attrition = 1.0': 0.25,
    'max_hostile_attrition = 2.0': 0.5,
    'reinforce_speed = 0.1': 0.15,
    'reinforce_speed = 0.15': 0.3,
    'reinforce_speed = 0.3': 0.6,

    ## Navy
    'heavy_ship_power = 0.05': 0.15,
    'heavy_ship_power = 0.1': 0.25,
    'heavy_ship_power = 0.15': 0.55,
    'heavy_ship_power = 0.2': 0.85,
    'heavy_ship_power = 0.25': 1,
    'galley_power = 0.1': 0.15,
    'galley_power = 0.15': 0.3,
    'galley_power = 0.2': 0.45,
    'galley_power = 0.25': 0.55,
    'ship_durability = 0.1': 0.15,
    'ship_durability = 0.15': 0.3,
    'ship_durability = 0.2': 0.45,
    'ship_durability = 0.25': 0.60,
    'naval_morale = 0.1': 0.15,
    'naval_morale = 0.15': 0.2,
    'naval_morale = 0.2': 0.25,
    'naval_morale = 0.25': 0.3,
    'sunk_ship_morale_hit_recieved = -0.05': 0.05,
    'sunk_ship_morale_hit_recieved = -0.1': 0.1,
    'sunk_ship_morale_hit_recieved = -0.15': 0.15,
    'sunk_ship_morale_hit_recieved = -0.2': 0.2,
    'sunk_ship_morale_hit_recieved = -0.25': 0.25,
    'global_naval_engagement_modifier = 0.05': 0.5,
    'global_naval_engagement_modifier = 0.1': 0.75,
    'global_naval_engagement_modifier = 0.15': 1,
    'global_naval_engagement_modifier = 0.2': 1.25,
    'global_naval_engagement_modifier = 0.25': 1.5,
    'movement_speed_in_fleet_modifier = 1.0': 0.2,
    'siege_blockade_progress = 1.0': 0.25,
    'own_coast_naval_combat_bonus = 1.0': 0.5,
    'allowed_marine_fraction = 0.5': 0.25,
    'allowed_marine_fraction = 0.2': 0.10,
    'allowed_marine_fraction = 0.1': 0.05,
    'light_ship_power = 0.05': 0.03,
    'light_ship_power = 0.1': 0.06,
    'light_ship_power = 0.15': 0.09,
    'light_ship_power = 0.2': 0.12,
    'light_ship_power = 0.25': 0.15,
    'leader_naval_manuever = 1': 0.1,
    'leader_naval_shock = 1': 0.1,
    'leader_naval_fire = 1': 0.1,
    'naval_forcelimit_modifier = 0.10': 0.08,
    'naval_forcelimit_modifier = 0.15': 0.13,
    'naval_forcelimit_modifier = 0.2': 0.15,
    'naval_forcelimit_modifier = 0.25': 0.17,
    'naval_forcelimit_modifier = 0.33': 0.2,
    'naval_forcelimit_modifier = 0.5': 0.25,
    'navy_tradition = 0.5': 0.1,
    'navy_tradition = 1.0': 0.2,
    'navy_tradition_decay = -0.01': 0.05,
    'navy_tradition_decay = -0.02': 0.1,

    ## Dev cost/APC/Tech cost/Idea cost
    'development_cost = -0.05': 1,
    'development_cost = -0.075': 1.5,
    'development_cost = -0.1': 2,
    'development_cost = -0.15': 3,
    'development_cost = -0.2': 4,
    'development_cost_in_primary_culture = -0.5': 0.5,
    'development_cost_in_primary_culture = -0.1': 1,
    'development_cost_in_primary_culture = -0.15': 1.5,
    'development_cost_in_primary_culture = -0.2': 2,
    'idea_cost = -0.05': 0.25,
    'idea_cost = -0.1': 0.5,
    'idea_cost = -0.15': 0.75,
    'idea_cost = -0.2': 1,
    'technology_cost = -0.05': 0.35,
    'technology_cost = -0.1': 0.5,
    'technology_cost = -0.15': 0.75,
    'technology_cost = -0.2': 1,
    'all_power_cost = -0.025': 1,
    'all_power_cost = -0.05': 2,
    'all_power_cost = -0.075': 3,
    'all_power_cost = -0.1': 4,

    ## Eco
    'production_efficiency = 0.1': 0.15,
    'production_efficiency = 0.15': 0.20,
    'production_efficiency = 0.2': 0.3,
    'production_efficiency = 0.25': 0.35,
    'merchants = 1.0': 0.5,
    'merchants = 2.0': 1,
    'merc_maintenance_modifier = -0.05': 0.05,
    'merc_maintenance_modifier = -0.1': 0.1,
    'merc_maintenance_modifier = -0.15': 0.15,
    'merc_maintenance_modifier = -0.2': 0.2,
    'merc_maintenance_modifier = -0.25': 0.25,
    'merc_maintenance_modifier = -0.3': 0.35,
    'may_perform_slave_raid_on_same_religion = yes': 0.5,
    'may_perform_slave_raid = yes': 0.3,
    'global_trade_goods_size_modifier = 0.1': 0.5,
    'global_trade_goods_size_modifier = 0.15': 0.75,
    'global_trade_goods_size_modifier = 0.2': 1,
    'yearly_corruption = -0.05': 0.2,
    'yearly_corruption = -0.1': 0.35,
    'yearly_corruption = -0.15': 0.5,
    'interest = -0.25': 0.2,
    'interest = -0.5': 0.3,
    'interest = -0.75': 0.4,
    'interest = -1.0': 0.5,
    'advisor_cost = -0.05': 0.10,
    'advisor_cost = -0.1': 0.15,
    'advisor_cost = -0.15': 0.30,
    'advisor_cost = -0.2': 0.45,
    'advisor_pool = 1.0': 0.05,
    'advisor_pool = 2.0': 0.1,
    'trade_efficiency = 0.1': 0.1,
    'trade_efficiency = 0.15': 0.15,
    'trade_efficiency = 0.2': 0.20,
    'trade_efficiency = 0.15': 0.25,
    'build_cost = -0.05': 0.1,
    'build_cost = -0.1': 0.2,
    'build_cost = -0.15': 0.3,
    'build_cost = -0.2': 0.4,
    'global_tax_modifier = 0.1': 0.05,
    'global_tax_modifier = 0.15': 0.08,
    'global_tax_modifier = 0.2': 0.10,
    'global_tax_modifier = 0.25': 0.12,
    'global_own_trade_power = 0.05': 0.05,
    'global_own_trade_power = 0.1': 0.1,
    'global_own_trade_power = 0.15': 0.15,
    'global_own_trade_power = 0.2': 0.2,
    'global_own_trade_power = 0.25': 0.25,
    'land_maintenance_modifier = -0.05': 0.05,
    'land_maintenance_modifier = -0.1': 0.10,
    'land_maintenance_modifier = -0.15': 0.15,
    'global_trade_power = 0.05': 0.05,
    'global_trade_power = 0.1': 0.1,
    'global_trade_power = 0.15': 0.15,
    'global_trade__power = 0.2': 0.2,
    'global_trade__power = 0.25': 0.25,
    'global_foreign_trade_power = 0.05': 0.04,
    'global_foreign_trade_power = 0.1': 0.07,
    'global_foreign_trade_power = 0.15': 0.1,
    'global_foreign_trade_power = 0.2': 0.13,
    'global_foreign_trade_power = 0.25': 0.15,
    'trade_steering = 0.05': 0.05,
    'trade_steering = 0.1': 0.1,
    'trade_steering = 0.15': 0.15,
    'trade_steering = 0.2': 0.2,
    'trade_steering = 0.25': 0.25,
    'trade_steering = 0.33': 0.33,
    'global_ship_trade_power = 0.05': 0.05,
    'global_ship_trade_power = 0.1': 0.1,
    'global_ship_trade_power = 0.15': 0.15,
    'global_ship_trade_power = 0.2': 0.2,
    'global_ship_trade_power = 0.25': 0.25,
    'ship_power_propagation = 0.05': 0.05,
    'ship_power_propagation = 0.2': 0.1,
    'ship_power_propagation = 0.15': 0.15,
    'ship_power_propagation = 0.2': 0.2,
    'ship_power_propagation = 0.25': 0.25,
    'state_maintenance_modifier = -0.15': 0.02,
    'state_maintenance_modifier = -0.2': 0.03,
    'state_maintenance_modifier = -0.25': 0.05,
    'inflation_reduction = 0.03': 0.03,
    'inflation_reduction = 0.05': 0.05,
    'inflation_reduction = 0.1': 0.1,
    'inflation_reduction = 0.15': 0.15,
    'inflation_reduction = 0.2': 0.2,

    ## Other
    'yearly_government_power = 1.0': 0.1,
    'province_warscore_cost = -0.05': 0.08,
    'province_warscore_cost = -0.1': 0.15,
    'province_warscore_cost = -0.15': 0.3,
    'province_warscore_cost = -0.2': 0.45,
    'warscore_cost_vs_other_religion = -0.1': 0.2,
    'warscore_cost_vs_other_religion = -0.15': 0.3,
    'warscore_cost_vs_other_religion = -0.2': 0.4,
    'warscore_cost_vs_other_religion = -0.25': 0.5,
    'imperial_authority = 0.1': 0.25,
    'imperial_authority = 0.15': 0.5,
    'imperial_authority = 0.2': 1,
    'build_time = -0.1': 0.2,
    'build_time = -0.15': 0.3,
    'build_time = -0.2': 0.4,
    'governing_capacity_modifier = 0.05': 0.2,
    'governing_capacity_modifier = 0.1': 0.4,
    'governing_capacity_modifier = 0.15': 0.5,
    'governing_capacity_modifier = 0.2': 0.6,
    'governing_capacity_modifier = 0.25': 0.7,
    'governing_capacity_modifier = 0.3': 0.8,
    'colonists = 1.0': 0.75,
    'colonists = 2.0': 1.5,
    'diplomats = 1.0': 0.25,
    'diplomats = 2.0': 0.35,
    'global_colonial_growth = 10.0': 0.15,
    'global_colonial_growth = 15.0': 0.2,
    'global_colonial_growth = 20.0': 0.25,
    'global_colonial_growth = 25.0': 0.3,
    'global_colonial_growth = 30.0': 0.35,
    'diplomatic_upkeep = 1.0': 0.25,
    'ae_impact = -0.1': 0.35,
    'ae_impact = -0.15': 0.5,
    'ae_impact = -0.2': 0.75,
    'core_creation = -0.1': 0.1,
    'core_creation = -0.15': 0.2,
    'core_creation = -0.2': 0.3,
    'core_creation = -0.25': 0.4,
    'monarch_admin_power = 1.0': 0.5,
    'monarch_military_power = 1.0': 0.8,
    'monarch_diplomatic_power = 1.0': 0.5,
    'reform_progress_growth = 0.15': 0.2,
    'reform_progress_growth = 0.2': 0.25,
    'reform_progress_growth = 0.25': 0.30,
    'reform_progress_growth = 0.3': 0.35,
    'reform_progress_growth = 0.35': 0.40,
    'num_accepted_cultures = 3.0': 1,
    'num_accepted_cultures = 2.0': 0.66,
    'num_accepted_cultures = 1.0': 0.33,
    'free_dip_policy = 1.0': 0.2,
    'free_mil_policy = 1.0': 0.5,
    'free_adm_policy = 1.0': 0.2,
    'raze_power_gain = 0.25': 0.3,
    'raze_power_gain = 0.15': 0.1,
    'raze_power_gain = 0.2': 0.2,
    'prestige = 1.0': 0.1,
    'prestige = 0.5': 0.05,
    'possible_policy = 1.0': 0.3,
    'administrative_efficiency = 0.05': 0.3,
    'administrative_efficiency = 0.1': 0.6,
    'administrative_efficiency = 0.15': 0.9,
    'global_allowed_num_of_buildings = 1.0': 0.5,
    'prestige_from_land = 0.5': 0.03,
    'prestige_from_land = 1.0': 0.06,
    'prestige_decay = -0.01': 0.04,
    'prestige_decay = -0.02': 0.08,
    'yearly_patriarch_authority = 0.005': 0.1,
    'yearly_patriarch_authority = 0.01': 0.2,
    'burghers_loyalty_modifier = 0.1': 0.05,
    'all_estate_loyalty_equilibrium = 0.05': 0.05,
    'country_military_power = 1': 0.5,
    'country_admin_power = 1': 0.3,
    'country_diplomatic_power = 1': 0.3,
    'missionaries = 1.0': 0.05,
    'missionaries = 2.0': 0.1,
    'diplomatic_annexation_cost = -0.15': 0.07,
    'diplomatic_annexation_cost = -0.2': 0.12,
    'diplomatic_annexation_cost = -0.25': 0.15,
    'global_autonomy = -0.05': 0.03,
    'global_autonomy = -0.1': 0.06,
    'papal_influence = 0.5': 0.05,
    'papal_influence = 1.0': 0.1,
    'papal_influence = 1.5': 0.15,
    'papal_influence = 2.0': 0.2,
}

## Function to parse the text file and convert it to a dictionary.
def parse_idea_groups(filename):
    idea_groups = {}
    current_group = None
    current_idea = None
    current_modifiers = []

    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()

        if not line or line.startswith('#'):  ## Skip empty lines and comments
            continue

        ## Detect start of a new idea group (e.g., "Z01_ideas = {")
        group_match = re.match(r'([a-zA-Z0-9_]+_ideas) = \{', line)
        if group_match:
            ## Start of new idea group
            current_group = group_match.group(1)
            idea_groups[current_group] = {'modifiers': []}
            ## print(f"Found new idea group: {current_group}")  ## Debugging
            continue

        ## Detect individual ideas and their modifiers.
        idea_match = re.match(r'(\w+_\w+) = \{', line)
        if idea_match:
            current_idea = idea_match.group(1)
            idea_groups[current_group][current_idea] = {}  ## Initialize dictionary for each idea
            current_modifiers = []  ## Reset list
            continue

        ## Parse modifier lines (e.g., "morale_damage_received = -0.1")
        modifier_match = re.match(r'(\w+[\w_]*\w*)\s*=\s*(-?\d+(\.\d+)?)', line)
        if modifier_match:
            modifier_name = modifier_match.group(1)
            modifier_value_str = modifier_match.group(2)  ## Raw value as string
            modifier_value = float(modifier_value_str)  ## Strip leading 0s
            ## print(f"Found modifier: {modifier_name} with raw value: {modifier_value_str} (parsed as {modifier_value})") ##Debugging

            if current_idea:
                idea_groups[current_group][current_idea][modifier_name] = modifier_value
            else:
                idea_groups[current_group]['modifiers'].append((modifier_name, modifier_value))

            continue
        ## Close
        if line == '}':
            current_idea = None  ## End of current idea(s)
            continue

    return idea_groups


## Function for total 'weight' of an idea group
def calculate_total_weight(ideas_group):
    total_weight = 0

    ## Wider modifier process
    for modifier, value in ideas_group['modifiers']:
        weight = name_value_to_weight.get(f"{modifier} = {value}", 0.01)  ## Default to 0.01 iff N/A
        total_weight += weight
        ## print(f"Modifier: {modifier} with value {value} has weight: {weight}")  ## Debugging

    ## Also calculate the weight for each idea's individual modifiers, if applicable
    for idea_name, idea_modifiers in ideas_group.items():
        if idea_name != 'modifiers':  ## Skip the 'modifiers' key itself
            for modifier, value in idea_modifiers.items():
                weight = name_value_to_weight.get(f"{modifier} = {value}",
                                                  0.01)  ## Default to 0.01 if N/A
                total_weight += weight
                ## print(f"Modifier in {idea_name}: {modifier} with value {value} has weight: {weight}")  ## Debugging
    return total_weight

## Path to the .txt file (update this with the correct path to your file)
filename = r"00_country_ideas.txt"


## Parse the file to extract idea groups
idea_groups = parse_idea_groups(filename)

## Debugging: Print the parsed idea groups to verify the parsing
## print(f"Parsed idea groups: {idea_groups}")  ## Debugging

## Calculate and store the weights for all idea groups
weights = {}
for group_name, ideas_group in idea_groups.items():
    total_weight = calculate_total_weight(ideas_group)
    weights[group_name] = total_weight

## Sort idea groups by total weight in descending order
sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)

## Print sorted
print("\nSorted Idea Groups by Weight:")
for group_name, weight in sorted_weights:
    print(f"{group_name}: {weight:.2f}")  ## Final output
