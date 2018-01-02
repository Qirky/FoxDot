""" Utilities related to logging """
import inspect
import functools
import logging
import time


def enablePerfLogging():
    """ This is just a small convenience method """
    logging.getLogger('FoxDot.perf').setLevel(logging.DEBUG)


class Timing(object):
    """
    Utility for profiling events

    :param str event: Unique identifier for the perf event
    :param str logger: Logger path (default 'FoxDot.perf')
    :param bool logargs: If true when used as a decorator, log the arguments to
        the decorated function

    This can be used in multiple ways. As a decorator::

        @Timing('fibonacci')
        def fib(num):
            ...

    As a context manager::

        with Timing('pi'):
            # calculate pi...

    Or directly as an object::

        timer = Timing('crank')
        # do crank
        timer.finish()

    Note that it will log the perf data to the specified logger (FoxDot.perf by
    default) at the DEBUG level. That means that in order for the information
    to be visible, you will need to configure either that logger or a parent
    logger to use the DEBUG level. For example::

        # Set root logger to DEBUG
        logging.root.setLevel(logging.DEBUG)
        # Set just the perf logger to DEBUG
        logging.getLogger('FoxDot.perf').setLevel(logging.DEBUG)

    """

    def __init__(self, event, logger='FoxDot.perf', logargs=False):
        self._event = event
        self._logger = logger
        self._log = logging.getLogger(logger)
        self._messages = []
        self._start = None
        self._logargs = logargs

    def __str__(self):
        return "Timing(%s)" % self._event

    def addMessage(self, message):
        self._messages.append(message)

    def start(self):
        if self._start is not None:
            self._log.warn("Entering %s twice!", self)
        self._start = time.time()

    def finish(self):
        if self._start is None:
            self._log.warn("Finishing %s before start!", self)
            return
        diff = 1000 * (time.time() - self._start)
        formatted_messages = ''
        if self._messages:
            formatted_messages = ', '.join(self._messages) + ': '
        self._log.debug("%s: %s%.02fms", self._event, formatted_messages, diff)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.finish()

    def __call__(self, fxn):
        @functools.wraps(fxn)
        def wrapper(*args, **kwargs):
            with Timing(self._event, self._logger) as timer:
                if self._logargs:
                    if args:
                        timer.addMessage("args:%s" % list(args))
                    if kwargs:
                        timer.addMessage("kwargs:%s" % kwargs)
                return fxn(*args, **kwargs)
        return wrapper
