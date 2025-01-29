---
layout: single
title: "从 Obsidian 发布文章到 GitHub Pages 完整指南"
date: 2025-01-29
categories:
  - Tutorial
tags:
  - Obsidian
  - GitHub Pages
  - Blog
toc: true
toc_sticky: true
---

# 从 Obsidian 发布文章到 GitHub Pages 完整指南

## 1. 环境设置

### 1.1 必要组件
- Obsidian 安装并设置
- Git 安装并配置
- GitHub 账号
- GitHub Pages 仓库设置完成

### 1.2 目录结构
```bash
Documents/
├── Obsidian/
│   └── runes780/
│       └── 1 Permanent Notes/
│           └── Blog/           # Obsidian 博客文章源文件
└── runes780.github.io/        # GitHub Pages 仓库
    ├── _posts/                # 博客文章发布目录
    ├── assets/
    │   └── images/
    │       └── posts/         # 博客图片目录
    └── scripts/
        └── restore.sh         # 恢复脚本
```

## 2. 自动化设置

### 2.1 Git Hooks 设置

1. **pre-commit hook** (路径: `.git/hooks/pre-commit`):
```bash
#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "${GREEN}Starting Obsidian Blog sync...${NC}"

# 定义目录
SOURCE_DIR="/Users/xuqining/Documents/Obsidian/runes780/1 Permannet Notes/Blog"
POSTS_DIR="_posts"
IMAGES_DIR="assets/images/posts"
BACKUP_DIR="$HOME/.blog_backup/$(date +%Y%m%d)"

# 创建必要的目录
mkdir -p "$POSTS_DIR"
mkdir -p "$IMAGES_DIR"
mkdir -p "$BACKUP_DIR"

# 创建备份
echo "${YELLOW}Creating backup...${NC}"
if [ -d "$POSTS_DIR" ]; then
    cp "$POSTS_DIR"/*.md "$BACKUP_DIR/" 2>/dev/null || true
    echo "Backup created at $BACKUP_DIR"
fi

# 检测删除的文件
echo "${YELLOW}Checking for deleted files...${NC}"
for post in "$POSTS_DIR"/*.md; do
    if [ -f "$post" ]; then
        basename=$(basename "$post")
        # 跳过指定的保留文件
        if [[ "$basename" == "2020-08-20-hello-world.md" ]] || [[ "$basename" == "2022-04-08-learning-list.md" ]]; then
            continue
        fi
        original_name=$(echo "$basename" | sed 's/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}-//')
        if [ ! -f "$SOURCE_DIR/$original_name" ]; then
            echo "${YELLOW}Detected deleted post: $basename${NC}"
            rm "$post"
            echo "$(date -u '+%Y-%m-%d %H:%M:%S'): Deleted $basename" >> "$POSTS_DIR/.deletion_log"
        fi
    fi
done

# 同步文件
echo "${YELLOW}Syncing Markdown files...${NC}"
for file in "$SOURCE_DIR"/*.md; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        
        # 复制到临时目录进行处理
        TEMP_DIR="/tmp/blog-sync-$(date +%s)"
        mkdir -p "$TEMP_DIR"
        cp "$file" "$TEMP_DIR/"
        
        # 确保文件名符合 Jekyll 格式
        if [[ ! $filename =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2} ]]; then
            created_date=$(date -r "$file" +%Y-%m-%d)
            new_filename="${created_date}-${filename}"
        else
            new_filename="$filename"
        fi
        
        # 处理 front matter 和内容
        awk -v filename="$filename" '
        BEGIN {front_matter=0}
        /^---$/ {
            if (front_matter == 0) {
                front_matter=1
                print "---"
                next
            }
            if (front_matter == 1) {
                front_matter=2
                print "---"
                next
            }
        }
        {
            if (front_matter == 0) {
                print "---"
                print "layout: single"
                print "title: \"" filename "\""
                print "date: " strftime("%Y-%m-%d")
                print "categories:"
                print "  - Blog"
                print "tags:"
                print "  - note"
                print "toc: true"
                print "toc_sticky: true"
                print "---"
                front_matter=2
            }
            print
        }' "$TEMP_DIR/$filename" > "$POSTS_DIR/$new_filename"
        
        echo "Processed: $filename -> $new_filename"
        
        # 处理图片
        echo "${YELLOW}Processing images for $filename...${NC}"
        while IFS= read -r line; do
            if [[ $line =~ \!\[.*\]\((.*)\) ]]; then
                img_path="${BASH_REMATCH[1]}"
                if [[ ! "$img_path" =~ ^https?:// ]]; then
                    full_img_path="$SOURCE_DIR/$img_path"
                    if [ -f "$full_img_path" ]; then
                        cp "$full_img_path" "$IMAGES_DIR/"
                        sed -i '' "s|$img_path|/assets/images/posts/$(basename "$img_path")|g" "$POSTS_DIR/$new_filename"
                        echo "Copied image: $img_path"
                    fi
                fi
            fi
        done < "$TEMP_DIR/$filename"
        
        # 清理临时目录
        rm -rf "$TEMP_DIR"
    fi
done

# 添加更改到暂存区
git add "$POSTS_DIR/"
git add "$IMAGES_DIR/"

# 获取更改的文件数量
CHANGED_FILES=$(git diff --cached --numstat | wc -l)

if [ "$CHANGED_FILES" -gt 0 ]; then
    echo "${GREEN}Successfully synced $CHANGED_FILES files${NC}"
else
    echo "${YELLOW}No changes detected${NC}"
fi

exit 0
```

