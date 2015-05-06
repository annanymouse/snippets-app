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
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("insert into snippets values (%s, %s)", ((name, snippet)))
    except psycopg2.IntegrityError as e:
        with connection, connection.cursor() as cursor:
            connection.rollback()
            cursor.execute("update snippets set message=%s where keyword=%s", (snippet, name))   
    logging.debug("Snippet stored successfully.")
    return name, snippet

def get(name):
    """Retrieve the snippet with a given name."""
    logging.info("Getting a snippet with name: {!r}".format(name))
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        row = cursor.fetchone()
    logging.debug("Snippet retrieved successfully.")
    try:
        return row[0]
    except TypeError:
        print("There is no snippet with that name.")
        
def catalog():
    """Retrieve all the names(keywords) in the database."""
    logging.info("Getting all snippet names in the database...")
    with connection, connection.cursor() as cursor:
        cursor.execute("select keyword from snippets")
        rows = cursor.fetchall()
    logging.debug("Snippet names retrieved successfully.")
    #return "{}".format("\n".join([row for row in rows]))
    return rows
#     try:
#         return "\n".join(["{}".format([row for row in rows])
#     except TypeError:
#         print("What's going on? There are no snippet names.")


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
    get_parser = subparsers.add_parser("get", help="Get a snippet")
    get_parser.add_argument("name", help="The name of the snippet to get")
    
    #Subparser for the catalog command
    logging.debug("Construcing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Catalog of all snippet names")
    
    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet)) # {!r} gives us the __repr__
    elif command == "catalog":
        names = catalog()
        print("Here are all the snippet names:")
        # generator expression used inside join to print the results of the rows from cursor.fetchall() nicely
        print("{}".format('\n'.join(name[0] for name in names)))

if __name__=="__main__":
    main()