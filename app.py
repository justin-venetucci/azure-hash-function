import azure.functions as func
import hashlib
import json
import logging
import base64

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

import azure.functions as func

@app.route(route="get-hash")
def get_hash(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid request body",
            status_code=400
        )

    try:
        file_body_base64 = req_body.get('file/body')
        file_name = req_body.get('file/name')
    except (KeyError, TypeError):
        return func.HttpResponse(
            "Invalid request parameters",
            status_code=400
        )

    if not file_body_base64 or not file_name:
        return func.HttpResponse(
            "Missing required parameters",
            status_code=400
        )

    try:
        file_content = base64.b64decode(file_body_base64)
    except (ValueError, TypeError):
        return func.HttpResponse(
            "Invalid base64 encoding for file/body",
            status_code=400
        )

    file_hash = hashlib.sha256(file_content).hexdigest()

    response_body = {
        "hash": file_hash
    }

    return func.HttpResponse(
        body=json.dumps(response_body),
        status_code=200,
        mimetype="application/json"
    )
