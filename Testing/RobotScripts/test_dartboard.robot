*** Settings ***
#Documentation     Example using the space separated format.
Library           OperatingSystem
Library           Selenium2Library

*** Variables ***
${webpage}       http://192.168.1.179:5010/scorekeeper
${browser}       Chrome


*** Test Cases ***
Test Dartboard
    Navigate to Scorekeeper
    Test Dartboard


*** Keywords ***
Navigate to Scorekeeper
    Open Browser    browser=${browser}   executable_path=C:/Users/marsh/AppData/Local/Programs/Python/Python39/chromedriver.exe
    Maximize Browser Window
    Go To           ${webpage}

Test Dartboard
    Hover Over Each Element
    Click Each Element


Hover Over Each Element
    Mouse Over   id=square1
    Mouse Over   id=square2
    Mouse Over   id=square3
    Mouse Over   id=square4
    Mouse Over   id=square5
    Mouse Over   id=square6
    Mouse Over   id=square7
    Mouse Over   id=square8
    Mouse Over   id=square9
    Mouse Over   id=square10
    Mouse Over   id=square11
    Mouse Over   id=square12
    Mouse Over   id=square13
    Mouse Over   id=square14
    Mouse Over   id=square15
    Mouse Over   id=square16
    Mouse Over   id=square17
    Mouse Over   id=square18
    Mouse Over   id=square19
    Mouse Over   id=square20
    Mouse Over   id=square21
    Mouse Over   id=square22
    Mouse Over   id=square23
    Mouse Over   id=square24
    Mouse Over   id=square25
    Mouse Over   id=square26
    Mouse Over   id=square27
    Mouse Over   id=square28
    Mouse Over   id=square29
    Mouse Over   id=square30
    Mouse Over   id=square31
    Mouse Over   id=square32
    Mouse Over   id=square33
    Mouse Over   id=square34
    Mouse Over   id=square35
    Mouse Over   id=square36
    Mouse Over   id=square37
    Mouse Over   id=square38
    Mouse Over   id=square39
    Mouse Over   id=square40
    Mouse Over   id=square41
    Mouse Over   id=square42
    Mouse Over   id=square43
    Mouse Over   id=square44
    Mouse Over   id=square45
    Mouse Over   id=square46
    Mouse Over   id=square47
    Mouse Over   id=square48
    Mouse Over   id=square49
    Mouse Over   id=square50
    Mouse Over   id=square51
    Mouse Over   id=square52
    Mouse Over   id=square53
    Mouse Over   id=square54
    Mouse Over   id=square55
    Mouse Over   id=square56
    Mouse Over   id=square57
    Mouse Over   id=square58
    Mouse Over   id=square59
    Mouse Over   id=square60
    Mouse Over   id=square61
    Mouse Over   id=square62
    Mouse Over   id=square63
    Mouse Over   id=square64
    Mouse Over   id=square65
    Mouse Over   id=square66
    Mouse Over   id=square67
    Mouse Over   id=square68
    Mouse Over   id=square69
    Mouse Over   id=square70
    Mouse Over   id=square71
    Mouse Over   id=square72
    Mouse Over   id=square73
    Mouse Over   id=square74
    Mouse Over   id=square75
    Mouse Over   id=square76
    Mouse Over   id=square77
    Mouse Over   id=square78
    Mouse Over   id=square79
    Mouse Over   id=square80
    Mouse Over   id=square81
    Mouse Over   id=square82

Click Each Element
    Click Element   id=square1
    Click Element At Coordinates    id=square2   100   100
    Click Element   id=square3
    Click Element   id=square4
    Click Element   id=square5
    Click Element   id=square6
    Click Element   id=square7
    Click Element   id=square8
    Click Element   id=square9
    Click Element   id=square10
    Click Element   id=square11
    Click Element   id=square12
    Click Element   id=square13
    Click Element   id=square14
    Click Element   id=square15
    Click Element   id=square16
    Click Element   id=square17
    Click Element   id=square18
    Click Element   id=square19
    Click Element   id=square20
    Click Element   id=square21
    Click Element   id=square22
    Click Element   id=square23
    Click Element   id=square24
    Click Element   id=square25
    Click Element   id=square26
    Click Element   id=square27
    Click Element   id=square28
    Click Element   id=square29
    Click Element   id=square30
    Click Element   id=square31
    Click Element   id=square32
    Click Element   id=square33
    Click Element   id=square34
    Click Element   id=square35
    Click Element   id=square36
    Click Element   id=square37
    Click Element   id=square38
    Click Element   id=square39
    Click Element   id=square40
    Click Element   id=square41
    Click Element   id=square42
    Click Element   id=square43
    Click Element   id=square44
    Click Element   id=square45
    Click Element   id=square46
    Click Element   id=square47
    Click Element   id=square48
    Click Element   id=square49
    Click Element   id=square50
    Click Element   id=square51
    Click Element   id=square52
    Click Element   id=square53
    Click Element   id=square54
    Click Element   id=square55
    Click Element   id=square56
    Click Element   id=square57
    Click Element   id=square58
    Click Element   id=square59
    Click Element   id=square60
    Click Element   id=square61
    Click Element   id=square62
    Click Element   id=square63
    Click Element   id=square64
    Click Element   id=square65
    Click Element   id=square66
    Click Element   id=square67
    Click Element   id=square68
    Click Element   id=square69
    Click Element   id=square70
    Click Element   id=square71
    Click Element   id=square72
    Click Element   id=square73
    Click Element   id=square74
    Click Element   id=square75
    Click Element   id=square76
    Click Element   id=square77
    Click Element   id=square78
    Click Element   id=square79
    Click Element   id=square80
    Click Element   id=square81
    Click Element   id=square82
    Close Browser   