from lambda_function import get_quotes
import json


def main():   
    print json.dumps(get_quotes(), indent=2)


if __name__ == '__main__':
    main()
