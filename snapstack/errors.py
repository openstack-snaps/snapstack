'''
Exception classes for those times when things don't go your way.

'''


class InfraFailure(Exception):
    '''
    Typically indicates an error in the Infrastructure around testing
    a snap, or an error in the test runner itself.

    For example, this would get raised if an Exception gets raises
    while setting up the snap base before running tests for a speciifc
    snap.

    '''
    pass


class TestFailure(Exception):
    '''
    Handy Exception to raise if there is a failure while running tests
    for a snap.

    '''
    pass
