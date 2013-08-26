#!/usr/bin/env python
import os
import re
import json
from subprocess import Popen, PIPE
from flask import Flask, request

import utils

PATH = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


@app.route('/')
def index():
    return "This is something, that you shouldn't know."


@app.route('/<cfg_name>', methods=['POST'])
def receive(cfg_name):
    # Init loggers
    error_logger = utils.spawn_logger(cfg_name, 'error')
    info_logger = utils.spawn_logger(cfg_name, 'info')

    # Dictionary from request.data, from json to native
    payload = json.loads(request.data)

    # For cases when exception raised before on_error defined from `config`
    on_error = lambda *args: None
    try:
        cfg = getattr(__import__('config.%s' % cfg_name, globals(), locals(), level=-1), cfg_name)
        # Hooks
        ref_not_fit = getattr(cfg, 'ref_not_fit', lambda *args: None)
        on_command = getattr(cfg, 'on_command', lambda *args: None)
        on_error = getattr(cfg, 'on_error', lambda *args: None)
        # Config variables
        path = utils.get_variable(cfg,
                                  'PATH',
                                  '',
                                  lambda p: not p or not os.path.exists(p),
                                  'PATH does not exists')
        refs = utils.get_variable(cfg,
                                  'REFS',
                                  [r'.*'],
                                  lambda r: not isinstance(r, list),
                                  'REFS must be a list')
        commands = utils.get_variable(cfg,
                                      'COMMANDS',
                                      [],
                                      lambda c: not isinstance(c, list),
                                      'Define COMMANDS variable, else nothing happens')

        for ref in refs:
            refExpr = re.compile(ref, re.IGNORECASE)
            if refExpr.match(payload['ref']) is None:
                # Log message about ref does not feet and exit
                ref_not_fit(ref, payload)
                info_logger.info('Ref does not fit')
                return ''

        for command in commands:
            # Variables from payload, access as repository[name]
            command.format(**payload)

            on_command(command, payload)
            # Execute current command and log out and errors
            out, err = Popen(command,
                             shell=True,
                             cwd=os.path.join(PATH, cfg.PATH),
                             # close_fds=True,
                             stdout=PIPE,
                             stderr=PIPE).communicate()
            if out:
                try:
                    info_logger.info(out.encode('utf8'))
                except UnicodeDecodeError:
                    pass
            if err:
                try:
                    error_logger.error(err.encode('utf8'))
                except UnicodeDecodeError:
                    pass

    except Exception, e:
        on_error(e, payload)
        error_logger.error(str(e))

    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)