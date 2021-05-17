from gidgethub.aiohttp import GitHubAPI
import mongoengine

MONGODB_HOST = "xxxxxxxxxx"
MONGODB_PORT = 
MONGODB_DB = "xxxxxx"
MONGODB_USERNAME = "xxxxxx"
MONGODB_PASSWORD = "xxxxxxx"

conn = mongoengine.connect(
        db = MONGODB_DB,
        host = MONGODB_HOST,
        port = MONGODB_PORT,
        username = MONGODB_USERNAME,
        password = MONGODB_PASSWORD)

db = conn[MONGODB_DB]
db.authenticate(MONGODB_USERNAME,MONGODB_PASSWORD)

coll = db["xxxxxxxxxxxxx"]

def code_insert():

    pass


def code_delete():

    pass


def code_update():

    pass


def bugs_insert():

    pass


# TODO: get repo file content
def get_repo_files():
    """
    use Github API to get repo files and update

    Args: url, api keys
    """
    pass


# TODO: web api to get
def get_issue_content():
    """
    use Github API to get issues

    Args: url, api keys

    Returns: json data
    """
    pass


# TODO: web api to send issue
def send_issue_comment():
    """
    use Github API to send_issue_comment

    Args: url, api keys, results
    """
    pass


# TODO: web api to get pull_request
def update_repo_files():
    """
    use Github API to get PR code and update local files

    Args: url, api keys
    """
    pass


# TODO: web api to send pull_request comments
def send_pr_comment():
    """
    use Github API to get PR code and update local files

    Args: url, api keys
    """
    pass

