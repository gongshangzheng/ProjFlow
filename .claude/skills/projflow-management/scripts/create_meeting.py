#!/usr/bin/env python3
"""创建会议纪要脚本"""

import os
import sys
from datetime import datetime

MEETINGS_DIR = "management/docs/meetings"

def create_meeting(date, participants, recorder, topics, notes="", todos=""):
    """创建会议纪要"""
    os.makedirs(MEETINGS_DIR, exist_ok=True)

    filename = f"{MEETINGS_DIR}/{date}.md"
    if os.path.exists(filename):
        print(f"文件已存在: {filename}")
        return False

    content = f"""# 会议纪要 — {date}

## 基本信息

- 参会人：{participants}
- 记录人：{recorder}
- 时间：{date}

## 议题

"""
    for i, topic in enumerate(topics, 1):
        content += f"{i}. {topic}\n"

    content += "\n## 讨论内容\n\n"
    for topic in topics:
        content += f"### {topic}\n\n...\n\n"

    content += "## 决议\n\n"
    content += notes if notes else "无\n"

    content += "\n## 待办\n\n"
    content += todos if todos else "无\n"

    with open(filename, 'w') as f:
        f.write(content)

    print(f"✓ 已创建会议纪要: {filename}")
    return True

def main():
    if len(sys.argv) < 4:
        print("用法:")
        print("  python3 create_meeting.py <日期> <参会人> <记录人> [议题1] [议题2] ...")
        print("示例:")
        print("  python3 create_meeting.py 2026-07-10 '张三,李四' 张三 '项目进度' '技术方案'")
        sys.exit(1)

    date = sys.argv[1]
    participants = sys.argv[2]
    recorder = sys.argv[3]
    topics = sys.argv[4:]

    create_meeting(date, participants, recorder, topics)

if __name__ == "__main__":
    main()
