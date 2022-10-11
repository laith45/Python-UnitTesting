#!/usr/bin/python3
"""
A simple teaching example of a module with a few classes.
Persistence for the data structures should be implemented using the shelve library
A Course object is a list of students, holding prerequisites and other information.
A Student object is a simple composition of student information.


Attributions

Enumerate additional attributions by adding items to this list:

1. Submitted by <your name here>, <date here>
2. Original problem sources by Prof. E. Brown, Oct, 2022

"""
import random
import datetime
import shelve


class Course(list):
    """A course is a list of students"""

    allCourses = []

    def __init__(self, cname, majProgram=None):
        """
        Provide a name for a course
        """
        self.courseName = cname
        self.major = majProgram
        self._prerequisites = []
        Course.allCourses.append(self)


    def prerequisite(self, preCourse):
        """
        Add to the list of prerequisites for this course object.
        """
        # Currently, this doesn't make much sense as it only
        # performs the list append operation. For future use when
        # prerequisite checks are added to the functionality.

        self._prerequisites.append(preCourse)
        return self._prerequisites

    def find(name):
        """Return the course object specified or return None"""

        for i in Course.allCourses:
            if i.courseName == name:
                return i

        return None

    def __str__(self):
        return self.courseName

class Institution:

    def __init__(self, name):
        self.instName = name

    def activate(self):

        if self.instName is None:

            d = shelve.open('newFile.txt','w')
            c = [Course.allcourses]
            r = [Student.registry]
            d.write(self.instName, "\n")
            d.sync()
            d.close()
        else:
            pass

    def clear(self):
        Course.allCourses.clear()
        Student.registry.clear()

    def deactivate(self):

        pass

class Student:
    """
    Information on individual students. Also maintains a dictionary of 
    all known students
    """

    registry = {}

    def __init__(self, sname, sid=None):
        self.sname = sname
        self.sid = sid
        if not self.sid: self._newid()
        self.registry[self.sid] = self

    def _newid(self):
        """
        Generate a new id for this student. Use
        the current year and five random digits
        """
        self.sid = str(datetime.date.today().year) \
                   + str(random.randint(1, 99999))  # can you spot the bug??
        return self.sid

    def __str__(self):
        return "[" + str(self.sid) + "]" + " " + self.sname

    # iterator method - go through courses and pick out those having
    # this student as a member
    def __iter__(self):
        # for clarity, using a different self variable rather 
        # than follow the convention 
        class StudentIter:
            def __init__(iself, theStudent):
                iself.courseIndex = 0
                iself.myStudent = theStudent

            def __next__(iself):  # next course I belong to.
                while iself.courseIndex < len(Course.allCourses):
                    nextCourse = Course.allCourses[iself.courseIndex]
                    iself.courseIndex += 1
                    if iself.myStudent in nextCourse:
                        return nextCourse
                raise StopIteration

        return StudentIter(self)

        # load and backup functions::

    defaultStorage = 'studentRegistry.store'
    logfile = open('registry.log', 'a')

    def backup(storefile=defaultStorage):
        """
        backup the student registry with a default file.
        This is written as a function rather than a method.  The 
        accepted way to create a static method is use a @staticmethod
        decorator, but as a teaching example, @staticmethod hasn't
        been introduced yet.
        """
        try:
            sfile = open(storefile, 'w');
            for key in Student.registry:
                assert key != None
                print(Student.registry[key], file=sfile)
        except:
            # we are using print for logging, as logging has 
            # not been covered yet.
            print('Error in storing registry', file=Student.logfile)
        else:
            sfile.close()

    def load(loadfile=defaultStorage):
        """
        load the student registry
        """
        Student.registry = {}
        try:
            for ln in open(loadfile, 'r'):
                (sid, sname) = ln.split()
                sid = sid[1:-1]  # strip leading and trailing
                if sid in Student.registry:
                    raise ValueError('Duplicate student id' + sid)
                if len(sid) != 9 or not sid.isdigit():
                    raise ValueError('Invalid student id ' + sid)
                Student(sname, sid)  # create the student

        except(OSError):
            print('Error in loading registry', file=Student.logfile)
            Student.registry = {}


def loaddemo():
    Student.load()
    print(str(len(Student.registry)) + " students loaded")

    # make up some courses for testing purposes
    Course("2005", "COMP")
    Course("3500", "ARTS")
    Course("1600", "MEDI")

    #  randomly add each student to some courses
    for s in Student.registry.values():
        for c in Course.allCourses:
            if random.random() > 0.5:
                c.append(s)

    # now test the student iterator
    for s in Student.registry.values():
        print(str(s) + " is doing these courses:")
        for c in s:  # testing the student iterator
            print("Course: ", str(c))


def command_loop():
    def command_c():
        """Find a course"""
        name = input("What is the course name? ")
        c = Course.find(name)
        print(c if c is not None else "No such course")

    def command_o():
        """offer new course"""
        name = input("What is the course name? ")
        maj = input("What is the course major program? ")
        if Course.find(name):
            print("That course name is taken")
            return
        c = Course(name, maj)
        while inP := input("Name a prerequisite or blank to complete: "):
            p = Course.find(inP)
            if p is None:
                print("No such prerequisite. Course offering complete.")
                return
            c.prerequisite(p)

    def command_s():
        """Find a student and sign up for courses"""
        s = Student.registry.get(input("What is the student id? "))
        if s is None:
            print("No such student")
            return
        print(s)
        c = Course.find(input("What course did the student want to take? "))
        if c is None:
            print("No such course")
            return
        if s in c:
            print(f"{s} is already subscribed to (c)")
            return
        c.append(s)

    def command_r():
        """Register new student"""
        name = input("What is the student name? ")
        s = Student(name)
        print(s)

    def command_p():
        """Print all information"""
        print("Courses")
        for c in Course.allCourses: print(c)
        print("Student Registry")
        for s in Student.registry.values(): print(s)

    def command_q():
        """Exit program"""
        print("Quitting program")
        exit()

    def usage():
        """Description of commands"""
        print("Choices are:")
        for (k, func) in commands.items():
            print(f'{k}: {func.__doc__}')

    commands = {
        'c': command_c,
        's': command_s,
        'o': command_o,
        'r': command_r,
        'p': command_p,
        'q': command_q,
        '0': usage,
    }

    com_list = list(commands.keys())
    query_string = f"Choose: {','.join(com_list[:-1])} or {com_list[-1]} ? "
    while True:
        in_command = input(query_string)
        com_func = commands.get(in_command) or usage
        com_func()


if __name__ == "__main__":
    command_loop()
