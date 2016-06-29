#
# Copyright 2011-2016 Thomas Chiroux
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
"""Test Dives with air."""
import unittest
# import here the module / classes to be tested
from dipplanner.main import activate_debug_for_tests

from dipplanner.dive import Dive
from dipplanner.tank import Tank
from dipplanner.segment import SegmentDive
from dipplanner.segment import UnauthorizedMod
from dipplanner.tools import seconds_to_mmss
from dipplanner import settings


class TestDive(unittest.TestCase):
    def setUp(self):
        # temporary hack (tests):
        activate_debug_for_tests()
        settings.RUN_TIME = True
        settings.SURFACE_TEMP = 12
        self.air12l = Tank(tank_vol=12.0,
                           tank_pressure=200,
                           tank_rule="10b")
        self.airtank = Tank(tank_vol=18.0,
                            tank_pressure=200,
                            tank_rule="10b")
        self.airtank12 = Tank(tank_vol=12.0,
                              tank_pressure=200,
                              tank_rule="10b")
        self.airdouble = Tank(tank_vol=30.0,
                              tank_pressure=200,
                              tank_rule="10b")  # bi15l 200b
        self.txtank1 = Tank(0.21,
                            0.30,
                            tank_vol=20.0,
                            tank_pressure=200,
                            tank_rule="10b")
        self.txtanknormodbl = Tank(0.21,
                                   0.30,
                                   tank_vol=30.0,
                                   tank_pressure=200,
                                   tank_rule="10b")
        self.deco1 = Tank(0.8,
                          0.0,
                          tank_vol=7.0,
                          tank_pressure=200,
                          tank_rule="10b")
        self.deco2 = Tank(0.5,
                          0.0,
                          tank_vol=7.0,
                          tank_pressure=200,
                          tank_rule="10b")
        self.decoo2 = Tank(1.0,
                           0.0,
                           tank_vol=7.0,
                           tank_pressure=200,
                           tank_rule="10b")

# ============================================================================
# ======= S Y S T E M A T I C        T E S T S ===============================
# ============================================================================


# AIR ========================================================================
# =============================================s====== 10m tests ==============
class TestDiveAir10m10min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 10 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 11:00",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertEqual(self.profile1.model.ox_tox.otu,
                         0.0,
                         "bad dive OTU ? (%s)" %
                         self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertEqual(self.profile1.model.ox_tox.cns * 100,
                         0.0,
                         "bad dive CNS ? (%s)" %
                         self.profile1.model.ox_tox.cns * 100)

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas,
                               365.5451775,
                               7,
                               "bad used gas (%s)" % self.airtank12.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining'
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         120,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir10m20min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 20 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 21:00",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertEqual(self.profile1.model.ox_tox.otu,
                         0.0,
                         "bad dive OTU ? (%s)" %
                         self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertEqual(self.profile1.model.ox_tox.cns * 100,
                         0.0,
                         "bad dive CNS ? (%s)" %
                         (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas,
                               709.5707775,
                               7,
                               "bad used gas (%s)" % self.airtank12.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining'
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         1140,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir10m30min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 30 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 31:43",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertEqual(self.profile1.model.ox_tox.otu,
                         0.0,
                         "bad dive OTU ? (%s)" %
                         self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertEqual(self.profile1.model.ox_tox.cns * 100,
                         0.0,
                         "bad dive CNS ? (%s)" %
                         self.profile1.model.ox_tox.cns * 100)

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas,
                               1067.7209458500001,
                               7,
                               "bad used gas (%s)" % self.airtank12.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining'
                         ' gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         0,
                         "Bad no flight time: %s" % no_flight_time)
                         #TODO: STRANGE VALUE..


class TestDiveAir10m40min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 40 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 41:43",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertEqual(self.profile1.model.ox_tox.otu,
                         0.0,
                         "bad dive OTU ? (%s)" %
                         self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertEqual(self.profile1.model.ox_tox.cns * 100,
                         0.0,
                         "bad dive CNS ? (%s)" %
                         self.profile1.model.ox_tox.cns * 100)

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas,
                               1411.74654585,
                               7,
                               "bad used gas (%s)" % self.airtank12.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining'
                         ' gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         0,
                         "Bad no flight time: %s" % no_flight_time)
                         #TODO: strange Value


