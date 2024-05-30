# Python program to check whether it is possible
# to make a rectangle from 4 segments
N = 4


# Utility method to return square of distance
# between two points
def getDis(a, b):
	return (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])


# method returns true if line Segments make
# a rectangle
def isPossibleRectangle(segments):
	st = set()

	# putting all end points in a set to
	# count total unique points
	for i in range(N):
		st.add((segments[i][0], segments[i][1]))
		st.add((segments[i][2], segments[i][3]))

	# If total unique points are not 4, then
	# they can't make a rectangle
	if len(st) != 4:
		return False

	# dist will store unique 'square of distances'
	dist = set()

	# calculating distance between all pair of
	# end points of line segments
	for it1 in st:
		for it2 in st:
			if it1 != it2:
				dist.add(getDis(it1, it2))

	# if total unique distance are more than 3,
	# then line segment can't make a rectangle
	if len(dist) > 3:
		return False

	# copying distance into array. Note that set maintains
	# sorted order.
	distance = []
	for x in dist:
		distance.append(x)

	# Sort the distance list, as set in python, does not sort the elements by default.
	distance.sort()

	# If line seqments form a square
	if len(dist) == 2:
		return (2 * distance[0] == distance[1])

	# distance of sides should satisfy pythagorean
	# theorem
	return (distance[0] + distance[1] == distance[2])


# Driver code to test above methods
segments = [
	[4, 2, 7, 5],
	[2, 4, 4, 2],
	[2, 4, 5, 7],
	[5, 7, 7, 5]
]

if (isPossibleRectangle(segments) == True):
	print("Yes")
else:
	print("No")
