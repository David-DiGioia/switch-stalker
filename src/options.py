import logger

# CAUTION setting debug to False will result in actual purchases
debug = True
run_tests = False
rewrite_cookies = False

# Credit card number and security code
ccn = ''
sc = ''

email = ''
password = ''

def read_profile():
    logger.log("Reading profile")
    global ccn, sc
    file = open('profile.txt', 'r')
    ccn = file.readline()
    sc = file.readline()
    email = file.readline()
    password = file.readline()
