#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, redirect, url_for
from flask import send_from_directory
from flask import flash
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
# from forms import *
import os
from werkzeug.utils import secure_filename
from algorithms.opencv_cascade import run_cascade_algorithm

is_heroku = os.environ.get('IS_HEROKU', None)

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

if is_heroku is None:
    from config import CAM_KEY
    app.config.from_object('config')
    UPLOAD_FOLDER = './static/img'
else:
    CAM_KEY = os.environ['CAM_KEY']
    basedir = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(basedir, 'static/img')
#db = SQLAlchemy(app)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/chandleruno')
def chandleruno():
    data = open("chanderuno.dat", "rb")
    # assuming one line for now in the file
    num_people = int(data.read())

    return render_template('pages/chandleruno.html', num_people=num_people)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # Check if the post request has the SECRET KEYY OOOO SPOOOKY
        if 'cam_key' not in request.args or request.args['cam_key'] != CAM_KEY:
            flash("You don't have the key")
            return redirect(request.url)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file_path = app.config['UPLOAD_FOLDER']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            num_people = run_cascade_algorithm(file_path)

            # add the data to the file
            data_file = open("chandleruno.dat", "wb+")
            data_file.write(str(num_people[0]))
            data_file.close()

            return redirect(url_for('upload_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


   # if request.method == 'POST':
   #    f = request.files['file']
   #    f.save(secure_filename(f.filename))
   #    return 'file uploaded successfully'

# @app.route('/login')
# def login():
#     form = LoginForm(request.form)
#     return render_template('forms/login.html', form=form)


# @app.route('/register')
# def register():
#     form = RegisterForm(request.form)
#     return render_template('forms/register.html', form=form)


# @app.route('/forgot')
# def forgot():
#     form = ForgotForm(request.form)
#     return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
