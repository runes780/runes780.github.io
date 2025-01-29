#!/bin/bash

BACKUP_DIR="$HOME/.blog_backup"
POSTS_DIR="_posts"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 列出可用的备份
echo "${GREEN}Available backups:${NC}"
ls -l "$BACKUP_DIR"

# 从用户输入获取要恢复的日期
read -p "Enter backup date (YYYYMMDD): " restore_date

if [ -d "$BACKUP_DIR/$restore_date" ]; then
    # 检查备份目录中是否有 .md 文件
    md_count=$(ls -1 "$BACKUP_DIR/$restore_date"/*.md 2>/dev/null | wc -l)
    if [ "$md_count" -eq 0 ]; then
        echo "${RED}No markdown files found in backup directory${NC}"
        exit 1
    fi

    # 创建临时备份
    echo "${YELLOW}Creating temporary backup of current files...${NC}"
    TEMP_BACKUP="$BACKUP_DIR/temp_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$TEMP_BACKUP"
    
    # 如果当前目录有 .md 文件，才进行备份
    if ls "$POSTS_DIR"/*.md 1> /dev/null 2>&1; then
        cp "$POSTS_DIR"/*.md "$TEMP_BACKUP/"
        echo "${GREEN}Current files backed up to: $TEMP_BACKUP${NC}"
    else
        echo "${YELLOW}No current files to backup${NC}"
    fi
    
    # 恢复文件
    echo "${YELLOW}Restoring files from backup $restore_date...${NC}"
    cp "$BACKUP_DIR/$restore_date"/*.md "$POSTS_DIR/"
    
    # 验证恢复
    restored_count=$(ls -1 "$POSTS_DIR"/*.md 2>/dev/null | wc -l)
    if [ "$restored_count" -gt 0 ]; then
        echo "${GREEN}Successfully restored $restored_count files from backup${NC}"
        echo "Restored files:"
        ls -l "$POSTS_DIR"/*.md
    else
        echo "${RED}Failed to restore files${NC}"
    fi
else
    echo "${RED}Backup directory not found: $BACKUP_DIR/$restore_date${NC}"
    echo "Available backup dates:"
    ls -1 "$BACKUP_DIR"
fi
