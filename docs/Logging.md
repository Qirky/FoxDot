# `Logging`

Utilities related to logging 

## Classes

### `Timing(self, event, logger=FoxDot.perf, logargs=False)`

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

#### Methods

---

## Functions

### `enablePerfLogging()`

This is just a small convenience method 

## Data

