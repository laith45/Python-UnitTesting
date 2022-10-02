## Assignment 3, CS2005 F2022

## Instructions

Modify the code for the <code>schoolProblem.py</code> module to pass the unittests in the <code>test_school.py</code> file.  The pydoc provided explains the code structures needed for the tests to run.
Additional tests will be run by the evaluator. 

Push your solution to your assigned github repository prior to the due date. 

Here's what you do to complete assignment 3:

* Correct the Course.find() method and the interactive command loop should work when running the module as a python program from a command prompt. This is the only fix you should need to get the command loop working.
  * There are no unit tests on the command loop, but it might help you try out your program.
* Remove the old load/backup methods and make registry and courses persist between executions of the program
    * using the python shelve library (https://docs.python.org/3/library/shelve.html)
* implement the Institution class so each institution will have its own courses list, student registry and persistent storage.
    * persistence should work without an explicit call: as soon as an Institution is initialized
    * you may require the `Institution` to `deactivated` before the program terminates to persist its student and course records.
* put your solution code in a file `school.py` so the tests can import it
* To remove the pylint warning about missing self parameter on class methods you will have to use the @classmethod decorator - although we haven't yet discussed decorators - it should be easy with the pycharm editor fixes.

## Evaluation:
* 15 points total
* One point for each of 15 tests passed.
* Seven tests are provided, the rest are held back.
* Each different pylint warning may lose one point except R(refactor) warnings. Refactor warnings will not be penalized. 