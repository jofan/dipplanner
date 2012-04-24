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
# Strongly inspired by Guy Wittig's MVPlan 
"""
Contains a Tank Class
in MVPlan, this class was the 'Gas' class
"""

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import logging
import math

# local imports
import settings
from dipp_exception import DipplannerException


class InvalidGas(DipplannerException):
  """Exception raised when the gas informations provided for the Tank
  are invalid
  
  """
  def __init__(self, description):
    """constructor : call the upper constructor and set the logger"""
    DipplannerException.__init__(self, description)
    self.logger = logging.getLogger("dipplanner.DipplannerException.InvalidGas")
    self.logger.error("Raising an exception: InvalidGas ! (%s)" % description)

class InvalidTank(DipplannerException):
  """Exception raised when the tank infos provided are invalid
  
  """
  def __init__(self, description):
    """constructor : call the upper constructor and set the logger"""
    DipplannerException.__init__(self, description)
    self.logger = logging.getLogger("dipplanner.DipplannerException.InvalidTank")
    self.logger.error("Raising an exception: InvalidTank ! (%s)" % description)
  
class InvalidMod(DipplannerException):
  """Exception raised when the given MOD is incompatible with the gas
  provided for the tank
  
  """
  def __init__(self, description):
    """constructor : call the upper constructor and set the logger"""
    DipplannerException.__init__(self, description)
    self.logger = logging.getLogger("dipplanner.DipplannerException.InvalidMod")
    self.logger.error("Raising an exception: InvalidMod ! (%s)" % description)
  
class EmptyTank(DipplannerException):
  """Exception raised when trying to consume more gas in tank than the
  remaining gas
  
  """
  def __init__(self, description):
    """constructor : call the upper constructor and set the logger"""
    DipplannerException.__init__(self, description)
    self.logger = logging.getLogger("dipplanner.DipplannerException.EmptyTank")
    self.logger.error("Raising an exception: EmptyTank ! (%s)" % description)
  
