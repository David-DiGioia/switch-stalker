import tests
import task
import websites

# CAUTION setting debug to False will result in actual purchases
debug = False
run_tests = False

target_neon_url = 'https://www.target.com/p/nintendo-switch-with-neon-blue-and-neon-red-joy-con/-/A-77464001'

def main():
    if run_tests and debug:
        tests.run_tests()

    target_neon = websites.Target(target_neon_url)
    task1 = task.Task(target_neon)
    task1.start()

if __name__ == "__main__":
    main()
