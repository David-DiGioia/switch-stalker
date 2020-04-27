import tests
import task
import websites
import options

target_neon_url = 'https://www.target.com/p/nintendo-switch-with-neon-blue-and-neon-red-joy-con/-/A-77464001'
target_url_in_stock = "https://www.target.com/p/super-mario-maker-2-nintendo-switch/-/A-54498967"


def main():
    if options.run_tests and options.debug:
        tests.run_tests()

    target_neon = websites.Target(target_url_in_stock)
    task1 = task.Task(target_neon)
    task1.start()

if __name__ == "__main__":
    main()
