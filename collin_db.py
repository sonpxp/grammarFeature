import sqlite3


def save_collins_dict_to_db(word: str, span: str):
    # Connecting to sqlite
    # connection object
    conn = sqlite3.connect('collins.db')

    # cursor object
    cursor = conn.cursor()
    try:
        # Drop the COLLINS table if already exists.
        # cursor.execute("DROP TABLE IF EXISTS COLLINS")

        # Creating table
        table = """ CREATE TABLE IF NOT EXISTS COLLINS (
                                Word NVARCHAR(255) NOT NULL,
                                HtmlCrawler TEXT
                            ); """
        cursor.execute(table)

        # Queries to INSERT records.
        # cursor.execute('''INSERT INTO COLLINS VALUES ('slow', 'html2')''')
        # cursor.execute('''INSERT INTO COLLINS VALUES ('big', 'html3')''')
        # cursor.execute('''INSERT INTO COLLINS VALUES ('dog', 'html4')''')

        # Display data inserted
        # print("Data Inserted in the table: ")
        # data = cursor.execute('''SELECT * FROM COLLINS''')
        # for row in data:
        #     print(row)

        # Insert data

        db_collins = "INSERT INTO COLLINS (Word,HtmlCrawler) values (?, ?)"
        # cursor.execute(db_collins, (span_title, str(span_html)))
        cursor.execute(db_collins, (str(word), span))

        # Commit your changes in the database
        conn.commit()
        # Close the connection
        conn.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table: ", error)

    finally:
        if conn:
            conn.close()
            print("the sqlite connection is closed")


# save_collins_dict_to_db('abc', 'xyz')
