import sys
sys.path.insert(0, '../')

from src.utils import linear_encode, transmit
from src.hamming import hamming_build_gen_matrix, hamming_decode
import galois

GF2 = galois.GF(2)

def demo(m = 3):
    """Pedagogical demo with prints."""
    message = GF2([1, 0, 1, 1])
    
    print("=" * 50)
    print("HAMMING [8,4,4] SECDED Code Demo")
    print("=" * 50)
    
    # Build matrices
    G, H = hamming_build_gen_matrix(m)
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
    received= transmit(codeword, GF2, 1)
    print(f"Received: {received}")
    
    # Decode
    print(f"\n--- DECODING ---")
    decoded, error_type = hamming_decode(received, H)
    print(f"Error type: {error_type} (1=corrected, 0=no error, 2=two errors, -1=uncorrectable)")
    print(f"Decoded: {decoded}")
    print(f"Match original? {(decoded == message).all()}")

if __name__ == "__main__":
    demo()
