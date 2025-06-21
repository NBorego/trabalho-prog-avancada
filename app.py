from flask import Flask, render_template, request, redirect, url_for
from models import db, Feedback
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meusistema.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')
def index():
    feedbacks = Feedback.query.all()
    return render_template('home.html', feedbacks=feedbacks)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        novo_feedback = Feedback(
            nome=request.form['nome'],
            email=request.form['email'],
            mensagem=request.form['mensagem']
        )
        db.session.add(novo_feedback)
        db.session.commit()
        return redirect(url_for('obrigado'))
    return render_template('feedback.html')

@app.route('/obrigado')
def obrigado():
    return render_template('obrigado.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
