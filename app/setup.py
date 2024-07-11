"""
Setup of a new app.
"""

try:
    from app import db
except ImportError:
    import db

if __name__ == "__main__":
    db.create_empty_db()
    print("Created an empty DB")
