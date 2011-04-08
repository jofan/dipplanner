#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Thomas Chiroux
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.
# If not, see <http://www.gnu.org/licenses/gpl.html>
# 
# This module is part of dipplanner, a Dive planning Tool written in python
"""Global settings for dipplanner
"""

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

# ======= "Internal" Settings ========
# unless knowing what you're doing, this prefs should not be changed
# by the user
# water density kg/l
FRESH_WATER_DENSITY = 1.0
SEA_WATER_DENSITY = 1.03
ABSOLUTE_MAX_PPO2 = 2.0
ABSOLUTE_MIN_PPO2 = 0.16
ABSOLUTE_MAX_TANK_PRESSURE = 300 # in bar
ABSOLUTE_MAX_TANK_SIZE = 30 # in liter

#TODO: what is the good value : 0.014 or 0.0627 ??
PP_H2O_SURFACE = 0.014 #0.0627 # 0.014 # in bar : eq 10.5mmHG (20°; 60% hum)

HE_NARCOTIC_VALUE = 0.23
N2_NARCOTIC_VALUE = 1.0
O2_NARCOTIC_VALUE = 1.0
AR_NARCOTIC_VALUE = 2.33

STOP_DEPTH_INCREMENT = 3 # in meter
LAST_STOP_DEPTH = 3 # in meter : last stop before surfacing
STOP_TIME_INCREMENT = 1 # in second
FORCE_ALL_STOPS = True # one deco stop begun, force to stop to each deco depth
                       # stop
AMBIANT_PRESSURE_SEA_LEVEL = 1.013#25 # surface pressure (in bar)
METHOD_FOR_DEPTH_CALCULATION = 'simple' # either simple (/10) or complex

# ========= User settings ========
WATER_DENSITY = SEA_WATER_DENSITY 
AMBIANT_PRESSURE_SURFACE = AMBIANT_PRESSURE_SEA_LEVEL

DEFAULT_MAX_PPO2 = 1.6
DEFAULT_MIN_PPO2 = 0.19

DIVE_CONSUMPTION_RATE = 17.0/60 # liter/s
DECO_CONSUMPTION_RATE = 12.0/60 # liter/s

DESCENT_RATE = float(20)/60 # m/s
ASCENT_RATE = float(10)/60 # m/s

RUN_TIME = True  # if True: segments represents runtime, 
                  # if false, segments represents segtime
              
USE_OC_DECO = True # if True, use enabled gases of decomp in oc or bailout

GF_LOW = 0.30
GF_HIGH = 0.80

MULTILEVEL_MODE = False 