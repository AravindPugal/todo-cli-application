import os
import sys
from datetime import datetime
from typing import Optional
currentDir = os.getcwd()
arguments = sys.argv


def addTask(filename, task):
    todoTasks = open(f"{currentDir}\\{filename}", "a+")
    todoTasks.write(task)
    todoTasks.close()


def getTasks(filename):
    try:
        todoTasks = open(f"{currentDir}\\{filename}", "r")
        tasks = todoTasks.readlines()
        todoTasks.close()
        return tasks, True
    except:
        print("something")
        sys.stdout.buffer.write("There are no pending todos!\n".encode('utf8'))
        return "nothing", False


def deleteTask(errMsg):
    taskIndex = int(arguments[2])
    try:
        tasks, status = getTasks("todo.txt")
        if status and taskIndex > 0:
            deletedTask = tasks.pop(taskIndex-1)
            todoTasks = open(f"{currentDir}\\todo.txt", "w+")
            todoTasks.writelines(tasks)
            todoTasks.close()
            return deletedTask, True
        else:
            sys.stdout.buffer.write(errMsg.encode('utf8'))
            return "nothing", False
    except:
        sys.stdout.buffer.write(errMsg.encode('utf8'))
        return "nothing", False


def giveReport(filename):
    try:
        todoTasks = open(f"{currentDir}\\{filename}", "r")
        tasks = todoTasks.readlines()
        todoTasks.close()
        return len(tasks)
    except:
        return 0


def help():
    message = '''Usage :-
$ ./todo add "todo item"  # Add a new todo
$ ./todo ls               # Show remaining todos
$ ./todo del NUMBER       # Delete a todo
$ ./todo done NUMBER      # Complete a todo
$ ./todo help             # Show usage
$ ./todo report           # Statistics\n'''
    sys.stdout.buffer.write(message.encode('utf8'))


if len(arguments) == 1:
    help()
else:
    # add add task
    if arguments[1] == "add":
        if len(arguments) == 2:
            sys.stdout.buffer.write(
                "Error: Missing todo string. Nothing added!\n".encode('utf8'))
        else:
            newtask = arguments[2]+"\n"
            addTask("todo.txt", newtask)
            sys.stdout.buffer.write(
                f'Added todo: "{newtask.strip()}"'.encode('utf8'))

    # list tasks
    elif arguments[1] == "ls":
        taskList, status = getTasks("todo.txt")
        if status and len(taskList) > 0:
            tasks = list(map(lambda string: string.strip(), taskList))
            count = len(tasks)
            for i in range(count-1, -1, -1):
                sys.stdout.buffer.write(f"[{i+1}] {tasks[i]}\n".encode('utf8'))
        else:
            sys.stdout.buffer.write(
                "There are no pending todos!\n".encode('utf8'))
    # delete task
    elif arguments[1] == "del":
        if len(arguments) == 2:
            sys.stdout.buffer.write(
                "Error: Missing NUMBER for deleting todo.\n".encode('utf8'))
        else:
            errMsg = f"Error: todo #{arguments[2]} does not exist. Nothing deleted.\n"
            deleted, status = deleteTask(errMsg)
            if status:
                sys.stdout.buffer.write(
                    f"Deleted todo #{arguments[2]}\n".encode('utf8'))
    # done task
    elif arguments[1] == "done":
        if len(arguments) == 2:
            sys.stdout.buffer.write(
                "Error: Missing NUMBER for marking todo as done.\n".encode('utf8'))
        else:
            errMsg = f"Error: todo #{arguments[2]} does not exist.\n"
            completedTask, status = deleteTask(errMsg)
            if status:
                currentDate = datetime.today().strftime('%Y-%m-%d')
                completedTask = f"x {currentDate} {completedTask}"
                addTask("done.txt", completedTask)
                sys.stdout.buffer.write(
                    f"Marked todo #{arguments[2]} as done.\n".encode('utf8'))

    # help Option
    elif arguments[1] == "help":
        help()
    elif arguments[1] == "report":
        currentDate = datetime.today().strftime("%Y-%m-%d")
        pending, completed = giveReport("todo.txt"), giveReport("done.txt")
        sys.stdout.buffer.write(
            f"{currentDate} Pending : {pending} Completed : {completed}\n".encode("utf8"))
    else:
        sys.stdout.buffer.write("Something went wrong".encode("utf8"))
