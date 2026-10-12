import galois #for GF2 arithmetics
import numpy as np
import matplotlib.pyplot as plt
from src.utils import linear_encode, transmit

GF2 = galois.GF(2)

def ldpc_build_gen_matrix(n, k, dc = 4):
    """Build LDPC generator and parity matrices in systematic form.
    dc = number of 1s per row, grows O(1)
    dv = number of 1s per col, grows O(1)"""

    I_nk = GF2.Identity(n-k)
    A = GF2.Zeros((n-k, k))
    for row in range(n-k):
        # Choose randomly dc-1 positions in row 
        A[row, np.random.choice(k, dc - 1, replace=False)] = 1

    # H = [A | I_{n-k}]
    H = GF2(np.concatenate([A, I_nk], axis=1))
    G = H.null_space()

    return G, H

def bit_flip(received, H, I_max = 2):
    codeword = GF2(received)
    for _ in range(I_max):
        s = H @ codeword.T 
        if (s == 0).all():
            # decoding success (or not if received is a codeword but not the original one)
            return codeword 

        count = np.array(s, dtype=int) @ np.array(H, dtype=int)
        argmax_idx = np.argmax(count)
        codeword[argmax_idx] += GF2(1)
    return codeword

def measure_bit_flip_success(G, H, n, k, t, trials=1000, I_max=20):
    successes = 0

    for _ in range(trials):
        # message and codewords
        message = GF2.Random(k)
        original = linear_encode(message, G)
        received = transmit(original, GF2, num_errors=t,)

        decoded = bit_flip(received, H, I_max=I_max)

        if (decoded == original).all():
            successes += 1

    return successes / trials


def sweep_bit_flip(
    n_values,
    code_rate,
    error_rates,
    matrices_per_point=5,
    trials=200,
    dc=4,
    I_max=20,
    seed=0,
):
    np.random.seed(seed)

    n_values = np.array(sorted(n_values))
    error_rates = np.array(sorted(error_rates))

    scores = np.zeros((len(n_values), len(error_rates)))
    k_values = []

    for i, n in enumerate(n_values):
        k = int(round(code_rate * n))

        if not (dc - 1 <= k < n):
            raise ValueError(f"Invalid value : n={n}, k={k}, dc={dc}")

        k_values.append(k)

        # For each n, try multiple matrices
        # Test with the error rates
        for _ in range(matrices_per_point):
            G, H = ldpc_build_gen_matrix(n, k, dc=dc)

            for j, p in enumerate(error_rates):
                # errors number
                t = int(round(p * n))

                scores[i, j] += measure_bit_flip_success(
                    G, H, n, k, t,
                    trials=trials,
                    I_max=I_max,
                )

        scores[i, :] /= matrices_per_point

    return n_values, error_rates, np.array(k_values), scores


def plot_sweep_results():
    ns, ps, ks, scores = sweep_bit_flip(
        n_values=[10, 25, 50, 100],
        code_rate=0.5,
        error_rates=[0, 0.01, 0.02, 0.04, 0.06, 0.08],
        matrices_per_point=5,
        trials=200,
        dc=4,
        I_max=20,
    )

    print("=" * 50)
    print("Checking Bit-Flipping Success Rate...")
    print("May take a few minutes...")
    print("=" * 50)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Success based on the error rate; one curve per n
    for i, n in enumerate(ns):
        axes[0].plot(ps, scores[i], marker="o", label=f"n={n}, k={ks[i]}")

    axes[0].set_xlabel("error rate")
    axes[0].set_ylabel("Percentage of Successful Exact Decodings")
    axes[0].set_title("Effect of the error rate")
    axes[0].set_ylim(0, 1.05)
    axes[0].grid(True)
    axes[0].legend()

    # Success as a function of n: a curve based on error rate
    for j, p in enumerate(ps):
        axes[1].plot(ns, scores[:, j], marker="o", label=f"taux={p:.0%}")

    axes[1].set_xlabel("Length of the code n")
    axes[1].set_ylabel("Percentage of Successful Exact Decodings")
    axes[1].set_title("Effect of Code Sizee")
    axes[1].set_ylim(0, 1.05)
    axes[1].grid(True)
    axes[1].legend()

    plt.tight_layout()
    plt.show()