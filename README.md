# SETTING UP THE BACKEND

## STEP ONE
Clone the backend repo to your root dir
```
git clone https://github.com/DIttoSensei/School_Timetable_conflict_detection_BE.git
```

## STEP TWO
- Create a virtual envirionment [venv]
```
python -m venv venv
```
- Activate environment
```
venv/Scripts/activate
```
- After creating, install required packages from requirements.txt
```
pip install -r requirements.txt
```

## STEP THREE
- To run the backend type:
```
fastapi dev
```
- Go to (http://127.0.0.1:8000/docs/) to view and test the endpoint along with documentation 
- Do note you need to set up an API_SECRET_KEY in main.py to access the endpoint securly, can be seen in line 13
- Proceed to connect the endpoint where needed in the frontend


## ENDPOINT FUNCTIONS
- /generate/ - Changes the content in the database eg, course name, time-start and time-end, lecturer name. Hence you get a unique set of data.
> This is a put request, it changes content within the database and return changes
- /courses/ - Returns all rows from the database, which include course name, time-start and time-end, lecturer name etc.
> This is a get request, it only retrives info from the database
- /courses/{day_of_the_week} - Returns rows from the database, which include course name, time-start and time-end, lecturer name etc of that specific day eg all courses for that day.
> This is a get request, it only retrives info from the database. Must pass the day of the week eg "/courses/Monday" day of the week should start with capital letters.
- /resolve/ - Looks at each day and finds courses-time that conflict with each other and fixes them. Does this for the whole timetable.
> This is a put request, it changes content within the database and return full updated rows

## NOTE
- /generate/ does return infomation but it dosen't return the entire row in the database hence use /courses/ to return full database info.
- /resolve/ however changes and return full database rows so no need to use /courses/.