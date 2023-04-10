# learning-app
This is an app for educational purposes. Provides viewsets for registration, professor and student. Also has a guest role for users to get list of all courses. The main features were created for student and professor needs. They allow to join the course and complete the tasks questions, and a professor user can create courses, tasks and grade them. To know more [see documentation](127.0.0.1:8000).


## `Requirements:`
1. Python 3.11
2. Poetry 1.3.1
3. PostgreSQL 14.5


## `Prerequisites:`
### If using Docker:
1. From your project directory, start up your application by running docker compose up:

    `docker compose up`

2. Use this command to create superuser:

    `docker compose exec app python learning_app/manage.py createsuperuser`


### If not using Docker:
1. Create inviroment and install requirement from `pyproject.toml`:

    `poetry install`
2. Create `.env` file according to `.env_example`
3. Create database named like `DB_NAME`:

    `sudo -u postgres psql`
```sql 
CREATE DATABASE {DB_NAME};
```
4. Make migrations:

    `python manage.py migrate`
5. Create superuser:

    `python manage.py createsuperuser`
6. Run server:

    `python manage.py runserver`

## Main features:
- `/users/register/` registration via email and document number
- `/login/` login via username (which is email) and password
- `/course/` get the list of all courses (search available)
- `/student/course/{id}/join_course/` a student can join the course and get task `/student/task/`
- `/student/answer/` a student can create an answer and upload an attachement `/student/answer/{id}/upload_attachment/`
- `/professor/course/` a professor can create a course
- `/professor/task/` a professor can create a task with questions
- `/professor/answer/{id}/` a professor can update a grade field

### After running the app we will have access to swagger documentation.
