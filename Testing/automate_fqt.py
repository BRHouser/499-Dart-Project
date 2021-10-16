import os
import sys
from datetime import datetime

# NEED TO CONTROL WHERE THE OUTPUT FILES OF THE ROBOT FILES GO


def main():
    project_directory = os.getcwd()
    project_directory = project_directory[0:project_directory.find("Project") + 7]    
    list_of_tests = os.listdir (project_directory + '/Testing/RobotScripts')
    #list_of_tests.remove("resources")
    selected_tests = []
    for input in sys.argv:
        if input.endswith("automate_fqt.py"):
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

    os.chdir(project_directory + "/Testing/RobotScripts")
    output_directory = datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
    for test in selected_tests:
        print(test)
        os.system("python -m robot -d  " + "../Output/" + test[0:test.find(".")] + "/" +  output_directory + "  " + test)


if __name__ == '__main__':
    main()
