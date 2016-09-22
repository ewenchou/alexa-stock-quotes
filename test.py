from lambda_function import get_quotes
import json


def main():
    intent = {}
    session = {}
    print json.dumps(get_quotes(intent, session), indent=2)


if __name__ == '__main__':
    main()
