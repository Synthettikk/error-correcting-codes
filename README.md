# Error-Correcting Codes

A pedagogical project to learn error-correcting codes (ECC) from scratch.

## 📚 Objective

Implement and understand classic ECC:
- **Hamming SECDED** ✅ (done)
- **Reed Solomon codes** ✅ (done)
- **LDPC codes** ✅ (done) 
- **Random codes** (in progress)

Each module includes **theory**, **implementation**, and **tests** to validate understanding.

## 🚀 Installation

### Prerequisites
- Python 3.8+
- `pip`

### Setup

Clone or download the project:
```bash
git clone https://github.com/Synthettikk/error-correcting-codes.git
cd error-correcting-codes
```

Install dependencies and the project in editable mode:
```bash
pip install -e .
```

## 💻 Quick Start

```python
from src.hamming import hamming_build_gen_matrix, hamming_encode, hamming_decode

# Build matrices for m=3 (8-bit codewords)
G, H = hamming_build_gen_matrix(m=3)

# Encode a message (4 bits)
message = [1, 0, 1, 0]
codeword = hamming_encode(message, G)
print(f"Codeword: {codeword}")

# Decode with automatic error correction
decoded = hamming_decode(codeword, H)
print(f"Decoded: {decoded}")
```

See `demos/demo_hamming.py` or `demos/` for more.

## 🎯 Demos

Run interactive demos:

Hamming Demo - Encoding and error correction
```bash
python -m demos.demo_hamming
```

Reed-Solomon Demo - Encoding and error correction
```bash
python -m demos.demo_rs
```

LDPC Demo - Error correction rate
```bash
python -m demos.demo_ldpc
```

## 📁 Project Structure

```python
error-correcting-codes/
├── src/
│   ├── __init__.py
│   ├── hamming.py         # Hamming SECDED implementation
│   ├── rs.py              # Reed-Solomon codes implementation
│   ├── ldpc.py            # LDPC codes + error correction rate
│   ├── utils.py           # Utilities
│   └── README.md          # Implementation choices
├── tests/                 
│   ├── test_hamming.py    # Pytest tests
│   ├── test_rs.py   
│   ├── test_ldpc.py  
├── demos/                 
│   ├── demo_hamming.py    # Interactive demos
│   ├── demo_rs.py
│   ├── demo_ldpc.py
├── docs/
│   └── ecc-theory.pdf     # Theory, explanation and examples
├── pyproject.toml
└── README.md
```

## 🧪 Tests

Run tests with:
```bash
pytest tests/
```

## 📖 Resources

Look for the pdf file in this repo and its references :

- [ECC Theory Guide](docs/ecc-theory.pdf)

