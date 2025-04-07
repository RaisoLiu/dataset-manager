import os
import hashlib
from pathlib import Path
from typing import Optional, Dict, Tuple
from tqdm import tqdm

def calculate_file_hash(file_path: str) -> str:
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_checksum(folder_path: str, output_path: Optional[str] = None) -> str:
    """
    Generate a checksum file for all files in the given folder.
    
    Args:
        folder_path: Path to the folder containing files to checksum
        output_path: Optional path for the checksum file. If not provided,
                    will create in the same folder as folder_path.
    
    Returns:
        Path to the generated checksum file
    """
    folder_path = Path(folder_path)
    if not folder_path.is_dir():
        raise ValueError(f"{folder_path} is not a valid directory")
    
    if output_path is None:
        output_path = folder_path / "checksum.txt"
    else:
        output_path = Path(output_path)
    
    # 獲取所有需要處理的檔案
    files_to_process = []
    for file_path in sorted(folder_path.glob("**/*")):
        if file_path.is_file() and file_path.name != "checksum.txt":
            files_to_process.append(file_path)
    
    # 顯示摘要資訊
    print(f"\n=== 摘要資訊 ===")
    print(f"資料夾路徑: {folder_path}")
    print(f"輸出檔案: {output_path}")
    print(f"待處理檔案數量: {len(files_to_process)}")
    print("================\n")
    
    checksums = []
    # 使用 tqdm 顯示進度
    for file_path in tqdm(files_to_process, desc="Generating checksums"):
        relative_path = file_path.relative_to(folder_path)
        file_hash = calculate_file_hash(str(file_path))
        checksums.append(f"{relative_path} {file_hash}")
    
    with open(output_path, "w") as f:
        f.write("\n".join(checksums))
    
    return str(output_path)

def verify_dataset(folder_path: str, checksum_path: Optional[str] = None) -> Tuple[bool, Dict[str, str]]:
    """
    Verify the integrity of files in a folder against a checksum file.
    
    Args:
        folder_path: Path to the folder to verify
        checksum_path: Optional path to the checksum file. If not provided,
                      will look for checksum.txt in the folder.
    
    Returns:
        Tuple of (is_valid, error_messages)
        is_valid: True if all files match their checksums
        error_messages: Dictionary of error messages for files that don't match
    """
    folder_path = Path(folder_path)
    if not folder_path.is_dir():
        raise ValueError(f"{folder_path} is not a valid directory")
    
    if checksum_path is None:
        checksum_path = folder_path / "checksum.txt"
    else:
        checksum_path = Path(checksum_path)
    
    if not checksum_path.exists():
        raise FileNotFoundError(f"Checksum file not found at {checksum_path}")
    
    # Read checksum file
    expected_checksums = {}
    with open(checksum_path) as f:
        for line in f:
            if line.strip():
                # 將每行分成兩部分：最後的 hash 值和前面的檔案名
                line = line.strip()
                hash_value = line.split()[-1]
                file_path = line[:-len(hash_value)].strip()
                expected_checksums[file_path] = hash_value
    
    # Verify files
    error_messages = {}
    is_valid = True
    
    # Check for missing files
    print("\n=== 驗證資訊 ===")
    print(f"資料夾路徑: {folder_path}")
    print(f"校驗文件: {checksum_path}")
    print(f"待驗證檔案數量: {len(expected_checksums)}")
    print("================\n")
    
    # Check for missing files
    for expected_path in tqdm(expected_checksums, desc="Checking for missing files"):
        full_path = folder_path / expected_path
        if not full_path.exists():
            error_messages[expected_path] = "File is missing"
            is_valid = False
    
    # Check existing files
    for file_path in tqdm(sorted(folder_path.glob("**/*")), desc="Verifying file hashes"):
        if file_path.is_file() and file_path.name != "checksum.txt":
            relative_path = str(file_path.relative_to(folder_path))
            if relative_path in expected_checksums:
                actual_hash = calculate_file_hash(str(file_path))
                if actual_hash != expected_checksums[relative_path]:
                    error_messages[relative_path] = f"Hash mismatch. Expected: {expected_checksums[relative_path]}, Got: {actual_hash}"
                    is_valid = False
    
    return is_valid, error_messages 