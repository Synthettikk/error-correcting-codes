import pytest
from src import hamming_build_gen_matrix, hamming_encode, transmit, hamming_decode
import galois

GF2 = galois.GF(2)

def test_gen_matrix_structure(m = 3):
    """Verify G and H matrices have correct dimensions."""
    G, H = hamming_build_gen_matrix(m)
    n, k = 2**m, 2**m - (m + 1)
    
    assert G.shape == (k, n), f"G should be {k}x{n}"
    assert H.shape == (m + 1, n), f"H should be {m+1}x{n}"

def test_null_space(m = 3):
    """Verify G @ H^T = 0."""
    G, H = hamming_build_gen_matrix(m)
    product = G @ H.T
    
    assert (product == 0).all(), "G @ H^T should be zero matrix"

def test_single_error_correction(m = 3):
    """Encode, introduce 1 error, decode and verify correction."""
    
    G, H = hamming_build_gen_matrix(m)
    message = GF2([1, 0, 1, 1])
    
    codeword = hamming_encode(message, G)
    received, _ = transmit(codeword, num_errors=1)
    decoded, error_type = hamming_decode(received, H)
    
    assert error_type == 1, "Should detect 1 error"
    assert (decoded == message).all(), "Should correct to original message"

def test_no_error(m = 3):
    """Encode, transmit without errors, decode."""
    G, H = hamming_build_gen_matrix(m)
    message = GF2([1, 0, 1, 1])
    
    codeword = hamming_encode(message, G)
    received, _ = transmit(codeword, num_errors=0)
    decoded, error_type = hamming_decode(received, H)
    
    assert error_type == 0, "Should detect no error"
    assert (decoded == message).all(), "Should match original message"

def test_two_error_detection(m = 3):
    """Encode, introduce 2 errors, decode and verify detection."""
    G, H = hamming_build_gen_matrix(m)
    message = GF2([1, 0, 1, 1])
    
    codeword = hamming_encode(message, G)
    received, _ = transmit(codeword, num_errors=2)
    decoded, error_type = hamming_decode(received, H)
    
    assert error_type == 2, "Should detect 2 errors (uncorrectable)"
