import json
import requests
import finite_state_sdk.queries as queries

API_URL = 'https://platform.finitestate.io/api/v1/graphql'
AUDIENCE = "https://platform.finitestate.io/api/v1/graphql"
TOKEN_URL = "https://finitestate.auth0.com/oauth/token"


def create_artifact(token, organization_context, business_unit_id=None, created_by_user_id=None, asset_version_id=None, artifact_name=None, product_id=None):
    """
    Create a new Artifact.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        business_unit_id (str, required):
            Business Unit ID to associate the artifact with.
        created_by_user_id (str, required):
            User ID of the user creating the artifact.
        asset_version_id (str, required):
            Asset Version ID to associate the artifact with.
        artifact_name (str, required):
            The name of the Artifact being created.
        product_id (str, optional):
            Product ID to associate the artifact with. If not specified, the artifact will not be associated with a product.

    Raises:
        ValueError: Raised if business_unit_id, created_by_user_id, asset_version_id, or artifact_name are not provided.
        Exception: Raised if the query fails.

    Returns:
        dict: createArtifact Object
    """
    if not business_unit_id:
        raise ValueError("Business unit ID is required")
    if not created_by_user_id:
        raise ValueError("Created by user ID is required")
    if not asset_version_id:
        raise ValueError("Asset version ID is required")
    if not artifact_name:
        raise ValueError("Artifact name is required")

    graphql_query = '''
    mutation CreateArtifactMutation($input: CreateArtifactInput!) {
        createArtifact(input: $input) {
            id
            name
            assetVersion {
                id
                name
                asset {
                    id
                    name
                }
            }
            createdBy {
                id
                email
            }
            ctx {
                asset
                products
                businessUnits
            }
        }
    }
    '''

    # Asset name, business unit context, and creating user are required
    variables = {
        "input": {
            "name": artifact_name,
            "createdBy": created_by_user_id,
            "assetVersion": asset_version_id,
            "ctx": {
                "asset": asset_version_id,
                "businessUnits": [business_unit_id]
            }
        }
    }

    if product_id is not None:
        variables["input"]["ctx"]["products"] = product_id

    response = send_graphql_query(token, organization_context, graphql_query, variables)
    return response['data']


def create_asset(token, organization_context, business_unit_id=None, created_by_user_id=None, asset_name=None, product_id=None):
    """
    Create a new Asset.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        business_unit_id (str, required):
            Business Unit ID to associate the asset with.
        created_by_user_id (str, required):
            User ID of the user creating the asset.
        asset_name (str, required):
            The name of the Asset being created.
        product_id (str, optional):
            Product ID to associate the asset with. If not specified, the asset will not be associated with a product.

    Raises:
        ValueError: Raised if business_unit_id, created_by_user_id, or asset_name are not provided.
        Exception: Raised if the query fails.

    Returns:
        dict: createAsset Object
    """
    if not business_unit_id:
        raise ValueError("Business unit ID is required")
    if not created_by_user_id:
        raise ValueError("Created by user ID is required")
    if not asset_name:
        raise ValueError("Asset name is required")

    graphql_query = '''
    mutation CreateAssetMutation($input: CreateAssetInput!) {
        createAsset(input: $input) {
            id
            name
            dependentProducts {
                id
                name
            }
            group {
                id
                name
            }
            createdBy {
                id
                email
            }
            ctx {
                asset
                products
                businessUnits
            }
        }
    }
    '''

    # Asset name, business unit context, and creating user are required
    variables = {
        "input": {
            "name": asset_name,
            "group": business_unit_id,
            "createdBy": created_by_user_id,
            "ctx": {
                "businessUnits": [business_unit_id]
            }
        }
    }

    if product_id is not None:
        variables["input"]["ctx"]["products"] = product_id

    response = send_graphql_query(token, organization_context, graphql_query, variables)
    return response['data']


def create_asset_version(token, organization_context, business_unit_id=None, created_by_user_id=None, asset_id=None, asset_version_name=None, product_id=None):
    """
    Create a new Asset Version.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        business_unit_id (str, required):
            Business Unit ID to associate the asset version with.
        created_by_user_id (str, required):
            User ID of the user creating the asset version.
        asset_id (str, required):
            Asset ID to associate the asset version with.
        asset_version_name (str, required):
            The name of the Asset Version being created.
        product_id (str, optional):
            Product ID to associate the asset version with. If not specified, the asset version will not be associated with a product.

    Raises:
        ValueError: Raised if business_unit_id, created_by_user_id, asset_id, or asset_version_name are not provided.
        Exception: Raised if the query fails.

    Returns:
        dict: createAssetVersion Object
    """
    if not business_unit_id:
        raise ValueError("Business unit ID is required")
    if not created_by_user_id:
        raise ValueError("Created by user ID is required")
    if not asset_id:
        raise ValueError("Asset ID is required")
    if not asset_version_name:
        raise ValueError("Asset version name is required")

    graphql_query = '''
    mutation CreateAssetVersionMutation($input: CreateAssetVersionInput!) {
        createAssetVersion(input: $input) {
            id
            name
            asset {
                id
                name
            }
            createdBy {
                id
                email
            }
            ctx {
                asset
                products
                businessUnits
            }
        }
    }
    '''

    # Asset name, business unit context, and creating user are required
    variables = {
        "input": {
            "name": asset_version_name,
            "createdBy": created_by_user_id,
            "asset": asset_id,
            "ctx": {
                "asset": asset_id,
                "businessUnits": [business_unit_id]
            }
        }
    }

    if product_id is not None:
        variables["input"]["ctx"]["products"] = product_id

    response = send_graphql_query(token, organization_context, graphql_query, variables)
    return response['data']


