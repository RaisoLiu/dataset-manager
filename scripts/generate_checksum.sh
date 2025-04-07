#!/bin/bash

# 檢查是否提供了資料夾路徑
if [ $# -eq 0 ]; then
    echo "請提供資料夾路徑"
    echo "使用方法: $0 <資料夾路徑> [校驗文件路徑]"
    exit 1
fi

# 獲取資料夾路徑
FOLDER_PATH="$1"
OUTPUT_PATH="${2:-$FOLDER_PATH/checksum.txt}"

# 檢查資料夾是否存在
if [ ! -d "$FOLDER_PATH" ]; then
    echo "錯誤: 資料夾 '$FOLDER_PATH' 不存在"
    exit 1
fi

# 檢查 Python 環境
if ! command -v python3 &> /dev/null; then
    echo "錯誤: 需要安裝 Python 3"
    exit 1
fi

# 獲取腳本所在目錄
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 執行 Python 腳本
python3 -c "
import sys
sys.path.append('$PROJECT_ROOT')
from dataset_manager.core import generate_checksum

try:
    result = generate_checksum('$FOLDER_PATH', '$OUTPUT_PATH')
    print(f'\n校驗文件已成功生成: {result}')
except Exception as e:
    print(f'錯誤: {str(e)}')
    sys.exit(1)
" 