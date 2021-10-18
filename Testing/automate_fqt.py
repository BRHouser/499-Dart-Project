import os
import sys
from datetime import datetime

# NEED TO CONTROL WHERE THE OUTPUT FILES OF THE ROBOT FILES GO


def createDoc(test, output):
    inTestCases = False
    inKeywords = False
    inVariables = False
    testlist = []
    variables = {}
    #output = '../Output/test_AED-player/17_10_2021-20_13_53/output.xml'
    test_script = open(test)
    output_doc = open(output + "/output.xml")
    important_words = []
    header = 0
    test = ""
    fail = False
    counter = 0
    check = 0
    for line in output_doc.readlines():
        if line.startswith("<kw") and checkElement(line):
            status = True
            if line.find("library") == -1:
                if len(important_words) == 0:
                    important_words.append(line)
                    header = 0
                    fail = False
                else:
                    if fail:
                        important_words[header] = "FAIL"
                    else:
                        important_words[header] = "PASS"
                    important_words.append(line)
                    fail = False
                    header = len(important_words) - 1
            test = line

        if line.startswith("<kw") and not checkElement(line):
            status = False

        if line.startswith('<status status="PASS"') and status:
            if counter - check == 2:
                check = counter
                continue
            else:
                important_words.append("PASS")
                check = counter
            
        if line.startswith('<status status="FAIL"') and status:
            fail = True
            if counter - check == 2:
                check = counter
                continue
            else:

                important_words.append("FAIL")
                check = counter

        counter = counter + 1
    if fail:
        important_words[header] = "FAIL"
    else:
        important_words[header] = "PASS"
    

    for line in test_script.readlines():

        if line.startswith("*** Variables ***"):
            inVariables = True
            continue
        if line.startswith("*** Test Cases ***"):
            inTestCases = True
            inVariables = False
            continue
        if line.startswith("*** Keywords ***"):
            inKeywords = True
            inTestCases = False
            continue


        if inVariables == True:
            if len(line.strip()) != 0:
                variables[line[0:line.find("}") + 1]] = line[line.find("}") + 2: len(line)].strip()
        if inTestCases == True:
            if line.startswith("Test"):
                testlist.append([line.strip()])
            if line.strip() != "" and line.startswith("   "):
                testlist[len(testlist) - 1].append([line.strip()])

        if inKeywords == True:
            if not line.startswith("   ") and line.strip() != "":
                for test in range(len(testlist)):
                    for num in range(1,len(testlist[test])):
                        if testlist[test][num][0].strip() == line.strip():
                            testx = test
                            testy = num
            
            if line.startswith("   ") and line.strip() != "":
                testlist[testx][testy].append(line.strip())

    x = 0
    make_output = open(output + "/output.adoc", "w+")
    make_output.write("*Execution Procedure*")
    make_output.write('\n[cols="17,4", width = "100%]')
    make_output.write("\n|===")

    if important_words[0] == "FAIL":
        fail = True
    else:
        fail = False

    for a in testlist:
        for b in a:
            if checkElement(b[0]):
                make_output.write("\n|" + convertRobotLine(b[0], variables))
                if not fail and important_words[x] == "FAIL":
                    fail = True
                if fail:
                    make_output.write("\n|FAIL\n")
                else:
                    make_output.write("\n|PASS\n")
                x = x + 1
            for c in range(1, len(b)):
                if checkElement(b[c]):
                    make_output.write("\n|" + convertRobotLine(b[c], variables))
                    x = x + 1

                    if not fail and important_words[x] == "FAIL":
                        fail = True
                    if fail:
                        make_output.write("\n|FAIL\n")
                    else:
                        make_output.write("\n|PASS\n")

    make_output.write("\n|===")
    

def convertRobotLine(element, variables):
    item = element
    if element.find("${") != -1:
        for key in variables:
            if str(key).strip() == element[element.find("${"): element.find("}") + 1].strip():
                item = item[0:element.find("${")] + str(variables[key]) + element[element.find("}") + 1:len(element)]
                break

    if element.find("Click Element") != -1:
        item = element[0:element.find("Element")] + element[element.find('@id=') + 5: len(element) - 2]
    elif element.find("Input Text") != - 1:
        item = "Input Text '" + element[element.find('"]') + 2:len(element)].strip() + "' into " + element[element.find("@id=") + 5:element.find('"]')]
    elif element.find("Clear Element Text") != -1:
        item = "Clear Text from " + element[element.find('@id=') + 5: len(element) - 2]
    elif element.find("executable_path") != -1:
        item = item[0:item.find("executable_path")]

    if item.find("ropdown") != -1:
        item = item[0:item.find("ropdown") - 1] +  item[item.find("ropdown") + 7: len(item)]
    if item.find("ChoosePlayer") != -1:
        item = item[0:item.find("ChoosePlayer") + 12] +  item[item.find("ChoosePlayer") + 13: len(item)]    
    while item.find("-") != -1:
        item = item[0:item.find("-")] + " " + item[item.find("-") + 1: len(item)]

    return item


def checkElement(element):
    if len(element) == 1:
        return False
    if element.find("Sleep") != -1:
        return False
    if element.find("Close Browser") != -1:
        return False
    if element.find("Wait") != -1:
        return False

    return True

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
        os.system("python -m robot -d  " + "../Output/" + test[0:test.find(".")] + "/" +  output_directory + "  " + test)
        createDoc(test, "../Output/" + test[0:test.find(".")] + "/" +  output_directory)
        os.system("asciidoctor-pdf " + "../Output/" + test[0:test.find(".")] + "/" +  output_directory + "/output.adoc")





if __name__ == '__main__':
    main()
