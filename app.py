import os
import re
import json
import logging
import logging.handlers
from subprocess import Popen, PIPE
from flask import Flask, request
app = Flask(__name__)

PATH = os.path.abspath(os.path.dirname(__file__))
LOG_PATH = os.path.join(PATH, 'logs')


@app.route('/')
def index():
    return "This is something, that you shouldn't know."


@app.route('/<cfg_name>', methods=['POST'])
def receive(cfg_name):
    def spawn_logger(cfg, logger_name):
        """
        Get logger instance for config_name and logger name
        :param cfg:
        :param logger_name:
        :return:
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        
        handler = logging.handlers.RotatingFileHandler(
            os.path.join(LOG_PATH, '%s.%s.log' % (cfg, logger_name)),
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

        refs = getattr(cfg, 'REFS', [r'.*'])
        if not isinstance(refs, list):
            raise TypeError('REFS must be a list')

        for ref in refs:
            refExpr = re.compile(ref, re.IGNORECASE)
            if refExpr.match(data['ref']) is None:
                # Log message about ref does not feet and exit
                info_logger.info('Ref does not fit')
                return ''

        for command in getattr(cfg, 'COMMANDS', []):
            print 'will run: %s' % command
            pipe = Popen(command,
                         shell=True,
                         cwd=os.path.join(PATH, cfg.PATH),
                         # close_fds=True,
                         stdout=PIPE,
                         stderr=PIPE)
            out, err = pipe.communicate()
            if out:
                print 'get stdout', out.encode('utf8')
                info_logger.info(out.encode('utf8'))

            if err:
                print 'get stderr %s' % err.encode('utf8')
                error_logger.error(err.encode('utf8'))

    except Exception, e:
        error_logger.error(str(e))

    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)