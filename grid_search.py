import time
import os
import numpy as np

lattices = ['square','triangular','hexagonal','random']
next_nearest = [True,False]
N_k = 30

for lattice in lattices:
	for nn in next_nearest:
		if lattice == 'square':
			if nn == False:
				Ks = np.concatenate((np.linspace(0.3,0.5,N_k),
					np.linspace(0.4,0.45,N_k)))
			else:
				Ks = np.concatenate((np.linspace(0.02,0.2,N_k),
					np.linspace(0.08,0.15,N_k)))
		if lattice == 'triangular':
			if nn == False:
				Ks = np.concatenate((np.linspace(0.2,0.4,N_k),
					np.linspace(0.24,0.28,N_k)))
			else:
				s = np.concatenate((np.linspace(0.01,0.1,N_k),
					np.linspace(0.06,0.08,N_k)))
		if lattice == 'hexagonal':
			if nn == False:
				Ks = np.concatenate((np.linspace(0.5,0.8,N_k),
					np.linspace(0.65,0.67,N_k)))
			else:
				Ks = np.concatenate((np.linspace(0.05,0.3,N_k),
					np.linspace(0.125,0.175,N_k)))
		if lattice == 'random':
			if nn == False:
				Ks = np.concatenate((np.linspace(0.2,0.5,N_k),
					np.linspace(0.28,0.4,N_k)))
			else:
				Ks = np.concatenate((np.linspace(0.02,0.12,N_k),
					np.linspace(0.06,0.09,N_k)))
			Ls = [2,3,5,6,7,10,20]
		else:
			Ls = [5,10,20,50,100]
		for K in Ks:
			for L in Ls:
				os.system('sbatch param_search.sh %d %f %s %r'%(L,K,lattice,nn))
				time.sleep(1)