def create_new_asset_version_artifact_and_test_for_upload(token, organization_context, business_unit_id=None, created_by_user_id=None, asset_id=None, version=None, product_id=None, test_type=None, artifact_description=None):
    """
    Creates the entities needed for uploading a file for Binary Analysis or test results from a third party scanner to an existing Asset. This will create a new Asset Version, Artifact, and Test.
    This method is used by the upload_file_for_binary_analysis and upload_test_results_file methods, which are generally easier to use for basic use cases.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        business_unit_id (str, optional):
            Business Unit ID to create the asset version for. If not provided, the default Business Unit will be used.
        created_by_user_id (str, optional):
            User ID to create the asset version for. If not provided, the default user will be used.
        asset_id (str, required):
            Asset ID to create the asset version for. If not provided, the default asset will be used.
        version (str, required):
            Version to create the asset version for.
        product_id (str, optional):
            Product ID to create the entities for. If not provided, the default product will be used.
        test_type (str, required):
            Test type to create the test for. Must be one of "finite_state_binary_analysis" or of the list of supported third party test types. For the full list, see the API documenation.
        artifact_description (str, optional):
            Description to use for the artifact. Examples inlcude "Firmware", "Source Code Repository". This will be appended to the default Artifact description. If none is provided, the default Artifact description will be used.

    Raises:
        ValueError: Raised if asset_id or version are not provided.
        Exception: Raised if the query fails.

    Returns:
        str: The Test ID of the newly created test that is used for uploading the file.
    """
    assets = get_all_assets(token, organization_context, asset_id=asset_id)
    asset = assets[0]

    # get the asset name
    asset_name = asset['name']

    # get the existing asset product IDs
    asset_product_ids = asset['ctx']['products']

    # get the asset product ID
    if product_id and product_id not in asset_product_ids:
        asset_product_ids.append(product_id)

    # if business_unit_id or created_by_user_id are not provided, get the existing asset
    if not business_unit_id or not created_by_user_id:
        if not business_unit_id:
            business_unit_id = asset['businessUnit']['id']
        if not created_by_user_id:
            created_by_user_id = asset['createdByUser']['id']

        if not business_unit_id:
            raise ValueError("Business Unit ID is required and could not be retrieved from the existing asset")
        if not created_by_user_id:
            raise ValueError("Created By User ID is required and could not be retrieved from the existing asset")

    if not asset_id:
        raise ValueError("Asset ID is required")
    if not version:
        raise ValueError("Version is required")

    # create the asset version
    response = create_asset_version(token, organization_context, business_unit_id=business_unit_id, created_by_user_id=created_by_user_id, asset_id=asset_id, asset_version_name=version)
    # get the asset version ID
    asset_version_id = response['createAssetVersion']['id']

    # create the test
    if test_type == "finite_state_binary_analysis":
        # create the artifact
        if not artifact_description:
            artifact_description = "Binary"
        binary_artifact_name = f"{asset_name} {version} - {artifact_description}"
        response = create_artifact(token, organization_context, business_unit_id=business_unit_id, created_by_user_id=created_by_user_id, asset_version_id=asset_version_id, artifact_name=binary_artifact_name, product_id=asset_product_ids)

        # get the artifact ID
        binary_artifact_id = response['createArtifact']['id']

        # create the test
        test_name = f"{asset_name} {version} - Finite State Binary Analysis"
        response = create_test_as_binary_analysis(token, organization_context, business_unit_id=business_unit_id, created_by_user_id=created_by_user_id, asset_id=asset_id, artifact_id=binary_artifact_id, product_id=asset_product_ids, test_name=test_name)
        test_id = response['createTest']['id']
        return test_id

    elif test_type == "cyclonedx":
        # create the artifact
        if not artifact_description:
            artifact_description = "Unspecified Artifact"
        artifact_name = f"{asset_name} {version} - {artifact_description}"
        response = create_artifact(token, organization_context, business_unit_id=business_unit_id, created_by_user_id=created_by_user_id, asset_version_id=asset_version_id, artifact_name=artifact_name, product_id=asset_product_ids)

        # get the artifact ID
        binary_artifact_id = response['createArtifact']['id']

        # create the test
        test_name = f"{asset_name} {version} - {test_type}"
        response = create_test_as_third_party_scanner(token, organization_context, business_unit_id=business_unit_id, created_by_user_id=created_by_user_id, asset_id=asset_id, artifact_id=binary_artifact_id, product_id=asset_product_ids, test_name=test_name, test_type=test_type)
        test_id = response['createTest']['id']
        return test_id

    else:
        raise ValueError(f"Test type {test_type} is not supported")


