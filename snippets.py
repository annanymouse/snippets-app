import logging

#set the log output file, and the log level
loggin.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """
    Store a snippet with an associated name.
    Returns the name and the snippet.
    """
    loggin.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet

def get(name):
    """
    Retrieve the snippet with a given name.
    If there is no such snippet, return a message that snippet does not exist.
    Returns the snipppet
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""