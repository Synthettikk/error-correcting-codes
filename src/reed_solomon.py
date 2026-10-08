import galois
import numpy as np
from src.utils import make_poly

def rs_build_gen_matrix(k, alphas, GF):
    """Build the Vandermonde matrix G associated to alpha_0,..., alpha_{n-1}, return G and H."""
    Vander = GF([[alpha**j for j in range(k)] for alpha in alphas])
    return Vander.T, (Vander.T).null_space()

def rs_decode(H, received, alphas, GF):
    """Decode the received message encoded with RS using Welch-Berlekamp method."""
    
    n = H.shape[1]
    k = n - H.shape[0]
    t = int((n - k) / 2)

    # Check if syndrome is zero, no error
    if (H @ received.T == 0).all():
        P = galois.lagrange_poly(alphas, received)
        return P.coeffs[::-1]

    # Build matrix A
    # Variables: [q_0, q_1, ..., q_{k+t-1}, e_0, e_1, ..., e_{t-1}]
    # Equations: Q(α_i) - r_i * E(α_i) = 0 for i = 0..n-1
    A = []
    for i in range(n):
        row = []
        # E's part
        for j in range(t):
            row.append(-received[i] * alphas[i] ** (j + 1))
        # Q's part
        for j in range(k + t):
            row.append(alphas[i] ** j)
        A.append(row)

    A = GF(A)
    x = np.linalg.solve(A, received)  # Solve Ax = received

    # Extract Q and E
    E_coeffs = np.concatenate([[GF(1)], x[:t]])  # Don't forget E_0 = 1
    Q_coeffs = x[t:]
    E = make_poly(E_coeffs, GF)
    Q = make_poly(Q_coeffs, GF)
    P, _ = divmod(Q, E)

    return P.coeffs[::-1]
