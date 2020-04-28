import tests
import task
import websites
import options
import logger
import sys

# TARGET
# Legit
target_neon_url = 'https://www.target.com/p/nintendo-switch-with-neon-blue-and-neon-red-joy-con/-/A-77464001'
target_grey_url = 'https://www.target.com/p/nintendo-switch-with-gray-joy-con/-/A-77464002'
# Debug
target_url_in_stock = "https://www.target.com/p/super-mario-maker-2-nintendo-switch/-/A-54498967"

#SMYTHS
smyth_in_stock_url = 'https://www.smythstoys.com/uk/en-gb/video-games-and-tablets/nintendo-gaming/nintendo-switch/nintendo-switch-games/super-mario-party-nintendo-switch/p/168632'
smyth_no_stock_url = 'https://www.smythstoys.com/uk/en-gb/video-games-and-tablets/nintendo-gaming/nintendo-switch/nintendo-switch-consoles/nintendo-switch-animal-crossing-limited-edition-console/p/187118'


def main():
    # Command line arguments
    if len(sys.argv) >= 2 and sys.argv[1] == options.cookie_arg:
        options.rewrite_cookies = True

    logger.init_logger()
    options.read_profile()
    if options.run_tests and options.debug:
        tests.run_tests()

    tasks = []

    f = open('websites.txt', 'r')
    lines = f.readlines()
    for line in lines:
        if len(line) < 2:
            continue
        if line.split()[0] == 'SmythsToys':
            smyths_toys = websites.SmythsToys(line.split()[1])
            t = task.Task(smyths_toys)
            t.start()
            tasks.append(t)
        elif line.split()[0] == 'Target':
            target = websites.Target(line.split()[1])
            t = task.Task(target)
            t.start()
            tasks.append(t)


if __name__ == "__main__":
    main()
