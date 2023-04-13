# pc_dj
Django server for the Pathology Classification Project

There are three separate components for this project:
1. ML Model: https://github.com/VSTARprojects/pc_ml
2. FrontEnd: https://github.com/VSTARprojects/pc_fe
3. BackEnd: https://github.com/khssupriya/pc_dj

## Prerequisites
Before running the Django server, you will need the following:

- Python 3 installed on your machine https://www.python.org/downloads/
- Django web framework installed https://docs.djangoproject.com/en/4.2/topics/install/
- A trained model for pathology image classification https://github.com/VSTARprojects/pc_ml

## Getting Started
- Create a virtual environment and activate it using your preferred method.
- Install the required Python packages by running `pip install -r requirements.txt.`
- Place your trained model in the ml directory.
- Modify the settings.py file to set the correct database settings and any other necessary configurations.
- Run `python manage.py migrate` to create the necessary database tables.
- Run `python manage.py runserver` to start the server.

Access the API endpoints using the URL http://localhost:8000/api/.

## API Endpoints
The following API endpoints are available:

- `api/v1/token/login/` - This endpoint is used for user authentication. A POST request is sent to this endpoint with the user's username and password to obtain an authentication token.
- `api/v1/token/logout/` - This endpoint is used for user logout. A POST request is sent to this endpoint with the user's token to log them out.
- `api/v1/sharedcomments/` - This endpoint is used for getting a list of shared comments. A GET request is sent to this endpoint to obtain a list of shared comments. A POST request to this endpoint is used to create new sharedComment objects.
- `api/v1/sharedcomments/updatecomment/` - This endpoint is used for updating an existing shared comment. A POST request is sent to this endpoint with the comment's ID and the receiver comment.
- `api/v1/sharedcomments/getsamplecomments/` - This endpoint is used for getting a list of comments for a specific sample. A GET request is sent to this endpoint with the sample's ID to obtain a list of comments for that sample.
- `api/v1/samples/` - This endpoint is used for getting a list of samples. A GET request is sent to this endpoint to obtain a list of all samples belonging to a user.
- `api/v1/patients/` - This endpoint is used for getting a list of patients. A GET request is sent to this endpoint to obtain a list of all patients.
- `api/v1/samples/search/` - This endpoint is used for searching for samples based on specific query. A GET request is sent to this endpoint with the search query to obtain a filtered list of samples.
- `api/v1/samples/predict/` - This endpoint is used for predicting the class of a sample image. A POST request is sent to this endpoint with the sample's ID to obtain a predicted class.
- `api/v1/samples/annotations/` - This endpoint is used for getting a list of annotations for a specific sample. A GET request is sent to this endpoint with the sample's ID to obtain a list of annotations for that sample.
- `api/v1/predict/` - This endpoint is used for predicting the class of an image. A POST request is sent to this endpoint with the image file to obtain a predicted class.
- `api/v1/samples/<slug:sample_id>/` - This endpoint is used for getting a specific sample. A GET request is sent to this endpoint with the sample's ID to obtain the details of that sample.
- `api/v1/patients/<slug:patient_id>/` - This endpoint is used for getting a specific patient. A GET request is sent to this endpoint with the patient's ID to obtain the details of that patient.



