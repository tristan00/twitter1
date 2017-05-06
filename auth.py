import sqlite3

def set_auth():
    conn = sqlite3.connect('auth.db')
    cursor = conn.cursor()
    #cursor.execute('''CREATE TABLE authentication(field text, value text)''')
    cursor.execute("INSERT INTO authentication VALUES ('API Key','xzJZAQg5ifxT0e3AVQqsRuIph')")
    cursor.execute("INSERT INTO authentication VALUES ('API Secret','062QX7PUE3C9eCwFEsf7ZzCsi3xsGD48F6d0fVClKidyL3oVQU')")
    cursor.execute("INSERT INTO authentication VALUES ('Owner','TristanDelforge')")
    cursor.execute("INSERT INTO authentication VALUES ('Owner ID','369261825')")
    cursor.execute("INSERT INTO authentication VALUES ('Access Token','369261825-Eu4DzPdWmg8k5vbYoeE36TVePUgXCrGNhQjrqBlt')")
    cursor.execute("INSERT INTO authentication VALUES ('Access Token Secret','LyOyNPT7QvLMWpf42FM8zFOTYq1VqLfq1zr1fmW7O1GlK')")
    conn.commit()

set_auth()