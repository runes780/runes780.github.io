#!/bin/bash

# 配置源目录和目标目录
SOURCE_DIR="/Users/xuqining/Documents/Obsidian/runes780/1 Permannet Notes/Blog"
POSTS_DIR="_posts"
IMAGES_DIR="assets/images/posts"

# 创建必要的目录
mkdir -p "$POSTS_DIR"
mkdir -p "$IMAGES_DIR"

# 同步 markdown 文件
for file in "$SOURCE_DIR"/*.md; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        # 确保文件名符合 Jekyll 格式 (YYYY-MM-DD-title.md)
        if [[ ! $filename =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2} ]]; then
            created_date=$(date -r "$file" +%Y-%m-%d)
            new_filename="${created_date}-${filename}"
        else
            new_filename="$filename"
        fi
        
        # 处理文件内容
        awk '
        BEGIN {front_matter=0}
        /^---$/ {
            if (front_matter == 0) {
                front_matter=1
                print "---"
                print "layout: single"
                print "author_profile: true"
                next
            }
        }
        {
            if (front_matter == 0) {
                print "---"
                print "layout: single"
                print "author_profile: true"
                print "title: \"" FILENAME "\""
                print "date: " strftime("%Y-%m-%d")
                print "categories:"
                print "  - Blog"
                print "tags:"
                print "  - note"
                print "---"
                front_matter=2
            }
            print
        }' "$file" > "$POSTS_DIR/$new_filename"
        
        # 处理图片
        for img in $(grep -o '!\[.*\](.*png\|.*jpg\|.*jpeg\|.*gif)' "$file" | grep -o '(.*png\|.*jpg\|.*jpeg\|.*gif)' | tr -d '()'); do
            if [[ "$img" =~ ^https?:// ]]; then
                continue
            fi
            img_path="$SOURCE_DIR/$img"
            if [ -f "$img_path" ]; then
                cp "$img_path" "$IMAGES_DIR/"
                sed -i '' "s|]($img)|](/assets/images/posts/$(basename "$img"))|g" "$POSTS_DIR/$new_filename"
            fi
        done
    fi
done