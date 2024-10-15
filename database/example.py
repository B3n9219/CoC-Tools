import psycopg2

# making a connection object
conn = psycopg2.connect(host="localhost", dbname="CoC-Tools", user="postgres",
                        password="Oreo9898", port=5432)
# creating a cursor (what is used to execute commands)
cur = conn.cursor()

cur.execute("""DROP TABLE IF EXISTS person;
""")

cur.execute("""CREATE TABLE IF NOT EXISTS person (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    gender CHAR
);
""")

cur.execute("""INSERT INTO person (id, name, age, gender) VALUES
            (1, 'Ben', 15, 'm'),
            (2, 'Oli', 17, 'm'),
            (3, 'Cam', 20, 'm'),
            (4, 'Mum', 50, 'f'),
            (5, 'Dad', 50, 'm');
            
""")

cur.execute("""SELECT * FROM person WHERE name = 'Ben';""")

print(cur.fetchone())

cur.execute("""SELECT * FROM person WHERE age < 50;""")

for row in cur.fetchall():
    print(row)

sql = cur.mogrify("""SELECT * FROM person WHERE starts_with(name, %s) AND age < %s;""", ("M", 60))

print(sql)
cur.execute(sql)
print(cur.fetchall())

# needs to be done at end to commit changes
conn.commit()
cur.close()
conn.close()