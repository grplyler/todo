#!/usr/local/bin/python
__author__ = "Ryan Plyler"
__version__ = 0.2

import sys
import json
import os

########################################################################
# Load config and other related things
########################################################################

CONFIG_FILENAME = os.path.join(os.getcwd(), 'todosavedata.json')
TODO_FILENAME = os.path.join(os.getcwd(), 'todo.list')

if(os.path.exists(os.path.join(os.path.dirname(__file__), CONFIG_FILENAME))):
    # Load the existing config
    config = json.load(open(CONFIG_FILENAME))
else:
    # Load the existing config and write the lastid = 0
    config = {"lastid": 0}
    json.dump(config, open(CONFIG_FILENAME, 'w'))

########################################################################
# Global Classes: bcolors Status
########################################################################

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

########################################################################
# Helper Fuctions: usage() nextID()
########################################################################

def usage():
    print "Usage:"
    print "todo new <new todo>              | Create a new todo"
    print "todo complete|done <todo-id>     | Mark a todo as complete"
    print "todo remove|delete <todo-id>     | Remote a todo"
    print "todo show|list                   | List all todos"
    print "todo purge|reset                 | Delete all todos and todo savedata for the cwd"

def nextID():
    return str(int(config['lastid']) + 1)

########################################################################
# Core functionality functions:
# newTodo() removeTodo(id) completeTodo(id) undoTodo(id)
# showTodos()
########################################################################

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

def undoTodo(id):
    oldFile = open(TODO_FILENAME, 'r')
    lines = oldFile.readlines()
    oldFile.close()
    todoCompleted = False
    newFile = open(TODO_FILENAME, 'w')
    idFormmated = "[" + str(id) + "]"

    for line in lines:
        if idFormmated in line:
            line = line.replace(Status.DONE, Status.PENDING)
            newFile.write(line)
            todoCompleted = True
        else:
            newFile.write(line)

    newFile.close()
    if todoCompleted:
        print "Undid todo #" + id + " now its pending again..."
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


########################################################################
# Parse command line arguments
########################################################################

if sys.argv[1] == "new":
        content = " ".join(sys.argv[2:])
        newTodo(content)
        print "Added todo #" + str(config['lastid'])

elif sys.argv[1] == "complete" or sys.argv[1] == "done":
    completeTodo(sys.argv[2])

elif sys.argv[1] == "undo":
    undoTodo(sys.argv[2])

elif sys.argv[1] == "remove" or sys.argv[1] == "delete":
    if len(sys.argv) < 3:
        print "You must specify a todo ID to remove."
    else:
        removeTodo(sys.argv[2])

elif sys.argv[1] == "show" or sys.argv[1] == "list":
    showTodos()

elif sys.argv[1] == "purge":
    ans = raw_input("Are you sure you want to delete and remove all traces of todos? (y/n): ")
    if ans == 'y':
        if os.path.isfile(CONFIG_FILENAME):
            os.remove(str(CONFIG_FILENAME))
            print "Removed config file."
        else:
            print "Could not delete save data file"

        if os.path.isfile(TODO_FILENAME):
            os.remove(str(TODO_FILENAME))
            print "Removed todo file"
        else:
            print "Could not delete todo file"

    else:
        print "Aborting deletion"

else:
    print "Unknown operation: " + sys.argv[1]
    usage()

########################################################################
# Cleanup and exit
########################################################################

json.dump(config, open(CONFIG_FILENAME, 'w'))
