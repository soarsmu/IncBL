import asyncio
import os
import time
import aiohttp
import jwt
import json
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from src.text_processor import text_processor
from src.bug_reader import bug_reader
from src.code_reader import mp_code_reader
from src.tfidf import get_docu_feature, tfidf_creation, update_tfidf_feature
from src.similarity import compute_similarity
from src.evaluation import evaluation
from gidgethub.aiohttp import GitHubAPI

PEM_FILE_PATH = "./incbl.pem"
GH_APP_ID = "110333"

def get_jwt(app_id):

    path_to_private_key = PEM_FILE_PATH
    pem_file = open(path_to_private_key, "rt").read()

    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + (10 * 60),
        "iss": app_id,
    }
    
    encoded = jwt.encode(payload, pem_file, algorithm="RS256")
    bearer_token = encoded

    return bearer_token

async def get_installation(gh, jwt):
    installations = []
    async for installation in gh.getiter(
        "/app/installations",
        jwt=jwt,
        accept="application/vnd.github.machine-man-preview+json",
    ):  
        installations.append(installation)
    return installations

    raise ValueError(f"Can't find installation by that user: {username}")

async def get_installation_access_token(gh, jwt, installation_id):
    # doc: https: // developer.github.com/v3/apps/#create-a-new-installation-token

    access_token_url = (
        f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    )
    response = await gh.post(
        access_token_url,
        data=b"",
        jwt=jwt,
        accept="application/vnd.github.machine-man-preview+json",
    )
  
    return response

async def main():
    async with aiohttp.ClientSession() as session:
        app_id = GH_APP_ID
        jwt = get_jwt(app_id)
        gh = GitHubAPI(session, "jiekeshi")
        try:
            installations = await get_installation(gh, jwt)
        except ValueError as ve:
            print(ve)
        else:
            access_tokens = []
            for installation in installations:
                access_tokens.append(await get_installation_access_token(
                    gh, jwt=jwt, installation_id=installation["id"]
                ))
            for access_token, installation in zip(access_tokens, installations):
                # print(access_token)
                gh_app = GitHubAPI(session, "black_out", oauth_token=access_token["token"])
                async for repo in gh.getiter(
                "https://api.github.com/users/"+installation['account']['login']+"/repos",
                accept="application/vnd.github.machine-man-preview+json",
                ):  
                    # if repo["full_name"] == "yangzhou6666/IncBL-demo":
                        # print(repo)
                    if not repo["has_issues"] == False:
                        issues = await gh_app.getitem(
                            "/repos/"+repo["full_name"]+"/issues",
                        )
                        for issue in issues:
                            if len(issue["labels"]):
                                for label in issue["labels"]:
                                    if label["name"] == "bug":
                                        bug_data = {issue["number"]: {"content":text_processor(issue["title"] + " " + issue["body"]), "fixed_files": [], "open_date": issue["created_at"]}}
                                        code_data, added_files, deleted_files, modified_files = mp_code_reader("/home/jack/Blinpy-app", ["py"], "./in/code", "/home/jack/Blinpy-app")
                                        idfs = get_docu_feature(code_data, "./in/code", True)

                                        bug_vector = tfidf_creation(bug_data, idfs, "./in/bug", False)
                                        code_vector = tfidf_creation(code_data, idfs, "./in/code", True)
                                        similarity = compute_similarity(bug_vector, code_vector, bug_data, {}, "./in/bug")
                                        
                                        similarity["score"] = -similarity["score"]
                                        results = np.sort(similarity, order = "score")[:,:10]
                                        similarity = np.sort(similarity, order = "score")
                                        similarity["score"] = -similarity["score"]
                                        b = []
                                        for i in range(results.shape[0]):
                                            for j in range(results[i].shape[0]):
                                                b.append("IncBL-demo/"+'/'.join(results[i][j]["file"].decode().split("/")[4:]))
                                        comment = ""
                                        for i, j in enumerate(b):
                                            comment+="📑"+str(i+1)+": <b>"+j+"</b>"+"\n"
                                        a = await gh_app.post(
                                            "/repos/"+repo["full_name"]+"/issues/"+str(issue["number"])+"/comments",
                                            data={
                                                "body": "Thanks for your issues! \nIncBL bot 🤖 will remind developers 👨‍💻 to check the following code files: \n "+ comment,
                                            },
                                        )
asyncio.run(main())
# # import asyncio
# # import os
# # import time

# # import aiohttp
# # import jwt
# # from gidgethub.aiohttp import GitHubAPI


# # def get_jwt(app_id):

# #     path_to_private_key = PEM_FILE_PATH
# #     pem_file = open(path_to_private_key, "rt").read()

# #     payload = {
# #         "iat": int(time.time()),
# #         "exp": int(time.time()) + (10 * 60),
# #         "iss": app_id,
# #     }
# #     encoded = jwt.encode(payload, pem_file, algorithm="RS256")

#     return encoded

# async def get_installation(gh, jwt, username):
#     async for installation in gh.getiter(
#         "/app/installations",
#         jwt=jwt,
#         accept="application/vnd.github.machine-man-preview+json",
#     ):
#         if installation["account"]["login"] == username:
#             return installation

#     raise ValueError(f"Can't find installation by that user: {username}")


# async def get_installation_access_token(gh, jwt, installation_id):
#     # doc: https: // developer.github.com/v3/apps/#create-a-new-installation-token

#     access_token_url = (
#         f"https://api.github.com/app/installations/{installation_id}/access_tokens"
#     )
#     response = await gh.post(
#         access_token_url,
#         data=b"",
#         jwt=jwt,
#         accept="application/vnd.github.machine-man-preview+json",
#     )
#     # example response
#     # {
#     #   "token": "v1.1f699f1069f60xxx",
#     #   "expires_at": "2016-07-11T22:14:10Z"
#     # }

#     return response


# async def main():
#     async with aiohttp.ClientSession() as session:
#         app_id = GH_APP_ID

#         jwt = get_jwt(app_id)
#         gh = GitHubAPI(session, "jiekeshi")

#         try:
#             installation = await get_installation(gh, jwt, "jiekeshi")

#         except ValueError as ve:
#             # Raised if jiekeshi did not installed the GitHub App
#             print(ve)
#         else:
#             access_token = await get_installation_access_token(
#                 gh, jwt=jwt, installation_id=installation["id"]
#             )

#             # treat access_token as if a personal access token

#             # Example, creating a GitHub issue as a GitHub App
#             gh_app = GitHubAPI(session, "black_out", oauth_token=access_token["token"])
#             await gh_app.post(
#                 "/repos/jiekeshi/jiekeshi.github.io/issues",
#                 data={
#                     "title": "We got a problem 🤖",
#                     "body": "Use more emoji! (I'm a GitHub App!) ",
#                 },
#             )


# asyncio.run(main())