"""
This is a simple Alexa Skill that gets the stock quotes for a list of tickers.
"""
from __future__ import print_function
from googlefinance import getQuotes

# Customize with your stock tickers
TICKERS = {
    "AAPL": "Apple",
    "FB": "Facebook",
    "NFLX": "Netflix"
}
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
    return get_quotes()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetStocksIntent":
        return get_quotes()
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

def get_quotes(tickers=TICKERS):
    """Get stock quotes using `googlefinance` Python module.

    @param: tickers: Dict with ticker symbol as key, and company name as value.

    Example output from googlefinance.getQuotes()
        [
            {
                "Index": "NASDAQ", 
                "LastTradeWithCurrency": "114.65", 
                "LastTradeDateTime": "2016-09-22T14:00:40Z", 
                "LastTradePrice": "114.65", 
                "LastTradeTime": "2:00PM EDT", 
                "LastTradeDateTimeLong": "Sep 22, 2:00PM EDT", 
                "StockSymbol": "AAPL", 
                "ID": "22144"
            }, 
            ...
        ]
    """
    if not tickers:
        return error_response()

    try:
        # Get the quotes
        quote_list = getQuotes(tickers.keys())
        # Parse the quotes and build a list of phrases
        quote_phrases = []
        for quote in quote_list:
            symbol = quote['StockSymbol']
            price = quote['LastTradePrice']
            name = tickers[symbol]
            quote_phrases.append("{name} is trading at ${price}".format(
                name=name, price=price))
        # Build the speech output sentence
        speech_output = "Here's how your stocks are doing, {}.".format(
            ", ".join(quote_phrases))
    except Exception as e:
        print("Failed to get quotes: {}".format(str(e)))
        return error_response()

    card_title = "Stock Report"
    session_attributes = {}
    should_end_session = True
    reprompt_text = None

    return build_response(
        session_attributes, 
        build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session)
    )


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
