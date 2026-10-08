import pytest
from src.utils import linear_encode, transmit
from src.reed_solomon import rs_build_gen_matrix, rs_decode
import galois
import numpy as np

GF = galois.GF(11)

def test_gen_matrix_structure():
    """Verify G and H matrices have correct dimensions."""
    k, n = 3, 5
    alphas = GF([0, 1, 2, 3, 4])
    
    G, H = rs_build_gen_matrix(k, alphas, GF)
    
    assert G.shape == (k, n), f"G should be {k}x{n}"
    assert H.shape == (n - k, n), f"H should be {n-k}x{n}"

def test_null_space():
    """Verify G @ H^T = 0."""
    k, n = 3, 5
    alphas = GF([0, 1, 2, 3, 4])
    
    G, H = rs_build_gen_matrix(k, alphas, GF)
    product = G @ H.T
    
    assert (product == 0).all(), "G @ H^T should be zero matrix"

def test_single_error_correction():
    """Encode, introduce 1 error, decode and verify correction."""
    k, n = 3, 5 # t = n-k / 2 = 1 here
    alphas = GF([0, 1, 2, 3, 4])
    
    G, H = rs_build_gen_matrix(k, alphas, GF)
    message = GF([2, 3, 1])
    
    codeword = linear_encode(message, G)
    # Introduce error at position 2
    error_vector = GF([0, 0, 4, 0, 0])
    received = transmit(codeword, GF, error_vector=error_vector)
    
    decoded = rs_decode(H, received, alphas, GF)
    
    assert (decoded == message).all(), "Should correct to original message"

def test_no_error():
    """Encode, transmit without errors, decode."""
    k, n = 3, 5
    alphas = GF([0, 1, 2, 3, 4])
    
    G, H = rs_build_gen_matrix(k, alphas, GF)
    message = GF([2, 3, 1])
    
    codeword = linear_encode(message, G)
    received = transmit(codeword, GF, error_vector=GF([0, 0, 0, 0, 0]))
    
    decoded = rs_decode(H, received, alphas, GF)
    
    assert (decoded == message).all(), "Should match original message"
