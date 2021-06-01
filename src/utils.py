from src.incbl import incbl
import mysql.connector

incbl_db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="123456"
)

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

def send_pr_comment():
    """
    use Github API to get PR code and update local files

    Args: url, api keys
    """
    pass

