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
"""dive class module

Contains:
Dive -- class
"""

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import logging
# local imports
import settings
from dipp_exception import DipplannerException
from segment import SegmentDive, SegmentDeco, SegmentAscDesc
from model.buhlmann.model import Model
from tools import depth_pressure

class NothingToProcess(DipplannerException):
  """raised when the is no input segments to process"""
  def __init__(self, description=""):
    """constructor : call the upper constructor and set the logger"""
    DipplannerException.__init__(self, description)
    self.logger = logging.getLogger("dipplanner.dipp_exception.NothingToProcess")
    self.logger.error("Raising an exception: NothingToProcess ! (%s)" % description)

class ProcessingError(DipplannerException):
  """raised when the is no input segments to process"""
  def __init__(self, description=""):
    """constructor : call the upper constructor and set the logger"""
    DipplannerException.__init__(self, description)
    self.logger = logging.getLogger("dipplanner.dipp_exception.ProcessingError")
    self.logger.error("Raising an exception: ProcessingError ! (%s)" % description)

class InfiniteDeco(DipplannerException):
  """raised when the deco time becomes enourmous (like infinite)"""
  def __init__(self, description=""):
    """constructor : call the upper constructor and set the logger"""
    DipplannerException.__init__(self, description)
    self.logger = logging.getLogger("dipplanner.dipp_exception.InfiniteDeco")
    self.logger.error("Raising an exception: InfiniteDeco ! (%s)" % description)

