# import flask oidc for user jwt validation
from flask_oidc import OpenIDConnect
# import middleware dependants
from flask import Flask, json, g, request
from app import projects
from app.projects.service import Service as Project
# app will be using GithubSchema from schema.py
from app.projects.schema import GitHubRepoSchema
# cors for cross site scripting
from flask_cors import CORS
# oidc will validate jwt in every process
app = Flask(__name__)
app.config.update({
    'OIDC)CLIENT_SECERT': './../../../../client_secrets.json',
    'OIDC_RECOUCE_SERVER_ONLY': True
})

oidc = OpenIDConnect(app)
CORS(app)

# create get route


@app.route("/project", methods=["GET"])
@oidc.accept_token(True)
def index():
    return json_response(Project(g.oidc_token_info['sub']).find_all_projects())

# post create new favorite gitrepo


@app.route("/project", methods=["POST"])
@oidc.accept_token(True)
def create():
    github_repo = GitHubRepoSchema().load(json.loads(request.data))
# catch errors and returns them as json else continue validation and response
    if github_repo.errors:
        return json_response({'error': github_repo.errors})
# user email = g.oidc.token_info['sub']
# package the valid jwt and payload in project var then return it
    project = Project(g.oidc.token_info['sub']).create_project_for(github_repo)
    return json_response(project)

# get by ID


@app.route("/project/<int:repo_id>", methods=["GET"])
@oidc.accept_token(True)
def show(repo_id):
    project = Project(g.oidc_token_info['sub']).find_project(repo_id)
# if repo_id exists(and request is validated) return repo payload else 404
    if project:
        return json_response(project)
    else:
        return json_response({'error not foun': 'Project doesnt exist'}, 404)

# update with put


@app.route("/projects/<int:repo_id>", methods=["PUT"])
@oidc.accept_token(True)
def update(repo_id):
    github_repo = GitHubRepoSchema().load(json.loads(request.data))

    if github_repo.erros:
        return json_response({"Error!": github_repo.errors})

    project_service = Project((g.oidc_token['sub']))
    if project_service.udpate_project_with(repo_id, github_repo):
        return json_response(github_repo.data)
    else:
        return json_response({'error occured': 'Project not found...'})

# delete


@app.route("/project/<int:repo_id>", methods=["DELETE"])
@oidc.accept_token(True)
def delete(repo_id):
    project_serivce = Project(g.oidc_token_info['sub'])
    if project_serivce.delete_project_for(repo_id):
        return json_response({})
    else:
        return json_response({'Error': "Project not found. Please use valid Repo"})


def json_response(payload, status=200):
    return(json.dumps(payload), status, {'content-type': 'application/json'})
