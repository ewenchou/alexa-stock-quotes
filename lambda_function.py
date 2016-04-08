"""
This is a simple Alexa Skill that gets the stock quotes for a list of tickers.
"""
from __future__ import print_function
from math import floor
import urllib2
import json
import decimal

# Customize with your list of stock tickers
STOCK_TICKERS = ['AAPL', 'FB', 'NFLX']

# Populate with your skill's application ID to prevent someone else from
# configuring a skill that sends requests to this function.
APP_ID = ""


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if APP_ID and (event['session']['application']['applicationId'] != APP_ID):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_stocks()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetStocksIntent":
        return get_stocks()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------

def get_url(ticker_list=STOCK_TICKERS):
    tickers = ",".join(ticker_list)
    return "http://finance.yahoo.com/webservice/v1/symbols/{tickers}/" \
           "quote?format=json&view=detail".format(tickers=tickers)

def parse_data(data):
    resources = data['list']['resources']
    stocks = []
    for r in resources:
        # Parse the name and remove the unnecessary bits
        name = r['resource']['fields']['name']
        name = name.replace("Common Stock", '')
        name = name.replace(' Inc','').replace(',','').replace('.','')
        name = name.replace('(NS) O','')
        name = name.replace("(The) Commo", "")
        name = name.strip()

        # Parse the change percent and make it speech-friendly
        change = r['resource']['fields']['chg_percent']  # this is a string
        if "-" in change:
            up_down = "is down"
        else:
            up_down = "is up"
        # Convert to decimal, get absolute value, and round to one decimal place
        change = round(abs(decimal.Decimal(change)), 1)
        if change == 0:
            spoken_change = "is trading at"
        else:
            # Avoid saying things like, "two point zero percent".
            # Instead, say "two percent"
            splits = str(change).split('.')
            if splits[1] == '0':
                spoken_change = "{up_down} {change}% at".format(
                    up_down=up_down, change=splits[0])
            else:
                spoken_change = "{up_down} {change}% at".format(
                    up_down=up_down, change=change)

        # Parse the price and make it speech-friendly
        price = round(decimal.Decimal(r['resource']['fields']['price']), 2)
        price = round(decimal.Decimal(price), 2)
        spoken_price = "${}".format(price)

        # Put all the pieces together
        spoken = "{name} {change} {price}.".format(
            name=name, change=spoken_change, price=spoken_price)

        # Append to the list of stocks
        stocks.append(spoken)
    return "  ".join(stocks)


def get_stocks(ticker_list=STOCK_TICKERS):
    card_title = "Stock Report"
    session_attributes = {}
    should_end_session = True
    try:
        url = get_url(ticker_list)
        res = urllib2.urlopen(url)
        data = json.loads(res.read())
        stocks = parse_data(data)

        if stocks:
            speech_output = "Here's how your stocks are doing, " + stocks
            reprompt_text = None
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
        else:
            return error_response()
    except Exception as e:
        print("Exception: {}".format(str(e)))
        return error_response()


def error_response():
    card_title = "Oops!"
    session_attributes = {}
    should_end_session = True
    speech_output = "Sorry, I was not able to get your stock prices. " \
                    "Please try again later."
    reprompt_text = None

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