class Dive(object):
  """Conducts dive based on inputSegments, knownGases, and an existing model.
  Iterates through dive segments updating the Model. When all dive segments are
  processed then calls ascend(0.0) to return to the surface.

  The Model can be either null in which case a new model is created, or can be
  an existing model with tissue loadings.

  Gas switching is done on the final ascent if OC deco or bailout is specified.

  Outputs profile to a List of dive segments
  
  Attributes:
  input_segments -- (list) Stores enabled input dive segment objects
  output_segments -- (list) Stores output segments produced by this class
  tanks -- (list) Stores enabled dive tank objects
  current_tank -- current tank object
  current_depth -- current dive depth
  ambiant_pressure -- (current) ambiant pressure
  current_f_He -- current gas fraction of He
  current_f_N2 -- current gas fraction of N2
  current_f_O2 -- current gas fraction of O2
  model -- model used for this dive
  run_time -- runTime
  pp_O2 -- CCR ppO2, if OC : 0.0
  is_closed_circuit -- Flag to store CC or OC
  in_final_ascent -- flag for final ascent
  is_repetative_dive -- Flag for repetative dives
  surface_interval -- for surf. int. in seconds
  metadata -- description for the dive
  
  """
  
  def __init__(self, known_segments, known_tanks, model=None):
    """Constructor for Profile class
    
    For fist dive, instanciate the profile class with no model (profile will
    create one for you)
    For repetative dives, instanciate profile class with the previous model
    
    Keyword Arguments:
    known_segments -- list of input segments
    known_tanks -- list of tanks for this dive
    model -- model object
    
    Return:
    <nothing>
        
    """
    #initiate class logger
    self.logger = logging.getLogger("dipplanner.dive.Dive")
    self.logger.debug("creating an instance of Dive")
    
    if model is None:
      # new dive : new model
      self.if_repetative_dive = False
      self.model = Model() # buhlman model by default
      self.metadata = ""
    else:
      # repetative dive
      self.if_repetative_dive = True
      self.model = model
      self.model.init_gradient()
    
    # filter input segment for only enabled segments
    self.input_segments = []
    for segment in known_segments:
      if segment.in_use:
        self.input_segments.append(segment)
        
    # filter lists of gases to make the used list of gases
    self.tanks = []
    for tank in known_tanks:
      if tank.in_use:
        self.tanks.append(tank)
        
    # initalise output_segment list
    self.output_segments = []
    
    # other initialisations
    self.surface_interval = 0
    self.is_closed_circuit = False # OC by default
    self.pp_O2 = 0.0 # OC by default
    self.current_tank = None
    self.current_depth = 0.0
    self.in_final_ascent = False
    self.run_time = 0 # in second
    self.metadata = ""

  def __repr__(self):
    """Returns a string representing the result of the dive"""
    text = "Dive profile : GF:%s-%s\n" % (settings.GF_LOW*100, 
                                          settings.GF_HIGH*100)
    for segment in self.output_segments:
      text += "%s\n" % str(segment)
    text += "Gas:\n"
    for tank in self.tanks:
      text += "  %s : used: %.1fl (rem: %.1fl or %db)\n" % \
                  (str(tank), 
                   tank.used_gas, 
                   tank.remaining_gas, 
                   tank.remaining_gas / tank.tank_vol)
    text += "Oxygen Toxicity: OTU:%d, CNS:%d%%\n" % \
                            (self.model.ox_tox.otu, self.model.ox_tox.cns*100)
    return text

  def __str__(self):
    """Return a human readable name of the segment"""
    return self.__repr__()

  def __unicode__(self):
    """Return a human readable name of the segment in unicode"""
    return u"%s" % self.__repr__()
    
  def __cmp__(self, otherdive):
    """Compare a dive to another dive, based on run_time

    Keyword arguments:
    otherdive -- another dive object

    Returns:
    Integer -- result of cmp()

    """
    return cmp(self.run_time, otherdive.run_time)
      
  def do_surface_interval(self, time):
    """Conducts a surface interval 
    by performing a constant depth calculation on air at zero meters
    
    Keyword Arguments:
    time -- duration of the interval, in seconds
    
    Returns:
    <nothing>
    
    Raise:
    <Exceptions from model>
    
    """
    self.model.const_depth(depth=0.0, seg_time=time, 
                            f_He=0.0, f_N2=0.79, pp_O2=0.0)
    self.surface_interval = time
  
  def is_dive_segments(self):
    """Returns true if there are loaded dive segments
    else false means there is nothing to process
    
    Keyword Arguments:
    <none>
    
    Returns:
    True -- if there is at least one input dive segment to process
    False -- if there is no dive segment to process
    
    """
    if len(self.input_segments) > 0:
      return True
    else:
      return False
      
  def do_dive(self):
    """Process the dive
    
    Keyword Arguments:
    <none>
    
    Returns:
    <nothing>
    
    Raise:
    NothingToProcess -- if there is no input segment to process
    +
    <Exceptions from model>
    
    """
    if self.is_dive_segments() == False:
      raise NothingToProcess
    
    run_time_flag = settings.RUN_TIME
     
    # sets initial state
    first_segment = self.input_segments[0]
    self.current_tank = first_segment.tank
    # Sort self.tanks based on MOD ? why ? see below ?
    self.tanks.sort()
    
    self.current_depth = 0.0
    self.pp_O2 = first_segment.setpoint
    if self.pp_O2 == 0.0:
      self.is_closed_circuit = False
    else:
      self.is_closed_circuit = True
    self.in_final_ascent = False
    
    for seg in self.input_segments:
      if seg.type == 'const': #only dive segment allowed for input ignore other
        delta_depth = float(seg.depth) - float(self.current_depth)
        #Ascend or descend to dive segment, 
        #using existing gas and ppO2 settings
        if delta_depth > 0.0: # descent
          self.model.asc_desc(depth_pressure(self.current_depth), #float(self.current_depth)/10, 
                              depth_pressure(seg.depth), #float(seg.depth)/10, 
                              settings.DESCENT_RATE,
                              self.current_tank.f_He,
                              self.current_tank.f_N2,
                              self.pp_O2)
          self.output_segments.append(SegmentAscDesc(self.current_depth, 
                                                     seg.depth, 
                                                     settings.DESCENT_RATE,
                                                     self.current_tank,
                                                     self.pp_O2))
          self.run_time += float(delta_depth) / float(settings.DESCENT_RATE)
          self.logger.debug("descent time : %ss" % \
                                  (float(delta_depth) / settings.DESCENT_RATE))
        else: # ascent
          # call ascend method of this class for decompression calculation
          self.ascend(seg.depth)
        
        # we are now at the desired depth : process the dive segment
        self.current_depth = seg.depth # new depth
        self.pp_O2 = seg.setpoint
        self.current_tank = seg.tank
        if seg.time > 0: #only do this if it's not a waypoint
          if run_time_flag:
            run_time_flag = False # do this one only
            self.model.const_depth(depth_pressure(seg.depth), #float(seg.depth)/10,
                                   seg.time - self.run_time,
                                   self.current_tank.f_He,
                                   self.current_tank.f_N2,
                                   self.pp_O2)
            self.output_segments.append(SegmentDive(seg.depth, 
                                                    seg.time - self.run_time, 
                                                    self.current_tank, 
                                                    self.pp_O2))
            self.metadata += "Dive to %s for %ss\n" % \
                                          (seg.depth, seg.time - self.run_time)
            self.logger.debug("Dive to %s for %ss" % \
                                         (seg.depth, seg.time - self.run_time))
            # run_time = seg_time because it's only done the first time
            self.run_time = seg.time 
            self.logger.debug("update run time : %ss" % self.run_time)
          else:
            self.model.const_depth(depth_pressure(seg.depth), #float(seg.depth)/10,
                                   seg.time,
                                   self.current_tank.f_He,
                                   self.current_tank.f_N2,
                                   self.pp_O2)
            self.output_segments.append(SegmentDive(seg.depth, 
                                                    seg.time, 
                                                    self.current_tank, 
                                                    self.pp_O2))
            self.metadata += "Dive to %s for %ss\n" % (seg.depth, seg.time)
            self.logger.debug("Dive to %s for %ss" % (seg.depth, seg.time))
            self.run_time += seg.time
            self.logger.debug("update run time : %ss" % self.run_time)
        else: #process waypoint
          self.output_segments.append(SegmentDive(seg.depth, 
                                                  seg.time, 
                                                  self.current_tank, 
                                                  self.pp_O2))
                                                  
    # all input segment are now processed : process to ascend to the surface 
    self.in_final_ascent = True
    # ascend to the surface
    self.ascend(0.0)
    # for each output segment, recalculate runtime and update segments
    total_time = 0
    for output_seg in self.output_segments:
      total_time += output_seg.time
      output_seg.run_time = total_time
    if total_time != self.run_time:
      self.logger.warning("dive run_time (%ss) differs from all segments \
@                           time (%ss)" % (self.run_time, total_time) )
    # write metadata into the model
    self.model.metadata = self.metadata
    # recalculate the gas consumptions
    self.do_gas_calcs()
    
  def ascend(self, target_depth):
    """Ascend to target depth, decompressing if necessary. 
    If inFinalAscent then gradient factors start changing, 
    and automatic gas selection is made. 
    
    Keyword Arguments:
    target_depth -- in meter, target depth for the ascend
    
    Returns:
    <nothing>
    
    Raise:
    <Exceptions from model>
    
    """
    force_deco_stop = False
    in_deco_cycle = False
    deco_stop_time = 0
    
    if self.in_final_ascent and settings.USE_OC_DECO:
      self.set_deco_gas(self.current_depth)
    
    if self.current_depth < target_depth:
      # going backwards !
      raise ProcessingError("Not allowed to ascend while descending !")
    
    # Set initial stop to be the next integral stop depth
    if self.current_depth % settings.STOP_DEPTH_INCREMENT > 0:
      # we are not on a stop depth already : go to the next stop depth
      # TODO : int() or round() ?
      next_stop_depth = int(float(self.current_depth) \
                            / float(settings.STOP_DEPTH_INCREMENT))\
                         * settings.STOP_DEPTH_INCREMENT
    else:
      next_stop_depth = int(self.current_depth - settings.STOP_DEPTH_INCREMENT)

    self.logger.debug("next_stop_depth: %s" % next_stop_depth)
    # hack in case we are overshooting or hit last stop or any of 
    # the other bizzar combinations ...
    if next_stop_depth < target_depth or \
       self.current_depth < settings.LAST_STOP_DEPTH:
      next_stop_depth = target_depth
    elif next_stop_depth == settings.LAST_STOP_DEPTH:
      self.logger.debug("next_stop_depth==LAST_STOP_DEPTH !")
      next_stop_depth = target_depth # TODO: bizarre...
    elif next_stop_depth < settings.LAST_STOP_DEPTH:
      next_stop_depth = settings.LAST_STOP_DEPTH

    start_depth = self.current_depth # Initialise ascent segment start depth
    in_ascent_cycle = True # Start in free ascent
    
    # Initialise gradient factor for next (in this case first) stop depth
    self.model.gradient.set_gf_at_depth(next_stop_depth)
    
    # Remember maxM-Value and controlling compartment
    max_MV = self.model.m_value(depth_pressure(self.current_depth)) #float(self.current_depth)/10)
    control = self.model.control_compartment()
    
    while self.current_depth > target_depth:
      self.logger.debug("ascent -- debug : %s, %s" % \
                                           (self.current_depth, target_depth))
      # can we move to the proposed next stop depth ?
      self.logger.debug("model ceiling: %s" % self.model.ceiling())
      while force_deco_stop or next_stop_depth < self.model.ceiling():
        in_deco_cycle = True
        force_deco_stop = False #Only used for first entry into deco stop
        if in_ascent_cycle: #Finalise last ascent cycle as we are now decomp
          if start_depth > self.current_depth:
            # add ascent segment
            self.logger.debug("Add AscDesc(1): start_depth:%s, \
                               current_depth:%s" % \
                               (start_depth, self.current_depth))
            self.output_segments.append(SegmentAscDesc(start_depth, 
                                                       self.current_depth, 
                                                       settings.ASCENT_RATE,
                                                       self.current_tank,
                                                       self.pp_O2))
          in_ascent_cycle = False
          # TODO: start depth is not re-initialised after first use
          
        # set m-value gradient under the following conditions:
        #   - if not in multilevel mode, then set it as soon as 
        #     we do a decompression cycle
        #   - otherwise wait until we are finally surfacing before setting it
        if (not settings.MULTILEVEL_MODE or self.in_final_ascent) and \
            (not self.model.gradient.gf_set):
          self.logger.debug("...set m-value gradient")
          self.model.gradient.set_gf_slope_at_depth(self.current_depth)
          self.model.gradient.set_gf_at_depth(next_stop_depth)
        
        #calculate stop_time
        if deco_stop_time == 0 and \
           self.run_time % settings.STOP_TIME_INCREMENT > 0:
          stop_time = int(self.run_time / settings.STOP_TIME_INCREMENT) *\
                      settings.STOP_TIME_INCREMENT +\
                      settings.STOP_TIME_INCREMENT -\
                      self.run_time
          if stop_time == 0:
            stop_time = settings.STOP_TIME_INCREMENT # in second
        else:
          stop_time = settings.STOP_TIME_INCREMENT # in second

        # execute the stop
        self.logger.debug("deco at %sm for %s (total:%s) (fhe:%s, fN2:%s, ppo2:%s), ceiling:%s" % \
                                                     (self.current_depth,
                                                      stop_time,
                                                      deco_stop_time,
                                                      self.current_tank.f_He,
                                                      self.current_tank.f_N2,
                                                      self.pp_O2,
                                                      self.model.ceiling()))
        self.model.const_depth(depth_pressure(self.current_depth), #float(self.current_depth)/10,
                               stop_time,
                               self.current_tank.f_He,
                               self.current_tank.f_N2,
                               self.pp_O2)
        
        deco_stop_time += stop_time
        # sanity check for infinite loop
        if deco_stop_time > 300000:
          raise InfiniteDeco("Infinite deco error")
          
      # finished decompression loop 
      if in_deco_cycle:
        self.logger.debug("...in deco cycle")
        # finalise the last deco cycle
        self.run_time += deco_stop_time
        self.logger.debug("update run time : %ss" % self.run_time)
        if settings.FORCE_ALL_STOPS:
          force_deco_stop = True
        
        # write deco segment
        deco_segment = SegmentDeco(self.current_depth, 
                                   deco_stop_time,
                                   self.current_tank,
                                   self.pp_O2)
        deco_segment.mv_max = max_MV
        deco_segment.gf_used = self.model.gradient.gf
        deco_segment.control_compartment = control
        self.output_segments.append(deco_segment)
        in_deco_cycle = False
        deco_stop_time = 0
      elif in_ascent_cycle:
        #self.logger.debug("...in ascent cycle")
        # did not decompress, just ascend
        # TODO : if we enable this code always (not in rlif, but direct) then
        #        model will ascend between deco stops, but ... 
        #        this causes collateral damage to runtim calculations
        self.model.asc_desc(depth_pressure(self.current_depth), #float(self.current_depth)/10, 
                            depth_pressure(next_stop_depth), #float(next_stop_depth)/10,
                            settings.ASCENT_RATE,
                            self.current_tank.f_He,
                            self.current_tank.f_N2,
                            self.pp_O2)
        self.run_time += abs(float(self.current_depth)-float(next_stop_depth)) \
                         / (float(settings.ASCENT_RATE))
        self.logger.debug("update run time : %ss" % self.run_time)
        # TODO: Issue here is that this ascent time is not accounted for 
        #       in any segments unless it was in an ascent cycle            
      
      #now we moved up the the next depth
      self.current_depth = next_stop_depth
      max_MV = self.model.m_value(depth_pressure(self.current_depth)) #float(self.current_depth)/10)
      control = self.model.control_compartment()
      
      # Check and switch deco gas
      temp_tank = self.current_tank # remember in case we switch
      if self.set_deco_gas(self.current_depth): # True if we changed gas
        if in_ascent_cycle:
          self.logger.debug("Add AscDesc(2): start_depth:%s, \
                             current_depth:%s" % \
                                            (start_depth, self.current_depth))
          self.output_segments.append(SegmentAscDesc(start_depth,
                                                     self.current_depth,
                                                     settings.ASCENT_RATE,
                                                     temp_tank,
                                                     self.pp_O2))
          start_depth = self.current_depth
      
      # set next rounded stop depth
      next_stop_depth = int(self.current_depth) - settings.STOP_DEPTH_INCREMENT
      self.logger.debug("next stop depth: %s, target: %s" % \
                                              (next_stop_depth, target_depth))

      # check in cas we are overshooting or hit last stop
      if next_stop_depth < target_depth or \
         self.current_depth < settings.LAST_STOP_DEPTH:
        self.logger.debug("next_stop_depth (%s) < target_depth (%s)" % \
                                              (next_stop_depth, target_depth))
        next_stop_depth = target_depth
      elif self.current_depth < settings.LAST_STOP_DEPTH:
        self.logger.debug("current_depth (%s) < LAST_STOP_DEPTH (%s)" % \
                                    (current_depth, settings.LAST_STOP_DEPTH))
        next_stop_depth = target_depth
      #elif next_stop_depth < settings.LAST_STOP_DEPTH:
      #  self.logger.debug("next_stop_depth (%s) < settings.LAST_STOP_DEPTH (%s)" % (next_stop_depth, settings.LAST_STOP_DEPTH))
      #  next_stop_depth = settings.LAST_STOP_DEPTH
      #TODO: j'ai commenté les lignes ci-dessus pour éviter une boucle infinie
      #      commprendre pourquoi elles existent...
       
      if self.model.gradient.gf_set: # update gf for next stop
        self.model.gradient.set_gf_at_depth(next_stop_depth)
        
    # are we still in ascent segment ?
    if in_ascent_cycle:
      self.logger.debug("Add AscDesc(3): start_depth:%s, \
                         current_depth:%s" % (start_depth, self.current_depth))
      self.output_segments.append(SegmentAscDesc(start_depth,
                                                 self.current_depth,
                                                 settings.ASCENT_RATE,
                                                 self.current_tank,
                                                 self.pp_O2))
  
  def do_gas_calcs(self):
    """Estimate gas consumption for all output segments 
    and set this into the respective gas objects
    
    Keyword Arguments:
    <none>
    
    Returns:
    <nothing>
    
    Raise:
    <Exceptions from tank>
    
    """
    for seg in self.output_segments:
      seg.tank.consume_gas(seg.gas_used())
      
  def set_deco_gas(self, depth):
    """Select appropriate deco gas for the depth specified
    Returns true if a gas switch occured
    
    Keyword Arguments:
    depth -- target depth to make the choice
    
    Returns:
    True -- if gas swich occured, False if not
    
    Raise:
    <Exceptions from tank>
    
    """
    gas_switch = False
    
    # check to see if we should be changing gases at all ... 
    # if so just return doing nothing
    if not self.in_final_ascent:
      return False
    if not settings.USE_OC_DECO:
      return False
    if len(self.tanks) == 0:
      return False
      
    # check and switch deco gases
    current_tank_sav = self.current_tank
    for temp_tank in self.tanks:
      if temp_tank.get_mod() >= depth and \
         temp_tank.get_min_od() < depth: # authorised tank at this depth
        if temp_tank < current_tank_sav:
          if self.is_closed_circuit:
            # only change from CC to OC when a valid tank for deco is available
            self.pp_O2 = False
            self.is_closed_circuit = False

          self.current_tank = temp_tank
          gas_switch = True
          self.logger.info("Changing gas from %s (mod:%s) to %s (mod:%s)" % \
                                                (current_tank_sav,
                                                current_tank_sav.get_mod(),
                                                self.current_tank,
                                                self.current_tank.get_mod() ))
      #else:
      #  break
    return gas_switch