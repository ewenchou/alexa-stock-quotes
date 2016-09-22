# Alexa Stock Quotes Skill

A simple Alexa skill that reads stock quotes for a predefined list of ticker symbols. The skill is written in Python and runs on AWS Lambda.

## Setup

For more information on how to setup your AWS Lambda function and Alexa Skill, visit my [blog post](https://ewenchou.github.io/blog/2016/04/08/asking-for-stocks/).

1. Clone this repository

        git clone https://github.com/ewenchou/alexa-stock-quotes.git

2. Customize the `TICKERS` and `APP_ID` variables in `lambda_function.py`

3. Install requirements in local directory:

        pip install -r requirements.txt -t .

4. Create a zip file with the following contents:

        googlefinance
        googlefinance-<version>.dist-info
        lambda_function.py

5. Configure your Alexa skill in the Amazon developer portal.

6. Test the skill by launching it with your invocation name. For example, "Alexa, open Stock Report".

## Testing

There is a simple test script that you can run after you've done Steps 1 to 3 above.

        python test.py

*Note: Tested using Python 2.7.12 on Ubuntu and `googlefinance` version 0.7*