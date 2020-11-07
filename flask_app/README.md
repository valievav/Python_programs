### Simple Flask app "Task Manager"

Functionality:
- add/update/delete/read task


**Deployment on Heroku:**
1. Sign up for free https://www.heroku.com/
2. Install Heroku CLI https://devcenter.heroku.com/articles/heroku-cli#getting-started
3. Activate virtual env - cmd-> activate env_name
4. Install Gunicorn - pip install gunicorn
5. Freeze only project-specific requirements - pipreqs path/to/project
6. Log in - heroku login -> login via web -> logged in to terminal
7. Create git repo or use existing - git init -> git add . -> git commit -m "First commit"
8. Create heroku app - heroku create name-of-the-app-unique
9. Push to heroku git - git remote -v -> git push heroku master (if pushing main package); git subtree push --prefix flask_app heroku master (if pushing sub-package)
10. Open app - heroku open or open link in the stack trace
