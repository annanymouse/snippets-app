# # Store an item using fully qualified names
# python snippets.py --type "put" --name "list" --snippet "A sequence of things - created using []"

# # Store an item using abbreviations
# python snippets.py -t "put" -n "list" -s "A sequence of things - created using []"

# # Use positional rather than optional arguments
# python snippets.py put list "A sequence of things - created using []"

import argparse
import logging
import sys

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

def update(name, snippet):
    """
    Updates the information in a snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""

def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    arguments = parser.parse_args(sys.argv[1:])

if __name__ == "__main__":
    main()