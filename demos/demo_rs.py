import sys
sys.path.insert(0, '../')

from src.utils import linear_encode, transmit
from src.reed_solomon import rs_build_gen_matrix, rs_decode
import galois

GF = galois.GF(11)

def demo():
    """Pedagogical demo with prints."""
    
    # Setup
    n, k = 5, 3
    alphas = GF([0, 1, 2, 3, 4])
    message = GF([2, 3, 1])
    
    print("=" * 50)
    print("Reed-Solomon RS(5, 3) over GF(11) Demo")
    print("=" * 50)
    
    # Build matrices
    G, H = rs_build_gen_matrix(k, alphas, GF)
    print(f"\nGenerator Matrix G:\n{G}")
    print(f"\nParity Matrix H:\n{H}")
    print(f"\nG @ H^T:\n{G @ H.T}")
    
    # Encode
    print(f"\n--- ENCODING ---")
    print(f"Message: {message}")
    codeword = linear_encode(message, G)
    print(f"Codeword: {codeword}")
    
    # Transmit with 1 error
    print(f"\n--- TRANSMISSION ---")
    error_vector = GF([0, 0, 4, 0, 0])
    received = transmit(codeword, GF, error_vector=error_vector)
    print(f"Error vector: {error_vector}")
    print(f"Received: {received}")
    
    # Decode
    print(f"\n--- DECODING ---")
    syndrome = H @ received.T
    print(f"Syndrome: {syndrome}")
    decoded = rs_decode(H, received, alphas, GF)
    print(f"Decoded: {decoded}")
    print(f"Match original? {(decoded == message).all()}")

if __name__ == "__main__":
    demo()
