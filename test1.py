### First attempt at calculating position of sun 
## Daniel Ryaboshapka

from math import cos, sin, atan2, asin, atan, radians
import numpy as np
import datetime
from jdcal import gcal2jd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# # Definitions from [wikipedia](https://en.wikipedia.org/wiki/Position_of_the_Sun#:~:text=The%20position%20of%20the%20Sun,circular%20path%20called%20the%20ecliptic.)

# Ecliptic Coordinates

# n = JD - 2451545.0 

# where 
# 	`n` = the number of days since Greenwich noon, Terrestrial Time, 1 Jan 2000
#   `JD` = Julian Date

# L = 280.460 degrees + 0.9856474 * n degrees

# where `L` = mean longitude of the Sun, corrected for aberration of light

# g = 357.528 deg + .9856003 * n deg

# where `g` is the mean anomaly of the Sun (of the Earth in its orbit around the Sun)
# pretend Sun is orbiting earth

# _lambda = L + 1.915sing + .02 sin2g

# where `_lambda` is the ecliptic longitude of the Sun

# the ecliptic latitude of the Sun is nearly _beta = 0deg

# R = 1.00014 - .01671 * cosg - .00014cos2g

# where R is distance of the Sun from the Earth in *astronomical units*

# Equatorial coordinates

# (_lambda, beta, R) form a complete position of the Sun in ecliptic coord system

# can be converted to equatorial coord system using _epsilon, or the 
# obliquity of the ecliptic, also known as *axial tilt*

# _alpha = arctan(cos(_epsilon)tan())


# Get L and g within a range of 0 - 360 degrees by adding 
# or subtracting multiples of 360 degrees
# def within360(n): 
# 	if n > 360: 
# 		return within360(n - 360)
# 	elif n < 0: 
# 		return within360(n + 356)
# 	else: 
# 		return n


def position_of_sun(JD, method="ecliptic"):
	n        = JD - 2451545
	L        = radians(((JD - 2451545) * .985647)  + 280.460)
	g        = radians(((JD - 2451545) * .9856003) + 357.528)
	_lambda  = radians((1.915 * sin(g)) + (.02 * (sin(2 * g))) + L)
	_beta    = 0
	R        = 1.00014 - (.01671 * cos(g)) - (.00014 * cos(2 * g))
	_epsilon = radians(23.439 - .0000004 * n)

	if method == "equatorial":
		# _alpha = (ATAN2(y,x))
		_alpha = atan2((cos(_epsilon) * sin(_lambda)), cos(_lambda))
		_delta = asin(sin(_epsilon) * sin(_lambda))
		return _alpha, _delta

	elif method == "rectangular_equatorial": 
		X = R * cos(_lambda)
		Y = R * cos(_epsilon) * sin(_lambda)
		Z = R * sin(_epsilon) * sin(_lambda)
		return X, Y, Z

# https://stackoverflow.com/questions/13943062/extract-day-of-year-and-
#julian-day-from-a-string-date#:~:text=To%20get%20the%20Julian%20day,
#in%20the%20proleptic%20Gregorian%20calendar.
def Julian_Date(s):
	fmt = '%Y.%m.%d'
	dt  = datetime.datetime.strptime(s, fmt)
	return sum(gcal2jd(dt.year, dt.month, dt.day))

today    = datetime.date.today().strftime('%Y.%m.%d')
jd_today = Julian_Date(today)
print("Today's Julian Date is %s" % (jd_today))

time    = np.linspace(0, 2459110, 1000)
X, Y, Z = list(zip(*[position_of_sun(x, method='rectangular_equatorial') for x in time]))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# X, Y, Z = position_of_sun(jd_today, method='rectangular_equatorial')

# In right-handed rectangular equatorial coordinates
# (where the X axis is in the direction of the vernal 
# point, and the Y axis is 90° to the east, in the plane
# of the celestial equator, and the Z axis is directed 
# toward the north celestial pole[6] ), in astronomical units:

# print(X, Y, Z)
ax.plot(X, Y, Z)

plt.show()
	

