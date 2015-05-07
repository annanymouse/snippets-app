# # Use positional rather than optional arguments
# python snippets.py put list "A sequence of things - created using []"

import argparse
import logging
import sys
import psycopg2

arguments = {}

#set the log output file, and the log level (this is the initialization)
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet, hide):
#     print("{}: {}, {}".format(name, snippet, hide))
    """Store a snippet with an associated name."""
#     print(arguments)
    logging.info("Storing snippet {!r}: {!r}.".format(name, snippet))
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("insert into snippets values (%s, %s, %s)", (name, snippet, hide,))
    except psycopg2.IntegrityError as e:
        with connection, connection.cursor() as cursor:
            connection.rollback()
            cursor.execute("update snippets set message=%s where keyword=%s", (snippet, name,))
    logging.debug("Snippet stored successfully.")
    return name, snippet, hide

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
        cursor.execute("select keyword from snippets where not hidden order by keyword")
        rows = cursor.fetchall()
    logging.debug("Snippet names retrieved successfully.")
    try:
        return rows
    except TypeError:
        print("What's going on? There are no snippet names.")
        
def search(name):
    """Retrieve the snippet with a given name."""
    logging.info("Getting all snippets with a keyword: {!r}".format(name))
    with connection, connection.cursor() as cursor:
#         cursor.execute("select * from snippets where message like '%%%s%%' and not hidden", (name,))
        stmt = "select * from snippets where message like '%%%s%%' and not hidden" % (name)
        cursor.execute(stmt)
        rows = cursor.fetchall()
    logging.debug("Snippets retrieved successfully.")
    try:
        return rows
    except TypeError:
        print("There are no snippets with that string.")

def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    #Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet", description='Store and retrieve snippets of text')
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    group = put_parser.add_mutually_exclusive_group() 
    group.add_argument("--hide", help="sets snippet to hide", action="store_true", dest='hide')
    group.add_argument("--show", help="sets snippet to show", action="store_false", dest='hide')
#     put_parser.set_defaults(func=put)
    
    #Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Get a snippet")
    get_parser.add_argument("name", help="The name of the snippet to get")
    
    #Subparser for the catalog command
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Catalog of all snippet names")
    
    #Subparser for the search command
    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search", help="Search for a snippets containing a string.")
    search_parser.add_argument("name", help="Name to search for in all the snippet messages.")
    
    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "put":
#         print("Arguments passed into put:")
#         print(arguments)
        name, snippet, hide = put(**arguments)
        print("Stored {!r} as {!r} with a hidden flag of {!r}.".format(snippet, name, hide))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet)) # {!r} gives us the __repr__
    elif command == "catalog":
        names = catalog()
        print("Here are all the snippet names:")
        # generator expression used inside join to print the results of the rows from cursor.fetchall() nicely
        print("{}".format('\n'.join(name[0] for name in names)))
    elif command == "search":
        results = search(**arguments)
        print("Here are all the search results for that string:")
        #print("{}".format('\n'.join((result[0] for result in results))))
        for result in results:
            print"{}:  {}".format(result[0], result[1])
        
if __name__=="__main__":
    main()