# Database Creation Fallbacks

Use this only when the selected database is not SQLite and Herd MCP is unavailable. Create the app database and testing database before running `laravel new`, `laravel new --using`, or `composer create-project`.

## Naming

- Default app database: safe snake_case version of the app name.
- Default testing database: `<app_database>_testing`.
- Use the user's provided database name if they give one, then append `_testing` for the test database.
- Stop before install if database creation cannot be confirmed.

## MySQL or MariaDB

Ask for host, port, username, and password only when needed. Prefer not to place passwords directly in saved shell history.

```sh
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS my_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS my_app_testing CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

## PostgreSQL

Use `createdb` when it is available and the current user has permission:

```sh
createdb my_app
createdb my_app_testing
```

Use an idempotent check when needed:

```sh
psql -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'my_app'" | grep -q 1 || createdb my_app
psql -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'my_app_testing'" | grep -q 1 || createdb my_app_testing
```

## SQL Server

```sh
sqlcmd -S localhost -U sa -P '<password>' -Q "IF DB_ID('my_app') IS NULL CREATE DATABASE my_app;"
sqlcmd -S localhost -U sa -P '<password>' -Q "IF DB_ID('my_app_testing') IS NULL CREATE DATABASE my_app_testing;"
```

## After Creation

- Configure `.env` and test environment settings to use the created databases.
- Run migrations only after both databases exist.
- Do not print or commit database passwords.
