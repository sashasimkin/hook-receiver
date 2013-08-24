About
===
Git [web-hook](https://help.github.com/articles/post-receive-hooks) receiver written in python.
Created for prevent a routine work, such as working with database, static files, etc., after pushing changes to repo.

System requirements
===
* python>=2.6(Tested on 2.7)
* OS: Linux(tested on Ubuntu), *BSD(Not tested), Windows(But have small bugs) or otherwise where can be runned python

Instalation
===
```bash
git clone git://github.com/sashasimkin/hook-receiver.py.git
cd hook-reciever.py/
./build.sh
```

Usage
===
* See the `config` section in this file and `config/samle.py`
* run server `python app.py` or use builtin `wsgi.py` as wsgi handler for your front server
* Use `http://IP:5000/{cofig_name}`(or else you configured) as hook url in github, gitlab, etc.

Config
===
Single config is a python module, which must be placed in `config` package and contains variables below.

* `PATH` - Root path for project, shell commands has been executed here
* `COMMANDS` - Array of shell commands, which will be performed after recieve hook. Default: `COMMANDS = []`
* `REFS` - List of patterns payload.ref to match for repform actions, otherwise - nothing hapens. Default `REFS = ['.*']`

TODO
===
* Pre-processing for COMMANDS