### 2.2 恢复脚本设置
1. **restore.sh** (路径: `scripts/restore.sh`):
```bash
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
    # 显示可用的文件
    echo "${GREEN}Available files in backup:${NC}"
    ls -1 "$BACKUP_DIR/$restore_date"/*.md 2>/dev/null
    
    # 询问用户要恢复哪些文件
    echo "${YELLOW}Enter the filenames to restore (space-separated), or 'all' for all files:${NC}"
    read -p "> " files_to_restore
    
    if [ "$files_to_restore" = "all" ]; then
        # 恢复所有文件
        cp "$BACKUP_DIR/$restore_date"/*.md "$POSTS_DIR/"
        echo "${GREEN}All files restored${NC}"
    else
        # 恢复选定的文件
        for file in $files_to_restore; do
            if [ -f "$BACKUP_DIR/$restore_date/$file" ]; then
                cp "$BACKUP_DIR/$restore_date/$file" "$POSTS_DIR/"
                echo "${GREEN}Restored: $file${NC}"
            else
                echo "${RED}File not found: $file${NC}"
            fi
        done
    fi
    
    # 显示恢复后的文件列表
    echo "${YELLOW}Current files in posts directory:${NC}"
    ls -l "$POSTS_DIR"/*.md 2>/dev/null || echo "No files in posts directory"
else
    echo "${RED}Backup directory not found: $BACKUP_DIR/$restore_date${NC}"
    echo "Available backup dates:"
    ls -1 "$BACKUP_DIR"
fi
```

## 3. 使用流程

### 3.1 发布新文章

1. **在 Obsidian 中创建文章**：
   - 在 Obsidian 的 Blog 目录中创建新的 .md 文件
   - 添加必要的 front matter
   - 编写文章内容

2. **提交更改**：
```bash
cd ~/Documents/runes780.github.io
git add .
git commit -m "Add new blog post: [文章标题]"
git push origin master
```

### 3.2 更新已有文章

1. **在 Obsidian 中编辑**：
   - 直接在 Obsidian 中修改文章内容
   - 保存更改

2. **同步更改**：
```bash
cd ~/Documents/runes780.github.io
git add .
git commit -m "Update blog post: [文章标题]"
git push origin master
```

### 3.3 删除文章

1. **从 Obsidian 删除**：
   - 直接在 Obsidian 中删除文件
   - 系统会自动同步删除操作到博客仓库

2. **确认删除**：
```bash
cd ~/Documents/runes780.github.io
git status  # 检查删除状态
git add .
git commit -m "Remove blog post: [文章标题]"
git push origin master
```

### 3.4 恢复文章

1. **查看可用备份**：
```bash
cd ~/Documents/runes780.github.io
./scripts/restore.sh
```

2. **选择要恢复的文件**：
   - 输入备份日期（YYYYMMDD格式）
   - 选择要恢复的具体文件

3. **提交恢复的文件**：
```bash
git add _posts/*.md
git commit -m "Restore blog posts: [文章标题]"
git push origin master
```

## 4. 故障排除

### 4.1 常见问题

1. **文件没有同步**：
   - 检查文件路径是否正确
   - 确认 pre-commit hook 是否有执行权限
   - 查看 git status 确认文件状态

2. **图片没有显示**：
   - 确认图片路径正确
   - 检查图片是否已复制到 assets/images/posts 目录
   - 验证图片链接格式是否正确

3. **恢复失败**：
   - 检查备份目录是否存在
   - 确认备份文件的完整性
   - 验证文件权限设置

### 4.2 日志查看

1. **删除日志**：
```bash
cat _posts/.deletion_log
```

2. **Git 日志**：
```bash
git log --pretty=format:"%h - %an, %ar : %s"
```

## 5. 维护建议

1. **定期备份**：
   - 系统会在每次提交时自动创建备份
   - 备份存储在 `~/.blog_backup/` 目录

2. **清理旧备份**：
```bash
# 删除30天前的备份
find ~/.blog_backup/* -type d -mtime +30 -exec rm -rf {} \;
```

3. **更新配置**：
   - 定期检查和更新 hooks 脚本
   - 确保路径配置保持最新

## 6. 高级功能

### 6.1 自定义 Front Matter

在 pre-commit hook 中修改 awk 脚本部分来自定义 front matter：
```bash
# 示例：添加自定义类别和标签
print "categories:"
print "  - Tech"
print "  - Tutorial"
print "tags:"
print "  - Obsidian"
print "  - GitHub"
```

### 6.2 图片处理优化

可以添加图片压缩和优化功能：
```bash
# 安装 ImageMagick
brew install imagemagick

# 在 pre-commit hook 中添加图片优化
convert "$full_img_path" -quality 85 "$IMAGES_DIR/$(basename "$img_path")"
```

## 7. 安全建议

1. **备份策略**：
   - 保持多个时间点的备份
   - 定期验证备份的完整性

2. **权限管理**：
   - 确保脚本具有适当的执行权限
   - 保护敏感配置信息

3. **版本控制**：
   - 使用有意义的提交信息
   - 保持清晰的变更历史

## 结论

这套工作流程能够帮助你：
- 在 Obsidian 中专注于写作
- 自动同步内容到 GitHub Pages
- 安全备份所有内容
- 轻松恢复误删的文章

通过这个系统，你可以专注于创作内容，而将技术细节交给自动化工具处理。
```

这个教程提供了：
1. 完整的环境设置说明
2. 详细的自动化脚本
3. 清晰的使用流程
4. 常见问题解决方案
5. 维护和安全建议

你要我修改或补充任何部分吗？