class Tank(object):
  """This class implements a representation of dive tanks wich 
  contains breathing Gas
  We provide proportion of N2, O2, He, calculates MOD and volumes during the
  dives
  We can also (optionnaly) provide the type of tanks : volume and pressure
  
  """
  
  def __init__(self,  f_O2=0.21, f_He=0.0, max_ppo2=settings.DEFAULT_MAX_PPO2, 
                      mod=None, tank_vol=12.0, tank_pressure=200):
    """Constructor for Tank class
    If nothing is provided, create a default 'Air' with 12l/200b tank
    and max_ppo2 to 1.6 (used to calculate mod)
    if mod not provided, mod is calculed based on max tolerable ppo2
    
    Keyword arguments:
    f_O2 -- Fraction of O2 in the gaz in % : between 0.0 and 1.0
    f_He -- Fraction of He in the gaz in % : between 0.0 and 1.0
    max_ppo2 -- sets the maximum ppo2 you want for this tank
                (default: settings.DEFAULT_MAX_PPO2)
    mod -- Specify the mod you want. 
            if not provided, calculates the mod based on max_ppo2
            if provided and not compatible with max_ppo2 : raise InvalidMod
    tank_vol -- Volume of the tank in liter
    Tank_pressure -- Pressure of the tank, in bar
    
    Returns:
    <nothing>
    
    Raise:
    InvalidGas -- see validate()
    InvalidMod -- if mod > max mod based on max_ppo2 and see validate()
    InvalidTank -- see validate()
    """
    #initiate class logger
    self.logger = logging.getLogger("dipplanner.tank.Tank")
    self.logger.debug("creating an instance of Tank: O2:%f, He:%f, \
max_ppo2:%f, mod:%s, tank_vol:%f, tank_pressure:%d" % (f_O2, f_He, max_ppo2,
                                                       mod, tank_vol,
                                                       tank_pressure))
    
    self.f_O2 = float(f_O2)
    self.f_He = float(f_He)
    self.f_N2 = 1.0 - (self.f_O2 + self.f_He)
    self.max_ppo2 = float(max_ppo2)
    self.tank_vol = float(tank_vol)
    self.tank_pressure = float(tank_pressure)
    if mod is not None:
      if mod > self._calculate_mod(self.max_ppo2):
        raise InvalidMod("The mod exceed maximum MOD based on given max ppo2")
      self.mod = float(mod)
    else:
      self.mod = self._calculate_mod(self.max_ppo2)
    
    self.in_use = True
  
    self.used_gas = 0.0
    if self.tank_vol and self.tank_pressure:
      self.total_gas = self.calculate_real_volume()
    else:
      self.total_gas = 0.0
    self.remaining_gas = self.total_gas
    self._validate()

  def calculate_real_volume(self, tank_vol=None, tank_pressure=None,
                                  f_O2=None, f_He=None):
    """
    Calculate the real gas volume of the tank (in liter) based
    on Van der waals equation:
    (P+n2.a/V2).(V-n.b)=n.R.T
    
    Keyword arguments:
    tank_vol -- Volume of the tank in liter
                optionnal : if not provided, use self.tank_vol
    tank_pressure -- Pressure of the tank in bar
                     optionnal : if not provided, use self.tank_pressure
    f_O2 -- fraction of O2 in the gas
            optionnal : if not provided, use self.f_O2
    f_He -- fraction of He in the gas
            optionnal : if not provided, use self.f_He

    Returns:
    float -- total gas volume of the tank in liter
    
    Raise:
    <nothing>
    """
    # handle parameters
    if tank_vol is None:
      tank_vol = self.tank_vol
    if tank_pressure is None:
      tank_pressure = self.tank_pressure
    if f_O2 is None:
      f_O2 = self.f_O2
    if f_He is None:
      f_He = self.f_He
    f_N2 = 1.0 - (f_O2 + f_He)

    # Constants used in calculations
    a_O2 = 1.382
    b_O2 = 0.03186
    a_N2 = 1.37
    b_N2 = 0.0387
    a_He = 0.0346
    b_He = 0.0238
    vm_O2 = 31.9988
    vm_N2 = 28.01348
    vm_He = 4.0020602
    R = 0.0831451
    T = 273.15+15 # temp at 15°C
    
    # at first, calculate a and b values for this gas    
    a_gas = math.sqrt(a_O2 * a_O2 * f_O2 * f_O2 + \
                      a_O2 * a_He * f_O2 * f_He + \
                      a_O2 * a_N2 * f_O2 * f_N2 + \
                      a_He * a_O2 * f_He * f_O2 + \
                      a_He * a_He * f_He * f_He + \
                      a_He * a_N2 * f_He * f_N2 + \
                      a_N2 * a_O2 * f_N2 * f_O2 + \
                      a_N2 * a_He * f_N2 * f_He + \
                      a_N2 * a_N2 * f_N2 * f_N2)
    
    b_gas = math.sqrt(b_O2 * b_O2 * f_O2 * f_O2 + \
                      b_O2 * b_He * f_O2 * f_He + \
                      b_O2 * b_N2 * f_O2 * f_N2 + \
                      b_He * b_O2 * f_He * f_O2 + \
                      b_He * b_He * f_He * f_He + \
                      b_He * b_N2 * f_He * f_N2 + \
                      b_N2 * b_O2 * f_N2 * f_O2 + \
                      b_N2 * b_He * f_N2 * f_He + \
                      b_N2 * b_N2 * f_N2 * f_N2)

    # now approximate n (quantities of molecules of gas in the tank in mol)
    # using perfect gas law : PV = nRT : n = PV/RT
    approx_n = (float(tank_pressure) * float(tank_vol)) / (R * T)
    
    # recalculate pressure on the tank whith approx_n
    # P=n.R.T/(V-n.b)-n2.a/V2)
    tank_pressure_mid = (approx_n * R * T) / (tank_vol - approx_n * b_gas) - \
                        (approx_n * approx_n * a_gas) / (tank_vol * tank_vol)
    
    # now try to approx tank_pressure with new_tank_pressure by
    # variating approx_n
    # start with *2 or /2 value (which is enormous !)
    if tank_pressure_mid < tank_pressure:
      n_left = approx_n
      n_right = approx_n * 2
    else:
      n_left = approx_n / 2
      n_right = approx_n
      
    while round(tank_pressure_mid,2) != round(tank_pressure,2):
      n_mid = (n_left + n_right) / 2
      tank_pressure_mid = (n_mid * R * T) / (tank_vol - n_mid * b_gas) - \
                          (n_mid * n_mid * a_gas) / (tank_vol * tank_vol)
      if tank_pressure_mid > tank_pressure:
        # keep left
        n_right = n_mid
      else:
        n_left = n_mid

    # now recalculate the real liters in the tank based on n
    total_gas_volume = n_mid * R * T / settings.AMBIANT_PRESSURE_SURFACE
    self.logger.debug("real total gas volume : %02fl instead of %02fl" % \
                        (total_gas_volume, tank_vol*tank_pressure))
    return total_gas_volume

  def __repr__(self):
    """Returns a string representing the actual tank"""
    return "%s - %s" % (self.name(), self.get_tank_info())
    
  def __str__(self):
    """Return a human readable name of the tank"""
    return "%s" % self.name()
    
  def __unicode__(self):
    """Return a human readable name of the tank in unicode"""
    return u"%s" % self.name()
    
  def __cmp__(self, othertank):
    """Compare a tank to another tank, based on MOD
    
    Keyword arguments:
    othertank -- another tank object
    
    Returns:
    Integer -- result of cmp()
    
    """
    return cmp(self.mod, othertank.mod)
    
  def _calculate_mod(self, max_ppo2):
    """calculate and returns mod for a given ppo2 based on this tank info
    result in meter
    
    Keyword arguments:
    max_ppo2 -- maximum ppo2 accepted (float). Any value accepted, but should 
                be > 0.0
                
    Returns:
    Integer : Maximum Operating Depth in meter
    
    """
    return int(10*(float(max_ppo2) / self.f_O2)-10)
    
  def _validate(self):
    """Test the validity of the tank informations inside this object
    if validity check fails raise an Exception 'InvalidTank'
    
    Keyword arguments:
    <nothing>
    
    Returns:
    <nothing>
    
    Raise:
    InvalidGas -- When proportions of gas exceed 100% for example (or negatives values)
    InvalidMod -- if mod > max mod based on max_ppo2 or ABSOLUTE_MAX_MOD
                  ABSOLUTE_MAX_MOD is a global settings which can not be
                  exceeded.
    InvalidTank -- when pressure or tank size exceed maximum values or are
                   incorrect (like negatives) values
    """
    if self.f_O2 < 0 or self.f_He < 0 or self.f_N2 < 0:
      raise InvalidGas("Proportion of gas should not be < 0")
    if self.f_O2 + self.f_He > 1:
      raise InvalidGas("Proportion of O2+He is more than 100%")
    if self.mod <= 0:
      raise InvalidMod("MOD should be >= 0")
    if self.mod > self._calculate_mod(self.max_ppo2) or \
       self.mod > self._calculate_mod(settings.ABSOLUTE_MAX_PPO2):
      raise InvalidMod("MOD exceed maximum tolerable MOD")
    
    if self.tank_pressure > settings.ABSOLUTE_MAX_TANK_PRESSURE: 
      raise InvalidTank("Tank pressure exceed maximum tolerable pressure")
    if self.tank_pressure <= 0:
      raise InvalidTank("Tank pressure should be greated than zero")
    if self.tank_vol > settings.ABSOLUTE_MAX_TANK_SIZE:
      raise InvalidTank("Tank size exceed maximum tolerable tank size")
    if self.tank_vol <= 0:
      raise InvalidTank("Tank size should be greater than zero")
    
  def name(self):
    """returns a Human readable name for the gaz and tanks
    Differnt possibilities:
    Air, Nitrox, Oxygen, Trimix, Heliox
    """
    name = 'Air'
    composition = ''
    if self.f_He == 0:
      composition = '%s' % int(self.f_O2*100)
      if self.f_O2 == 0.21:
        name = 'Air'
      elif self.f_O2 == 1:
        name = 'Oxygen'
      else:
        name = 'Nitrox ' + composition
    else:
      composition = '%s/%s' % (int(self.f_O2*100), int(self.f_He*100))
      if self.f_He + self.f_O2 == 1:
        name = 'Heliox ' + composition
      else:
        name = 'Trimix ' + composition
    return name
  
  def get_tank_info(self):
    """returns tank infos : size, remaining vol
    example of tank info: 
    15l-90% (2800/3000l)
    """
    if self.total_gas > 0:
      return "%sl-%s%% (%s/%sl)" % (self.tank_vol, 
                                 int(100*self.remaining_gas/self.total_gas),
                                 self.remaining_gas,
                                 self.total_gas)
    else:
      return "(no tank info, used:%sl)" % self.used_gas
      
  def get_mod(self, max_ppo2=None):
    """return mod in meter
    if no argument provided, return the mod based on the current tank (and 
    configured max_ppo2)
    if max_ppo2 is provied, returns the (new) mod based on the given ppo2
    """
    if not max_ppo2:
      return self.mod
    else:
      return self._calculate_mod(max_ppo2)
  
  def get_min_od(self, min_ppo2=settings.ABSOLUTE_MIN_PPO2):
    """return in meter the minimum operating depth for the gas in the tank
    return 0 if diving from/to surface is ok with this gaz
    """
    return self._calculate_mod(min_ppo2)
    
  def consume_gas(self, gas_consumed):
    """Consume gas inside this tank
    take one argument : gas_consumed, in liter
    return EmptyTank Exception if all the gas is consumed
    return remaining gaz in tank (in liter) in other cases
    """
    if self.remaining_gas - gas_consumed < 0:
      raise EmptyTank("There is not enought gas in this tank")
    else:
      self.used_gas += gas_consumed
      self.remaining_gas -= gas_consumed
      return self.remaining_gas