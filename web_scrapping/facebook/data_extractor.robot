*** Settings ***
Variables  Utility/variable.py
Resource  Resources/common_resource.robot

Suite Setup  Launch Browser And Login   ${USER}    ${PASSWORD}
Suite Teardown  Close All Browsers

*** Test Cases ***
Open Facebook And Extract Offcorss Reactions
    [Tags]  facebook
    Get Post Reactions  offcorss

Open Facebook And Extract Epk Reactions
    Get Post Reactions  epk

Open Facebook And Extract Polito Reactions
    Get Post Reactions  PolitoColombia

Transform Data
    Convert Json To Csv