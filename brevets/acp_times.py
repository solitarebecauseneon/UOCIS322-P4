"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#
MAX_SPEEDS = [34, 32, 30, 28]
MIN_SPEEDS = [15, 15, 15, 11.428]

final_close = {200: 13.5, 300: 20, 400: 27, 600: 40, 1000: 75}


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
    hr = round((dist / speed))
    mns = round(((dist / speed) - hr) * 60)
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
    cd = control_dist_km
    m_shift = 0  # The shift of time in minutes
    count = 0  # Count number of iterations
    if control_dist_km > brevet_dist_km:  # cuts off any overflow value
        cd -= control_dist_km - brevet_dist_km
    while cd >= 200 and count < 3:  # counts number of times 200 occurs, up to 3 times (200, 400, 600, or 1000)
        cd -= 200
        count += 1
    m_shift += _minute_calc(cd, MAX_SPEEDS[count])  # Will be 0 if cd does not matter, < 200 otherwise
    for i in range(count):  # Calculates 'maxed' control distances
        m_shift += _minute_calc(200, MAX_SPEEDS[i])
    hr = m_shift // 60
    mns = m_shift - (hr * 60)
    # arrow object shifted by hr, mns
    opentime = brevet_start_time.shift(hours=+hr, minutes=+mns)

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
    if control_dist_km > brevet_dist_km:  # cuts off any overflow value
        duration = final_close[brevet_dist_km]
        closetime = brevet_start_time.shift(hours=duration)
        return closetime
    cd = control_dist_km
    m_shift = 0  # The shift of time in minutes
    count = 0  # Count number of iterations
    while cd >= 200 and count < 3:  # counts number of times 200 occurs, up to 3 times (200, 400, 600, or 1000)
        cd -= 200
        count += 1
    if control_dist_km <= 60:  # divide by 20, add one hour; count should be 0
        m_shift += 60
        m_shift += (cd / 20) * 60
        cd = 0
    m_shift += _minute_calc(cd, MIN_SPEEDS[count])  # Will be 0 if cd does not matter, < 200 otherwise
    for i in range(count):  # Calculates all distance in a given range of speed
        m_shift += _minute_calc(200, MIN_SPEEDS[i])
    # arrow object shifted by hr, mns
    hr = m_shift // 60
    mns = m_shift - (hr * 60)
    closetime = brevet_start_time.shift(hours=+hr, minutes=+mns)

    return closetime
