About
===
Git [web-hook](https://help.github.com/articles/post-receive-hooks) receiver written in python.
Created for prevent a routine work, such as working with database, static files, etc., after pushing changes to repo.

System requirements
===
* python>=2.6(Tested on 2.7)
* OS: Linux(tested on Ubuntu), *BSD(Not tested), Windows(But have small bugs) or otherwise where can be launched python

Installation
===
```bash
git clone git://github.com/sashasimkin/hook-receiver.git
cd hook-receiver/
./build.sh
```
This creates virtualenv under `.env/` directory in `hook-receiver/` and install there requirements for project.

Usage
===
* See the `config` section in this file and `config/sample.py`
* run server `python app.py` or use builtin `wsgi.py` as wsgi handler for your front server
* Use `http://IP:5000/{config_name}`(or else you configured) as hook url in github, gitlab, etc.

Config
===
Single config is a python module, which must be placed in `config` package and contains variables below.

* `PATH` - Root path for project, shell commands has been executed here
* `COMMANDS` - Array of shell commands, which will be performed after receive hook. Default: `COMMANDS = []`
* `REFS` - List of patterns payload.ref to match for perform actions, otherwise - nothing happens. Default `REFS = ['.*']`

Also available some hooks (Too must be placed in module as functions or other callable):

* `ref_not_fit` - This calls when ref from REFS does not fit to payload[refs]
* `on_command` - Called before any command from `COMMANDS` will be executed
* `on_error` - Called when any Exception raise
