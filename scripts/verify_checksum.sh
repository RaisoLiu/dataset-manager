#!/bin/bash

# 檢查是否提供了資料夾路徑
if [ $# -eq 0 ]; then
    echo "請提供資料夾路徑"
    echo "使用方法: $0 <資料夾路徑> [校驗文件路徑]"
    exit 1
fi

# 獲取資料夾路徑
FOLDER_PATH="$1"
CHECKSUM_PATH="${2:-$FOLDER_PATH/checksum.txt}"

# 檢查資料夾是否存在
if [ ! -d "$FOLDER_PATH" ]; then
    echo "錯誤: 資料夾 '$FOLDER_PATH' 不存在"
    exit 1
fi

# 檢查校驗文件是否存在
if [ ! -f "$CHECKSUM_PATH" ]; then
    echo "錯誤: 校驗文件 '$CHECKSUM_PATH' 不存在"
    exit 1
fi

# 檢查是否安裝了 sha256sum
if ! command -v sha256sum &> /dev/null; then
    echo "錯誤: 需要安裝 sha256sum 工具"
    echo "在 macOS 上，您可以通過 'brew install coreutils' 安裝"
    exit 1
fi

echo "開始驗證校驗文件..."
echo "資料夾: $FOLDER_PATH"
echo "校驗文件: $CHECKSUM_PATH"

# 臨時文件用於存儲當前校驗值
TEMP_CHECKSUM=$(mktemp)

# 生成當前校驗值
find "$FOLDER_PATH" -type f -not -path "*/\.*" -not -name "checksum.txt" -exec sha256sum {} \; | \
    sed "s|$FOLDER_PATH/||" | \
    sort > "$TEMP_CHECKSUM"

# 比較校驗值
if diff -q "$CHECKSUM_PATH" "$TEMP_CHECKSUM" > /dev/null; then
    echo "驗證成功：所有檔案都符合校驗值"
    rm "$TEMP_CHECKSUM"
    exit 0
else
    echo "驗證失敗：發現不一致的檔案"
    echo "詳細差異："
    diff "$CHECKSUM_PATH" "$TEMP_CHECKSUM"
    rm "$TEMP_CHECKSUM"
    exit 1
fi 