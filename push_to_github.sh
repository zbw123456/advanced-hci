#!/bin/bash

# MindCare - GitHub Push Script
# Run this after creating your repository on GitHub

echo "🚀 MindCare GitHub Push Script"
echo "================================"
echo ""

# Prompt for repository name
read -p "请输入你在GitHub上创建的仓库名 (例如: mindcare-hci): " REPO_NAME

if [ -z "$REPO_NAME" ]; then
    echo "❌ 仓库名不能为空！"
    exit 1
fi

echo ""
echo "📋 将推送到: https://github.com/zbw123456/$REPO_NAME"
echo ""
read -p "确认无误？(y/n): " CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "❌ 已取消"
    exit 1
fi

echo ""
echo "🔗 添加远程仓库..."
git remote add origin "https://github.com/zbw123456/$REPO_NAME.git"

if [ $? -ne 0 ]; then
    echo "⚠️  远程仓库已存在，尝试更新..."
    git remote set-url origin "https://github.com/zbw123456/$REPO_NAME.git"
fi

echo "✅ 远程仓库已配置"
echo ""

echo "📤 推送到GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 成功推送到GitHub!"
    echo ""
    echo "🌐 访问你的仓库："
    echo "   https://github.com/zbw123456/$REPO_NAME"
    echo ""
    echo "🎉 完成！"
else
    echo ""
    echo "❌ 推送失败，可能需要身份验证"
    echo ""
    echo "💡 提示："
    echo "1. 确保已登录GitHub"
    echo "2. 可能需要使用Personal Access Token"
    echo "3. 参考: https://docs.github.com/en/authentication"
fi
