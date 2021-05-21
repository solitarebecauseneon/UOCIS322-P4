"""
Nose tests for acp_times.py, which calculates for flask_brevets.py

Uses fringe cases for ACP brevet times and cases
"""

from acp_times import open_time, close_time

import nose  # Testing framework
import arrow

d_arrow = arrow.get('2000-01-01 00:00:00', 'YYYY-MM-DD HH:mm:ss')


def a_same(s, t):
    """
    Asserts two arrows are the same
    """
    return s.format('YYYY-MM-DD HH:mm:ss') == t.format('YYYY-MM-DD HH:mm:ss')


def test_low_1():
    """
    Tests 0km control distances
    """
    assert a_same(open_time(0, 200, d_arrow), d_arrow)
    assert a_same(close_time(0, 200, d_arrow), arrow.get('2000-01-01 01:00:00', 'YYYY-MM-DD HH:mm:ss'))


def test_low_2():
    """
    Tests <= 60km values (special cases) for
    control distances in both. Should create
    special exceptions for close_time and
    not do so for open_time
    """
    # open_time should calculate as normal
    assert a_same(open_time(50, 400, d_arrow), arrow.get('2000-01-01 01:28:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(close_time(20, 300, d_arrow), arrow.get('2000-01-01 02:00:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(close_time(40, 400, d_arrow), arrow.get('2000-01-01 03:00:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(close_time(60, 600, d_arrow), arrow.get('2000-01-01 04:00:00', 'YYYY-MM-DD HH:mm:ss'))
    # Should use updated formula past 61
    assert a_same(close_time(61, 1000, d_arrow), arrow.get('2000-01-01 04:04:00', 'YYYY-MM-DD HH:mm:ss'))


def test_high_1():
    """
    Tests non-overkill values (where control distance = brevet distance)
    """
    # Should have no effect on either set
    assert a_same(open_time(200, 200, d_arrow), arrow.get('2000-01-01 05:53:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(open_time(400, 400, d_arrow), arrow.get('2000-01-01 12:08:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(close_time(1000, 1000, d_arrow), arrow.get('2000-01-04 03:00:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(close_time(600, 600, d_arrow), arrow.get('2000-01-02 16:00:00', 'YYYY-MM-DD HH:mm:ss'))


def test_high_2():
    """
    Tests overkill values (control values that exceed
    the brevet distance by 20% or less)
    """
    # Both should be identical to high_1 results
    assert a_same(open_time(240, 200, d_arrow), arrow.get('2000-01-01 05:53:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(open_time(480, 400, d_arrow), arrow.get('2000-01-01 12:08:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(close_time(1200, 1000, d_arrow), arrow.get('2000-01-04 03:00:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(close_time(720, 600, d_arrow), arrow.get('2000-01-02 16:00:00', 'YYYY-MM-DD HH:mm:ss'))


def test_high_3():
    """
    Tests overkill values that exceed brevet distance by only one
    """
    # Both should be identical to high_1 results
    assert a_same(open_time(201, 200, d_arrow), arrow.get('2000-01-01 05:53:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(open_time(401, 400, d_arrow), arrow.get('2000-01-01 12:08:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(close_time(1001, 1000, d_arrow), arrow.get('2000-01-04 03:00:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(close_time(601, 600, d_arrow), arrow.get('2000-01-02 16:00:00', 'YYYY-MM-DD HH:mm:ss'))


def test_random():
    """
    Tests a small variety of non-special values
    """
    # open_time
    assert a_same(open_time(144, 200, d_arrow), arrow.get('2000-01-01 04:14:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(open_time(453, 600, d_arrow), arrow.get('2000-01-01 13:54:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(open_time(200, 400, d_arrow), arrow.get('2000-01-01 05:53:00', 'YYYY-MM-DD HH:mm:ss'))
    # close_time
    assert a_same(close_time(888, 1000, d_arrow), arrow.get('2000-01-03 17:12:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(close_time(81, 300, d_arrow), arrow.get('2000-01-01 05:24:00', 'YYYY-MM-DD HH:mm:ss'))
    assert a_same(close_time(347, 600, d_arrow), arrow.get('2000-01-01 23:08:00', 'YYYY-MM-DD HH:mm:ss'))
