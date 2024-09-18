from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from seed import Base, Student, Group, Subject, Teacher, Grade

# Налаштування бази даних
DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Створюємо екземпляр Faker
fake = Faker()

def create_groups():
    groups = [Group(name=fake.word()) for _ in range(3)]
    session.add_all(groups)
    session.commit()
    return groups

def create_teachers():
    teachers = [Teacher(name=fake.name()) for _ in range(5)]
    session.add_all(teachers)
    session.commit()
    return teachers

def create_subjects():
    subjects = [Subject(name=fake.word()) for _ in range(8)]
    session.add_all(subjects)
    session.commit()
    return subjects

def create_students(groups):
    students = []
    for _ in range(30):
        student = Student(
            name=fake.name(),
            group_id=fake.random_element(elements=groups).id
        )
        session.add(student)
        students.append(student)
    session.commit()
    return students

def create_grades(students, subjects, teachers):
    for student in students:
        for _ in range(20):
            grade = Grade(
                student_id=student.id,
                subject_id=fake.random_element(elements=subjects).id,
                teacher_id=fake.random_element(elements=teachers).id,
                grade=fake.random_int(min=1, max=12)  # Припустимо, що оцінки від 1 до 12
            )
            session.add(grade)
    session.commit()

def seed_database():
    # Створюємо всі необхідні таблиці
    Base.metadata.create_all(engine)

    # Додаємо дані
    groups = create_groups()
    teachers = create_teachers()
    subjects = create_subjects()
    students = create_students(groups)
    create_grades(students, subjects, teachers)

if __name__ == "__main__":
    seed_database()
