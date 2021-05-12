import asyncio
import os
import time
import aiohttp
import jwt

from gidgethub.aiohttp import GitHubAPI

if __name__ = "__main__":
    get_repo_files()

    while(True):
        update_repo_files()
        
        incbl = incbl()
        incbl.index_update()
        incbl.model_update()
        
        send_pr_comment()
        
        incbl.localization()
        
        send_issue_comment()
        
        incbl.fixed_bugs_update()