def create_new_asset_version_and_upload_binary(token, organization_context, business_unit_id=None, created_by_user_id=None, asset_id=None, version=None, file_path=None, product_id=None, artifact_description=None):
    """
    Creates a new Asset Version for an existing asset, and uploads a binary file for Finite State Binary Analysis.
    By default, this uses the existing Business Unit and Created By User for the Asset. If you need to change these, you can provide the IDs for them.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        business_unit_id (str, optional):
            Business Unit ID to create the asset version for. If not provided, the existing Business Unit for the Asset will be used.
        created_by_user_id (str, optional):
            Created By User ID to create the asset version for. If not provided, the existing Created By User for the Asset will be used.
        asset_id (str, required):
            Asset ID to create the asset version for.
        version (str, required):
            Version to create the asset version for.
        file_path (str, required):
            Local path to the file to upload.
        product_id (str, optional):
            Product ID to create the asset version for. If not provided, the existing Product for the Asset will be used, if it exists.
        artifact_description (str, optional):
            Description of the artifact. If not provided, the default is "Firmware Binary".

    Raises:
        ValueError: Raised if asset_id, version, or file_path are not provided.
        Exception: Raised if any of the queries fail.

    Returns:
        dict: The response from the GraphQL query, a createAssetVersion Object.
    """
    if not asset_id:
        raise ValueError("Asset ID is required")
    if not version:
        raise ValueError("Version is required")
    if not file_path:
        raise ValueError("File path is required")

    # create the asset version and binary test
    if not artifact_description:
        artifact_description = "Firmware Binary"
    binary_test_id = create_new_asset_version_artifact_and_test_for_upload(token, organization_context, business_unit_id=business_unit_id, created_by_user_id=created_by_user_id, asset_id=asset_id, version=version, product_id=product_id, test_type="finite_state_binary_analysis", artifact_description=artifact_description)

    # upload file for binary test
    response = upload_file_for_binary_analysis(token, organization_context, test_id=binary_test_id, file_path=file_path)
    return response


def create_new_asset_version_and_upload_test_results(token, organization_context, business_unit_id=None, created_by_user_id=None, asset_id=None, version=None, file_path=None, product_id=None, test_type=None, artifact_description=""):
    """
    Creates a new Asset Version for an existing asset, and uploads test results for that asset version.
    By default, this uses the existing Business Unit and Created By User for the Asset. If you need to change these, you can provide the IDs for them.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        business_unit_id (str, optional):
            Business Unit ID to create the asset version for. If not provided, the existing Business Unit for the Asset will be used.
        created_by_user_id (str, optional):
            Created By User ID to create the asset version for. If not provided, the existing Created By User for the Asset will be used.
        asset_id (str, required):
            Asset ID to create the asset version for.
        version (str, required):
            Version to create the asset version for.
        file_path (str, required):
            Path to the test results file to upload.
        product_id (str, optional):
            Product ID to create the asset version for. If not provided, the existing Product for the Asset will be used.
        test_type (str, required):
            Test type. This must be "cyclonedx" or one of the list of supported third party scanner types. For the full list of supported third party scanner types, see the Finite State API documentation.
        artifact_description (str, optional):
            Description of the artifact being scanned (e.g. "Source Code Repository", "Container Image"). If not provided, the default artifact description will be used.

    Raises:
        ValueError: If the asset_id, version, or file_path are not provided.
        Exception: If the test_type is not a supported third party scanner type, or if the query fails.

    Returns:
        dict: The response from the GraphQL query, a createAssetVersion Object.
    """
    if not asset_id:
        raise ValueError("Asset ID is required")
    if not version:
        raise ValueError("Version is required")
    if not file_path:
        raise ValueError("File path is required")
    if not test_type:
        raise ValueError("Test type is required")

    # create the asset version and test
    test_id = create_new_asset_version_artifact_and_test_for_upload(token, organization_context, business_unit_id=business_unit_id, created_by_user_id=created_by_user_id, asset_id=asset_id, version=version, product_id=product_id, test_type=test_type, artifact_description=artifact_description)

    # upload test results file
    response = upload_test_results_file(token, organization_context, test_id=test_id, file_path=file_path)
    return response


def create_product(token, organization_context, business_unit_id=None, created_by_user_id=None, product_name=None, product_description=None, vendor_id=None, vendor_name=None):
    """
    Create a new Product.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        business_unit_id (str, required):
            Business Unit ID to associate the product with.
        created_by_user_id (str, required):
            User ID of the user creating the product.
        product_name (str, required):
            The name of the Product being created.
        product_description (str, optional):
            The description of the Product being created.
        vendor_id (str, optional):
            Vendor ID to associate the product with. If not specified, vendor_name must be provided.
        vendor_name (str, optional):
            Vendor name to associate the product with. This is used to create the Vendor if the vendor does not currently exist.

    Raises:
        ValueError: Raised if business_unit_id, created_by_user_id, or product_name are not provided.
        Exception: Raised if the query fails.

    Returns:
        dict: createProduct Object
    """

    if not business_unit_id:
        raise ValueError("Business unit ID is required")
    if not created_by_user_id:
        raise ValueError("Created by user ID is required")
    if not product_name:
        raise ValueError("Product name is required")

    graphql_query = '''
    mutation CreateProductMutation($input: CreateProductInput!) {
		createProduct(input: $input) {
            id
            name
            vendor {
                name
            }
            group {
                id
                name
            }
            createdBy {
                id
                email
            }
            ctx {
                businessUnit
            }
		}
    }
    '''

    # Product name, business unit context, and creating user are required
    variables = {
        "input": {
            "name": product_name,
            "group": business_unit_id,
            "createdBy": created_by_user_id,
            "ctx": {
                "businessUnit": business_unit_id
            }
        }
    }

    if product_description is not None:
        variables["input"]["description"] = product_description

    # If the vendor ID is specified, this will link the new product to the existing vendor
    if vendor_id is not None:
        variables["input"]["vendor"] = {
            "id": vendor_id
        }

    # If the vendor name is specified, this will create a new vendor and link it to the new product
    if vendor_name is not None:
        variables["input"]["createVendor"] = {
            "name": vendor_name
        }

    response = send_graphql_query(token, organization_context, graphql_query, variables)

    return response['data']


