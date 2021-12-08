#Automated Test
#Author: Marshall Rosenhoover
#Created 11/1/21

*** Settings ***
Library           OperatingSystem
Library           Selenium2Library


*** Variables ***
${webpage}       http://192.168.1.177:5010/
${browser}       Chrome


*** Test Cases ***
Test AddPlayer
    Navigate to HomePage
    Test AddPlayer-FirstName Error
    Test AddPlayer-LastName Error
    Test AddPlayer-BullsEyes Error
    Add Player
    Test AddPlayer Error

Test EditPlayer
    Test EditPlayer-SelectNoPlayer Error
    Test EditPlayer-FirstName Error
    Test EditPlayer-LastName Error
    Test EditPlayer-BullsEyes Error
    Edit Player
    
Test DeletePlayer
    Test DeletePlayer-SelectNoPlayer Error
    Test Delete Player

*** Keywords ***
Navigate to HomePage
    Open Browser    browser=${browser}   executable_path=C:/Users/marsh/AppData/Local/Programs/Python/Python39/chromedriver.exe
    Maximize Browser Window
    Go To           ${webpage}

Test AddPlayer-FirstName Error
    Click Element   //*[@id="AddPlayer"]
    Input Text    //*[@id="LastName"]   Billy
    Input Text    //*[@id="NumberOfThrows"]   5
    Input Text    //*[@id="Bullseyes"]       2
    Click Element   //*[@id="Submit-Button"]
    Click Element   //*[@id="Okay-Button"]

Test AddPlayer-LastName Error
    Input Text    //*[@id="FirstName"]   Billy
    Input Text    //*[@id="NumberOfThrows"]   8
    Input Text    //*[@id="Bullseyes"]       3
    Click Element   //*[@id="Submit-Button"]
    Click Element   //*[@id="Okay-Button"]


Test AddPlayer-BullsEyes Error
    Input Text    //*[@id="FirstName"]   Billy
    Input Text    //*[@id="LastName"]   Bob
    Input Text    //*[@id="NumberOfThrows"]   10
    Input Text    //*[@id="Bullseyes"]       500
    Click Element   //*[@id="Submit-Button"]
    Click Element   //*[@id="Okay-Button"]


Add Player
    Input Text    //*[@id="FirstName"]   Billy  
    Input Text    //*[@id="LastName"]   Bob
    Input Text    //*[@id="NumberOfThrows"]   500
    Input Text    //*[@id="Bullseyes"]       21
    Click Element   //*[@id="Submit-Button"]


Test AddPlayer Error
    Wait Until Element Is Visible   //*[@id="AddPlayer"]
    Click Element   //*[@id="AddPlayer"]
    Wait Until Element Is Visible   //*[@id="FirstName"]
    Input Text    //*[@id="FirstName"]   Billy  
    Input Text    //*[@id="LastName"]   Bob
    Input Text    //*[@id="NumberOfThrows"]   500
    Input Text    //*[@id="Bullseyes"]       21
    Wait Until Element Is Visible   //*[@id="Submit-Button"]
    Click Element   //*[@id="Submit-Button"]
    Wait Until Element Is Visible   //*[@id="Okay-Button"]
    Click Element   //*[@id="Okay-Button"]
    Wait Until Element Is Visible   //*[@id="Close-Button"]
    Click Element   //*[@id="Close-Button"]


Test EditPlayer-SelectNoPlayer Error
    Click Element   //*[@id="Edit-Player"]
    Click Element   //*[@id="Edit-Button"]
    Click Element   //*[@id="Okay-Button"]


Test EditPlayer-FirstName Error
    Click Element   //*[@id="ChoosePlayerDropdown1"]
    Click Element   //*[@id="Billy Bob-dropdown"]
    Click Element   //*[@id="Edit-Button"]
    Clear Element Text      //*[@id="First_Name-row"]        
    Click Element   //*[@id="Edit-Button"]       
    Click Element   //*[@id="Okay-Button"]


Test EditPlayer-LastName Error
    Clear Element Text      //*[@id="Last_Name-row"]       
    Click Element   //*[@id="Edit-Button"]
    Click Element   //*[@id="Okay-Button"]


Test EditPlayer-BullsEyes Error
    Input Text      //*[@id="Total_Number_of_BullsEyes-row"]     11111111111111    
    Click Element   //*[@id="Edit-Button"]
    Click Element   //*[@id="Okay-Button"]


Edit Player
    Input Text      //*[@id="First_Name-row"]   Graham
    Input Text      //*[@id="Last_Name-row"]    Chase
    Input Text      //*[@id="Total_Number_of_Throws-row"]    100000
    Input Text      //*[@id="Total_Number_of_BullsEyes-row"]   12345    
    Click Element   //*[@id="Edit-Button"]
    Sleep   1

Test DeletePlayer-SelectNoPlayer Error
    Click Element   //*[@id="Delete-Player"]
    Click Element   //*[@id="Delete-Button"]
    Click Element   //*[@id="Okay-Button"]

Test Delete Player
    Click Element   //*[@id="ChoosePlayerDropdown0"]
    Click Element   //*[@id="Graham Chase-dropdown"]
    Click Element   //*[@id="Delete-Button"]
    Sleep   1

    
    Close Browser   
