import logger

# CAUTION setting debug to False will result in actual purchases
debug = False
run_tests = False
# Set this to True by passing cookie_arg command line argument
rewrite_cookies = False

# Command line arguments
cookie_arg = '-c'

# Credit card number and security code
ccn = ''
sc = ''
month = ''
year = ''
email = ''
password = ''


def read_profile():
    logger.log("Reading profile")
    global ccn, sc, month, year, email, password
    file = open('profile.txt', 'r')
    ccn = file.readline()
    sc = file.readline()
    month = file.readline()
    year = file.readline()
    email = file.readline()
    password = file.readline()
