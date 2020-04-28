import logger

# CAUTION setting debug to False will result in actual purchases
debug = False
run_tests = False
rewrite_cookies = False

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
    # print("20" + year[:-1] + "AFTER")
