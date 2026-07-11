#!/usr/bin/env python3
"""添加团队成员脚本"""

import os
import sys
import re
from datetime import datetime

TEAM_DIR = "management/team"
README_FILE = "management/team/README.md"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def update_team_readme(name, english_id, role, join_date):
    """更新团队成员列表"""
    ensure_dir(TEAM_DIR)

    if not os.path.exists(README_FILE):
        # 创建默认 README
        content = """# 团队成员

本目录存放团队所有成员的档案文件。

## 成员列表

| 姓名 | 英文标识 | 角色 | 入职日期 |
|------|----------|------|----------|
"""
        with open(README_FILE, 'w') as f:
            f.write(content)

    # 读取现有内容
    with open(README_FILE, 'r') as f:
        content = f.read()

    # 检查是否已存在
    if english_id in content:
        print(f"成员 {name} ({english_id}) 已存在")
        return False

    # 添加新成员到表格
    new_row = f"| {name} | {english_id} | {role} | {join_date} |\n"

    # 找到表格最后一行（暂无或最后成员行）并替换
    if "暂无" in content:
        content = content.replace("暂无", f"{name} | {english_id} | {role} | {join_date}")
    else:
        # 找到表格结束位置插入
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '|' in line and '---' not in line and '姓名' not in line:
                # 找到成员列表最后一行后插入
                pass
        content = content.rstrip('\n') + '\n' + new_row

    with open(README_FILE, 'w') as f:
        f.write(content)

    return True

def create_member_profile(name, english_id, role, join_date, research_area, tech_stack, modules, notes=""):
    """创建成员档案"""
    ensure_dir(TEAM_DIR)

    filename = os.path.join(TEAM_DIR, f"{english_id}.md")
    if os.path.exists(filename):
        print(f"档案 {filename} 已存在")
        return False

    content = f"""# {name}

## 基本信息

| 字段 | 内容 |
|------|------|
| 姓名 | {name} |
| 英文标识 | {english_id} |
| 角色 | {role} |
| 入职日期 | {join_date} |
| 研究方向 | {research_area} |

## 技术栈

"""
    for tech in tech_stack:
        content += f"- {tech}\n"

    content += "\n## 负责模块\n\n"
    for module in modules:
        content += f"- {module}\n"

    if notes:
        content += f"\n## 备注\n\n{notes}\n"

    with open(filename, 'w') as f:
        f.write(content)

    return True

def main():
    if len(sys.argv) < 3:
        print("用法:")
        print("  添加成员: python3 add_member.py <姓名> <英文ID> <角色> <入职日期> [研究方向]")
        print("示例:")
        print("  python3 add_member.py 张三 zhangsan 算法工程师 2026-01-15 LLM")
        sys.exit(1)

    name = sys.argv[1]
    english_id = sys.argv[2]
    role = sys.argv[3]
    join_date = sys.argv[4]
    research_area = sys.argv[5] if len(sys.argv) > 5 else ""

    # 更新列表
    if update_team_readme(name, english_id, role, join_date):
        print(f"✓ 已更新团队列表")

    # 创建档案
    if create_member_profile(
        name, english_id, role, join_date,
        research_area,
        ["Python", "PyTorch"],  # 默认技术栈
        ["待分配"],              # 默认模块
        ""
    ):
        print(f"✓ 已创建成员档案: {english_id}.md")

    print(f"\n成员 {name} 添加完成！")

if __name__ == "__main__":
    main()
