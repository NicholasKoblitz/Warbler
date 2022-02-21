# Warbler

## Description

Warbler is a lightweight Twiter clone that allows a user to create a user, post messages, and follow or unfollow other users. This clone was made as part of an exercise in Python and Flask back-end development. The code base was given with most of the features already implamentented. These files are seen as one of the first commits in the commit history.

## Installation

1. Clone the repo

   ```
   git clone {repo}
   ```

2. Create virtual environment

   ```
   python -m venv venv
   ```

3. Instal dependencies

   ```
   pip install -r requirements.txt
   ```

4. Create the database

   ```
   creatdb warbler
   ```

5. Run seed file (or create or own)

   ```
   python3 -m seed.py
   ```

## Running Provied Tests

1. Create testing database

   ```
   createdb warbler-test
   ```

2. Run Test

   ```
   python3 -m unittest {test file}
   ```
