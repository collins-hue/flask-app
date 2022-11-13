from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import session
import random
import smtplib
import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['MY-KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

EMAIL = os.environ['EMAIL']
PASSWORD = os.environ['PASSWORD']


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f"{self.name} - {self.email}"


# db.create_all()


def sendmessage():
    # To get the particular column in the database
    for name in session.query(Users.name).distinct():
        for email in session.query(Users.email).distinct():
            with open('prompts.txt', encoding='utf8') as content:
                file = content.readlines()
                prompt = random.choice(file)
            with open('affirmations.txt', encoding='utf8') as f:
                content = f.readlines()
                affirmation = random.choice(content)

            with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
                connection.starttls()
                connection.login(user=EMAIL, password=PASSWORD)
                connection.sendmail(from_addr=EMAIL, to_addrs=f"{email}",
                                    msg=f"Subject:Good morning {name} \nHere is your daily affirmation and Journal "
                                        f"prompt \n\n "
                                        f"Affirmation of the day: {affirmation}"
                                        f"Prompt of the Day: {prompt}"
                                    )
                connection.quit()


# schedule.every().day.at('8:00').do(sendmessage)


@app.route('/')
def home():
    year = datetime.datetime.now().year
    with open('prompts.txt', encoding='utf8') as content:
        file = content.readlines()
        prompt = random.choice(file)
    return render_template('index.html', prompt=prompt, current_year=year)


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        new_user = Users(
            name=request.form.get("name"),
            email=request.form.get("email"),
        )

        db.session.add(new_user)
        db.session.commit()
        flash('Name and Email successfully entered')

    return render_template('signup.html')


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        name = request.form.get('name'),
        email = request.form.get('email'),
        subject = request.form.get('subject'),
        message = request.form.get('message')

        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=f"{email}", to_addrs=EMAIL,
                                msg=f"Subject: {subject}\n\n "
                                    f"Name:{name},\n{message}"
                                )
            return redirect(url_for('home'))
    return render_template('contact.html')


@app.route('/journal')
def journal():
    return render_template('journal.html')


@app.route('/bullet-journal-ideas')
def bullet_journal_ideas():
    return render_template('bullet-journal.html')


@app.route('/prompt-generator')
def prompt_generator():
    return render_template('prompt-generator.html')


@app.route('/make-journaling-fun')
def make_journaling_fun():
    return render_template('make-journaling-fun.html')


if __name__ == '__main__':
    app.run(debug=True)