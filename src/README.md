# Implementation choices

## Shared utilities

All code families use the same generic encoding function, which encodes a message using a generator matrix $G$. The shared utilities also provide a transmission function that adds either a specified error vector or a randomly generated error pattern to a codeword.

## Hamming codes

The parity-check matrix $H$ is stored in systematic form. For a single-bit error, the syndrome identifies the corresponding column of $H$, and therefore the error position.

## Reed–Solomon codes

### Generator matrix

The generator matrix $G$ is constructed from a Vandermonde matrix over the code’s finite field, using the chosen evaluation points.

### Decoder

We use the Welch–Berlekamp decoder because it is relatively simple and follows naturally from the polynomial definition of Reed–Solomon codes. Berlekamp–Massey is generally more efficient for decoding classical Reed–Solomon codes, but is not used in this implementation.

## LDPC codes

### Parity-check matrix generation

We construct the parity-check matrix in systematic form:
$H = [A \mid I_{n-k}]$,

where $A$ is a randomly generated $(n-k) \times k$ matrix and $I_{n-k}$ is the identity matrix. Each row of $A$ is assigned $d_c - 1$ randomly selected ones, so each row of $H$ has $d_c$ ones.

A fully random parity-check matrix may not have the desired rank. Including the identity block guarantees that $H$ has full row rank $n-k$, giving a null space of dimension $k$.

### Decoder

We use a simple bit-flipping decoder that flips one bit per iteration. It is conceptually related to bit-flipping decoding used in BIKE, but it is a simplified implementation.
