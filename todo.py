#!/usr/local/bin/python
__author__ = "Ryan Plyler"
__version__ = 0.1
import argparse
import sys
import json
import os



# parser = argparse.ArgumentParser()
#
# parser.add_argument("new", help="Create new todo", action="store_true")
# parser.add_argument("complete", help="Mark a task as completed", action="store_true")
# parser.add_argument("remove", help="Remove task from the list", action="store_true")
# parser.add_argument("show", help="List the todo list for this project", action="store_true")

# todo: Load config/constants
CONFIG_FILENAME = os.path.join(os.getcwd(), ".todo_savedata.json")
TODO_FILENAME = os.path.join(os.getcwd(), ".todo.list")

# Check if save data file is already there
if(os.path.exists(os.path.join(os.path.dirname(__file__), CONFIG_FILENAME))):
    # Load the existing config
    config = json.load(open(CONFIG_FILENAME))
else:
    # Load the existing config and write the lastid = 0
    config = {"lastid": 0}
    json.dump(config, open(CONFIG_FILENAME, 'w'))


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    RECV  = '\033[33m' # yellow
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    INFO = '\033[37m'
    WHITE = '\033[97m'


class Status:
    PENDING = "PENDING"
    DONE = "DONE"

def usage():
    print "Usage:"
    print "todo new <new todo>              | Create a new todo"
    print "todo complete|done <todo-id>     | Mark a todo as complete"
    print "todo remove|delete <todo-id>     | Remote a todo"
    print "todo show|list                   | List all todos"
    print "todo purge|reset                 | Delete all todos and todo savedata for the cwd"

def nextID():
    return str(int(config['lastid']) + 1)

def newTodo(content):
    formmated = bcolors.WHITE + "[" + nextID() + "] " + bcolors.ENDC + Status.PENDING + ": " + content + "\n"
    with open(TODO_FILENAME, "a") as f:
        f.write(formmated)
    config['lastid'] = config['lastid'] + 1

def removeTodo(id):
    oldFile = open(TODO_FILENAME, 'r')
    lines = oldFile.readlines()
    oldFile.close()
    todoRemoved = False
    newFile = open(TODO_FILENAME, 'w')
    idFormmated = "[" + str(id) + "]"

    for line in lines:
        if idFormmated in line:
            todoRemoved = True
        else:
            newFile.write(line)

    newFile.close()
    if todoRemoved:
        print "Removed todo #" + id
    else:
        print "No todo #" + id + " found."

def completeTodo(id):
    oldFile = open(TODO_FILENAME, 'r')
    lines = oldFile.readlines()
    oldFile.close()
    todoCompleted = False
    newFile = open(TODO_FILENAME, 'w')
    idFormmated = "[" + str(id) + "]"

    for line in lines:
        if idFormmated in line:
            line = line.replace(Status.PENDING, Status.DONE)
            newFile.write(line)
            todoCompleted = True
        else:
            newFile.write(line)

    newFile.close()
    if todoCompleted:
        print "Completed todo #" + id
    else:
        print "No todo #" + id + " found."

def showTodos():
    try:
        todoFile = open(TODO_FILENAME, 'r')
        lines = todoFile.readlines()
        for line in lines:
            if Status.PENDING in line:
                line = line.replace(Status.PENDING, bcolors.FAIL + Status.PENDING + bcolors.ENDC)
            elif Status.DONE in line:
                line = line.replace(Status.DONE, bcolors.OKGREEN + Status.DONE + bcolors.ENDC)
            sys.stdout.write(line)

    except IOError:
        print "No todos created for this directory yet"

if (sys.argv[1] == "new"):
        content = " ".join(sys.argv[2:])
        newTodo(content)
        print "Added todo #" + str(config['lastid'])

elif (sys.argv[1] == "complete" or sys.argv[1] == "done"):
    completeTodo(sys.argv[2])

elif (sys.argv[1] == "remove" or sys.argv[1] == "delete"):
    if len(sys.argv) < 3:
        print "You must specify a todo ID to remove."
    else:
        removeTodo(sys.argv[2])

elif (sys.argv[1] == "show" or sys.argv[1] == "list"):
    showTodos()

elif sys.argv[1] == "purge":
    ans = raw_input("Are you sure you want to delete and remove all traces of todos? (y/n): ")
    if ans == 'y':
        os.remove(CONFIG_FILENAME)
        os.remove(TODO_FILENAME)
        print "Everything deleted"
    else:
        print "Aborting deletion"

else:
    print "Unknown operation: " + sys.argv[1]
    usage()

# Save config exit
json.dump(config, open(CONFIG_FILENAME, 'w'))
