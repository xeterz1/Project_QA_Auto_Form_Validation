*** Settings ***
Library           SeleniumLibrary
Suite Teardown    Close All Browsers

*** Variables ***
${URL}        http://localhost:8000/
${BROWSER}    chrome

*** Test Cases ***
Happy Path – user sees success message
    [Tags]    acceptance    happy
    Open Browser    ${URL}    ${BROWSER}
    Input Text      id=name      Akram
    Input Text      id=email     akram@example.com
    Input Text      id=age       25
    Input Text      id=message   Hello
    Click Button    css:button[type="submit"]
    Wait Until Element Is Visible    id=formMessage    5s
    Element Should Contain           id=formMessage    Form submitted successfully

Age Above 120 – backend rejects with message
    [Tags]    acceptance    server
    Open Browser    ${URL}    ${BROWSER}
    Input Text      id=name      Akram
    Input Text      id=email     akram@example.com
    Input Text      id=age       121
    Input Text      id=message   Hi
    Click Button    css:button[type="submit"]
    Wait Until Element Is Visible    id=formMessage    5s
    Element Should Contain           id=formMessage    Invalid age
