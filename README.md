# Tournament Server

This project is a backend to run tournaments of any kind.

## Using the Server

1. Create a `.env` file
1. Add a key `ENV` with the value `development` **exactly**.
    1. Note: When you deploy, you will create this key on Heroku the value `production`. This will distinguish the development and production settings set in this template.
1. Run `pipenv shell` to start up your virtual environment.
1. Run `pipenv install` to install dependencies.
2. Create a psql database for your project
    1. Edit `settings.sql` then run `psql -U postgres -f settings.sql`
    OR:
    1. Type `psql` to get into interactive shell.
    2. Run `CREATE DATABASE "project_db_name";` where `project_db_name` is the name you want for your database.
1. Add the database name to the `.env` file using the key `DB_NAME_DEV`.
2. Generate a secret key using [this tool](https://djecrety.ir) and add it to the `.env` file using the key `SECRET`.

### The `.env` File

After following the steps above, your `.env` file should look _something_ like
the following, replacing `project_db_name` with your database name and `secret_key`.

```sh
ENV=development
DB_NAME_DEV=project_db_name
SECRET=secret_key
```

## Commands

Commands are run with the syntax `python3 manage.py <command>`:

| command | action |
|---------|--------|
| `runserver`  |  Run the server |
| `makemigrations`  | Generate migration files based on changes to models  |
| `migrate`  | Run migration files to migrate changes to db  |
| `startapp`  | Create a new app  |

## Deployment

Once ready, you can follow the steps in the [django-heroku-deployment-guide](https://git.generalassemb.ly/ga-wdi-boston/django-heroku-deployment-guide).
