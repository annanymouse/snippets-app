import logging

#set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """
    Store a snippet with an associated name.
    Returns the name and the snippet.
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet

def get(name):
    """
    Retrieve the snippet with a given name.
    If there is no such snippet, return a message that snippet does not exist.
    Returns the snipppet
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""

def trash(name, snippet):
    """
    Trash a snippet with an associated name.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return "The message has been removed."

def seek(name, snippet):
    """
    Returns all messages containing certain words.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""