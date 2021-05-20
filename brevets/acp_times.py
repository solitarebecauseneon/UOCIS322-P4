"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
from math import floor
import arrow

#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#
VALID_BREVET = [200, 300, 400, 600, 1000]
MAX_SPEEDS = [34, 32, 30, 28]
MIN_SPEEDS = [15, 15, 15, 11.428]


def _brevet_check(brevet_distance):
    """
    Args:
        brevet_distance: if brevet_distance is not
        contained in VALID_BREVET, error in value passed
        elsewhere in the application. Indicates that code
        should be killed and return error
    Returns:
        True if brevet_distance is valid; false otherwise
    """
    if brevet_distance in VALID_BREVET:
        return True
    return False


def _minute_calc(dist, speed):
    """
    Args:
        dist: positive integer, distance being calculating in kilometers
        speed: current speed (taken from either MIN_SPEEDS or MAX_SPEEDS)
            open_time and close_time are responsible for passing it. Speed
            represents kilometers/hour.
    Returns:
        A positive integer representing the time, in minutes, that the
        distance will be traveled in at the given speed, calculated
        according to official ACP brevet calculation methods
    """
    hr = floor((dist / speed))
    mns = floor(((dist / speed) - hr) * 60)
    return (hr * 60) + mns


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    # use a.shift() to change times and hours.
    if not(_brevet_check(brevet_dist_km)):
        return 1
    cd = control_dist_km
    m_shift = 0  # The shift of time in minutes
    count = 0  # Count number of iterations
    while cd >= 200 and count < 3:  # counts number of times 200 occurs, up to 3 times (200, 400, 600, or 1000)
        cd -= 200
        count += 1
    if control_dist_km > brevet_dist_km:  # If this is not true, that means arg1 > arg2, so remainder is not used
        cd = 0;
    m_shift += _minute_calc(cd, MAX_SPEEDS[count]) # Will be 0 if cd does not matter, < 200 otherwise
    for i in range(count):  # Calculates 'maxed' control distances
        m_shift += _minute_calc(200, MAX_SPEEDS[count])
    hr = m_shift % 60
    mns = m_shift - hr
    # arrow object shifted by hr, mns
    opentime = brevet_start_time.shift(hour=+hr, minute=+mns)

    return opentime


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    if not(_brevet_check(brevet_dist_km)):
        return 1
    cd = control_dist_km
    m_shift = 0  # The shift of time in minutes
    count = 0  # Count number of iterations
    while cd >= 200 and count < 3:  # counts number of times 200 occurs, up to 3 times (200, 400, 600, or 1000)
        cd -= 200
        count += 1
    if control_dist_km <= 60:  # divide by 20, add one hour; count should be 0
        m_shift += 60
        m_shift += cd / 20
    if control_dist_km > brevet_dist_km:  # If this is not true, that means arg1 > arg2, so remainder is not used
        cd = 0;
    m_shift += _minute_calc(cd, MIN_SPEEDS[count])  # Will be 0 if cd does not matter, < 200 otherwise
    for i in range(count):  # Calculates all distance in a given range of speed
        m_shift += _minute_calc(200, MIN_SPEEDS[i])
    # arrow object shifted by hr, mns
    hr = m_shift % 60
    mns = m_shift - hr
    closetime = brevet_start_time.shift(hour=+hr, minute=+mns)

    return closetime
