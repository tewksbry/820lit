#Author: Samuel Resendez


import requests

def main():
    while(True):
        r = requests.get('https://lit820.herokuapp.com/litControl/get_pattern/')
        print r.text

main()