def create_test(token, organization_context, business_unit_id=None, created_by_user_id=None, asset_id=None, artifact_id=None, test_name=None, product_id=None, test_type=None, tools=[]):
    """
    Create a new Test object for uploading files.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        business_unit_id (str, required):
            Business Unit ID to associate the Test with.
        created_by_user_id (str, required):
            User ID of the user creating the Test.
        asset_id (str, required):
            Asset ID to associate the Test with.
        artifact_id (str, required):
            Artifact ID to associate the Test with.
        test_name (str, required):
            The name of the Test being created.
        product_id (str, optional):
            Product ID to associate the Test with. If not specified, the Test will not be associated with a product.
        test_type (str, required):
            The type of test being created. Valid values are "cyclonedx" and "finite_state_binary_analysis".
        tools (list, optional):
            List of Tool objects used to perform the test. Each Tool object is a dict that should have a "name" and "description" field. This is used to describe the actual scanner that was used to perform the test.

    Raises:
        ValueError: Raised if business_unit_id, created_by_user_id, asset_id, artifact_id, test_name, or test_type are not provided.
        Exception: Raised if the query fails.

    Returns:
        dict: createTest Object
    """
    if not business_unit_id:
        raise ValueError("Business unit ID is required")
    if not created_by_user_id:
        raise ValueError("Created by user ID is required")
    if not asset_id:
        raise ValueError("Asset ID is required")
    if not artifact_id:
        raise ValueError("Artifact ID is required")
    if not test_name:
        raise ValueError("Test name is required")
    if not test_type:
        raise ValueError("Test type is required")

    graphql_query = '''
    mutation CreateTestMutation($input: CreateTestInput!) {
        createTest(input: $input) {
            id
            name
            artifactUnderTest {
                id
                name
                assetVersion {
                    id
                    name
                    asset {
                        id
                        name
                        dependentProducts {
                            id
                            name
                        }
                    }
                }
            }
            createdBy {
                id
                email
            }
            ctx {
                asset
                products
                businessUnits
            }
        }
    }
    '''

    # Asset name, business unit context, and creating user are required
    variables = {
        "input": {
            "name": test_name,
            "createdBy": created_by_user_id,
            "artifactUnderTest": artifact_id,
            "testResultFileFormat": test_type,
            "ctx": {
                "asset": asset_id,
                "businessUnits": [business_unit_id]
            },
            "tools": tools
        }
    }

    if product_id is not None:
        variables["input"]["ctx"]["products"] = product_id

    response = send_graphql_query(token, organization_context, graphql_query, variables)
    return response['data']


def create_test_as_binary_analysis(token, organization_context, business_unit_id=None, created_by_user_id=None, asset_id=None, artifact_id=None, test_name=None, product_id=None):
    """
    Create a new Test object for uploading files for Finite State Binary Analysis.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        business_unit_id (str, required):
            Business Unit ID to associate the Test with.
        created_by_user_id (str, required):
            User ID of the user creating the Test.
        asset_id (str, required):
            Asset ID to associate the Test with.
        artifact_id (str, required):
            Artifact ID to associate the Test with.
        test_name (str, required):
            The name of the Test being created.
        product_id (str, optional):
            Product ID to associate the Test with. If not specified, the Test will not be associated with a product.

    Raises:
        ValueError: Raised if business_unit_id, created_by_user_id, asset_id, artifact_id, or test_name are not provided.
        Exception: Raised if the query fails.

    Returns:
        dict: createTest Object
    """
    tools = [
        {
            "description": "SBOM and Vulnerability Analysis from Finite State Binary SCA and Binary SAST.",
            "name": "Finite State Binary Analysis"
        }
    ]
    return create_test(token, organization_context, business_unit_id=business_unit_id, created_by_user_id=created_by_user_id, asset_id=asset_id, artifact_id=artifact_id, test_name=test_name, product_id=product_id, test_type="finite_state_binary_analysis", tools=tools)


def create_test_as_cyclone_dx(token, organization_context, business_unit_id=None, created_by_user_id=None, asset_id=None, artifact_id=None, test_name=None, product_id=None):
    """
    Create a new Test object for uploading CycloneDX files.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        business_unit_id (str, required):
            Business Unit ID to associate the Test with.
        created_by_user_id (str, required):
            User ID of the user creating the Test.
        asset_id (str, required):
            Asset ID to associate the Test with.
        artifact_id (str, required):
            Artifact ID to associate the Test with.
        test_name (str, required):
            The name of the Test being created.
        product_id (str, optional):
            Product ID to associate the Test with. If not specified, the Test will not be associated with a product.

    Raises:
        ValueError: Raised if business_unit_id, created_by_user_id, asset_id, artifact_id, or test_name are not provided.
        Exception: Raised if the query fails.

    Returns:
        dict: createTest Object
    """
    return create_test(token, organization_context, business_unit_id=business_unit_id, created_by_user_id=created_by_user_id, asset_id=asset_id, artifact_id=artifact_id, test_name=test_name, product_id=product_id, test_type="cyclonedx")


