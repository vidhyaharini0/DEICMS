# Resetting the database

Run these from the project root (`deicms\`) in PowerShell, with the Flask
server **stopped**.

## 1. Activate the virtual environment

    .\venv\Scripts\Activate.ps1

The prompt should now start with `(venv)`. If it does not, nothing below
will work - the commands will run against the system Python, which does
not have Flask installed.

## 2. Delete the database (all three files)

    Remove-Item deicms.db, deicms.db-wal, deicms.db-shm -ErrorAction SilentlyContinue

SQLite runs in write-ahead-log mode, so `deicms.db-wal` and `deicms.db-shm`
hold recent writes. Deleting only `deicms.db` leaves those behind and the
next run can resurrect stale rows.

## 3. Recreate and seed

    python seed.py

Watch the output. The last three lines must be:

     Database seeded successfully!
     Open http://127.0.0.1:5001 and log in with:
     admin@deicms.com   / Admin@1234

If instead you see a traceback, **stop and read it** - the database will be
half-built and logging in will fail. Do not start the server until the seed
finishes cleanly.

## 4. Confirm before starting the server

    python -c "import sqlite3;c=sqlite3.connect('deicms.db');print('investigators:',c.execute('SELECT COUNT(*) FROM investigators').fetchone()[0]);print('case_access  :',c.execute('SELECT COUNT(*) FROM case_access').fetchone()[0])"

Expected:

    investigators: 4
    case_access  : 7

`investigators: 0` is the exact symptom of "I cannot log in with any
account". `case_access: 0` means Admin works but every other role sees an
empty system.

## 5. Start the application

    python run.py

Then open <https://127.0.0.1:5001> and accept the self-signed certificate
warning.

## Accounts

| Email | Password | Role | Sees |
|---|---|---|---|
| `admin@deicms.com` | `Admin@1234` | Admin | all 8 cases (exempt from the check) |
| `lead@deicms.com` | `Lead@1234` | Lead Investigator | 4 cases, as Owner |
| `analyst@deicms.com` | `Analyst@1234` | Analyst | 3 cases, as Member |
| `readonly@deicms.com` | `Readonly@1234` | Read-Only | **none** - shows the empty state |

The differing counts are deliberate. Only the Admin is exempt from the
case-membership check; every other role sees a strict subset. This is what
makes Figures 18.3 and 18.4 show different totals over the same database,
and what gives Figure 18.5 its explanatory empty state.

## Note

Resetting destroys any evidence you uploaded through the UI. Re-upload the
files in `demo_files\` afterwards - see `demo_files\README.md`.
