*** Settings ***
Variables  Utility/variable.py
Resource  Resources/common_resource.robot

Suite Setup  Launch Browser And Login   ${USER}    ${PASSWORD}
Suite Teardown  Close All Browsers

*** Test Cases ***
Open Facebook And Extract Reactions
    [Tags]  facebook
    Get Post Reactions  offcorss
    Get Post Reactions  epk
    Get Post Reactions  PolitoColombia
