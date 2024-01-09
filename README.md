> Disclaimer: This project was an interview task simulating building multiple endpoints within a three-day timeframe. While 3 days may not be typical for real-world project timelines, it provided a valuable opportunity to test my skills and problem-solving abilities under pressure.

Build a project management tool where users can create projects, assign tasks to team members, track progress, and set deadlines (Use Django Rest Framework). The tool should have time tracking functionality, a dashboard to display project metrics, and a messaging system for team members to communicate. 

API Endpoints
- /api/auth/register/ - allows users to register a new account.
- /api/auth/login/ - allows users to login and obtain a token for authentication.
- /api/auth/logout/ - allows users to logout and invalidate the token
- /api/auth/user/ - returns the user's details and allows users to update their profile
- /api/projects/ - returns a list of projects created by the user and allows users to create a new project
- /api/projects/<project_id>/ - returns details for a specific project and allows users to update or delete the project 
- /api/tasks/ - returns a list of tasks assigned to the user and allows users to create a new task
- /api/tasks/<task_id>/ - returns details for a specific task and allows users to update or delete the task. /api/- time-tracker/ - allows team members to track time spent on a task and view time entries
 

# Steps to run
Here are some steps to be able to start local project.

1. Copy the .env.example to .env
```sh
cp .env.example .env
```

2. Create virtual environment and install `pipenv`
```sh
pip install pipenv
```

3. Install dependency with pipenv
```sh
pipenv install --dev  # with additional dev packages
```

4. Start project
```sh
pipenv run start
```

## For migrations we can run

```sh
pipenv run migrations # create our migrations
```

```sh
pipenv run migrate # apply migrations
```

