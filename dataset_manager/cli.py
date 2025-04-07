import argparse
from pathlib import Path
from .core import generate_checksum, verify_dataset

def generate_checksum_command():
    parser = argparse.ArgumentParser(description='Generate checksum file for a dataset')
    parser.add_argument('folder_path', type=str, help='Path to the dataset folder')
    parser.add_argument('--output', '-o', type=str, help='Path to the output checksum file')
    
    args = parser.parse_args()
    try:
        result = generate_checksum(args.folder_path, args.output)
        print(f"Checksum file generated: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

def verify_checksum_command():
    parser = argparse.ArgumentParser(description='Verify dataset using checksum file')
    parser.add_argument('folder_path', type=str, help='Path to the dataset folder')
    parser.add_argument('--checksum', '-c', type=str, help='Path to the checksum file')
    
    args = parser.parse_args()
    try:
        is_valid, error_messages = verify_dataset(args.folder_path, args.checksum)
        if is_valid:
            print("Verification successful: All files match their checksums")
        else:
            print("Verification failed: Found mismatched files")
            for file_path, error in error_messages.items():
                print(f"- {file_path}: {error}")
            exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1) 