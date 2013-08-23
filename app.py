import os
import re
import json
import logging
from subprocess import Popen, PIPE
from flask import Flask, request

PATH = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


@app.route('/')
def index():
    return "This is something, that you shouldn't know."


@app.route('/<cfg_name>', methods=['POST'])
def receive(cfg_name):
    def spawn_logger(cfg, logger_name):
        """
        Get logger instance for config_name and logger name
        :param cfg: Current config name
        :param logger_name: Logger name, now error and info
        :return:
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        handler = logging.handlers.RotatingFileHandler(
            os.path.join(PATH, 'logs/%s.%s.log' % (cfg, logger_name)),
            backupCount=5
        )
        handler.setFormatter(logging.Formatter(u'[%(asctime)s]  %(message)s'))
        logger.addHandler(handler)

        return logger

    # Init loggers
    error_logger = spawn_logger(cfg_name, 'error')
    info_logger = spawn_logger(cfg_name, 'info')

    # Dictionary from request.data
    data = json.loads(request.data)

    try:
        cfg = getattr(__import__('config.%s' % cfg_name, globals(), locals(), level=-1), cfg_name)

        def get_variable(name, default, condition, fail_message):
            v = getattr(cfg, name, default)
            if condition(v):
                raise RuntimeError(fail_message)

        path = get_variable('PATH',
                            '',
                            lambda p: not p or not os.path.exists(p),
                            'PATH does not exists')
        refs = get_variable('REFS',
                            [r'.*'],
                            lambda r: not isinstance(r, list),
                            'REFS must be a list')
        commands = get_variable('COMMANDS',
                                [],
                                lambda c: not isinstance(c, list),
                                'Define COMMANDS variable, else nothing happens')

        for ref in refs:
            refExpr = re.compile(ref, re.IGNORECASE)
            if refExpr.match(data['ref']) is None:
                # Log message about ref does not feet and exit
                info_logger.info('Ref does not fit')
                return ''

        for command in commands:
            # Execute current command and log out and errors
            out, err = Popen(command,
                             shell=True,
                             cwd=os.path.join(PATH, cfg.PATH),
                             # close_fds=True,
                             stdout=PIPE,
                             stderr=PIPE).communicate()
            if out:
                info_logger.info(out.encode('utf8'))
            if err:
                error_logger.error(err.encode('utf8'))

    except Exception, e:
        error_logger.error(str(e))

    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)