import os
import sys

# NEED TO CONTROL WHERE THE OUTPUT FILES OF THE ROBOT FILES GO


def main():
    project_directory = os.getcwd()
    project_directory = project_directory[0:project_directory.find("Project") + 7]    
    list_of_tests = os.listdir (project_directory + '/RobotScripts')
    selected_tests = []
    for input in sys.argv:
        if input == "automate_fqt.py":
            if len(sys.argv) == 1:
                selected_tests = list_of_tests
                break
            continue
        elif input == "all":
            selected_tests = list_of_tests
            break
        else:
            in_test = False
            for test in list_of_tests:
                if input in test:
                    in_test = True
                    continue
            if in_test:
                selected_tests.append(input)
            else:
                print(input + " is not a test")
                exit()
    for test in selected_tests:
        print(test)
    #os.system("python -m robot getData.robot ")


if __name__ == '__main__':
    main()
