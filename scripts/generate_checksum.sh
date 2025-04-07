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

# 檢查是否安裝了 sha256sum
if ! command -v sha256sum &> /dev/null; then
    echo "錯誤: 需要安裝 sha256sum 工具"
    echo "在 macOS 上，您可以通過 'brew install coreutils' 安裝"
    exit 1
fi

echo "開始生成校驗文件..."
echo "資料夾: $FOLDER_PATH"
echo "輸出文件: $OUTPUT_PATH"

# 生成校驗文件
find "$FOLDER_PATH" -type f -not -path "*/\.*" -not -name "checksum.txt" -exec sha256sum {} \; | \
    sed "s|$FOLDER_PATH/||" | \
    sort > "$OUTPUT_PATH"

# 檢查是否成功
if [ $? -eq 0 ]; then
    echo "校驗文件已成功生成"
    echo "共處理 $(wc -l < "$OUTPUT_PATH") 個檔案"
else
    echo "生成校驗文件時發生錯誤"
    exit 1
fi 