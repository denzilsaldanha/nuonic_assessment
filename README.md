# Nuonic Python Assessment 

Welcome to the python assessment for nuonic.


## Installation Instructions
In order to run this assessment execute the following program in the terminal

To create a virtual environment 
```python3 -m venv venv```

To activate the virtual environment

```source venv/bin/activate```

To install the requirements

```pip install -r requirements.txt```

To run uvicorn
```uvicorn main:app --reload --port 8001```

In order to navigate to the documentation go to: 
http://127.0.0.1:8001/docs#/

## Steps to use the API. 

You can use the swagger document to easily interact with the API.

It would be easier to first create (POST) a Student followed by a Subject and the enrollment.

## References for the assessment. 

The assessment used vanilla FastAPI and SQLAlchemy. 
I only referred to the docs as well as FastAPIs getting started page.

## Reflection

It was a fun exercise to try to build an API in a timed environment. I approached it by designing the api first 
followed by the database, this really saved me a lot of time.

## Timing for the assessment

The test took 1 hour and 15 mins. 
The solution took a couple of mins extra to segregate it into various files to make it readable and test the entire solution.
I then spent 15 mins writing this documentation.