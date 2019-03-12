import numpy as np
from random import uniform
from random_lattice import *
import copy

class Model():
	# The abstract class for the ising model. It takes care of initializing the
	# model, return neighbor indices, calculating magnetization, and running
	# a single step of the Wolff clustering algorithm. 
	def __init__(self,lattice,L,K,next_nearest=False, rand_neigh=None):
		''' Initialize the model with the specified lattice structure and size.
			Parameters:
				lattice: a string describing the type of lattice to initalize (
					square, triangular, hexagonal, random).
				L: The side length of the lattice (the lattice will have L^2 points
					in total).
				next_nearest: whether or not to use next-nearest interactions.
				rand_neigh: A pre-initialized dictionary of neighbors to be used
					for the random lattice (this allows the same lattice to be
					used multiple times).
		'''
		self.next_nearest = next_nearest
		if lattice == 'hexagonal':
			self.N = 2*(L**2)
		else:
			self.N = L**2
		self.spins = np.random.randint(2, size=self.N)
		self.spins[self.spins==0] = -1
		self.lattice = lattice
		self.L = L
		self.K = K
		self.p = 1-np.exp(-2*K)
		if self.lattice == 'random':
			if rand_neigh is None:
				self.neighbors,_,_ = random_lattice_neighbors(self.N)
			else:
				self.neighbors = rand_neigh
		else:
			self.neighbors = None
		# Build interaction matrix using the neighbors
		self.int_mat = np.zeros((self.N,self.N))
		for n in range(self.N):
			if self.next_nearest:
				interactions = self.get_next_nearest(n)
			else:
				interactions = self.get_neighbors(n)
			for inter in interactions:
				self.int_mat[n,inter] = self.K

	def get_magnetization(self):
		# Return the mean magnetization of the sample
		return np.mean(self.spins)

	def get_energy(self):
		# Return the energy of the system
		energy = np.dot(self.spins,np.dot(self.int_mat,self.spins))
		# Get rid of double counting
		return energy/2


	def get_neighbors(self,i):
		''' Returns the indices of the neighbors of lattice site i.
			Parameters:
				i: the index of the lattice point
		'''
		if self.lattice == 'square':
			L2 = self.N
			return [(i+1)%L2,(i-1)%L2,(i+self.L)%L2,
				(i-self.L)%L2]
		if self.lattice == 'triangular':
			L2 = self.N
			return [(i+1)%L2,(i-1)%L2,(i+self.L)%L2,
				(i-self.L)%L2,(i+self.L-1)%L2,(i-self.L+1)%L2]
		if self.lattice == 'hexagonal':
			L2 = self.N
			if i % 2 == 0:
				return [(i+1)%L2,(i-1)%L2,(i-2*self.L+1)%L2]
			else:
				return [(i+1)%L2,(i-1)%L2,(i+2*self.L-1)%L2]
		if self.lattice == 'random':
			return list(self.neighbors[i])

	def get_next_nearest(self,i):
		''' Returns the indices of the neighbors of lattice site i.
			Parameters:
				i: the index of the lattice point
		'''
		neighs = self.get_neighbors(i)
		next_nearest = set()
		for n in neighs:
			next_nearest.update(self.get_neighbors(n))
		next_nearest.update(neighs)
		return next_nearest

	def wolff_step(self,i):
		''' Starting the cluster at node i, run a single step of the 
			Wolff algorithm.
			Paramters:
				i: the node that will seed the cluster.
		'''
		spin = self.spins[i]
		self.spins[i] = - spin
		# Use a set object to avoid adding neighbors that are already in
		# the set.
		if self.next_nearest:
			neighbors = copy.deepcopy(self.get_next_nearest(i))
		else:
			neighbors = copy.deepcopy(self.get_neighbors(i))
		# Continue until there are no more neighbors left.
		while neighbors:
			n_i = neighbors.pop()
			if self.spins[n_i] == spin and np.random.random(1) < self.p:
				self.spins[n_i] = -spin
				if self.next_nearest:
					neighbors.extend(self.get_next_nearest(n_i))
				else:
					neighbors.extend(self.get_neighbors(n_i))

	def wolff_algorithm(self,n_eq,n_samps,samp_rate=10):
		''' Run the full Wolff cluster update algorithm on the given model.
			Parameters:
				n_eq: the number of steps to take before considering the
					model in equilibrium
				n_samps: the number of sampling steps to take
				samp_rate: the rate at which to probe the magnetization
		'''
		m = []
		e = []
		for step in range(n_samps+n_eq):
			i = np.random.randint(0,self.N)
			self.wolff_step(i)
			if step >= n_eq and step%samp_rate == 0:
				m.append(np.abs(self.get_magnetization()))
				e.append(self.get_energy())
		
		return np.array(m),np.array(e)









