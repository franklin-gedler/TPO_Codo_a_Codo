"""Module with health endpoint."""
from flask import Blueprint


health = Blueprint("health", __name__)


@health.route("/health")
def main():
    """health endpoint, used to know if the app is up."""
    return "OK"
