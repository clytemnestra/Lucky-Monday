## Lucky Monday
A [Flask](https://github.com/pallets/flask) app that connects to Google Drive and updates Lucky Monday result spreadsheet based on form answers.

##Steps:

Install Python3, pip, git and clone the project

Go to project root and open a command line window

Install the virtual environment
```
python -m venv venv
```
Activate the virtual environment([on Windows](http://flask.pocoo.org/docs/1.0/installation/#create-an-environment))
```
venv\Scripts\activate
```
Install requirements
```
pip install -r requirements.txt
```

Create Google app in the console
Create credentials in the console-> credentials, service account key, create service account, json.
Paste JSON contents into 'client_secrets.json'
Share Google Drive folder with 'client_email' value

You can now run commands with 'flask [options] command_name [arguments]'

## Available commands

1. update_lm_session
