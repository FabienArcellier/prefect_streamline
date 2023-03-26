import os

import alfred

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))


@alfred.command("tests", help="workflow to execute all automatic tests")
def tests():
    """
    workflow to execute all automatic tests

    >>> $ alfred tests
    """
    alfred.invoke_command('tests:units')
    alfred.invoke_command('tests:integrations')
    alfred.invoke_command('tests:acceptances')


@alfred.command("tests:acceptances", help="execute unit tests")
def tests__acceptances():
    """

    >>> $ alfred tests:acceptances
    """
    pytest = alfred.sh("pytest")
    os.chdir(ROOT_DIR)
    alfred.run(pytest, ['tests/acceptances'])

@alfred.command("tests:integrations", help="execute integrations tests")
def tests__integrations():
    """

    >>> $ alfred tests:integrations
    """
    pytest = alfred.sh("pytest")
    os.chdir(ROOT_DIR)
    alfred.run(pytest, ['tests/integrations'])

@alfred.command("tests:units", help="execute unit tests")
def tests__units():
    """

    >>> $ alfred tests:units
    """
    pytest = alfred.sh("pytest")
    os.chdir(ROOT_DIR)
    alfred.run(pytest, ['tests/units'])

