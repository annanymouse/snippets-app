# # Store an item using fully qualified names
# python snippets.py --type "put" --name "list" --snippet "A sequence of things - created using []"

# # Store an item using abbreviations
# python snippets.py -t "put" -n "list" -s "A sequence of things - created using []"

# # Use positional rather than optional arguments
# python snippets.py put list "A sequence of things - created using []"

import argparse
import logging
import sys
import psycopg2

#set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    command = "insert into snippets values (%s, %s)"
    cursor.execute(command, (name, snippet))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet

def get(name):
    """Retrieve the snippet with a given name."""
    logging.info("Getting a snippet with name: {!r}".format(name))
    cursor = connection.cursor()
    #command = "select message from snippets where keyword = %s"
    #cur.execute("SELECT * FROM test WHERE id = %s", (3,))
    cursor.execute("select message from snippets where keyword = %s", (name,))
    row = cursor.fetchone()
    connection.commit()
    logging.debug("Snippet retrieved successfully.")
    try:
        if row!="":
            return row[0]
    except TypeError:
        print("There is no snippet with that name.")

# def trash(name, snippet):
#     """
#     Trash a snippet with an associated name.
#     """
#     logging.error("FIXME: Unimplemented - get({!r})".format(name))
#     return "The message has been removed."

# def seek(name, snippet):
#     """
#     Returns all messages containing certain words.
#     """
#     logging.error("FIXME: Unimplemented - get({!r})".format(name))
#     return ""

# def update(name, snippet):
#     """
#     Updates the information in a snippet.
#     """
#     logging.error("FIXME: Unimplemented - get({!r})".format(name))
#     return ""

def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    #Subparser for the put command
    logging.debug("Construcing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    
    #Subparser for the get command
    logging.debug("Construcing get subparser")
    put_parser = subparsers.add_parser("get", help="Get a snippet")
    put_parser.add_argument("name", help="The name of the snippet to get")

    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))

if __name__=="__main__":
    main()