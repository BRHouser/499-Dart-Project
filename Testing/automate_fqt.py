import os
import sys
from datetime import datetime

#Script for automated testing
#Author: Marshall Rosenhoover
#Created 10/10/21, edited 11/30/21

start_time = 0
end_time = 0
test_name = "TEST NAME"
date = datetime.now().strftime("%m/%d/%Y")
traceability = "NONE"
preparations = "NONE"


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
        bob = line
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

        if line.find('creenshot') != -1:
            status = False
            continue

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
    make_output.write("= " + test_name + "|===\n\n|===\n")
    make_output.write('|{set:cellbgcolor:#01456C}+++\n<strong><color rgb="#FFFFFF">Information</color></strong>+++|\n')
    make_output.write('|{set:cellbgcolor:#FFFFFF}Date: '+ date +'\n')
    make_output.write('.2+|Witness(es):\n\n')
    make_output.write('|Operator:  Robot\n')
    make_output.write('|Procedure Start Time:  ' + str(start_time) + '\n')
    make_output.write('\nProcedure Stop Time: ' + str(end_time))
    if fail:
        make_output.write('|Run Assessment: +++<strong><color rbg="#CC0000">FAIL</color></strong>+++')
    else:
        make_output.write('|Run Assessment: +++<strong><color rbg="#00BB00">PASS</color></strong>+++')
    make_output.write('\n|Feature Traceability: ' + traceability)
    make_output.write('|Notes/Pre-Test Preparations: '+ preparations +'\n')
    make_output.write("|===\n\n")
    make_output.write('\n[cols="2,11,10,5", width = "100%]')
    make_output.write("\n|===")
    make_output.write('\n|{set:cellbgcolor:#01456C}|+++\n<strong><color rgb="#FFFFFF">EXECUTION PROCEDURE</color></strong>+++\n|+++<strong><color rgb="#FFFFFF">EXPECTED RESULT</color></strong>+++\n|+++<strong><color rgb="#FFFFFF">SUCESSFULLY EXECUTED</color></strong>+++\n')
    if important_words[0] == "FAIL":
        fail = True
    else:
        fail = False

    main_test = 0
    secondary_test = 0
    third_test = 0
    fail_rest = False
    for a in testlist:
        secondary_test = 0
        third_test = 0
        main_test = main_test + 1
        for b in a:
            third_test = 0
            if checkElement(b[0]):
                secondary_test = secondary_test + 1
                make_output.write("\n|{set:cellbgcolor:#FFFFFF}" + str(main_test) + "." + str(secondary_test) +  "." + str(third_test))
                make_output.write("\n|TEST SECTION: " + b[0] + "|\n")
                if fail_rest == False:
                    if important_words[x] == "FAIL":
                        fail = True
                if fail or fail_rest:
                #    make_output.write("\n|FAIL\n")
                    if fail_rest == False:
                        fail = False
                #else:
                    #make_output.write("\n|PASS\n")
                
                make_output.write("|\n")
                x = x + 1
            for c in range(1, len(b)):
                if checkElement(b[c]):
                    third_test = third_test + 1
                    make_output.write("\n|" + str(main_test) + "." + str(secondary_test) +  "." + str(third_test))
                    make_output.write("\n|" + convertRobotLine(b[c], variables))
                    
                    if fail_rest:
                        make_output.write("\n|FAIL\n")
                        continue

                    if important_words[x] == "FAIL":
                        fail = True
                    if fail:
                        make_output.write("\n|DID NOT SUCCEED IN PERFORMING TASK")
                        make_output.write("\n|No\n")
                        fail_rest = True
                    else:
                        make_output.write("\n|"+ convertPASS(b[c], variables))
                        make_output.write("\n|Yes\n")
                    x = x + 1 


    make_output.write("\n|===")
    
def convertPASS(element, variables):
    item = element
    if item.find("${") != -1:
        for key in variables:
            if str(key).strip() == item[item.find("${"): item.find("}") + 1].strip():
                item = item[0:item.find("${")] + str(variables[key]) + item[item.find("}") + 1:len(item)]
                break

    if item.find("Click Element") != -1:
        item = item[item.find('@id=') + 5: len(item) - 2] + " was clicked"
    elif item.find("Input Text") != - 1:
        item = "'" + item[item.find('"]') + 2:len(item)].strip() + "' was inputted into " + item[item.find("@id=") + 5:item.find('"]')]
    elif item.find("Clear Element Text") != -1:
        item = "Text was cleared from " + item[item.find('@id=') + 5: len(item) - 2]
    elif item.find("executable_path") != -1:
        item = "Chrome was opened"

    if item.find("ropdown") != -1:
        item = item[0:item.find("ropdown") - 1] +  item[item.find("ropdown") + 7: len(item)]
    if item.find("ChoosePlayer") != -1:
        item = item[0:item.find("ChoosePlayer") + 12] +  item[item.find("ChoosePlayer") + 13: len(item)]
    while item.find("-") != -1:
        item = item[0:item.find("-")] + " " + item[item.find("-") + 1: len(item)]

    return item


def convertRobotLine(element, variables):
    item = element
    if item.find("${") != -1:
        for key in variables:
            if str(key).strip() == item[item.find("${"): item.find("}") + 1].strip():
                item = item[0:item.find("${")] + str(variables[key]) + item[item.find("}") + 1:len(item)]
                break

    if item.find("Click Element") != -1:
        item = item[0:item.find("Element")] + item[item.find('@id=') + 5: len(item) - 2]
    elif item.find("Input Text") != - 1:
        item = "Input Text '" + item[item.find('"]') + 2:len(item)].strip() + "' into " + item[item.find("@id=") + 5:item.find('"]')]
    elif item.find("Clear Element Text") != -1:
        item = "Clear Text from " + item[item.find('@id=') + 5: len(item) - 2]
    elif item.find("executable_path") != -1:
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

def setTestInfo(testname):
    global test_name
    global traceability
    global preparations
    test_info = open("resources/" + testname + ".txt")
    for line in test_info.readlines():
        if line.startswith("Test Name"):
            test_name = line[line.find(":") + 2: len(line)]
        elif line.startswith("Test Traceability"):
            traceability = line[line.find(":") + 2: len(line)]
        elif line.startswith("Pre-Test Preparations"):
            preparations = line[line.find(":") + 2: len(line)]


def main():
    project_directory = os.getcwd()
    project_directory = project_directory[0:project_directory.find("Project") + 7]    
    list_of_tests = os.listdir (project_directory + '/Testing/RobotScripts')
    list_of_tests.remove("resources")
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
    directory = datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
    os.chdir(project_directory + "/Testing/RobotScripts")
    global start_time
    global end_time
    for test in selected_tests:
        setTestInfo(test[0:test.find(".")])
        start_time = datetime.now().strftime("%H:%M:%S")
        os.system("python -m robot -d  " + "../Output/" + test[0:test.find(".")] + "/" +  directory + "  " + test)
        end_time = datetime.now().strftime("%H:%M:%S")
        createDoc(test, "../Output/" + test[0:test.find(".")] + "/" +  directory)
        os.system("asciidoctor-pdf " + "../Output/" + test[0:test.find(".")] + "/" +  directory + "/output.adoc")





if __name__ == '__main__':
    main()
