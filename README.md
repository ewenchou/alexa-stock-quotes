# Alexa Stock Quotes Skill

A simple Alexa skill that reads stock quotes for a predefined list of ticker symbols. The skill is written in Python and runs on AWS Lambda.

## Setup

1. Clone this repository
2. Customize the `STOCK_TICKERS` and `APP_ID` variables in `lambda_function.py`
3. Copy/Paste `lambda_function.py` or upload as a zip file to your AWS Lambda function.
4. Configure your Alexa skill in the Amazon developer portal.
5. Test the skill by launching it with your invocation name. For example, "Alexa, open Stock Report".

You can read more about it on my [blog](https://ewenchou.github.io/blog/2016/04/08/asking-for-stocks/)
