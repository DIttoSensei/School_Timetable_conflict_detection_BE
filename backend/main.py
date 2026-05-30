from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import random


app = FastAPI()
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CourseItemDB(Base):
    __tablename__ = "COURSEITEM"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    course_code = Column(String, unique=True, index=True)
    lecturer_name = Column(String)
    day_of_the_week = Column(String)
    time_start = Column(String)
    time_end = Column(String)


class CourseItems(BaseModel):
    id : int
    name: str
    description: str | None = None
    course_code: str
    lecturer_name : str
    day_of_the_week: str
    time_start: str
    time_end: str

    class Config:
        from_attributes = True


NAMES = ['Mr Andrew', 'Mrs Bukola', 'Mr Taiwo', 'Mr Grayson', 'Mrs Jade', 'Mr Olubiyi', 'Mr Adisa', 'Mr Richard', 'Mrs Oyewale', 'Mr Adekunle']
COURSES = ['Data Structure', 'Artificial Intelligence', 'Compiler Construction', 'Computer Simulations', 'IT Hardware', 'Computer Center Management',
           'System Analysis', 'Digital Computer Logic Design', 'Computer Hardware', 'Computer Operating Systems', 'Experts Systems', 'Database Management',
           'Game Development', 'Data and Object Structuring']
TIME_SLOTS = [
    ('7:00', '8:30'),
    ('8:30', '10:00'),
    ('10:00', '11:30'),
    ('11:30', '1:00'),
    ('1:00', '2:30'),
    ('2:30', '4:00')        
              ]


@app.put("/generate/", response_model=list[CourseItems])
async def generate_timetable(db: Session = Depends(get_db)):
    all_courses = db.query(CourseItemDB).all()
    number_of_course_to_edit = random.randint(3,9)
    random_selected = random.sample(all_courses, number_of_course_to_edit)
    for course in random_selected:
        random_time = random.choice(TIME_SLOTS)
        course.lecturer_name = random.choice(NAMES)
        course.name = random.choice(COURSES)
        course.time_start = random_time[0]
        course.time_end = random_time[1]
    db.commit()
    return random_selected



@app.get("/courses/", response_model=list[CourseItems])
async def get_all_course(db: Session = Depends(get_db)):
    course = db.query(CourseItemDB).all()
    return course


@app.get("/courses/{day_of_the_week}", response_model= list[CourseItems])
async def get_specific_day_course(day_of_the_week : str, db: Session = Depends(get_db)):
    monday_course = db.query(CourseItemDB).filter(CourseItemDB.day_of_the_week == day_of_the_week).all()
    if monday_course is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return monday_course



def time_to_min (time_str : str) -> int:
    hr_str, min_str = time_str.split(":")
    total_min = (int(hr_str) * 60) + int(min_str)
    return total_min


@app.put("/resolve/", response_model=list[CourseItems])
async def fix_all_course_time(db: Session = Depends(get_db)):
    DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    for day in DAYS_OF_WEEK:
        daily_course = db.query(CourseItemDB).filter(CourseItemDB.day_of_the_week == day).all()
        time_track = []
        for course in daily_course:
            start_min = time_to_min(course.time_start)
            end_min = time_to_min(course.time_end)
            time_track.append((course.id, start_min, end_min))

        for i in time_track:
            id_i, start_i, end_i = i

            for j in time_track:
                id_j, start_j, end_j = j

                if id_i == id_j:
                    continue
          
                if start_i < end_j and end_i > start_j:
                    for potential_slot in TIME_SLOTS:
                        pot_start = time_to_min(potential_slot[0])
                        pot_end = time_to_min(potential_slot[1])
                        slot_is_busy = False

                        for track in time_track:
                            t_id, t_start, t_end = track
                            if pot_start < t_end and pot_end > t_start:
                                slot_is_busy = True
                                break


                        if not slot_is_busy:
                            for course in daily_course:
                                if course.id == id_j:
                                    course.time_end = potential_slot[1]
                                    course.time_start = potential_slot[0]
                                    break
                        
                            time_track.remove(j)
                            time_track.append((id_j, pot_start, pot_end))
                            break
                    break
    db.commit()
    return db.query(CourseItemDB).all()