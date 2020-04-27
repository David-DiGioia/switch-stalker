import tests
import task
import websites
import options
import logger

# Legit
target_neon_url = 'https://www.target.com/p/nintendo-switch-with-neon-blue-and-neon-red-joy-con/-/A-77464001'
target_grey_url = 'https://www.target.com/p/nintendo-switch-with-gray-joy-con/-/A-77464002'

# Debug
target_url_in_stock = "https://www.target.com/p/super-mario-maker-2-nintendo-switch/-/A-54498967"


def main():
    logger.init_logger()
    options.read_profile()
    if options.run_tests and options.debug:
        tests.run_tests()

    target_neon = websites.Target(target_neon_url)
    task1 = task.Task(target_neon)
    task1.start()

    # target_grey = websites.Target(target_grey_url)
    # task2 = task.Task(target_grey)
    # task2.start()

    # if options.debug:
    #     target_in_stock = websites.Target(target_url_in_stock)
    #     task3 = task.Task(target_in_stock)
    #     task3.start()


if __name__ == "__main__":
    main()
