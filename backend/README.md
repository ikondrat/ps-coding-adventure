# To start

## Tools to use

-   pipenv to manage dependencies
-   pytest to run tests
-   fastapi to create the API
-   uvicorn to run the server
-   requests to make requests to the API
-   sqlalchemy to interact with the database
-   postgresql as the database
-   alembic to manage the database migrations

## Run

```bash
pipenv shell
pipenv install

uvicorn main:app --app-dir app --reload

```
