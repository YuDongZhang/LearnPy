"""
待办事项管理工具 (Todo List CLI)
===============================

一个完整的命令行工具，综合运用 Python 基础知识。
"""

import json
import os
from datetime import datetime

TODO_FILE = "todos.json"

class TodoList:
    def __init__(self):
        self.tasks = []
        self.load()
    
    def load(self):
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []
    
    def save(self):
        with open(TODO_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def add(self, task):
        task_dict = {
            "id": len(self.tasks) + 1,
            "content": task,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task_dict)
        self.save()
        print(f"✓ 已添加任务: {task}")
    
    def list(self):
        if not self.tasks:
            print("暂无待办事项")
            return
        
        print("\n" + "=" * 50)
        print("我的待办事项")
        print("=" * 50)
        
        for task in self.tasks:
            status = "✓" if task["completed"] else "○"
            content = task["content"]
            if task["completed"]:
                content = f"\033[9m{content}\033[0m"
            print(f"  [{task['id']}] {status} {content}")
            print(f"       创建时间: {task['created_at']}")
        
        print("=" * 50)
        print(f"总计: {len(self.tasks)} 个任务")
        completed = sum(1 for t in self.tasks if t["completed"])
        print(f"已完成: {completed}, 未完成: {len(self.tasks) - completed}")
        print()
    
    def done(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save()
                print(f"✓ 已完成任务: {task['content']}")
                return
        print(f"✗ 未找到任务 #{task_id}")
    
    def delete(self, task_id):
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                removed = self.tasks.pop(i)
                self.save()
                print(f"✓ 已删除任务: {removed['content']}")
                self.reindex()
                return
        print(f"✗ 未找到任务 #{task_id}")
    
    def reindex(self):
        for i, task in enumerate(self.tasks):
            task["id"] = i + 1
        self.save()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="待办事项管理工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    add_parser = subparsers.add_parser("add", help="添加新任务")
    add_parser.add_argument("task", help="任务内容")
    
    list_parser = subparsers.add_parser("list", help="列出所有任务")
    
    done_parser = subparsers.add_parser("done", help="完成任务")
    done_parser.add_argument("id", type=int, help="任务ID")
    
    delete_parser = subparsers.add_parser("delete", help="删除任务")
    delete_parser.add_argument("id", type=int, help="任务ID")
    
    args = parser.parse_args()
    
    todo = TodoList()
    
    if args.command == "add":
        todo.add(args.task)
    elif args.command == "list":
        todo.list()
    elif args.command == "done":
        todo.done(args.id)
    elif args.command == "delete":
        todo.delete(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
