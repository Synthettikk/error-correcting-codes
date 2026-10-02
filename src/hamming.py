import galois #for GF2 arithmetics
import random # for errors
import numpy as np

GF2 = galois.GF(2)

def hamming_build_gen_matrix(m):
    """Build SECDED Hamming [2^m, 2^m - m - 1, 4] generator and parity matrices."""
    n = 2**m
    k = n - (m + 1)
    H = []
    
    H.append([1] * n)
    H += [((np.arange(n) >> bit_pos) & 1).tolist() for bit_pos in range(m)]
    H = GF2(H)
    
    parity_cols = [0] + [2**bit for bit in range(m)]
    info_cols = [i for i in range(n) if i not in parity_cols]
    
    permutation = info_cols + parity_cols
    H = H[:, permutation]
    H = H.row_reduce(eye='right')
    G = H.null_space()
    
    return G, H

def hamming_encode(message, G):
    """Encode message using generator matrix G."""
    codeword = message @ G
    return codeword

def transmit(codeword, num_errors=None):
    """Add random errors to codeword (0, 1, or 2)."""
    if num_errors is None:
        num_errors = random.randint(0, 2)
    
    n = len(codeword)
    error_positions = random.sample(range(n), min(num_errors, n))
    error = GF2([1 if i in error_positions else 0 for i in range(n)])
    
    received = codeword + error
    return received, error_positions

def hamming_decode(received, H):
    """Decode received word using parity matrix H (SECDED logic)."""
    n = H.shape[1]
    k = n - H.shape[0]
    
    syndrome = H @ received.T
    syndrome_is_zero = np.all(syndrome == 0)
    overall_parity = received.sum()
    
    if syndrome_is_zero and overall_parity == 0:
        return received[:k], 0  # No error
    
    if syndrome_is_zero and overall_parity == 1:
        return received[:k], -1  # Uncorrectable (global parity error)
    
    if overall_parity == 0:
        return received[:k], 2  # Two errors detected (uncorrectable)
    
    # One error: find position
    error_positions = [
        pos for pos in range(n)
        if np.array_equal(H[:, pos], syndrome)
    ]
    
    if len(error_positions) != 1:
        return received[:k], -1  # Unable to locate
    
    error_pos = error_positions[0]
    corrected_word = received.copy()
    corrected_word[error_pos] ^= GF2(1)
    
    return corrected_word[:k], 1  # One error corrected

