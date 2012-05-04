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
"""Test for Dive class

TODO: more test profiles
"""

__authors__ = [
  # alphabetical order by last name
  'Thomas Chiroux',
]

import unittest
# import here the module / classes to be tested
from dive import Dive
from dive import ProcessingError, NothingToProcess, InfiniteDeco
from tank import Tank, EmptyTank
from segment import SegmentDive, SegmentDeco, SegmentAscDesc
from segment import UnauthorizedMod
import dipplanner
from tools import seconds_to_strtime
import settings

class TestDive(unittest.TestCase):
  def setUp(self):
    # temporary hack (tests):
    dipplanner.activate_debug_for_tests()
    settings.RUN_TIME = True
    settings.SURFACE_TEMP = 12
    self.txhypo = Tank(0.10, 0.50, tank_vol=30.0, tank_pressure=200) # 2x 15l
    self.txtravel = Tank(0.21, 0.30, tank_vol=24.0, tank_pressure=200) # 2x S80
    self.deco1 = Tank(0.8, 0.0, tank_vol=7.0, tank_pressure=200) # 1x S80

    self.divesegdesc1 = SegmentDive(40, 130, self.txtravel, 0)
    self.divesegdesc2 = SegmentDive(40, 30, self.txhypo, 0)

# TxHypo 10/50 + tavel Tx21/30 + DECO Nx80 ==========================================================
# ===================================================== 50m tests ==============
class TestDiveTxHypo50m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 10*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 28:05", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 15.085794724, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 9.25324232336, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 1121.3468175,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo50m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 20*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 64:12", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 40.5271071069, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 23.781737278, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 2152.4648175,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo50m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 30*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "106:25", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 70.3441910104, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 41.1585265797, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3183.5828175,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo50m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 40*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "151:45", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 103.019004534, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 59.3024183811, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 4214.7008175,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo50m50min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(50, 50*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 60m tests ==============
class TestDiveTxHypo60m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 10*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 35:59", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 22.6781367022, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 12.24637595, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 1348.970145,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo60m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 20*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 82:02", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 59.356052656, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 33.2065116454, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 2551.861245,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo60m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 30*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "139:30", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 103.648740553, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 56.8951325031, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3754.752345,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo60m40min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(60, 40*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 70m tests ==============
class TestDiveTxHypo70m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(70, 10*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 44:15", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 31.4264091635, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 16.9976293459, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 1638.7945107,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo70m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(70, 20*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "104:09", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 80.6536163113, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 43.8632021012, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3013.4587107,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo70m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(70, 30*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 80m tests ==============
class TestDiveTxHypo80m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(80, 10*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 54:23", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 41.4673829455, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 22.3007527516, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 2029.6502232,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo80m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(80, 20*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "128:51", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 105.545837844, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 56.7080740285, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3576.0875232,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo80m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(80, 30*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 90m tests ==============
class TestDiveTxHypo90m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(90, 10*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 64:50", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 51.5091204462, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 27.572024528, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 2446.2719007,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo90m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(90, 20*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "155:49", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 131.177021581, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 69.682314275, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 4164.4823007,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo90m30min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(90, 30*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 100m tests ==============
class TestDiveTxHypo100m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(100, 10*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 77:09", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 63.1488565638, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 33.7512984378, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 2888.6595432,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo100m15min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(100, 15*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "127:52", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 109.324197213, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 58.4622854066, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3833.6512932, 7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo100m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(100, 20*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 110m tests ==============
class TestDiveTxHypo110m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(110, 10*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == " 90:33", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 76.6022172498, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 41.0316534593, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3356.8131507,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo110m15min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(110, 15*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "151:30", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 131.394274072, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 72.0895867268, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 4349.33686635, 7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo110m20min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(110, 20*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 120m tests ==============
class TestDiveTxHypo120m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(120, 10*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "105:13", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 89.6851255334, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 49.4798842193, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 3813.97518225,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo120m15min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(120, 15*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 130m tests ==============
class TestDiveTxHypo130m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(130, 10*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "122:26", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 106.065822759, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 60.779893093, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 4290.07631415,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo130m15min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(130, 15*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 140m tests ==============
class TestDiveTxHypo140m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(140, 10*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "141:35", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 123.425344661, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 82.8407639466, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 4829.26258665,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo140m15min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(140, 15*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 150m tests ==============
class TestDiveTxHypo150m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(150, 10*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()
    
  def test_RT(self):
    assert seconds_to_strtime(self.profile1.run_time) == "163:19", "bad dive runtime ? (%s)" % seconds_to_strtime(self.profile1.run_time)
  
  def test_OTU(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.otu, 142.516387326, 7, "bad dive OTU ? (%s)" % self.profile1.model.ox_tox.otu)

  def test_CNS(self):
    self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100, 153.814368358, 7, "bad dive CNS ? (%s)" % (self.profile1.model.ox_tox.cns * 100))
    
  def test_tank_cons(self):
    self.assertAlmostEqual(self.txhypo.used_gas, 5393.48731455,7, "bad used gas (%s)" % self.txhypo.used_gas)

  def test_tank_cons_rule_0(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank_cons_rule_1(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), True, 'Wrong tank status : it should pass the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank_cons_rule_2(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

class TestDiveTxHypo150m15min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    diveseg1 = SegmentDive(150, 15*60, self.txhypo, 0)
    self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
    self.profile1.do_dive()

  def test_tank0_cons(self):
    self.assertEqual(self.profile1.tanks[0].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[0].check_rule(), self.profile1.tanks[0].name()))

  def test_tank1_cons(self):
    self.assertEqual(self.profile1.tanks[1].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[1].check_rule(), self.profile1.tanks[1].name()))

  def test_tank2_cons(self):
    self.assertEqual(self.profile1.tanks[2].check_rule(), False, 'Wrong tank status : it should fail the remaining gas rule test (result:%s on %s)' % (self.profile1.tanks[2].check_rule(), self.profile1.tanks[2].name()))

# ===================================================== 160m tests ==============
class TestDiveTxHypo160m10min(TestDive):
  def setUp(self):
    TestDive.setUp(self)
    
  def runTest(self):
    try:
      diveseg1 = SegmentDive(160, 10*60, self.txhypo, 0)
      self.profile1 = Dive([self.divesegdesc1, self.divesegdesc2, diveseg1], [self.txtravel, self.txhypo, self.deco1])
      self.profile1.do_dive()
    except UnauthorizedMod:
      pass
    else:
      self.fail("should raise UnauthorizedMod")

# ==============================================================================
# ========================== M A I N ===========================================
# ==============================================================================
if __name__ == "__main__":
  import sys
  suite = unittest.findTestCases(sys.modules[__name__])
  #suite = unittest.TestLoader().loadTestsFromTestCase(TestDiveTxHypo150m10min)
  unittest.TextTestRunner(verbosity=2).run(suite)