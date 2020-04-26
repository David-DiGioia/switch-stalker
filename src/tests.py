import websites
import task
import logger
import time

target_url_in_stock = "https://www.target.com/p/super-mario-maker-2-nintendo-switch/-/A-54498967"
target_url_no_stock = "https://www.target.com/p/nintendo-switch-with-neon-blue-and-neon-red-joy-con/-/A-77464001"


# Convert boolean value into pass/fail string
def pf(bool):
    if bool:
        return 'PASS'
    else:
        return 'FAIL'


def run_tests():
    logger.log("TESTS BEGIN----------------------------------------------")
    target1 = websites.Target(target_url_in_stock, True)
    t1 = task.Task(target1)
    expected1 = True
    actual1 = target1.in_stock(t1.driver, t1.timeout)
    logger.log(f"Target in stock:\t{pf(expected1 == actual1)}")
    target1.add_to_cart(t1.driver, t1.timeout)
    time.sleep(10000)
    t1.close()

    target2 = websites.Target(target_url_no_stock, True)
    t2 = task.Task(target2)
    expected2 = False
    actual2 = target2.in_stock(t2.driver, t2.timeout)
    logger.log(f"Target no stock:\t{pf(expected2 == actual2)}")
    t2.close()

    logger.log("TESTS END------------------------------------------------")
