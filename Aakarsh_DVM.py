"""
    - **Course**: A course class will hold basic information about a course, the examination dates etc.
    - You should have the following methods:
        - one to get all the lecture/tutorial/lab sections available
        - one to print out basic information about the subject
        - one method to populate new sections of the course (this is a method which would have to have restricted access, duh!, have a separate way to access this)
"""

import csv
from enum import Enum

class Course_Components(Enum):
    LEC         = 0
    LECTUT      = 1
    LECLAB      = 2
    LECLABTUT   = 3

class Course:

    def __init__(self, course_code, course_name, credits, course_ic, course_comp, exam_dates=[]):
        self.course_code = course_code
        self.course_name = course_name
        self.exam_dates = exam_dates
        self.course_ic = course_ic
        self.credits = credits
        self.sections = set()
        self.complete = False

        if not isinstance(course_comp, Course_Components):
            raise ValueError("course_comp must be a member of Course_Components enum")
        self.course_comp = course_comp 

    def get_all_sections(self):
        return self.sections

    def __str__(self):
        """Print basic information about the course."""
        print(f"Course Code: {self.course_code}")
        print(f"Course Name: {self.course_name}")
        print(f"Exam Dates: {', '.join(self.exam_dates)}")
        print(f"Course IC: {self.course_ic}")
        print(f"Credits: {self.credits}")
        print("Sections:")
        for section in self.sections:
            print(section)

    def __populate_sections(self, section):
        # self.sections.append(section)
        pass

    def pop_section_getter(self, section):
        self.__populate_sections(section)


"""
    - **Sections**: This is a class that stores information about a section, you are free about how to implement the different types of sections (lecture, lab,tutorial) [ps. look into class inheritance, not necessary to use though]
    - The main thing this should store is which slot(s) of which day of the week this section occupies, this will be used to check for clashes between different sections. [**HINT**: you may use a dictionary for this purpose]
    - This **MUST** be linked to the corresponding course
"""

class Section:
    def __init__(self, section_id, section_type, day_and_slots, course):
        self.section_id = section_id
        self.section_type = section_type
        self.day_and_slots = day_and_slots
        self.course = course
        course.pop_section_getter(self)

    def __str__(self):
        return f"Section {self.section_id} ({self.section_type}) - {', '.join(self.day_and_slots)}"

class LectureSection(Section):
    def __init__(self, section_id,  day_and_slots, course):
        super().__init__(section_id, "Lecture", day_and_slots, course)


class LabSection(Section):
    def __init__(self, section_id, day_and_slots, course):
        super().__init__(section_id, "Lab", day_and_slots, course)


class TutorialSection(Section):
    def __init__(self, section_id, day_and_slots, course):
        super().__init__(section_id, "Tutorial", day_and_slots, course)


"""
    - **Timetable**: A timetable class that stores instances of the Course class and also other related information and required methods
    - The basic features that you need to have are enrolling subjects to your timetable, checking for the clashes (both examination clashes and also lecture section classes) and exporting to a csv file. (CSV file, excel won't work),
"""

class Timetable:
    def __init__(self):
        self.courses = []

    def enroll_subject(self, course):
        self.courses.append(course)

    def check_clashes(self):
        """Check for clashes in both examination dates and lecture section classes."""
        exam_dates = set()
        section_schedule = {}

        for course in self.courses:
            # Check for examination date clashes
            for exam_date in course.exam_dates:
                if exam_date in exam_dates:
                    print(f"Exam date clash for course {course.course_code} on {exam_date}")

                exam_dates.add(exam_date)

            # Check for section schedule clashes
            for section in course.sections:
                for day_and_slot in section.day_and_slots:
                    if day_and_slot in section_schedule:
                        print(f"Class schedule clash for section {section.section_id} ({course.course_code}) on {day_and_slot}")

                    section_schedule[day_and_slot] = section

    def export_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Course Code', 'Course Name', 'Exam Dates', 'Section ID', 'Section Type', 'Day and Slot']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for course in self.courses:
                for section in course.sections:
                    for exam_date in course.exam_dates:
                        writer.writerow({
                            'Course Code': course.course_code,
                            'Course Name': course.course_name,
                            'Exam Dates': exam_date,
                            'Section ID': section.section_id,
                            'Section Type': section.section_type,
                            'Day and Slot': ', '.join(section.day_and_slots)
                        })
