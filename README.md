Project management tool where users can create projects, assign tasks to team members, track progress, and set deadlines.


# Steps
Here are some steps to be able to start local project.

1. Copy the .env.example to .env
```sh
cp .env.example .env
```

2. Create virtual environment and install `pipenv`.
```sh
pip install pipenv
```

3. Install dependancy with pipenv
```sh
pipenv install --dev  # with additional dev packages
```

4. Start project
```sh
pipenv run start
```

> For migrations we can run

```sh
pipenv run migrations # create our migrations
```

```sh
pipenv run migrate # apply migrations
```
