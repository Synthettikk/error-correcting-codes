import galois #for GF2 arithmetics
import numpy as np
#import matplotlib.pyplot as plt
from src.utils import transmit, linear_encode

GF2 = galois.GF(2)

def random_gen_matrix(n, k):
    """Build randoms generator and parity matrices over GF(2)"""

    success = False
    while not success:
        H = GF2.Random((n-k, n))
        rank_H = np.linalg.matrix_rank(H)
        if rank_H == n-k: 
            success = True

    G = H.null_space()

    return G, H

def Prange(r, H, t, max_iter = 100000):
    """Decodes a received word r from a random code [n, k]
    Returns the codeword c and the number of iterations"""
    n = H.shape[1]
    k = n - H.shape[0]
    iter = 0

    # compute the syndrom 
    s = H @ r # = H @ e.T  (n x k)

    # ISD
    while(iter < max_iter):
        positions = np.random.choice(n, n-k, replace=False)
        H_pos = H[:, positions]
        iter += 1
        try:
            e_pos = np.linalg.solve(H_pos, s)
        except np.linalg.LinAlgError: # if H_pos not inv
            continue

        # if solve succeeds, reconstructs the full e, and c
        e = GF2.Zeros(n)
        e[positions] = e_pos
        if np.count_nonzero(e) > t: # looking for <= t errors
            continue
        c = r + e
        return c, iter
    
    # if fail
    return None, iter
