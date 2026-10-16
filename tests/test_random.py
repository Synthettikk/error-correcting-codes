import pytest
import galois #for GF2 arithmetics
import numpy as np
from src.utils import transmit, linear_encode, min_distance_bruteforce
from src.random_code import random_gen_matrix, Prange

GF2 = galois.GF(2)

def test_gen_matrix_structure():
    n, k = 100, 50

    G, H = random_gen_matrix(n, k)

    # Dimensions
    assert G.shape == (k, n), f"G should be {k}x{n}, got {G.shape}"
    assert H.shape == (n - k, n), f"H should be {n-k}x{n}, got {H.shape}"

    # Ranks
    rank_G = np.linalg.matrix_rank(G)
    assert rank_G == k, f"G should be rank {k}, got {rank_G}"
    rank_H = np.linalg.matrix_rank(G)
    assert rank_H == n-k, f"H should be rank {n-k}, got {rank_H}"

def test_min_dist():
    G = GF2([[1, 1, 1]])
    H = GF2([[1, 1, 0],
             [0, 1, 1]])

    d = min_distance_bruteforce(G, GF2)
    assert d == 3, f"d should be {3}, got {d}"

def test_prange_decodes_one_error(monkeypatch):
    G = GF2([[1, 1, 1]])
    H = GF2([[1, 1, 0],
             [0, 1, 1]])

    c = GF2([1, 1, 1])
    e = GF2([1, 0, 0])
    r = c + e

    # Forces the selection of positions [0, 1] in Prange, which contains the error.
    monkeypatch.setattr(
        np.random,
        "choice",
        lambda n, size, replace=False: np.array([0, 1])
    )

    c_hat, iterations = Prange(r, H, t=1, max_iter=1)

    assert iterations == 1
    assert np.all(c_hat == c)
    assert np.all(H @ c_hat == 0)
    assert np.count_nonzero(r + c_hat) <= 1

def test_prange_decodes_fail(monkeypatch):
    G = GF2([[1, 1, 1]])
    H = GF2([[1, 1, 0],
             [0, 1, 1]])

    c = GF2([1, 1, 1])
    e = GF2([1, 0, 0])
    r = c + e

    # Forces the selection of positions [1, 2] in Prange, which does not contain the error.
    monkeypatch.setattr(
        np.random,
        "choice",
        lambda n, size, replace=False: np.array([1, 2])
    )

    c_hat, iterations = Prange(r, H, t=1, max_iter=1)

    assert iterations == 1
    assert c_hat is None
