# Dataset Manager

A Python tool for managing and verifying datasets.

## Features

- Generate checksum files for datasets
- Verify dataset integrity using checksum files
- Progress bar support for large datasets

## Installation

### From GitHub

```bash
pip install git+https://github.com/RaisoLiu/dataset-manager.git
```

### From Source

```bash
# Clone the repository
git clone https://github.com/RaisoLiu/dataset-manager.git
cd dataset-manager

# Install in development mode
pip install -e .
```

## Usage

### Generate Checksum File

```python
from dataset_manager import generate_checksum

# Generate checksum file in the same directory
generate_checksum("path/to/dataset")

# Generate checksum file in a specific location
generate_checksum("path/to/dataset", "path/to/checksum.txt")
```

### Verify Dataset

```python
from dataset_manager import verify_dataset

# Verify dataset using checksum file in the same directory
is_valid, errors = verify_dataset("path/to/dataset")

# Verify dataset using specific checksum file
is_valid, errors = verify_dataset("path/to/dataset", "path/to/checksum.txt")
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/RaisoLiu/dataset-manager.git
cd dataset-manager

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## License

MIT 