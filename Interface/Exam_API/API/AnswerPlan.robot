*** Settings ***
Library           RequestsLibrary
Library           Collections
Variables         ../Common/Variables/Base.py

*** Keyword ***
GET/answerPlans
    [Documentation]    答题计划
    Create Session    exam    ${url}
    ${header}    Create Dictionary    Authorization    ${token}
    ${resp}=    Get Request    exam    /answerPlans    headers=${header}
    Should Be Equal As Strings    ${resp.status_code}    200
    ${data}    to json    ${resp.content}
    [Return]    ${data}
