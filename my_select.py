from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from seed import Base, Student, Group, Subject, Teacher, Grade

# Налаштування бази даних
DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    result = session.query(
        Student.id,
        Student.name,
        func.avg(Grade.grade).label('average_grade')
    ).join(Grade).group_by(Student.id).order_by(func.avg(Grade.grade).desc()).limit(5).all()
    return result

def select_2(subject_id):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    result = session.query(
        Student.id,
        Student.name,
        func.avg(Grade.grade).label('average_grade')
    ).join(Grade).filter(Grade.subject_id == subject_id).group_by(Student.id).order_by(func.avg(Grade.grade).desc()).first()
    return result

def select_3(subject_id):
    """Знайти середній бал у групах з певного предмета."""
    result = session.query(
        Group.id,
        Group.name,
        func.avg(Grade.grade).label('average_grade')
    ).join(Student).join(Grade).filter(Grade.subject_id == subject_id).group_by(Group.id).all()
    return result

def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    result = session.query(func.avg(Grade.grade)).scalar()
    return result

def select_5(teacher_id):
    """Знайти які курси читає певний викладач."""
    result = session.query(Subject).join(Grade).filter(Grade.teacher_id == teacher_id).distinct().all()
    return result

def select_6(group_id):
    """Знайти список студентів у певній групі."""
    result = session.query(Student).filter(Student.group_id == group_id).all()
    return result

def select_7(group_id, subject_id):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    result = session.query(
        Student.name,
        Grade.grade
    ).join(Group).filter(Student.group_id == group_id, Grade.subject_id == subject_id).all()
    return result

def select_8(teacher_id):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    result = session.query(
        func.avg(Grade.grade)
    ).filter(Grade.teacher_id == teacher_id).scalar()
    return result

def select_9(student_id):
    """Знайти список курсів, які відвідує певний студент."""
    result = session.query(Subject).join(Grade).filter(Grade.student_id == student_id).distinct().all()
    return result

def select_10(student_id, teacher_id):
    """Список курсів, які певному студенту читає певний викладач."""
    result = session.query(Subject).join(Grade).filter(
        Grade.student_id == student_id,
        Grade.teacher_id == teacher_id
    ).distinct().all()  
    return result

if __name__ == "__main__":
    # Тестування функцій
    print("5 студентів із найбільшим середнім балом:", select_1())
    print("Студент із найвищим середнім балом з предмета 1:", select_2(1))
    print("Середній бал у групах з предмета 1:", select_3(1))
    print("Середній бал на потоці:", select_4())
    print("Курси, які читає викладач 1:", select_5(1))
    print("Список студентів у групі 1:", select_6(1))
    print("Оцінки студентів у групі 1 з предмета 1:", select_7(1, 1))
    print("Середній бал, який ставить викладач 1:", select_8(1))
    print("Список курсів, які відвідує студент 1:", select_9(1))
    print("Курси, які студенту 1 читає викладач 1:", select_10(1, 1))
