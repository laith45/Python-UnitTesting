import subprocess
from unittest import TestCase
from school import Course, Student, Institution


class SchoolTest(TestCase):
    course_data = [
        ["COMP2001", "COMP", []],
        ["COMP2030", "COMP", ["COMP2001"]],
        ["COMP2040", "COMP", ["COMP2001", "COMP2030"]],
        ["COMP4000", "COMP", ["COMP2030"]],
        ["FORK4040", "FORK", []],
        ["ARTI4020", "ARTI", ["COMP4000", "COMP2030"]],
    ]

    student_data = [
        ['Fred Smith', 202219876, ["COMP2001", "COMP2040"]],
        ['Sally Jones', 202287652, []],
        ['Caesar Augustus', 202287655, ["ARTI4020", "FORK4040", "COMP4000"]],
        ['Wayburn Masso', 202289722, ["COMP2001"]],
        ['Masq Cano', 202134221, ["COMP2001"]],
        ['Noah Greenspan', 202098765, ["COMP2001"]],
        ['Mosha El Kabro', 202234218, ["COMP2001"]],
        ['Benji Takin', 202294384, ["COMP2001"]],
        ['Justin Case', 202287665, ["COMP2001"]],
        ['Al B Querque', 202276511, ["COMP2001"]],
        ['Charon St John', 202212322, ["COMP2001"]],
        ['Les Fletcher', 202254331, ["COMP2001"]]
    ]

    def setUp(self):
        self.institution = Institution("TestSchool")
        self.institution.clear()

        for row in self.course_data:
            c = Course(row[0], row[1])
            for p in row[2]:
                c.prerequisite(Course.find(p))

        for row in self.student_data:
            s = Student(row[0], row[1])
            for cname in row[2]:
                Course.find(cname).append(s)

    def tearDown(self):
        self.institution.deactivate()

    def test_institution(self):
        courses1 = Course.allCourses.copy()
        students1 = Student.registry.copy()
        self.institution.deactivate()
        new_institution = Institution("testInstitution2")
        self.assertFalse(Course.find(courses1[0]), "found course in wrong institution")
        self.assertEqual(None, Student.registry.get(next(iter(students1))), "found student in wrong institution")
        new_institution.clear()
        self.assertSequenceEqual([], Course.allCourses, "new institution should have no courses")
        self.assertDictEqual({}, Student.registry, "new institution should have no students")
        c = Course("FAKE3200", "FAKE")
        s = Student("Harry Kim")
        self.assertSequenceEqual([c], Course.allCourses)
        self.assertEqual(s, Student.registry[s.sid])
        new_institution.deactivate()
        self.institution.activate()
        self.test_student()

    def test_find(self):
        self.assertEqual(len(self.course_data), len(Course.allCourses))
        for row in self.course_data:
            c = Course.find(row[0])
            self.assertEqual(row[0], c.courseName)
            # check prerequisites
            pre_names = [p.courseName for p in c._prerequisites]
            for pname in row[2]:
                self.assertTrue(pname in pre_names)

    def test_persist_find(self):
        """test running in other environment"""
        self.institution.deactivate()  # close the shelf file
        sub_result = subprocess.run(["python3", "-m", "unittest", "-f", "test_school.TestPersist.persist_find"],
                                    capture_output=True)
        self.assertFalse(b"FAIL" in sub_result.stderr, "other process didn't find courses")
        self.institution.activate()

    def test_student_present(self):
        self.assertEqual(len(self.student_data), len(Student.registry))
        for row in self.student_data:
            s = Student.registry[(row[1])]
            for cname in row[2]:
                c = Course.find(cname)
                sfound = [c_member for c_member in c if c_member.sid == s.sid]
                self.assertEqual(1, len(sfound), "should be exactly one matching student in the course")
                self.assertEqual(s.sname, sfound[0].sname, "different student name under same id")

    def test_student(self):
        self.assertEqual(len(self.student_data), len(Student.registry))
        for row in self.student_data:
            s = Student.registry[(row[1])]
            for cname in row[2]:
                c = Course.find(cname)
                sfound = [c_member for c_member in c if c_member.sid == s.sid]
                self.assertEqual(1, len(sfound), "should be exactly one matching student in the course")
                self.assertEqual(s.sname, sfound[0].sname, "different student name under same id")
                self.assertEqual(s, sfound[0], "student object in course are copies not the same as registry objects")

    def test_reset_student(self):
        """close and reopen"""
        self.institution.deactivate()
        self.institution.activate()
        self.test_student()

    def test_persist_student(self):
        """test running in other environment"""
        self.institution.deactivate()  # close the shelf file
        sub_result = subprocess.run(["python3", "-m", "unittest", '-f', "test_school.TestPersist.persist_student"],
                                    capture_output=True)
        self.assertFalse(b"FAIL" in sub_result.stderr, "other process didn't find student")
        self.institution.activate()


class TestPersist(TestCase):
    """ tests to run in a different/separate process to test persistence across execution environments

        Make sure the tests are not discoverable because we only want them to run when
        explicitly invoked.
    """

    def setUp(self):
        self.institution = Institution("TestSchool")

    def tearDown(self):
        self.institution.deactivate()

    def persist_find(self):  # not DRY
        for row in SchoolTest.course_data:
            c = Course.find(row[0])
            self.assertEquals(row[0], c.courseName)
            # check prerequisites
            pre_names = [p.courseName for p in c._prerequisites]
            for pname in row[2]:
                self.assertTrue(pname in pre_names)

    def persist_student(self):  # not DRY
        for row in SchoolTest.student_data:
            s = Student.registry[(row[1])]
            for cname in row[2]:
                self.assertTrue(s in Course.find(cname), "student should be recorded in course")
