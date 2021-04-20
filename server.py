import os
import sys
import logging

from flask import Flask, redirect, request
from blinpy.utils import handlers, webutils
from conf.auth import AUTH, BASE_URL

def create_app():
    """Use Flask to create app"""

    app = Flask(__name__)

    @app.route("/", methods=['GET', 'POST'])
    def main():
        """Main function to handle all requests."""

        if request.method == "POST":
            # GitHub sends the secret key in the payload header
            if webutils.match_webhook_secret(request):
                event = request.headers["X-GitHub-Event"]
                event_to_action = {
                    # "pull_request": handlers.handle_pull_request,
                    # "integration_installation": handlers.handle_integration_installation,
                    # "integration_installation_repositories": handlers.handle_integration_installation_repo,
                    # "installation_repositories": handlers.handle_integration_installation_repo,
                    # "ping": handlers.handle_ping,
                    "issue_comment": handlers.handle_issue_comment,
                    # "installation": handlers.handle_installation,
                }
                supported_event = event in event_to_action
                # if supported_event:
                return event_to_action[event](request)
        #         else:
        #             return handlers.handle_unsupported_requests(request)
        #     else:
        #         app.logger.info("Received an unauthorized request")
        #         return handlers.handle_unauthorized_requests()
        # else:
        #     return

    app.secret_key = os.environ.setdefault("APP_SECRET_KEY", "")
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = False
    return app

app = create_app()

if __name__ == '__main__':
    app.run()