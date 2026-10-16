import sys
sys.path.insert(0, '../')

from src.utils import linear_encode, transmit
from src.random_code import random_gen_matrix, Prange
import numpy as np
import galois
import matplotlib.pyplot as plt

GF2 = galois.GF(2)


def demo():
    """Pedagogical demo with prints."""
    
    # Setup
    n, k, t = 30, 15, 1
    
    print("=" * 50)
    print("Random Code with Prange Decoding [30, 15]")
    print("=" * 50)
    
    # Build matrices
    print(f"\n--- BUILDING MATRICES ---")
    G, H = random_gen_matrix(n, k)
    print(f"Generator Matrix G = \n{G}")
    print(f"\nParity Matrix H = \n{H}")
    
    # Create message and encode
    print(f"\n--- ENCODING ---")
    message = GF2.Random(k)
    print(f"Message (k={k}): {message}")
    codeword = linear_encode(message, G)
    print(f"Codeword (n={n}): {codeword}")
    
    # Transmit with t errors
    print(f"\n--- TRANSMISSION with {t} error(s) ---")
    received = transmit(codeword, GF2, num_errors=t)
    print(f"Received: {received}")
    
    # Decode with Prange
    print(f"\n--- DECODING with Prange ISD ---")
    syndrome = H @ received
    print(f"Syndrome (H @ r): {syndrome}")
    decoded, iterations = Prange(received, H, t)
    print(f"Decoded: {decoded}")
    print(f"Iterations: {iterations}")
    if decoded is not None:
        print(f"Match original codeword? {(decoded == codeword).all()}")
    else:
        print("Decoding FAILED (max iterations exceeded)")

    # Demo with multiple errors (may fail)
    print(f"\n--- TRANSMISSION with 5 errors (harder case) ---")
    t_hard = 5
    received_hard = transmit(codeword, GF2, num_errors=t_hard)
    print(f"Received: {received_hard}")
    
    print(f"\n--- DECODING with Prange ISD (t={t_hard}) ---")
    syndrome_hard = H @ received_hard
    print(f"Syndrome: {syndrome_hard}")
    decoded_hard, iterations_hard = Prange(received_hard, H, t_hard)
    print(f"Iterations: {iterations_hard}")
    if decoded_hard is not None:
        print(f"Decoded: {decoded_hard}")
        print(f"Match original codeword? {(decoded_hard == codeword).all()}")
    else:
        print("Decoding FAILED after max iterations")


def measure_prange_performance(n, k, t, num_trials=10):
    """Measure average iterations for Prange decoder.
    
    Args:
        n: code length
        k: code dimension
        t: number of errors
        num_trials: number of trials to average over
        
    Returns:
        (avg_iterations, success_rate)
    """
    iterations_list = []
    successes = 0
    
    for trial in range(num_trials):
        G, H = random_gen_matrix(n, k)
        message = GF2.Random(k)
        codeword = linear_encode(message, G)
        received = transmit(codeword, GF2, num_errors=t)
        
        decoded, iterations = Prange(received, H, t, max_iter=100000)
        
        if decoded is not None and (decoded == codeword).all():
            successes += 1
        iterations_list.append(iterations)
    
    avg_iterations = np.mean(iterations_list) if iterations_list else np.inf
    success_rate = successes / num_trials
    
    return avg_iterations, success_rate

def sweep_prange_stats(R, n_values, t_max, num_trials=5):
    """Sweep Prange performance over n and t at fixed code rate R = k/n.
    
    Args:
        R: code rate (k/n)
        n_values: list of code lengths to test
        t_max: maximum number of errors to test
        num_trials: trials per (n, t) configuration
        
    Returns:
        dict with results
    """
    results = {
        'n_values': [],
        't_values': [],
        'iterations': [],  # 2D: [t][n]
        'success_rates': []  # 2D: [t][n]
    }
    
    print(f"\n{'='*60}")
    print(f"Sweeping Prange Performance (R = {R})")
    print(f"{'='*60}")
    
    for n in n_values:
        k = int(R * n)
        results['n_values'].append(n)
        print(f"\nn = {n}, k = {k}")
        
    for t in range(1, t_max + 1):
        print(f"\nTesting t = {t} errors:")
        iter_row = []
        success_row = []
        
        for n in n_values:
            k = int(R * n)
            avg_iter, success_rate = measure_prange_performance(n, k, t, num_trials)
            iter_row.append(avg_iter)
            success_row.append(success_rate)
            
            status = "✓" if success_rate >= 0.8 else "✗"
            print(f"  n={n:2d}: {avg_iter:8.1f} iter, {success_rate*100:5.1f}% success {status}")
        
        results['t_values'].append(t)
        results['iterations'].append(iter_row)
        results['success_rates'].append(success_row)
    
    return results

def plot_prange_results(results):
    """Plot Prange performance sweep results."""
    n_values = results['n_values']
    t_values = results['t_values']
    iterations = np.array(results['iterations'])
    success_rates = np.array(results['success_rates'])
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Iterations vs n for different t
    ax1 = axes[0]
    for i, t in enumerate(t_values):
        ax1.semilogy(n_values, iterations[i], 'o-', linewidth=2, markersize=8, label=f't={t}')
    ax1.set_xlabel('Code length n', fontsize=12)
    ax1.set_ylabel('Avg iterations (log scale)', fontsize=12)
    ax1.set_title('Prange Decoder: Iterations vs Code Length', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=11)
    
    # Plot 2: Success rate vs n for different t
    ax2 = axes[1]
    for i, t in enumerate(t_values):
        ax2.plot(n_values, success_rates[i], 's-', linewidth=2, markersize=8, label=f't={t}')
    ax2.set_xlabel('Code length n', fontsize=12)
    ax2.set_ylabel('Success rate', fontsize=12)
    ax2.set_title('Prange Decoder: Success Rate vs Code Length', fontsize=13, fontweight='bold')
    ax2.set_ylim([0, 1.05])
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=11)
    ax2.axhline(y=0.8, color='r', linestyle='--', alpha=0.5, label='80% threshold')
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Demo simple
    demo()
    
    # Sweep stats
    R = 0.5  # Code rate k/n
    n_values = [10, 20, 50, 100, 200]
    t_max = 8
    
    results = sweep_prange_stats(R, n_values, t_max, num_trials=5)
    plot_prange_results(results)
