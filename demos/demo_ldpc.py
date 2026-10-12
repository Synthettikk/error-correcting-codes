import sys
sys.path.insert(0, '../')

from src.utils import linear_encode, transmit
from src.ldpc import ldpc_build_gen_matrix, bit_flip, measure_bit_flip_success, plot_sweep_results
import galois


GF2 = galois.GF(2)

def demo():
    """Pedagogical demo with prints."""
    
    # Setup
    n, k = 6, 3
    message = GF2([1, 0, 1])
    
    print("=" * 50)
    print("LDPC [6, 3] Demo")
    print("=" * 50)
    
    # Build matrices
    G = GF2(
    [[1, 0, 0, 1, 0, 1],
     [0, 1, 0, 1, 1, 1],
     [0, 0, 1, 1, 1, 0]])
    H = GF2(
    [[1, 1, 1, 1, 0, 0],
     [0, 1, 1, 0, 1, 0],
     [1, 1, 0, 0, 0, 1]])
    
    print(f"\nGenerator Matrix G:\n{G}")
    print(f"\nParity Matrix H:\n{H}")
    print(f"\nG @ H^T:\n{G @ H.T}")
    
    # Encode
    print(f"\n--- ENCODING ---")
    print(f"Message: {message}")
    codeword = linear_encode(message, G)
    print(f"Codeword: {codeword}")
    
    # Transmit with 1 error
    print(f"\n--- TRANSMISSION with 1 error ---")
    error_vector = GF2([0, 1, 0, 0, 0, 0])
    received = transmit(codeword, GF2, error_vector=error_vector)
    print(f"Error vector: {error_vector}")
    print(f"Received: {received}")
    
    # Decode
    print(f"\n--- DECODING ---")
    syndrome = H @ received.T
    print(f"Syndrome: {syndrome}")
    decoded = bit_flip(received, H)
    print(f"Decoded: {decoded}")
    print(f"Match original? {(decoded[:k] == message).all()}")

    # Transmit with 3 errors
    print(f"\n--- TRANSMISSION with 3 errors ---")
    error_vector = GF2([1, 1, 1, 0, 1, 0])
    received = transmit(codeword, GF2, error_vector=error_vector)
    print(f"Error vector: {error_vector}")
    print(f"Received: {received}")
    
    # Decode
    print(f"\n--- DECODING ---")
    syndrome = H @ received.T
    print(f"Syndrome: {syndrome}")
    decoded = bit_flip(received, H, 4)
    print(f"Decoded: {decoded}")
    print(f"Match original? {(decoded[:k] == message).all()}")




if __name__ == "__main__":
    demo()
    plot_sweep_results()