class TestDiveAir10m50min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 50 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 51:43",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertEqual(self.profile1.model.ox_tox.otu,
                         0.0,
                         "bad dive OTU ? (%s)" %
                         self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertEqual(self.profile1.model.ox_tox.cns * 100,
                         0.0,
                         "bad dive CNS ? (%s)" %
                         self.profile1.model.ox_tox.cns * 100)

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas,
                               1755.77214585,
                               7,
                               "bad used gas (%s)" % self.airtank12.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         0,
                         "Bad no flight time: %s" % no_flight_time)
                         # TODO:Strange Value


class TestDiveAir10m60min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 60 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 61:43",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertEqual(self.profile1.model.ox_tox.otu,
                         0.0,
                         "bad dive OTU ? (%s)" %
                         self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertEqual(self.profile1.model.ox_tox.cns * 100,
                         0.0,
                         "bad dive CNS ? (%s)" %
                         self.profile1.model.ox_tox.cns * 100)

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas,
                               2099.7977458500004,
                               7,
                               "bad used gas (%s)" % self.airtank12.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         60,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir10m70min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(10, 70 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12])

    def runTest(self):
        self.profile1.do_dive()
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())


# ==================================================== 20m tests ==============
class TestDiveAir20m10min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 10 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 12:43",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               3.01929957641,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               1.58670286184,
                               7,
                               "bad dive CNS ? (%s)" %
                               self.profile1.model.ox_tox.cns * 100)

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas,
                               581.5510783499999,
                               7,
                               "bad used gas (%s)" % self.airtank12.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         0,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir20m20min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 20 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 23:26",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               6.36182197227,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               3.34108882675,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas,
                               1115.1422076000001,
                               7,
                               "bad used gas (%s)" % self.airtank12.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         180,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir20m30min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 30 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 34:58",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               9.70434436813,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               5.09547479167,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas,
                               1665.3017119500003,
                               7,
                               "bad used gas (%s)" % self.airtank12.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         720,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir20m40min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 40 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 49:15",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               13.046866764,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               6.84986075658,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank12.used_gas,
                               2249.853556950001,
                               7,
                               "bad used gas (%s)" % self.airtank12.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         1440,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir20m50min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(20, 50 * 60, self.airtank12, 0)
        self.profile1 = Dive([diveseg1], [self.airtank12])

    def runTest(self):
        self.profile1.do_dive()
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())


# ==================================================== 30m tests ==============
class TestDiveAir30m10min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 10 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 15:09",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               6.34006508471,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               2.41216441637,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank.used_gas,
                               831.27378525,
                               7,
                               "bad used gas (%s)" % self.airtank.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         120,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir30m20min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 20 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 31:12",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               13.7054851702,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               5.18994219415,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank.used_gas,
                               1637.3158623000004,
                               7,
                               "bad used gas (%s)" % self.airtank.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         780,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir30m30min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 30 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 53:12",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               21.0724203812,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               7.97003478674,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank.used_gas,
                               2563.5074326500003,
                               7,
                               "bad used gas (%s)" % self.airtank.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         1920,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir30m40min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 40 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 81:30",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               28.4378404667,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               10.7478125645,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank.used_gas,
                               3598.4174548500005,
                               7,
                               "bad used gas (%s)" % self.airtank.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         False,
                         'Wrong tank status : it should not pass the '
                         'remaining gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         3240,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir30m50min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(30, 50 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank])

    def runTest(self):
        self.profile1.do_dive()
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())


# ==================================================== 40m tests ==============
class TestDiveAir40m10min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 10 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 18:14",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               9.0003053587,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               3.43415474781,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank.used_gas,
                               1098.6860910000003,
                               7,
                               "bad used gas (%s)" % self.airtank.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         240,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir40m20min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 20 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 44:17",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               20.032685074329557,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               7.68703392836257,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank.used_gas,
                               2304.0800886,
                               7,
                               "bad used gas (%s)" % self.airtank.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         1620,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir40m30min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 30 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 83:06",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               31.399550660319893,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               12.2139407685185,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airtank.used_gas,
                               3751.838651550002,
                               7,
                               "bad used gas (%s)" % self.airtank.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         3480,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir40m40min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 40 * 60, self.airtank, 0)
        self.profile1 = Dive([diveseg1], [self.airtank])

    def runTest(self):
        self.profile1.do_dive()
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())


