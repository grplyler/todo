#!/usr/bin/python
__author__ = "Ryan Plyler"
__version__ = 0.2

import sys
import json
import os

########################################################################
# Config
########################################################################

TODO_FILENAME = os.path.join(os.getcwd(), '.todo.list')


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
    DONE = "   DONE"

########################################################################
# Helper Fuctions: usage() nextID()
########################################################################

def usage():
    print "\nUsage:"
    print "\ttodo                                    | List the todos for the current directory"
    print "\ttodo show|list                          | Same as 'todo'"
    print "\ttodo new <new todo>                     | Create a new todo"
    print "\ttodo complete|done <todo-id>            | Mark a todo as complete"
    print "\ttodo remove|rm|delete|del <todo-id>     | Remove a todo"
    print "\ttodo undo <todo-id>                     | Undo a 'DONE' todo. Make it pending again."
    print "\ttodo purge                              | Delete all todos and todo savedata for the cwd"
    print "\ttodo help                               | Show this help"
    print

def getLineCount():
    with open(TODO_FILENAME) as f:
        lines = f.readlines()
        return len(lines)

def readlines():
    with open(TODO_FILENAME) as f:
        lines = f.readlines()
        linecount = len(lines)
        return lines, linecount

def nextID():
    """Get the the number of what the next todo ID should be"""
    return getLineCount() + 1


########################################################################
# Core functionality functions:
# newTodo() removeTodo(id) completeTodo(id) undoTodo(id)
# showTodos()
########################################################################

def newTodo(content):
    formmated = bcolors.WHITE + "[" + "%id" + "] " + bcolors.ENDC + Status.PENDING + ": " + content + "\n"
    with open(TODO_FILENAME, "a") as f:
        f.write(formmated)
    print "Added todo #%d" % getLineCount()


def removeTodo(id):
    id = int(id)

    lineCounter = 1
    lines, linecount = readlines()
    todoRemoved = False
    newFile = open(TODO_FILENAME, 'w')

    for line in lines:
        # Write all the lines back to the file except the line number of id
        if lineCounter is not id:
            newFile.write(line)
        else:
            todoRemoved = True

        # increment the line counter
        lineCounter += 1


    newFile.close()
    if todoRemoved:
        print "Removed todo #%s" % id
    else:
        print "No todo #%s found" % id

def completeTodo(id):
    id = int(id)
    lines, linecount = readlines()
    todoCompleted = False
    newFile = open(TODO_FILENAME, 'w')
    lineCounter = 1

    for line in lines:
        # Write all the lines back to the file except the line number of id
        if lineCounter == id:
            line = line.replace(Status.PENDING, Status.DONE)
            newFile.write(line)
            todoCompleted = True
        else:
            newFile.write(line)

        # increment the line counter
        lineCounter += 1

    newFile.close()
    if todoCompleted:
        print "Completed todo #%s" % id
    else:
        print "No todo #%s found." % id

def undoTodo(id):
    # oldFile = open(TODO_FILENAME, 'r')
    # lines = oldFile.readlines()
    # oldFile.close()
    # todoCompleted = False
    # newFile = open(TODO_FILENAME, 'w')
    # idFormmated = "[" + str(id) + "]"
    #
    # for line in lines:
    #     if idFormmated in line:
    #         line = line.replace(Status.DONE, Status.PENDING)
    #         newFile.write(line)
    #         todoCompleted = True
    #     else:
    #         newFile.write(line)
    #
    # newFile.close()
    # if todoCompleted:
    #     print "Undid todo #" + id + " now its pending again..."
    # else:
    #     print "No todo #" + id + " found."

    id = int(id)
    lines, linecount = readlines()
    todoCompleted = False
    newFile = open(TODO_FILENAME, 'w')
    lineCounter = 1

    for line in lines:
        # Write all the lines back to the file except the line number of id
        if lineCounter == id:
            line = line.replace(Status.DONE, Status.PENDING)
            newFile.write(line)
            todoCompleted = True
        else:
            newFile.write(line)

        # increment the line counter
        lineCounter += 1

    newFile.close()
    if todoCompleted:
        print "Undid todo #%s" % id
    else:
        print "No todo #%s found." % id

def showTodos():
    lineCounter = 1
    try:
        lines, linecount = readlines()
        for line in lines:
            # if Status.PENDING in line:
            #     line = line.replace(Status.PENDING, bcolors.FAIL + Status.PENDING + bcolors.ENDC)
            # elif Status.DONE in line:
            #     line = line.replace(Status.DONE, bcolors.OKGREEN + Status.DONE + bcolors.ENDC)
            # sys.stdout.write(line)

            # Auto assign the todo ID based on the the line its on in the todo.list file
            line = line.replace("%id", str(lineCounter))
            if Status.PENDING in line:
                line = line.replace(Status.PENDING, bcolors.FAIL + Status.PENDING + bcolors.ENDC)
            elif Status.DONE in line:
                line = line.replace(Status.DONE, bcolors.OKGREEN + Status.DONE + bcolors.ENDC)

            sys.stdout.write(line)
            lineCounter += 1


    except IOError:
        print "No todos created for this directory yet"


########################################################################
# Parse command line arguments
########################################################################

if len(sys.argv) == 1:
    showTodos()

elif sys.argv[1] == "new":
    content = " ".join(sys.argv[2:])
    newTodo(content)

elif sys.argv[1] == "complete" or sys.argv[1] == "done":
    completeTodo(sys.argv[2])

elif sys.argv[1] == "undo":
    undoTodo(sys.argv[2])

elif sys.argv[1] == "remove" or sys.argv[1] == "delete" or sys.argv[1] == "del" or sys.argv[1] == "rm":
    if len(sys.argv) < 3:
        print "You must specify a todo ID to remove."
    else:
        removeTodo(sys.argv[2])

elif sys.argv[1] == "show" or sys.argv[1] == "list":
    showTodos()

elif sys.argv[1] == "help":
    usage()

elif sys.argv[1] == "purge":
    ans = raw_input("Are you sure you want to delete and remove all traces of todos? (y/n): ")
    if ans == 'y':
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
