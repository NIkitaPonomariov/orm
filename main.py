from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Створюємо двигун і базовий клас
engine = create_engine('sqlite:///university.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Модель для груп
class Group(Base):
    __tablename__ = 'groups'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Відношення до студентів
    students = relationship('Student', back_populates='group')

    def __repr__(self):
        return f"<Group(name={self.name})>"

# Модель для студентів
class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))  # Зовнішній ключ до таблиці груп
    
    # Відношення до групи
    group = relationship('Group', back_populates='students')
    # Відношення до оцінок
    grades = relationship('Grade', back_populates='student')

    def __repr__(self):
        return f"<Student(name={self.name}, group_id={self.group_id})>"

# Модель для викладачів
class Teacher(Base):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    # Відношення до предметів
    subjects = relationship('Subject', back_populates='teacher')

    def __repr__(self):
        return f"<Teacher(name={self.name})>"

# Модель для предметів
class Subject(Base):
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))  # Зовнішній ключ до викладачів
    
    # Відношення до викладача
    teacher = relationship('Teacher', back_populates='subjects')
    # Відношення до оцінок
    grades = relationship('Grade', back_populates='subject')

    def __repr__(self):
        return f"<Subject(name={self.name}, teacher_id={self.teacher_id})>"

# Модель для оцінок
class Grade(Base):
    __tablename__ = 'grades'
    
    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)  # Оцінка
    date_received = Column(DateTime, default=datetime.utcnow)  # Дата отримання оцінки
    student_id = Column(Integer, ForeignKey('students.id'))  # Зовнішній ключ до студентів
    subject_id = Column(Integer, ForeignKey('subjects.id'))  # Зовнішній ключ до предметів

    # Відношення до студентів
    student = relationship('Student', back_populates='grades')
    # Відношення до предметів
    subject = relationship('Subject', back_populates='grades')

    def __repr__(self):
        return f"<Grade(value={self.value}, date_received={self.date_received}, student_id={self.student_id}, subject_id={self.subject_id})>"

# Створення таблиць у базі даних
Base.metadata.create_all(engine)



# Створюємо викладачів
teacher1 = Teacher(name="Іван Петрович")
teacher2 = Teacher(name="Ольга Михайлівна")

# Створюємо предмети
subject1 = Subject(name="Математика", teacher=teacher1)
subject2 = Subject(name="Фізика", teacher=teacher2)

# Створюємо групу
group1 = Group(name="Група A")

# Створюємо студентів
student1 = Student(name="Андрій Іванов", group=group1)
student2 = Student(name="Марія Петрівна", group=group1)

# Додаємо оцінки студентам
grade1 = Grade(value=85, student=student1, subject=subject1)
grade2 = Grade(value=90, student=student2, subject=subject2)

# Додаємо дані в сесію і зберігаємо в базі
session.add_all([teacher1, teacher2, subject1, subject2, group1, student1, student2, grade1, grade2])
session.commit()
