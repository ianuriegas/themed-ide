#!/usr/bin/env python3
import os
import sys
from github import Github

def update_deployment_status(token, repo_name, deployment_id, state, environment_url=None):
    g = Github(token)
    repo = g.get_repo(repo_name)
    deployment = repo.get_deployment(deployment_id)
    
    status = {
        'state': state,
        'environment': 'Preview'
    }
    
    if environment_url:
        status['environment_url'] = environment_url
        
    deployment.create_status(**status)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python deploy.py <token> <repo_name> <deployment_id> <state> [environment_url]")
        sys.exit(1)
        
    token = sys.argv[1]
    repo_name = sys.argv[2]
    deployment_id = int(sys.argv[3])
    state = sys.argv[4]
    environment_url = sys.argv[5] if len(sys.argv) > 5 else None
    
    update_deployment_status(token, repo_name, deployment_id, state, environment_url) 