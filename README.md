todo
====

An intuitive, uber-simple, directory based todo list manager for programmers.
Work with a team? `todod` Server coming soon!

Rationale
====
When I work on multiple projects and switch between them sometimes I forget
where I left off. When I come back to a project, I always have to find
figure out what I was doing the last time I was working on it.

With todo, it couldn't be easier create a quick todo in your current working directory.
Never again forget where you left off, and keep track up bugs and enchanvements for your
basement code.

Installation
=====
1. Clone the repo
2. Add a symbolic link todo the `todo.py` (whereever you placed it)

Usage
=====
```
Usage:
	todo                                    | List the todos for the current directory
	todo show|list                          | Same as 'todo'
	todo new <new todo>                     | Create a new todo
	todo complete|done <todo-id>            | Mark a todo as complete
	todo remove|rm|delete|del <todo-id>     | Remove a todo
	todo undo                               | Undo a 'DONE' todo. Make it pending again.
	todo purge|reset                        | Delete all todos and todo savedata for the cwd
	todo help                               | Show this help
	todo pop                                | Remove the LAST todo from the list
```

Troubleshooting
=====
1. Cannot run the todo.py program: `chmod +x todo.py`
2. Bad interpreter: Change the deafult `#!/usr/local/bin/python` your python executable
3. Operation problem: if you think its a bug, submit an issue on github and I will fix asap.