def create_test_as_third_party_scanner(token, organization_context, business_unit_id=None, created_by_user_id=None, asset_id=None, artifact_id=None, test_name=None, product_id=None, test_type=None):
    """
    Create a new Test object for uploading Third Party Scanner files.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        business_unit_id (str, required):
            Business Unit ID to associate the Test with.
        created_by_user_id (str, required):
            User ID of the user creating the Test.
        asset_id (str, required):
            Asset ID to associate the Test with.
        artifact_id (str, required):
            Artifact ID to associate the Test with.
        test_name (str, required):
            The name of the Test being created.
        product_id (str, optional):
            Product ID to associate the Test with. If not specified, the Test will not be associated with a product.
        test_type (str, required):
            Test type of the scanner which indicates the output file format from the scanner. Valid values are "cyclonedx" and others. For the full list see the API documentation.

    Raises:
        ValueError: Raised if business_unit_id, created_by_user_id, asset_id, artifact_id, or test_name are not provided.
        Exception: Raised if the query fails.

    Returns:
        dict: createTest Object
    """
    return create_test(token, organization_context, business_unit_id=business_unit_id, created_by_user_id=created_by_user_id, asset_id=asset_id, artifact_id=artifact_id, test_name=test_name, product_id=product_id, test_type=test_type)


def file_chunks(file_path, chunk_size=1024 * 1024 * 1024 * 5):
    """
    Helper method to read a file in chunks.

    Args:
        file_path (str):
            Local path to the file to read.
        chunk_size (int, optional):
            The size of the chunks to read. Defaults to 5GB.

    Yields:
        bytes: The next chunk of the file.

    Raises:
        FileIO Exceptions: Raised if the file cannot be opened or read correctly.
    """
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break


def get_all_artifacts(token, organization_context, artifact_id=None, business_unit_id=None):
    """
    Get all artifacts in the organization. Uses pagination to get all results.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        artifact_id (str, optional):
            An optional Artifact ID if this is used to get a single artifact, by default None
        business_unit_id (str, optional):
            An optional Business Unit ID if this is used to get artifacts for a single business unit, by default None

    Raises:
        Exception: Raised if the query fails.

    Returns:
        list: List of Artifact Objects
    """
    return get_all_paginated_results(token, organization_context, queries.ALL_ARTIFACTS['query'], queries.ALL_ARTIFACTS['variables'](artifact_id, business_unit_id), 'allAssets')


def get_all_assets(token, organization_context, asset_id=None, business_unit_id=None):
    """
    Gets all assets in the organization. Uses pagination to get all results.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        asset_id (str, optional):
            Asset ID to get, by default None. If None specified, will get all Assets. If specified, will get only the Asset with that ID.
        business_unit_id (str, optional):
            Business Unit ID to filter by, by default None. If None specified, will get all Assets. If specified, will get only the Assets in the specified Business Unit.

    Raises:
        Exception: Raised if the query fails.

    Returns:
        list: List of Asset Objects
    """
    return get_all_paginated_results(token, organization_context, queries.ALL_ASSETS['query'], queries.ALL_ASSETS['variables'](asset_id, business_unit_id), 'allAssets')


def get_all_asset_versions(token, organization_context):
    """
    Get all asset versions in the organization. Uses pagination to get all results.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".

    Raises:
        Exception: Raised if the query fails.

    Returns:
        list: List of AssetVersion Objects
    """
    return get_all_paginated_results(token, organization_context, queries.ALL_ASSET_VERSIONS['query'], queries.ALL_ASSET_VERSIONS['variables'], 'allAssetVersions')


def get_all_asset_versions_for_product(token, organization_context, product_id):
    """
    Get all asset versions for a product. Uses pagination to get all results.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        product_id (str):
            The Product ID to get asset versions for

    Returns:
        list: List of AssetVersion Objects
    """
    return get_all_paginated_results(token, organization_context, queries.ONE_PRODUCT_ALL_ASSET_VERSIONS['query'], queries.ONE_PRODUCT_ALL_ASSET_VERSIONS['variables'](product_id), 'allProducts')


def get_all_business_units(token, organization_context):
    """
    Get all business units in the organization. NOTE: The return type here is Group. Uses pagination to get all results.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".

    Raises:
        Exception: Raised if the query fails.

    Returns:
        list: List of Group Objects
    """
    return get_all_paginated_results(token, organization_context, queries.ALL_BUSINESS_UNITS['query'], queries.ALL_BUSINESS_UNITS['variables'], 'allGroups')


def get_all_organizations(token, organization_context):
    """
    Get all organizations available to the user. For most users there is only one organization. Uses pagination to get all results.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".

    Raises:
        Exception: Raised if the query fails.

    Returns:
        list: List of Organization Objects
    """
    return get_all_paginated_results(token, organization_context, queries.ALL_ORGANIZATIONS['query'], queries.ALL_ORGANIZATIONS['variables'], 'allOrganizations')


