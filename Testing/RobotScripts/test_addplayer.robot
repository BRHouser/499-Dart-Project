*** Settings ***
#Documentation     Example using the space separated format.
Library           OperatingSystem
Library           Selenium2Library


*** Variables ***
${webpage}       http://192.168.1.179:5010/
${browser}       Chrome


*** Test Cases ***
Test AddPlayer
    Navigate to HomePage
    Test FirstName Error
    Test LastName Error
    Test BullsEyes Error
    Add Player
    Test AddPlayer Error

*** Keywords ***
Navigate to HomePage
    Open Browser    browser=${browser}   executable_path=C:/Users/marsh/AppData/Local/Programs/Python/Python39/chromedriver.exe
    Maximize Browser Window
    Go To           ${webpage}

Test FirstName Error
    Click Element   //*[@id="AddPlayer"]
    Input Text    //*[@id="LastName"]   Billy
    Input Text    //*[@id="NumberOfThrows"]   5
    Input Text    //*[@id="Bullseyes"]       2
    Click Element   //*[@id="Submit-Button"]
    Click Element   //*[@id="Okay-Button"]

Test LastName Error
    Input Text    //*[@id="FirstName"]   Billy
    Input Text    //*[@id="NumberOfThrows"]   8
    Input Text    //*[@id="Bullseyes"]       3
    Click Element   //*[@id="Submit-Button"]
    Click Element   //*[@id="Okay-Button"]

Test BullsEyes Error
    Input Text    //*[@id="FirstName"]   Billy
    Input Text    //*[@id="LastName"]   Bob
    Input Text    //*[@id="NumberOfThrows"]   100
    Input Text    //*[@id="Bullseyes"]       50
    Click Element   //*[@id="Submit-Button"]
    Click Element   //*[@id="Okay-Button"]

Add Player
    Input Text    //*[@id="FirstName"]   Billy  
    Input Text    //*[@id="LastName"]   Bob
    Input Text    //*[@id="NumberOfThrows"]   500
    Input Text    //*[@id="Bullseyes"]       21
    Click Element   //*[@id="Submit-Button"]

Test Add Player Error
    Wait Until Element Is Visible   //*[@id="AddPlayer"]
    Click Element   //*[@id="AddPlayer"]
    Wait Until Element Is Visible   //*[@id="FirstName"]
    Input Text    //*[@id="FirstName"]   Billy  
    Input Text    //*[@id="LastName"]   Bob
    Input Text    //*[@id="NumberOfThrows"]   500
    Input Text    //*[@id="Bullseyes"]       21
    Click Element   //*[@id="Submit-Button"]
    Click Element   //*[@id="Okay-Button"]
    Close Browser   
