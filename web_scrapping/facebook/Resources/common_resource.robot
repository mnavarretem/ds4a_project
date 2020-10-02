*** Settings ***
Library  SeleniumLibrary
Library  StringFormat
Library  ../Utility/actions.py
Library  ../Utility/scraper.py
Library  Collections

Variables   ../Locators/properties.yaml
Variables  ../Utility/variable.py

Resource  ../Resources/common_resource.robot

*** Variables ***
&{REACTIONS_DICT}

*** Keywords ***
Click Element By Text
    [Arguments]   ${TEXT_TO_CLICK}
    Wait Until Element Is Visible   xpath=//*[text()='${TEXT_TO_CLICK}']  10
    Set Focus To Element     xpath=//*[text()='${TEXT_TO_CLICK}']
    Click Element    xpath=//*[text()='${TEXT_TO_CLICK}']

Launch Browser
    Open Browser   ${URL}   ${BROWSER}
    Maximize Browser Window

Login Application
    [Arguments]   ${USER_VALUE}  ${PASSWORD_VALUE}
    Wait Until Element Is Visible  ${input_email}  10
    Input Text  ${input_email}  ${USER_VALUE}
    Input Text  ${input_password}  ${PASSWORD_VALUE}
    Click Element  ${login_button}

Launch Browser And Login
    [Arguments]  ${USER_MAIL}  ${PASSWORD}
    Launch Browser
    Login Application   ${USER_MAIL}  ${PASSWORD}
    Set Selenium Speed   ${SELENIUM_DELAY}

Wait And Click
    [Arguments]  ${ELEMENT_LOCATOR}
    Wait Until Element Is Visible  ${ELEMENT_LOCATOR}  10
    Click Element   ${ELEMENT_LOCATOR}

Get Post Reactions
    [Arguments]   ${PAGE}
    ${URLS}=  Get Posts Url  ${PAGE}
    Sleep  1s
    FOR    ${URL}    IN    @{URLS}
        #Log  ${URL}  console=yes
        Run Keyword If  "${URL[1]}"=="${None}"   Set To Dictionary  ${REACTIONS_DICT}  ${URL[0]}  ${None}
        ...  ELSE  Get Reactions  ${URL[0]}  ${URL[1]}
    END
    Write Reactions Json  ${PAGE}  ${REACTIONS_DICT}
	${REACTIONS_DICT} =  Create Dictionary

Get Reactions
    [Arguments]  ${POST_ID}  ${URL}
    Go To  ${URL}
    #Log  ${URL}  console=yes
    ${PASSED}=  Run Keyword And Return Status   Wait Until Element Is Visible  ${comments_container}  10
    ${COMMENTS_HTML} =  Run Keyword If     ${PASSED}   Get Element Attribute  ${comments_container}   innerHTML
        ...     ELSE   Reload Page And Get HTML

    #${COMMENTS_HTML} =  Get Element Attribute  ${comments_container}   innerHTML
    ${REACTIONS}=  Extract Reaction  ${COMMENTS_HTML}
    Log  ${POST_ID}:${REACTIONS}  console=yes
    Set To Dictionary  ${REACTIONS_DICT}    ${POST_ID}   ${REACTIONS}

Reload Page And Get HTML
    Reload Page
    ${PASSED}=  Run Keyword And Return Status   Wait Until Element Is Visible  ${comments_container}  10
    ${COMMENTS_HTML} =  Run Keyword If     ${PASSED}   Get Element Attribute  ${comments_container}   innerHTML
        ...     ELSE   Set Variable   EMPTY_TEXT
    [Return]   ${COMMENTS_HTML}

# To improve
Get Post Comments
    Open Comments
    ${HTML}=  Get Source
    Extract Comments  ${HTML}

# To improve
Open Comments
    Click Element By Text  Ahora no
    Execute JavaScript    window.scrollTo(0, 700)
    Wait Until Element Is Visible  ${comments_link}
    Set Focus To Element  ${comments_link}
    Wait And Click  ${comments_link}
    Wait Until Element Is Visible  ${relevant_comments}
    Set Focus To Element  ${relevant_comments}
    Wait And Click  ${relevant_comments}
    Set Focus To Element  ${all_comments}
    Wait And Click  ${all_comments}
    Wait And Click  ${more_comments}
    #   Click Element  ${LIKE}
    #   ${X} =  Get Text  ${comments}
    #   Log  ${X}  console=yes