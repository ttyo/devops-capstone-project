"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application

############################################################
# Health Endpoint
############################################################


@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            # paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################


@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    # Uncomment once get_accounts has been implemented
    # location_url = url_for("get_accounts", account_id=account.id, _external=True)
    location_url = "/"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# LIST ALL ACCOUNTS
######################################################################


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """
    List all Accounts
    This endpoint will list all Accounts
    """
    app.logger.info("Request to list Accounts")

    accounts = Account.all()
    account_list = [account.serialize() for account in accounts]

    app.logger.info("Returning [%s] accounts", len(account_list))
    return jsonify(account_list), status.HTTP_200_OK

######################################################################
# READ AN ACCOUNT
######################################################################


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """
    Reads an Account
    This endpoint will read an Account based the account_id that is requested
    """
    app.logger.info("Request to read an Account with id: %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")

    return account.serialize(), status.HTTP_200_OK

# ... (other route definitions)


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_allowed(error):
    """
    Handle Method Not Allowed (405) errors
    """
    return jsonify(
    error="Method not allowed",
    message="The requested method is not allowed for this endpoint."
), status.HTTP_405_METHOD_NOT_ALLOWED


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """
    Handle Not Found (404) errors
    """
    return jsonify(
    error="Not Found",
    message="The requested resource was not found."
), status.HTTP_404_NOT_FOUND

######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):

#    Update an Account
#    This endpoint will update an Account based on the posted data

    app.logger.info("Request to update an Account with id: %s", account_id)

    # Find the account by ID in the database
    account = Account.query.get(account_id)

    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id [{account_id}] could not be found.",
        )

    # Deserialize the request JSON data and update the account
    account_data = request.get_json()
    account.deserialize(account_data)
    account.update()

    return jsonify(account.serialize()), status.HTTP_200_OK


######################################################################
# DELETE AN ACCOUNT
######################################################################


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):

#    Delete an Account
#    This endpoint will delete an Account based on the account_id that is requested

    app.logger.info("Request to delete an Account with id: %s", account_id)

    account = Account.find(account_id)
    if account:
        account.delete()

    return "", status.HTTP_204_NO_CONTENT

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
