## University Website

* Corrected the Course.find() method, the interactive command loop should work when running the module as a python program from a command prompt.
  * There are no unit tests on the command loop.
  * old load/backup methods are reloaded, made registry and courses persist between executions of the program
    * using the python shelve library (https://docs.python.org/3/library/shelve.html)
* implemented the Institution class so each institution will have its own courses list, student registry and persistent storage.
    * persistence should work without an explicit call: as soon as an Institution is initialized
    * you may require the `Institution` to `deactivated` before the program terminates to persist its student and course records.


* To remove the pylint warning about missing self parameter on class methods you will have to use the @classmethod decorator - although we haven't yet discussed decorators - it should be easy with the pycharm editor fixes.
