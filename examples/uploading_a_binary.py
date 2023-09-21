import finite_state_sdk
import json
import os

from finite_state_sdk.token_cache import TokenCache

"""
This is an example of uploading a binary for analysis with Finite State Binary Analysis.
NOTE, the create_new_asset_version_and_upload_binary function is a convenience function that
can be used as the basis for integration with your CI/CD pipeline.

Uploading a Binary for analysis with Finite State Binary Analysis
To upload a binary, you will need:

* Business Unit ID (get this from the API or app, see this example)
* Created By User ID (get this from the API or app)
* An Asset ID (get this from the API or app, see this example)
* A version name (you make this up, or it comes from your build system, e.g. 1.0, 1.2, etc.)
* A File Path (this is the path to the file on your local machine)

In this example:
* We assume that you have already created an Asset, and are creating a new AssetVersion for that Asset. This corresponds to analyzing a new version of your firmware, for example.

Note: An Asset and AssetVersion may or may not be related to a Product. In this example, it is not.

To install the SDK, use pip:
pip install finite-state-sdk
"""

"""
You can store your secrets in a file called .env in the same directory as this script
that looks like:

export CLIENT_ID="your client id"
export CLIENT_SECRET="your client secret"
export ORGANIZATION_CONTEXT="your organization context"

Before running the script, run the following command in the terminal:
source .env

DO NOT COMMIT THIS FILE TO YOUR SOURCE CODE REPOSITORY!!!
"""

# get CLIENT_ID and CLIENT_SECRET from env
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
ORGANIZATION_CONTEXT = os.environ.get("ORGANIZATION_CONTEXT")


# Get an auth token - this is a bearer token that you will use for all subsequent requests
# The token is valid for 24 hours
token_cache = TokenCache(ORGANIZATION_CONTEXT)
token = token_cache.get_token(CLIENT_ID, CLIENT_SECRET)

# get all business units to get the business_unit_id
business_units = finite_state_sdk.get_all_business_units(token, ORGANIZATION_CONTEXT)
# print(json.dumps(business_units, indent=4))

"""
Example Response:
[
    {
        "_cursor": "{\"id\":\"xxxxxxxx28\"}",
        "id": "xxxxxxxx28",
        "name": "Finite State Products"
    }
]
"""

# You can also get this from the app by clicking Account and navigating to the Business Unit
business_unit_id = ""  # CHANGEME: Get the business unit ID of the BU that owns the product

# get all users to get the user id
users = finite_state_sdk.get_all_users(token, ORGANIZATION_CONTEXT)
print(json.dumps(users, indent=4))

"""
Example Response:
[
    {
        "_cursor": "{\"id\":\"xxxxxxx73\"}",
        "id": "xxxxxxx73",
        "email": "xxxxxxx@xxxxxxxxxx.xxx"
    }
]
"""

# You can also get this from the app by clicking Account and navigating to the User
created_by_user_id = ""  # CHANGEME: Get the user ID to associate with the creation of the product

# You can also get this from the app by navigating to the Asset, this ID is the number in the URL
# https://platform.finitestate.io/artifacts/<YOUR_ASSET_ID>
asset_id = ""  # CHANGEME: Get the asset ID to associate with the binary

file_path = ""  # CHANGEME: Path to the file you want to upload
version_name = ""  # CHANGEME: Name of the version you are uploading (e.g. 1.0, 1.1, etc.)

# upload the binary
response = finite_state_sdk.create_new_asset_version_and_upload_binary(token, ORGANIZATION_CONTEXT, business_unit_id=business_unit_id, created_by_user_id=created_by_user_id, asset_id=asset_id, version=version_name, file_path=file_path, product_id=None)
print("Uploaded the binary:")
print(json.dumps(response, indent=4))

"""
Example Response:
{
    "completeMultipartUpload": {
        "key": "test_results/org=xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/asset_version=xxxxxxxxx/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
}
"""