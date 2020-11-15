*** Settings ***
Variables  Utility/variable.py
Resource  Resources/common_resource.robot
Library  Process

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
    Convert Json To Csv  offcorss
    Convert Json To Csv  epk
    Convert Json To Csv  PolitoColombia

Concatenate And Get Scores
     ${result}=  run process  python  Utility/concatenate.py
     Should be equal as integers  ${result.rc}   0
     Log  ${result.stdout}  console=yes
     Log  ${result.stderr}  console=yes
     ${result}=  run process  python  Utility/get_score.py
     Should be equal as integers  ${result.rc}   0
     Log  ${result.stdout}  console=yes
     Log  ${result.stderr}  console=yes
