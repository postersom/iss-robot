import sys
import json

def main():
    response = { 
        "status": "OK",
        "error_message": "Return value from ODC"
    }
    return json.dumps(response)


if __name__ == '__main__':
    print(main())