# ==================================================== 50m tests ==============
class TestDiveAir50m10min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 10 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 22:50",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               11.1841702136,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               4.34131570513,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas,
                               1412.8618996500004,
                               7,
                               "bad used gas (%s)" % self.airdouble.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         420,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir50m20min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 20 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 63:07",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               26.221462177920216,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               10.420352620579195,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas,
                               3121.7950509,
                               7,
                               "bad used gas (%s)" % self.airdouble.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         2460,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir50m30min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 30 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         "119:48",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               42.20535874820258,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               16.950032408883846,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas,
                               5153.23695765,
                               7,
                               "bad used gas (%s)" % self.airdouble.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         7260,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir50m40min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(50, 40 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble])

    def runTest(self):
        self.profile1.do_dive()
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())


# ==================================================== 60m tests ==============
class TestDiveAir60m10min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 10 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 27:44",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               13.11557113727918,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               6.23985013198273,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas,
                               1752.7026780000008,
                               7,
                               "bad used gas (%s)" % self.airdouble.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         540,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir60m20min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 20 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         " 83:42",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))
    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               32.45512662267348,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               15.587532760930456,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas,
                               4018.665693600001,
                               7,
                               "bad used gas (%s)" % self.airdouble.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         3540,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir60m25min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 25 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         "122:51",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               43.292968196629374,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               20.78297623071619,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas,
                               5366.0548326,
                               7,
                               "bad used gas (%s)" % self.airdouble.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         7740,
                         "Bad no flight time: %s" % no_flight_time)


class TestDiveAir60m30min(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(60, 30 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1], [self.airdouble])

    def runTest(self):
        self.profile1.do_dive()
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         False,
                         'Wrong tank status : it should fail the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())


# ==================================================== 70m tests ==============
class TestDiveAir70m10min(TestDive):
    def setUp(self):
        TestDive.setUp(self)

    def runTest(self):
        try:
            diveseg1 = SegmentDive(70, 10 * 60, self.airdouble, 0)
            self.profile1 = Dive([diveseg1], [self.airdouble])
            self.profile1.do_dive()
        except UnauthorizedMod:
            pass
        else:
            self.fail("should raise UnauthorizedMod")


# ======================= Multilevel Dive =====================================
class TestDiveMultilevel(TestDive):
    def setUp(self):
        TestDive.setUp(self)
        diveseg1 = SegmentDive(40, 10 * 60, self.airdouble, 0)
        diveseg2 = SegmentDive(50, 12 * 60, self.airdouble, 0)
        diveseg3 = SegmentDive(30, 15 * 60, self.airdouble, 0)
        self.profile1 = Dive([diveseg1, diveseg2, diveseg3], [self.airdouble])
        self.profile1.do_dive()

    def test_rt(self):
        self.assertEqual(seconds_to_mmss(self.profile1.run_time),
                         "107:20",
                         "bad dive runtime ? (%s)" %
                         seconds_to_mmss(self.profile1.run_time))

    def test_otu(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.otu,
                               37.82532120330425,
                               7,
                               "bad dive OTU ? (%s)" %
                               self.profile1.model.ox_tox.otu)

    def test_cns(self):
        self.assertAlmostEqual(self.profile1.model.ox_tox.cns * 100,
                               14.831367723336383,
                               7,
                               "bad dive CNS ? (%s)" %
                               (self.profile1.model.ox_tox.cns * 100))

    def test_tank_cons(self):
        self.assertAlmostEqual(self.airdouble.used_gas,
                               4720.2200475,
                               7,
                               "bad used gas (%s)" % self.airdouble.used_gas)

    def test_tank_cons_rule(self):
        self.assertEqual(self.profile1.tanks[0].check_rule(),
                         True,
                         'Wrong tank status : it should pass the remaining '
                         'gas rule test (result:%s)' %
                         self.profile1.tanks[0].check_rule())

    def test_no_flight(self):
        no_flight_time = self.profile1.no_flight_time()
        self.assertEqual(no_flight_time,
                         5460,
                         "Bad no flight time: %s" % no_flight_time)


# =============================================================================
# ========================= M A I N ===========================================
# =============================================================================
def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('tests',
                        metavar='TestName',
                        type=str,
                        nargs='*',
                        help='name of the tests to run (separated by space)'
                        ' [optionnal]')
    args = parser.parse_args()
    if args.tests:
        suite = unittest.TestLoader().loadTestsFromNames(args.tests,
                                                         sys.modules[__name__])
    else:
        suite = unittest.findTestCases(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    main()
