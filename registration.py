# register.py

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from db import initialize_mysql, mysql_config, insert_user,retrieve_user,get_positionnames,get_candidates,insert_vote

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Initialize MySQL
mysql = initialize_mysql(app)

# Set MySQL configurations
for key, value in mysql_config.items():
    app.config[key] = value


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Retrieve user from database
        user = retrieve_user(mysql,email)
        if user and user['email'] == email and user['password'] == password:
            # Store user ID in the session
            session['user_id'] = user['id']
            # Redirect to home page
            return render_template('home.html', message="login successful")
        else:
            return render_template('login.html', message="invalid email or password error")

    # Render the login form template for both GET and failed POST requests
    return render_template('login.html')

# Route for user logout
@app.route('/logout')
def logout():
    # Remove user ID from the session
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        if firstname.strip() == '' or lastname.strip() == '' or email.strip() == '' or password.strip() == '':
            flash('All fields are required!', 'error')
        else:
            # Insert user data into the database
            insert_user(mysql, firstname, lastname, email, password)
            return render_template('login.html')

    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    # # Check if user is logged in
    # if 'user_id' not in session:
    #     return redirect(url_for('login'))
    return render_template('home.html')


# Route for rendering current_polls HTML template
@app.route('/current_polls', methods=['GET', 'POST'])
def current_polls():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('current_polls.html')


# Route for getting positionnames
@app.route('/get_positionnames')
def fetch_positionnames():
    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    position_names_list = get_positionnames(mysql)
    return jsonify(position_names_list)

# Route for getting candidates
@app.route('/get_candidates', methods=['GET'])
def get_candidates_route():
    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    position = request.args.get('position')
    if position:
        candidates = get_candidates(mysql, position)
        return jsonify(candidates)
    else:
        return jsonify([])  # Return empty list if position not provided


# Route for submitting votes
@app.route('/vote', methods=['POST'])
def vote():
    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.json  # Assuming JSON data is sent
    position_name = data.get('position')
    candidate_id = data.get('candidate')
    user_id = session['user_id']  # Retrieve user ID from session
    if position_name and candidate_id:
        # Insert the vote into the database
        insert_vote(mysql, user_id, candidate_id, position_name)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid data provided'})

if __name__ == '__main__':
    app.run(debug=True)
