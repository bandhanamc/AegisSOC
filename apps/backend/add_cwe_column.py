from app.database.database import engine
from sqlalchemy import text


with engine.connect() as conn:

    conn.execute(
        text(
            """
            ALTER TABLE vulnerabilities
            ADD COLUMN IF NOT EXISTS cwe_id VARCHAR(50);
            """
        )
    )

    conn.commit()


print("CWE column added")