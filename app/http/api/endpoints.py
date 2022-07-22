# import flask oidc for user jwt validation
from flask_oidc import OpenIDConnect 
# import middleware dependants 
from flask import Flask, json, g ,request
from app.projects.service import Service as Project
from app.projects.schema import GitHubRepoSchema
# cors for cross site scripting 
from flask_cors import CORS

app = Flask(__name__)
app.config.update({
    'OIDC)CLIENT_SECERT':'./../../../../client_secerts.json',
    'OIDC_RECOUCE_SERVER_ONLY': True
})

oidc = OpenIDConnect(app)
CORS(app)

@app.route("/projects", methods=["GET"])
@oidc.accept_token(True)
def index():
    return json_response(Project(g.oidc_token_info['sub']).find_all_projects)

def json_response():
    pass