from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, BooleanField, FloatField, HiddenField
from wtforms.fields.html5 import EmailField
import requests

AUTH_TOKEN = ""


BASE_URL = "https://www.freelancer-sandbox.com"
POST_PROJECT_ENDPOINT = "/api/projects/0.1/projects/?compact="


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = EmailField('Email address: ', [validators.DataRequired(), validators.Email()])
    latitude = HiddenField('latitude')
    longitude = HiddenField('longitude')
    add_videographers = BooleanField('Hire videographers? ', default=True)
    budget = FloatField('Overall Budget (Pesos): ')
    comments = TextAreaField('Comments: ')


# Just so we don't need to restart the server every time there are changes
def before_request():
    app.jinja_env.cache = {}


app = Flask(__name__)
app.before_request(before_request)
app.config.update(
    DEBUG=True,
    TESTING=True,
    TEMPLATES_AUTO_RELOAD=True
)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = ''

@app.route('/', methods=['GET', 'POST'])
def index(context=None):
    form = ReusableForm(request.form)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        add_videographers = request.form['add_videographers']
        budget = request.form['budget']
        comments = request.form['comments']

        if form.validate():
            context = {
                "name": name,
                "email": email,
                "latitude": latitude,
                "longitude": longitude,
                "add_videographers": add_videographers,
                "budget": budget,
                "comments": comments
            }

            responses = post_local_jobs(context)
            for response in responses:
                print(response.text)

            return render_template('success.html', context=context)
        else:
            flash('All the form fields are required. ')

    return render_template('index.html', form=form)#, status=status)


@app.route('/success')
def success(context=None):
    return render_template('success.html', details=details)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def post_local_jobs(context):
    header = {
        'content-type': 'application/json',
        'Freelancer-OAuth-V1': AUTH_TOKEN,
    }

    # Hire flashmob
    data = {
        "title": "MobFlash Participants - Local Jobs",
        "description": "We need Flash Mob participants...",
        "currency": {
            "id": 7
        },
        "budget": {
            "minimum": float(context["budget"]) * 1.2,
            "maximum": float(context["budget"]) * 1.2
        },
        "jobs": [{
            "id": 864
        }],
        "location": {
            "city": "Random City",
            "country": {
                "name": "Random Country"
            },
            "latitude": float(context["latitude"]),
            "longitude": float(context["longitude"])
        }
    }

    response = [requests.post(BASE_URL + POST_PROJECT_ENDPOINT, headers=header, json=data)]

    # Hire videographers
    if context["add_videographers"] == "y":
        data = {
            "title": "Document and take awesome pictures of MobFlash surprise",
            "description": "We need Flash Mob videographers...",
            "currency": {
                "id": 7
            },
            "budget": {
                "minimum": 1500,
                "maximum": 2000
            },
            "jobs": [{
                "id": 27
            }],
            "location": {
                "city": "Random City",
                "country": {
                    "name": "Random Country"
                },
                "latitude": float(context["latitude"]),
                "longitude": float(context["longitude"])
            }
        }
        response.append(requests.post(BASE_URL + POST_PROJECT_ENDPOINT, headers=header, json=data))

    return response
