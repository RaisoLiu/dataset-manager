# Dataset Manager

一個用於管理數據集校驗和的工具。

## 功能

- 生成數據集的校驗和文件
- 驗證數據集的完整性

## 安裝

```bash
pip install git+https://github.com/username/dataset-manager.git
```

## 使用方法

### 命令列工具

安裝後，你可以使用以下命令：

#### 生成校驗和

```bash
dm-generate-checksum <資料夾路徑> [--output <輸出文件路徑>]
```

例如：
```bash
# 在資料夾內生成 checksum.txt
dm-generate-checksum /path/to/dataset

# 指定輸出文件位置
dm-generate-checksum /path/to/dataset --output /path/to/checksum.txt
```

#### 驗證校驗和

```bash
dm-verify-checksum <資料夾路徑> [--checksum <校驗文件路徑>]
```

例如：
```bash
# 使用資料夾內的 checksum.txt 進行驗證
dm-verify-checksum /path/to/dataset

# 使用指定的校驗文件進行驗證
dm-verify-checksum /path/to/dataset --checksum /path/to/checksum.txt
```

### Python API

你也可以在 Python 程式中使用：

```python
from dataset_manager import generate_checksum, verify_dataset

# 生成校驗和
generate_checksum("path/to/dataset")
generate_checksum("path/to/dataset", "path/to/checksum.txt")

# 驗證校驗和
is_valid, errors = verify_dataset("path/to/dataset")
is_valid, errors = verify_dataset("path/to/dataset", "path/to/checksum.txt")
```

## 依賴

- Python >= 3.7
- tqdm >= 4.65.0

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