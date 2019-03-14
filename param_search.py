import sys, pickle
import numpy as np
from ising_model import *
# A script to search over the parameters K and L and record the magnetization
# to calculate the critical exponenets.

L = int(sys.argv[1])
K = float(sys.argv[2])
lattice = sys.argv[3]
nnn = bool(sys.argv[4])

N_lattices = 5
n_eq = 1000
n_samps = 2000
samp_rate = 10

m_full = np.zeros((N_lattices,n_samps//samp_rate))
e_full = np.zeros((N_lattices,n_samps//samp_rate))

prefix = '/home/users/swagnerc/phys_212/ising_model/'

if lattice == 'random':
	rand_lattice_path = prefix + 'rand_lat/lattice_L_%d.pkl'%(L)
	with open(rand_lattice_path,'rb') as pk_file:
		neigh_dict,_,_ = pickle.load(pk_file)
else:
	neigh_dict = None

for n in range(N_lattices):
	ising = Model(lattice,L,K,next_nearest=nnn,rand_neigh=neigh_dict)
	m_full[n],e_full[n] = ising.wolff_algorithm(n_eq,n_samps,samp_rate)

prefix = prefix + 'me_data/'
np.savetxt(prefix+'m_full_%d_%f_%s_%r'%(L,K,lattice,nnn),m_full)
np.savetxt(prefix+'e_full_%d_%f_%s_%r'%(L,K,lattice,nnn),e_full)
