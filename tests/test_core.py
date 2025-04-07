import os
import tempfile
import shutil
from pathlib import Path
import pytest
from dataset_manager.core import generate_checksum, verify_dataset

@pytest.fixture
def test_folder():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Create some test files
    test_files = {
        "file1.txt": "This is test file 1",
        "file2.txt": "This is test file 2",
        "subfolder/file3.txt": "This is test file 3"
    }
    
    # Create the files
    for file_path, content in test_files.items():
        full_path = Path(temp_dir) / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
    
    yield temp_dir
    
    # Cleanup
    shutil.rmtree(temp_dir)

def test_generate_checksum(test_folder):
    # Generate checksum file
    checksum_path = generate_checksum(test_folder)
    
    # Verify the checksum file exists
    assert os.path.exists(checksum_path)
    
    # Read the checksum file
    with open(checksum_path) as f:
        lines = f.readlines()
    
    # Verify the number of entries
    assert len(lines) == 3  # We created 3 files
    
    # Verify each line has the correct format
    for line in lines:
        assert len(line.strip().split()) == 2

def test_generate_checksum_custom_path(test_folder):
    # Generate checksum file in a custom location
    custom_path = os.path.join(tempfile.gettempdir(), "custom_checksum.txt")
    checksum_path = generate_checksum(test_folder, custom_path)
    
    # Verify the checksum file exists at the custom location
    assert checksum_path == custom_path
    assert os.path.exists(custom_path)
    
    # Cleanup
    os.remove(custom_path)

def test_verify_dataset_valid(test_folder):
    # Generate checksum file
    generate_checksum(test_folder)
    
    # Verify the dataset
    is_valid, errors = verify_dataset(test_folder)
    
    # Should be valid
    assert is_valid
    assert not errors

def test_verify_dataset_missing_file(test_folder):
    # Generate checksum file
    generate_checksum(test_folder)
    
    # Delete a file
    os.remove(os.path.join(test_folder, "file1.txt"))
    
    # Verify the dataset
    is_valid, errors = verify_dataset(test_folder)
    
    # Should be invalid
    assert not is_valid
    assert "file1.txt" in errors
    assert errors["file1.txt"] == "File is missing"

def test_verify_dataset_modified_file(test_folder):
    # Generate checksum file
    generate_checksum(test_folder)
    
    # Modify a file
    with open(os.path.join(test_folder, "file1.txt"), "w") as f:
        f.write("Modified content")
    
    # Verify the dataset
    is_valid, errors = verify_dataset(test_folder)
    
    # Should be invalid
    assert not is_valid
    assert "file1.txt" in errors
    assert "Hash mismatch" in errors["file1.txt"]

def test_verify_dataset_custom_checksum(test_folder):
    # Generate checksum file in a custom location
    custom_path = os.path.join(tempfile.gettempdir(), "custom_checksum.txt")
    generate_checksum(test_folder, custom_path)
    
    # Verify the dataset using custom checksum file
    is_valid, errors = verify_dataset(test_folder, custom_path)
    
    # Should be valid
    assert is_valid
    assert not errors
    
    # Cleanup
    os.remove(custom_path)

def test_verify_dataset_extra_files(test_folder):
    # Generate checksum file
    generate_checksum(test_folder)
    
    # Add an extra file
    extra_file = os.path.join(test_folder, "extra_file.txt")
    with open(extra_file, "w") as f:
        f.write("This is an extra file")
    
    # Verify the dataset
    is_valid, errors = verify_dataset(test_folder)
    
    # Should be valid because we don't check for extra files
    assert is_valid
    assert not errors
    
    # Add an extra file in a subfolder
    extra_subfolder = os.path.join(test_folder, "subfolder", "extra_file2.txt")
    with open(extra_subfolder, "w") as f:
        f.write("This is another extra file")
    
    # Verify the dataset again
    is_valid, errors = verify_dataset(test_folder)
    
    # Should still be valid
    assert is_valid
    assert not errors 