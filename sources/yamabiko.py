import logging

from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement
from dogfood import get_metric_value
import time

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    card_title = render_template('card_title')
    question_text = render_template('welcome')
    reprompt_text = render_template('welcome_reprompt')
    return question(question_text).reprompt(reprompt_text).simple_card(card_title, question_text)


@ask.intent('WhatsTheValueIntent', mapping={'metric': 'Metric'})
def metric_is(metric):
    card_title = render_template('card_title')
    now = int(time.time())
    if metric is not None:
        metric_value = get_metric_value(now, metric)
        if metric_value is None:
            question_text = render_template('unknown_metric_reprompt')
            return question(question_text).reprompt(question_text).simple_card(card_title, question_text)
        if type(metric_value) is not str:
            metric_value = str(metric_value)
        statement_text = render_template('known_metric_bye', metric=metric, value=metric_value)
        return statement(statement_text).simple_card(card_title, statement_text)
    else:
        question_text = render_template('unknown_metric_reprompt')
        return question(question_text).reprompt(question_text).simple_card(card_title, question_text)


@ask.session_ended
def session_ended():
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