def get_all_paginated_results(token, organization_context, query, variables=None, field=None):
    """
    Get all results from a paginated GraphQL query

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        query (str):
            The GraphQL query string
        variables (dict, optional):
            Variables to be used in the GraphQL query, by default None
        field (str, required):
            The field in the response JSON that contains the results

    Raises:
        Exception: If the response status code is not 200, or if the field is not in the response JSON

    Returns:
        list: List of results
    """

    if not field:
        raise Exception("Error: field is required")

    # query the API for the first page of results
    response_data = send_graphql_query(token, organization_context, query, variables)

    # if there are no results, return an empty list
    if not response_data:
        return []

    # create a list to store the results
    results = []

    # add the first page of results to the list
    if field in response_data['data']:
        results.extend(response_data['data'][field])
    else:
        raise Exception(f"Error: {field} not in response JSON")

    if len(response_data['data'][field]) > 0:
        # get the cursor from the last entry in the list
        cursor = response_data['data'][field][len(response_data['data'][field]) - 1]['_cursor']

        while cursor:
            variables['after'] = cursor

            # add the next page of results to the list
            response_data = send_graphql_query(token, organization_context, query, variables)
            results.extend(response_data['data'][field])

            try:
                cursor = response_data['data'][field][len(response_data['data'][field]) - 1]['_cursor']
            except IndexError:
                # when there is no additional cursor, stop getting more pages
                cursor = None

    return results


def get_all_products(token, organization_context):
    """
    Get all products in the organization. Uses pagination to get all results.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".

    Raises:
        Exception: Raised if the query fails.

    Returns:
        list: List of Product Objects
    """
    return get_all_paginated_results(token, organization_context, queries.ALL_PRODUCTS['query'], queries.ALL_PRODUCTS['variables'], 'allProducts')


def get_all_users(token, organization_context):
    """
    Get all users in the organization. Uses pagination to get all results.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".

    Raises:
        Exception: Raised if the query fails.

    Returns:
        list: List of User Objects
    """
    return get_all_paginated_results(token, organization_context, queries.ALL_USERS['query'], queries.ALL_USERS['variables'], 'allUsers')


def get_artifact_context(token, organization_context, artifact_id):
    """
    Get the context for a single artifact. This is typically used for querying for existing context, which is used for role based access control. This is not used for creating new artifacts.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".

    Raises:
        Exception: Raised if the query fails.

    Returns:
        dict: Artifact Context Object
    """
    artifact = get_all_paginated_results(token, organization_context, queries.ALL_ARTIFACTS['query'], queries.ALL_ARTIFACTS['variables'](artifact_id, None), 'allAssets')

    return artifact[0]['ctx']


