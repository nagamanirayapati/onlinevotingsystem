# db.py

from flask_mysqldb import MySQL

# Function to initialize MySQL and return the MySQL object
def initialize_mysql(app):
    mysql = MySQL(app)
    return mysql

# MySQL configurations
mysql_config = {
    'MYSQL_HOST': 'localhost',
    'MYSQL_USER': 'root',
    'MYSQL_PASSWORD': 'ammanana01',
    'MYSQL_DB': 'onlinevotingsystem_schema',
    'MYSQL_CURSORCLASS': 'DictCursor'
}

# Function to insert user data into the database
def insert_user(mysql, firstname, lastname, email, password):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tbusers (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)",
                (firstname, lastname, email, password))
    mysql.connection.commit()
    cur.close()

# Function to retrieve user from the database
def retrieve_user(mysql, email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id,email, password FROM tbusers WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    return user


# Function to get positions from the database
def get_positionnames(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT position_name FROM tbpositions")
    position_names = [row['position_name'] for row in cur.fetchall()]
    cur.close()
    return position_names


# Function to get candidates by position
def get_candidates(mysql, position):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, candidate_name FROM tbcandidates WHERE position_id IN (SELECT id FROM tbpositions WHERE position_name = %s)", (position,))
    candidates = cur.fetchall()
    cur.close()
    return candidates


# Function to insert vote into the database
def insert_vote(mysql, user_id, candidate_id, position_name):
    cur = mysql.connection.cursor()
    # Query to get position_id from position_name
    cur.execute("SELECT id FROM tbpositions WHERE position_name = %s", (position_name,))
    position_id = cur.fetchone()
    # Extract the position_id from the tuple
    if position_id is not None:
        position_id = position_id['id']
    else:
        cur.close()
        return
    cur.execute("INSERT INTO tbvotes (user_id, candidate_id, position_id) VALUES (%s, %s, %s)", (user_id, candidate_id, position_id))
    mysql.connection.commit()
    cur.close()




