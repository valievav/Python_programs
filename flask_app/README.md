### Simple Flask app "Task Manager"

Functionality:
- add/update/delete/read task

___

**Pre-deployment steps**:
1. Activate virtual env - ```cmd folder``` -> ```activate env_name```
2. Install Gunicorn - ```pip install gunicorn```
3. Freeze requirements - ```pip freeze > requirements.txt``` or ```pipreqs path/to/project``` (for cases with general env, to capture project-specific only)

**Deployment on Heroku:**
1. Sign up for free https://www.heroku.com/
2. Install Heroku CLI https://devcenter.heroku.com/articles/heroku-cli#getting-started

3. Log in - ```heroku login``` -> login via web
4. Create git repo or use existing - ```git init``` -> ```git add .``` -> ```git commit -m "First commit"```
5. Create heroku app - ```heroku create app-name```
6. Push via heroku git - ```git remote -v``` -> ```git push heroku master``` (if pushing main package) or ```git subtree push --prefix flask_app heroku master``` (if pushing sub-package only)
7. Open app - ```heroku open``` or open link in the stack trace or UI->Open APP


**Setup POSTGRES:**
1. UI->APP->Resources->add Add-on 'Heroku Postgres'
2. Check DB URI - ```heroku config --app app-name``` (or UI->APP->Settings->Config Vars)
3. Create tables:
```
heroku run python 
>> from app import db 
>> db.create_all()
>> exit()
```
4.Check tables are created:
```
heroku pg:psql --app app-name
>> SELECT * FROM todo;
```


*If errors - ```heroku logs -t```
