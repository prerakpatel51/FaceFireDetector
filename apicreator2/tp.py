import psycopg2
import json

# Sample data
data = [
    {
        "unique_id": "4a9858d5-f622-5b58-aa37-e656d5cdfda3",
        "urls": [
            {
                "url": "http://127.0.0.1:8000/admin/api/url/add/",
                "camera_id": "db3cd3cb-873c-53e0-8891-f3f16417f7cb",
                "images": [
                    {
                        "image_url": "http://127.0.0.1:8000/media/images/hritik.png",
                        "image_name": "prerak"
                    },
                    {
                        "image_url": "http://127.0.0.1:8000/media/images/katrinakaif.png",
                        "image_name": "jay"
                    }
                ]
            },
            {
                "url": "http://nasa.com",
                "camera_id": "62e52078-2e7e-58b6-9744-dfb587684379",
                "images": [
                    {
                        "image_url": "http://127.0.0.1:8000/media/images/hritik_jfngdnS.png",
                        "image_name": "nasa"
                    }
                ]
            }
        ]
    },
    # Add other data items here...
]

def create_table_if_not_exists(conn):
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS data_table (
    id SERIAL PRIMARY KEY,
    unique_id UUID,
    urls JSONB
);
""")
        conn.commit()
        cursor.close()

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname='face',
    user='face',
    password='root',
    host='localhost',
    port=5432
)
create_table_if_not_exists(conn)
# Create a cursor object
cur = conn.cursor()

# Insert the data into the data_table
for item in data:
    cur.execute(
        """
        INSERT INTO data_table (unique_id, urls) VALUES (%s, %s)
        """,
        (item['unique_id'], json.dumps(item['urls']))
    )

# Commit the changes
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
