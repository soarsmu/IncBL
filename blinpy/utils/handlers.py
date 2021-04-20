import os
from blinpy.utils import webutils

def handle_issue_comment(request):
    ghrequest = models.GHRequest(request, request.headers["X-GitHub-Event"])

    # if not ghrequest.OK:
    #     return utils.Response(ghrequest)

    # # Get the .pep8speaks.yml config file from the repository
    # config = helpers.get_config(ghrequest.repository, ghrequest.base_branch, ghrequest.after_commit_hash)

    # splitted_comment = ghrequest.comment.lower().split()

    # # If diff is required
    # params1 = ["@pep8speaks", "suggest", "diff"]
    # condition1 = all(p in splitted_comment for p in params1)
    # # If asked to pep8ify
    # params2 = ["@pep8speaks", "pep8ify"]
    # condition2 = all(p in splitted_comment for p in params2)

    # if condition1:
    #     return _create_diff(ghrequest, config)
    # elif condition2:
    #     return _pep8ify(ghrequest, config)

    return webhooks.Response(ghrequest, 'hell0')


def handle_unauthorized_requests():
    response_object = {
        "message": "Unauthorized request"
    }
    return utils.Response(response_object, 401)
