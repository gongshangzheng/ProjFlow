#!/usr/bin/env python3
"""创建报表脚本 - 支持日报、周报、月报"""

import os
import sys
from datetime import datetime

REPORT_TYPES = {
    'daily': '日报',
    'weekly': '周报',
    'monthly': '月报'
}

def create_daily(author, date=None):
    """创建日报"""
    if date is None:
        date = datetime.now().strftime('%Y/%m/%d')
    else:
        # 转换日期格式
        dt = datetime.strptime(date, '%Y-%m-%d')
        date = dt.strftime('%Y/%m/%d')

    year, month, day = date.split('/')
    filename = f"management/daily/{year}/{month}/{day}-{author}.md"

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    if os.path.exists(filename):
        print(f"文件已存在: {filename}")
        return False

    content = f"""# {REPORT_TYPES['daily']} — {author} — {date.replace('/', '-')}

## 今日工作

-

## 明日计划

-

## 备注

无
"""

    with open(filename, 'w') as f:
        f.write(content)

    print(f"✓ 已创建日报: {filename}")
    return True

def create_weekly(author, year=None, week=None):
    """创建周报"""
    if year is None:
        year = datetime.now().strftime('%Y')
    if week is None:
        # 计算当前周数
        now = datetime.now()
        week = now.isocalendar()[1]

    filename = f"management/weekly/{year}/W{week:02d}-{author}.md"

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    if os.path.exists(filename):
        print(f"文件已存在: {filename}")
        return False

    content = f"""# {REPORT_TYPES['weekly']} — {author} — {year} 第 {week} 周

## 本周工作

-

## 下周计划

-

## 备注

无
"""

    with open(filename, 'w') as f:
        f.write(content)

    print(f"✓ 已创建周报: {filename}")
    return True

def create_monthly(author, year=None, month=None):
    """创建月报"""
    if year is None:
        year = datetime.now().strftime('%Y')
    if month is None:
        month = datetime.now().strftime('%m')

    filename = f"management/monthly/{year}/{month}-{author}.md"

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    if os.path.exists(filename):
        print(f"文件已存在: {filename}")
        return False

    content = f"""# {REPORT_TYPES['monthly']} — {author} — {year} 年 {month} 月

## 本月工作

-

## 下月计划

-

## 备注

无
"""

    with open(filename, 'w') as f:
        f.write(content)

    print(f"✓ 已创建月报: {filename}")
    return True

def main():
    if len(sys.argv) < 3:
        print("用法:")
        print("  python3 create_report.py daily <作者> [日期 YYYY-MM-DD]")
        print("  python3 create_report.py weekly <作者> [年份 YYYY] [周数 W]")
        print("  python3 create_report.py monthly <作者> [年份 YYYY] [月份 MM]")
        print("示例:")
        print("  python3 create_report.py daily zhangsan")
        print("  python3 create_report.py daily zhangsan 2026-07-10")
        print("  python3 create_report.py weekly zhangsan")
        print("  python3 create_report.py monthly zhangsan")
        sys.exit(1)

    report_type = sys.argv[1].lower()
    author = sys.argv[2]

    if report_type == 'daily':
        date = sys.argv[3] if len(sys.argv) > 3 else None
        create_daily(author, date)
    elif report_type == 'weekly':
        year = sys.argv[3] if len(sys.argv) > 3 else None
        week = sys.argv[4] if len(sys.argv) > 4 else None
        create_weekly(author, year, week)
    elif report_type == 'monthly':
        year = sys.argv[3] if len(sys.argv) > 3 else None
        month = sys.argv[4] if len(sys.argv) > 4 else None
        create_monthly(author, year, month)
    else:
        print(f"未知报表类型: {report_type}")
        sys.exit(1)

if __name__ == "__main__":
    main()
