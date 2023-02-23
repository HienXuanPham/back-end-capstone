# Journal

This back end was made as a capstone project for Ada Developers Academy. Journal is a website that a user write their diary.

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

