import json
import logging
from libs import lib
from timeit import default_timer as timer
from datetime import timedelta

LOG = logging.getLogger(__name__)


class SequenceDefinition(object):
    def __init__(self, name):
        self.name = name
        self.finalization = True

    def add_step(self, function, name=None, condition="True", **kwargs):
        if not self.finalization:
            return False
        try:
            userdict = lib.apdicts.userdict
            start = timer()
            if not eval(condition):
                return True
            f_name = name if name else function.__name__
            LOG.info(f'---> Starting Step "{f_name}" ({function.__module__}.{function.__name__})')
            result = function(**kwargs['kwargs']) if kwargs else function()
            if 'PASS' == result:
                LOG.info(f'Sequence={self.name}, Step={f_name}, result=PASS, '
                         f'runtime= {str(timedelta(seconds=timer()-start))[:-3]}')
                return True
            elif result:
                LOG.error(result)
                print(json.dumps({'status': 'FAIL', 'error_message': result}))
                self.finalization = False
                return False
            LOG.error('Missing return statement. Please return PASS or message(string)')
        except Exception as err:
            LOG.error(err, exc_info=True)
        self.finalization = False
        print(json.dumps({'status': 'FAIL',
                          'error_message': 'Script Run Error:\n Please Inform Developer For Fix Issue.'}))
        return False
