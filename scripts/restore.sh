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
    # 创建临时备份
    echo "${YELLOW}Creating temporary backup of current files...${NC}"
    TEMP_BACKUP="$BACKUP_DIR/temp_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$TEMP_BACKUP"
    cp "$POSTS_DIR"/*.md "$TEMP_BACKUP/" 2>/dev/null || true
    
    # 恢复文件
    cp "$BACKUP_DIR/$restore_date"/*.md "$POSTS_DIR/"
    echo "${GREEN}Files restored from backup $restore_date${NC}"
    echo "Temporary backup of previous state created at: $TEMP_BACKUP"
else
    echo "${RED}Backup not found${NC}"
fi
