import pytest
from src.utils import linear_encode, transmit
from src.ldpc import ldpc_build_gen_matrix, bit_flip, measure_bit_flip_success, sweep_bit_flip
import galois
import numpy as np

GF2 = galois.GF(2)

def test_gen_matrix_structure():
    """Verify G and H matrices have correct dimensions, weight distribution, and systematic form."""
    n, k = 10, 4
    dc = 4
    
    G, H = ldpc_build_gen_matrix(n, k, dc=dc)
    
    # Dimensions
    assert G.shape == (k, n), f"G should be {k}x{n}, got {G.shape}"
    assert H.shape == (n - k, n), f"H should be {n-k}x{n}, got {H.shape}"
    
    # Row weights (on H)
    H_np = np.array(H, dtype=int)
    row_weights = H_np.sum(axis=1)
    assert (row_weights == dc).all(), f"Each row of H should have exactly {dc} ones"
    
    # Column weights (on H) — stats only
    col_weights = H_np.sum(axis=0)
    print(f"\n  H col weights — mean: {col_weights.mean():.2f}, std: {col_weights.std():.2f}, range: [{col_weights.min()}, {col_weights.max()}]")
    
    # Row weights (on G) — stats only
    G_np = np.array(G, dtype=int)
    G_row_weights = G_np.sum(axis=1)
    print(f"  G row weights — mean: {G_row_weights.mean():.2f}, std: {G_row_weights.std():.2f}, range: [{G_row_weights.min()}, {G_row_weights.max()}]")
    
    # Systematic form: H = [A | I_{n-k}]
    H_identity_part = H_np[:, -(n - k):]
    expected_identity = np.eye(n - k, dtype=int)
    assert (H_identity_part == expected_identity).all(), \
        f"Last {n-k} columns of H should form identity matrix"


def test_null_space():
    """Verify G @ H^T = 0."""
    n, k = 100, 60
    dc = 4
    
    G, H = ldpc_build_gen_matrix(n, k, dc)
    product = G @ H.T
    
    assert (product == 0).all(), "G @ H^T should be zero matrix"



def test_generator_matrix_is_valid():
    n, k, dc = 12, 6, 3
    G, H = ldpc_build_gen_matrix(n, k, dc=dc)

    assert G.shape == (k, n)
    assert H.shape == (n - k, n)
    assert (H @ G.T == 0).all()


def test_noiseless_transmission_is_decoded():
    n, k, dc = 12, 6, 3
    G, H = ldpc_build_gen_matrix(n, k, dc=dc)

    success_rate = measure_bit_flip_success(
        G, H, n, k,
        t=0,
        trials=10,
        I_max=1,
    )

    # With no errors, should not change codeword
    assert success_rate == 1.0


def test_sweep_returns_valid_results():
    ns, ps, ks, scores = sweep_bit_flip(
        n_values=[10, 12],
        code_rate=0.5,
        error_rates=[0, 0.1],
        matrices_per_point=1,
        trials=3,
        dc=3,
        I_max=2,
    )

    assert scores.shape == (len(ns), len(ps))
    assert len(ks) == len(ns)
    assert np.isfinite(scores).all()
    assert ((scores >= 0) & (scores <= 1)).all()


