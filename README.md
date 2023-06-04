# Journal

Journal is a web application that allows users to write and manage their personal diary. It provides a platform for users to document their thoughts, experiences, and reflections in a secure and private manner.

# Demo

https://github.com/HienXuanPham/journal-back-end/assets/44250274/b667020b-3dcb-4c86-a78e-39096bf099e7

# Dependencies
- Front-end: React
- Back-end: Flask
- Database: Postgresql
- External API: https://type.fit/api/quotes

# Features
- Authenticating a user login and signup with `Flask-Session` and `redis`
- `CRUD` endpoints that a user can create, get, update and delete their notes.

# Environment Set up
1. Fork and clone this repo.
2. Set up a visual environment
```
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Create a database in Postgresql.
- Installing Postgres
  - `brew install postgresql`
  - `brew services start postgresql`
- Create the Postgres user
  - `createuser -s postgres`
  - The most common default username and password for Postgres is
    - username: postgres
    - password: postgres
- Create a database in Postgres
  - Enter Postgres terminal: `psql -U postgres`
  - Create a database: `CREATE DATABASE db_name;`
  - Exit Postgres terminal: `\q`

