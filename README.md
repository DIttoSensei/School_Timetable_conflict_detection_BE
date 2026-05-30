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