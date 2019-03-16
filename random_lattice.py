import numpy as np
import matplotlib.pyplot as plt
from sympy.geometry.ellipse import Circle,Point
from sympy.geometry.exceptions import GeometryError
from itertools import combinations

def random_lattice_neighbors(N):
	''' Generate the neighbor dict for random lattice interactions constructed
		using the Voronoi/Delaunay prescription. This requires a lot of
		geometry and therefore is likely computationaly costly. 
		Parameters:
			N: The number of ising sites.
	'''
	x_coords = np.random.rand(N)
	y_coords = np.random.rand(N)
	neigh_dict = dict()
	# Initialize every dictionary entry to an empty set
	for n in range(N):
		neigh_dict[n] = set()
	# Iterate through every possible combination of three points to determine
	# if the circle they create contains no points.
	for comb in list(combinations(range(N),3)):
		# Extract points in circle
		x1,y1 = x_coords[comb[0]],y_coords[comb[0]]
		x2,y2 = x_coords[comb[1]],y_coords[comb[1]]
		x3,y3 = x_coords[comb[2]],y_coords[comb[2]]
		# Calculate the center and radius of the circle defined by the
		# three points.
		try:
			c = Circle(Point(x1, y1), Point(x2, y2), Point(x3, y3))
		except GeometryError:
			continue 
		c_x , c_y = c.center
		c_x = float(c_x)
		c_y = float(c_y)
		r = float(c.radius)
		# Run through all the points and see if any are within the circle
		pt_in_circ = False
		for n in range(N):
			x,y = x_coords[n],y_coords[n]
			if (c_x-x)**2 + (c_y-y)**2 < r**2-1e-8:
				pt_in_circ = True
				break
		if pt_in_circ == False:
			neigh_dict[comb[0]].update(set([comb[1],comb[2]]))
			neigh_dict[comb[1]].update(set([comb[0],comb[2]]))
			neigh_dict[comb[2]].update(set([comb[0],comb[1]]))

	return neigh_dict,x_coords,y_coords

def plot_random_lattice(neigh_dict,x_coords,y_coords,highlight=None):
	'''	Plots the random lattice created by random_lattice_neighbors.
		Paramteres:
			neigh_dict: A dictionary mapping spin to a set of its neighbors
			x_coords: The x coordinates of each ising spin
			y_coords: The y coordinates of each ising spin
			highlight: a list of lattice site to highlight in the plot
	'''
	N = len(neigh_dict)
	plt.figure(figsize=(6, 6))
	plt.axis('off')
	for n in range(N):
		for neigh in neigh_dict[n]:
			plt.plot([x_coords[n],x_coords[neigh]],
				[y_coords[n],y_coords[neigh]],'b')
	plt.plot(x_coords,y_coords,'.m')
	if highlight is not None:
		plt.plot(x_coords[highlight],y_coords[highlight],'ok')
	plt.show()	
	