def get_auth_token(client_id, client_secret, token_url=TOKEN_URL, audience=AUDIENCE):
    """
    Get an auth token for use with the API using CLIENT_ID and CLIENT_SECRET

    Args:
        client_id (str):
            CLIENT_ID as specified in the API documentation
        client_secret (str):
            CLIENT_SECRET as specified in the API documentation
        token_url (str, optional):
            Token URL, by default TOKEN_URL
        audience (str, optional):
            Audience, by default AUDIENCE

    Raises:
        Exception: If the response status code is not 200

    Returns:
        str: Auth token. Use this token as the Authorization header in subsequent API calls.
    """
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": AUDIENCE,
        "grant_type": "client_credentials"
    }

    headers = {
        'content-type': "application/json"
    }

    response = requests.post(TOKEN_URL, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        auth_token = response.json()['access_token']
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

    return auth_token


def get_findings(token, organization_context, asset_version_id=None, category=None):
    """
    Gets all the Findings for an Asset Version. Uses pagination to get all results.
    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        asset_version_id (str, optional):
            Asset Version ID to get findings for. If not provided, will get all findings in the organization.
        category (str, optional):
            The category of Findings to return. Valid values are "CONFIG_ISSUES", "CREDENTIALS", "CRYPTO_MATERIAL", "CVE", "SAST_ANALYSIS". If not specified, will return all findings. See https://docs.finitestate.io/types/finding-category
    Raises:
        Exception: Raised if the query fails, required parameters are not specified, or parameters are incompatible.
    Returns:
        list: List of Finding Objects
    """
    if not asset_version_id:
        raise Exception("Asset Version ID is required")

    return get_all_paginated_results(token, organization_context, queries.GET_FINDINGS['query'], queries.GET_FINDINGS['variables'](asset_version_id=asset_version_id, category=category), 'allFindings')


def get_product_asset_versions(token, organization_context, product_id=None):
    """
    Gets all the asset versions for a product.
    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        product_id (str, optional):
            Product ID to get asset versions for. If not provided, will get all asset versions in the organization.
    Raises:
        Exception: Raised if the query fails, required parameters are not specified, or parameters are incompatible.
    Returns:
        list: List of AssetVersion Objects
    """
    if not product_id:
        raise Exception("Product ID is required")

    return get_all_paginated_results(token, organization_context, queries.GET_PRODUCT_ASSET_VERSIONS['query'], queries.GET_PRODUCT_ASSET_VERSIONS['variables'](product_id), 'allProducts')


def get_products(token, organization_context, business_unit_id=None):
    """
    Gets all the products for the specified business unit.
    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        business_unit_id (str, optional):
            Business Unit ID to get products for. If not provided, will get all products in the organization.
    Raises:
        Exception: Raised if the query fails, required parameters are not specified, or parameters are incompatible.
    Returns:
        list: List of Product Objects
    """

    if not business_unit_id:
        raise Exception("Business Unit ID is required")

    return get_all_paginated_results(token, organization_context, queries.GET_PRODUCTS_BUSINESS_UNIT['query'], queries.GET_PRODUCTS_BUSINESS_UNIT['variables'](business_unit_id), 'allProducts')


def get_software_components(token, organization_context, asset_version_id=None, type=None):
    """
    Gets all the Software Components for an Asset Version. Uses pagination to get all results.
    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        asset_version_id (str, optional):
            Asset Version ID to get software components for.
        type (str, optional):
            The type of software component to return. Valid values are "APPLICATION", "ARCHIVE", "CONTAINER", "DEVICE", "FILE", "FIRMWARE", "FRAMEWORK", "INSTALL", "LIBRARY", "OPERATING_SYSTEM", "OTHER", "SERVICE", "SOURCE". If not specified, will return all software components. See https://docs.finitestate.io/types/software-component-type
    Raises:
        Exception: Raised if the query fails, required parameters are not specified, or parameters are incompatible.
    Returns:
        list: List of Software Component Objects
    """
    if not asset_version_id:
        raise Exception("Asset Version ID is required")

    return get_all_paginated_results(token, organization_context, queries.GET_SOFTWARE_COMPONENTS['query'], queries.GET_SOFTWARE_COMPONENTS['variables'](asset_version_id=asset_version_id, type=type), 'allSoftwareComponentInstances')


def search_sbom(token, organization_context, name=None, version=None, asset_version_id=None, search_method='EXACT', case_sensitive=False):
    """
    Searches the SBOM of a specific asset version or the entire organization for matching software components.
    Search Methods: EXACT or CONTAINS
    An exact match will return only the software component whose name matches the name exactly.
    A contains match will return all software components whose name contains the search string.
    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        name (str, required):
            Name of the software component to search for.
        version (str, optional):
            Version of the software component to search for. If not specified, will search for all versions of the software component.
        asset_version_id (str, optional):
            Asset Version ID to search for software components in. If not specified, will search the entire organization.
        search_method (str, optional):
            Search method to use. Valid values are "EXACT" and "CONTAINS". Defaults to "EXACT".
        case_sensitive (bool, optional):
            Whether or not to perform a case sensitive search. Defaults to False.
    Raises:
        ValueError: Raised if name is not provided.
        Exception: Raised if the query fails.
    Returns:
        list: List of SoftwareComponentInstance Objects
    """
    if asset_version_id:
        query = '''
query GetSoftwareComponentInstances(
    $filter: SoftwareComponentInstanceFilter
    $after: String
    $first: Int
) {
    allSoftwareComponentInstances(
        filter: $filter
        after: $after
        first: $first
    ) {
        _cursor
        id
        name
        version
        originalComponents {
            id
            name
            version
        }
    }
}
'''
    else:
        # gets the asset version info that contains the software component
        query = '''
query GetSoftwareComponentInstances(
    $filter: SoftwareComponentInstanceFilter
    $after: String
    $first: Int
) {
    allSoftwareComponentInstances(
        filter: $filter
        after: $after
        first: $first
    ) {
        _cursor
        id
        name
        version
        assetVersion {
            id
            name
            asset {
                id
                name
            }
        }
    }
}
'''

    variables = {
        "filter": {
            "mergedComponentRefId": None
        },
        "after": None,
        "first": 100
    }

    if asset_version_id:
        variables["filter"]["assetVersionRefId"] = asset_version_id

    if search_method == 'EXACT':
        if case_sensitive:
            variables["filter"]["name"] = name
        else:
            variables["filter"]["name_like"] = name
    elif search_method == 'CONTAINS':
        variables["filter"]["name_contains"] = name

    if version:
        if search_method == 'EXACT':
            variables["filter"]["version"] = version
        elif search_method == 'CONTAINS':
            variables["filter"]["version_contains"] = version

    records = get_all_paginated_results(token, organization_context, query, variables=variables, field="allSoftwareComponentInstances")

    return records


def send_graphql_query(token, organization_context, query, variables=None):
    """
    Send a GraphQL query to the API

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        query (str):
            The GraphQL query string
        variables (dict, optional):
            Variables to be used in the GraphQL query, by default None

    Raises:
        Exception: If the response status code is not 200

    Returns:
        dict: Response JSON
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
        'Organization-Context': organization_context
    }
    data = {
        'query': query,
        'variables': variables
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def upload_file_for_binary_analysis(token, organization_context, test_id=None, file_path=None, chunk_size=1024 * 1024 * 1024 * 5):
    """
    Upload a file for Binary Analysis. Will automatically chunk the file into chunks and upload each chunk. Chunk size defaults to 5GB.
    NOTE: This is NOT for uploading third party scanner results. Use upload_test_results_file for that.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        test_id (str, required):
            Test ID to upload the file for.
        file_path (str, required):
            Local path to the file to upload.
        chunk_size (int, optional):
            The size of the chunks to read. Defaults to 5GB.

    Raises:
        ValueError: Raised if test_id or file_path are not provided.
        Exception: Raised if the query fails.

    Returns:
        dict: The response from the GraphQL query, a completeMultipartUpload Object.
    """
    # To upload a file for Binary Analysis, you must use the generateMultiplePartUploadUrl mutation

    if not test_id:
        raise ValueError("Test ID is required")
    if not file_path:
        raise ValueError("File path is required")

    # Start Multi-part Upload
    graphql_query = '''
    mutation Start($input: startMultipartUploadInput!) {
        startMultipartUpload(input: $input) {
            id
            key
        }
    }
    '''

    variables = {
        "input": {
            "testId": test_id
        }
    }

    response = send_graphql_query(token, organization_context, graphql_query, variables)

    upload_id = response['data']['startMultipartUpload']['id']
    upload_key = response['data']['startMultipartUpload']['key']

    # if the file is greater than max chunk size (or 5 GB), split the file in chunks,
    # call generateUploadPartUrl for each chunk of the file (even if it is a single part)
    # and upload the file to the returned upload URL
    i = 1
    part_data = []
    for chunk in file_chunks(file_path, chunk_size):
        graphql_query = '''
        mutation GenerateUploadPartUrl($input: generateUploadPartUrlInput!) {
            generateUploadPartUrl(input: $input) {
                key
                uploadUrl
            }
        }
        '''

        variables = {
            "input": {
                "partNumber": i,
                "uploadId": upload_id,
                "uploadKey": upload_key
            }
        }

        response = send_graphql_query(token, organization_context, graphql_query, variables)

        chunk_upload_url = response['data']['generateUploadPartUrl']['uploadUrl']

        # upload the chunk to the upload URL
        response = upload_bytes_to_url(chunk_upload_url, chunk)

        part_data.append({
            "ETag": response.headers['ETag'],
            "PartNumber": i
        })

    # call completeMultiPartUpload
    graphql_query = '''
    mutation CompleteMultipartUpload($input: CompleteMultipartUploadInput!) {
        completeMultipartUpload(input: $input) {
            key
        }
    }
    '''

    variables = {
        "input": {
            "partData": part_data,
            "testId": test_id,
            "uploadId": upload_id,
            "uploadKey": upload_key
        }
    }

    response = send_graphql_query(token, organization_context, graphql_query, variables)

    return response['data']


def upload_test_results_file(token, organization_context, test_id=None, file_path=None):
    """
    Uploads a test results file to the test specified by test_id. NOTE: This is not for Binary Analysis. Use upload_file_for_binary_analysis for that.

    Args:
        token (str):
            Auth token. This is the token returned by get_auth_token(). Just the token, do not include "Bearer" in this string, that is handled inside the method.
        organization_context (str):
            Organization context. This is provided by the Finite State API management. It looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        test_id (str, required):
            Test ID to upload the file for.
        file_path (str, required):
            Local path to the file to upload.

    Raises:
        ValueError: Raised if test_id or file_path are not provided.
        Exception: Raised if the query fails.

    Returns:
        dict: The response from the GraphQL query, a completeTestResultUpload Object.
    """
    if not test_id:
        raise ValueError("Test ID is required")
    if not file_path:
        raise ValueError("File path is required")

    # Gerneate Test Result Upload URL
    graphql_query = '''
    mutation GenerateTestResultUploadUrl($input: generateTestResultUploadUrlInput!) {
        generateTestResultUploadUrl(input: $input) {
            uploadUrl
            key
        }
    }
    '''

    variables = {
        "input": {
            "orgId": organization_context,
            "testId": test_id
        }
    }

    response = send_graphql_query(token, organization_context, graphql_query, variables)

    # get the upload URL and key
    upload_url = response['data']['generateTestResultUploadUrl']['uploadUrl']
    key = response['data']['generateTestResultUploadUrl']['key']

    # upload the file
    upload_file_to_url(upload_url, file_path)

    # complete the upload
    graphql_query = '''
    mutation CompleteTestResultUpload($input: completeTestResultUploadInput!) {
        completeTestResultUpload(input: $input) {
            key
        }
    }
    '''

    variables = {
        "input": {
            "testId": test_id,
            "key": key
        }
    }

    response = send_graphql_query(token, organization_context, graphql_query, variables)
    return response['data']


def upload_bytes_to_url(url, bytes):
    """
    Used for uploading a file to a pre-signed S3 URL

    Args:
        url (str):
            (Pre-signed S3) URL
        bytes (bytes):
            Bytes to upload

    Raises:
        Exception: If the response status code is not 200

    Returns:
        requests.Response: Response object
    """
    response = requests.put(url, data=bytes)

    if response.status_code == 200:
        return response
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def upload_file_to_url(url, file_path):
    """
    Used for uploading a file to a pre-signed S3 URL

    Args:
        url (str):
            (Pre-signed S3) URL
        file_path (str):
            Local path to file to upload

    Raises:
        Exception: If the response status code is not 200

    Returns:
        requests.Response: Response object
    """
    with open(file_path, 'rb') as file:
        response = requests.put(url, data=file)

    if response.status_code == 200:
        return response
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
