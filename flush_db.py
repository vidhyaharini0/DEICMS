"""
flush_db.py - make the SQLite database file demo-ready.

SQLite runs in WAL (write-ahead log) mode, so recent writes may sit in the
side files ``deicms.db-wal`` / ``deicms.db-shm`` and are not visible when you
open ``deicms.db`` in a SQLite browser while (or just after) the app has run.

This script performs a full WAL checkpoint, folding every pending write back
into ``deicms.db`` itself, then prints a short summary so you can confirm the
live audit trail is really there.

Usage:
    python flush_db.py

Run it after using the app (ideally with the Flask server stopped) and then
open deicms.db in DB Browser for SQLite - the audit_records table will show
every event, not just the seed data.
"""
import os
import sqlite3
import sys

from config import Config


def _db_path():
    """Resolve the SQLite file path from the app's configured database URI."""
    uri = Config.SQLALCHEMY_DATABASE_URI
    prefix = 'sqlite:///'
    if not uri.startswith(prefix):
        print(f"Configured database is not SQLite ({uri}); nothing to flush.")
        sys.exit(0)
    return uri[len(prefix):]


def main():
    path = _db_path()
    if not os.path.exists(path):
        print(f"Database file not found: {path}")
        print("Run 'python seed.py' or start the app at least once first.")
        sys.exit(1)

    conn = sqlite3.connect(path)
    try:
        # Fold the WAL back into the main database file.
        mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
        result = conn.execute("PRAGMA wal_checkpoint(FULL);").fetchone()
        conn.commit()

        # result = (busy, log_frames, checkpointed_frames)
        busy, log_frames, checkpointed = result if result else (None, None, None)

        print("DEICMS database flush")
        print("=" * 40)
        print(f"File            : {os.path.abspath(path)}")
        print(f"Journal mode    : {mode}")
        print(f"WAL frames      : {log_frames} (checkpointed: {checkpointed})")
        if busy:
            print("Note: the database was busy - stop the running app and re-run "
                  "this script for a complete flush.")

        # Quick sanity summary the professor can cross-check in the browser.
        print("\nRow counts")
        print("-" * 40)
        for table in ('investigators', 'cases', 'evidence_items',
                      'custody_logs', 'audit_records'):
            try:
                n = conn.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]
                print(f"  {table:<16}: {n}")
            except sqlite3.Error:
                print(f"  {table:<16}: (table not found)")

        # Show the five most recent audit events so it's obvious the live
        # trail (not just seed data) is persisted in the file.
        try:
            rows = conn.execute(
                "SELECT id, event_type, timestamp, result "
                "FROM audit_records ORDER BY id DESC LIMIT 5;").fetchall()
            if rows:
                print("\nMost recent audit events")
                print("-" * 40)
                for r in rows:
                    print(f"  #{r[0]:<4} {r[1]:<18} {r[3]:<8} {r[2]}")
        except sqlite3.Error:
            pass

        print("\nDone. You can now open deicms.db in a SQLite browser.")
    finally:
        conn.close()


if __name__ == '__main__':
    main()
