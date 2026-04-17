import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ragdb",
    user="postgres",
    password="123456"
)

def insert_document(content, embedding):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
        (content, embedding)
    )
    conn.commit()
    cur.close()

def search_similar(embedding):
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT content
            FROM documents
            ORDER BY embedding <-> %s::vector
            LIMIT 5
        """, (embedding,))

        results = [row[0] for row in cur.fetchall()]
        return results

    except Exception as e:
        conn.rollback()   # ✅ RESET FAILED TRANSACTION
        print("DB ERROR:", e)
        return []

    finally:
        cur.close()