import time
import os
import numpy as np

lattices = ['square','triangular','hexagonal','random']
N_k = 30

for lattice in lattices:
	if lattice == 'square':
		Ks = np.linspace(0.3,0.5,N_k)
	if lattice == 'triangular':
		Ks = np.linspace(0.2,0.4,N_k)
	if lattice == 'hexagonal':
		Ks = np.linspace(0.5,0.8,N_k)
	if lattice == 'random':
		Ks = np.linspace(0.2,0.5,N_k)
		Ls = [2,3,5,6,7,10,20]
	else:
		Ls = [5,10,20,50,100]
	for K in Ks:
		for L in Ls:
			os.system('sbatch param_search.sh %d %f %s'%(L,K,lattice))
			time.sleep(1)

