from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from models import *
import populate_db

# import blueprints
from routes.admin_bp import admin_bp
from routes.auth_bp import auth_bp
from routes.doctor_bp import doctor_bp
from routes.patient_bp import patient_bp


def create_app():
  app = Flask(__name__)
  app.secret_key = 'simple_secret_key'  # for flask-login sessions

  # setup database
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
  db.init_app(app)

  # create tables and populate
  with app.app_context():
    db.create_all()
    if User.query.count() == 0:  # empty DB
      populate_db.populate()

  # setup flask-login
  login_manager = LoginManager()
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

  # register blueprints
  app.register_blueprint(admin_bp)
  app.register_blueprint(auth_bp)
  app.register_blueprint(doctor_bp)
  app.register_blueprint(patient_bp)

  # root route
  @app.route('/')
  def index():
    if current_user.is_authenticated:
      if current_user.type == 'admin':
        return redirect(url_for('admin_bp.admin_home'))
      elif current_user.type == 'doctor':
        return redirect(url_for('doctor_bp.doctor_home'))
      elif current_user.type == 'patient':
        return redirect(url_for('patient_bp.patient_home'))
    user_count = User.query.count()
    return render_template('index.html', user_count=user_count)

  return app


app = create_app()

if __name__ == '__main__':
  app.run(debug=True)
