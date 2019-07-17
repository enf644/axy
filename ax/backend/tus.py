""" Sanic blueprint for tus protocol - resumable uploads.
Google for TUS protocol fo more info """

import os
import sys
import base64
import uuid
import shutil
from pathlib import Path
from sanic import response
from sanic import Blueprint
from loguru import logger
import ujson as json
import backend.misc as ax_misc

this = sys.modules[__name__]
tus_bp = Blueprint('sanic_tus')
upload_folder = ax_misc.path('tmp')
if ax_misc.server_is_app_engine():
    upload_folder = str(Path('/tmp'))
upload_url = 'upload'
tus_api_version = '1.0.0'
tus_api_version_supported = '1.0.0'
tus_api_extensions = ['creation', 'termination', 'file-check']
tus_max_file_size = 4294967296  # 4GByte


def write_info(data):
    """ write <guid>.info file with upload info"""
    file_guid = data['guid']
    info_path = os.path.join(
        this.upload_folder, file_guid, file_guid + '.info')
    with open(info_path, 'w') as info_file:
        json.dump(data, info_file, indent=4)


def read_info(file_guid):
    """ reads <guid>.info file with upload info"""

    data = None
    info_path = os.path.join(
        this.upload_folder, file_guid, file_guid + '.info')
    if not os.path.exists(info_path):
        raise Exception
    with open(info_path, 'r') as info_file:
        data = json.load(info_file)
    return data


@tus_bp.route('/api/upload', methods=['POST', 'OPTIONS'])
async def tus_file_upload(request):
    """
        OPTION -> return tus information
        POST -> Create empty file with <guid> name and
            <guid>.info wich contain file info
    """

    if request.method == 'OPTIONS' and request.headers.get(
            'Access-Control-Request-Method', None) is not None:
        # CORS option request, return 200, OK
        return response.text("", status=200)

    if request.method == 'OPTIONS':
        return response.text(
            "",
            headers={
                'Tus-Resumable': this.tus_api_version,
                'Tus-Version': this.tus_api_version_supported,
                'Tus-Extension': ",".join(this.tus_api_extensions),
                'Tus-Max-Size': this.tus_max_file_size
            },
            status=204
        )

    if request.headers.get("Tus-Resumable") is None:
        msg = "Received File upload for unsupported file transfer protocol"
        logger.warning(msg)
        return response.text(msg, status=500)  # INTERNAL_SERVER_ERROR

    # We have POST request, do tus CREATION
    metadata = {}
    for kv in request.headers.get("Upload-Metadata", None).split(","):
        (key, value) = kv.split(" ")
        metadata[key] = base64.b64decode(value)

    file_size = int(request.headers.get("Upload-Length", "0"))
    if file_size > this.tus_max_file_size:
        return response.text(msg, status=413)  # REQUEST_ENTITY_TOO_LARGE

    file_guid = str(uuid.uuid4())
    print('-----------------' + str(this.upload_folder))
    content_dir = os.path.join(this.upload_folder, file_guid)
    os.makedirs(content_dir)

    write_info({
        'guid': file_guid,
        'filename': metadata.get("filename"),
        'file_size': file_size,
        'offset': 0,
        'upload-metadata': request.headers.get("Upload-Metadata")
    })

    try:
        content_path = os.path.join(this.upload_folder, file_guid, file_guid)
        with open(content_path, 'w') as content_file:
            content_file.seek(file_size - 1)
            content_file.write("\0")
    except IOError as ex:
        logger.error("Unable to create file: {}".format(ex))
        return response.text("", status=500)  # INTERNAL_SERVER_ERROR

    return response.text(
        "",
        headers={
            'Location': f"{this.upload_url}/{file_guid}"
        },
        status=201
    )  # CREATED


@tus_bp.route('/api/upload/<file_guid>', methods=['HEAD', 'DELETE', 'PATCH'])
def tus_file_upload_chunk(request, file_guid):
    """
        HEAD -> returns current offset
        DELETE -> deletes upload
        PATCH -> add bytes to uploaded file. If filesize is reached -> rename
            uploaded file
    """

    upload_file_path = os.path.join(this.upload_folder, file_guid, file_guid)
    if os.path.lexists(upload_file_path) is False:
        return response.text(
            "",
            headers={
                'Tus-Resumable': this.tus_api_version,
                'Tus-Version': this.tus_api_version_supported
            },
            status=404
        )  # GONE

    file_info = read_info(file_guid=file_guid)

    if request.method == 'HEAD':
        return response.text(
            "",
            headers={
                'Tus-Resumable': this.tus_api_version,
                'Tus-Version': this.tus_api_version_supported,
                'Upload-Offset': file_info['offset'],
                'Cache-Control': 'no-store'
            },
            status=200
        )  # OK

    if request.method == 'DELETE':
        folder = os.path.join(this.upload_folder, file_guid)
        shutil.rmtree(folder)

        return response.text(
            "",
            headers={
                'Tus-Resumable': this.tus_api_version,
            },
            status=204
        )  # NO_CONTENT

    if request.method == 'PATCH':
        filename = file_info['filename']
        file_offset = int(request.headers.get("Upload-Offset", 0))
        chunk_size = int(request.headers.get("Content-Length", 0))
        file_size = int(file_info['file_size'])

        # check to make sure we're in sync
        if file_offset != int(file_info['offset']):
            return response.text("", status=409)  # CONFLICT

        try:
            content_file = open(upload_file_path, "r+b")
        except IOError:
            content_file = open(upload_file_path, "wb")
        finally:
            content_file.seek(file_offset)
            content_file.write(request.body)
            content_file.close()

        new_offset = file_offset + chunk_size
        file_info['offset'] = new_offset
        write_info(file_info)

        # file transfer complete, rename from resource id to actual filename
        if file_size == new_offset:
            os.rename(upload_file_path, os.path.join(
                this.upload_folder, file_guid, filename))
            os.remove(upload_file_path + '.info')

        return response.text(
            "",
            headers={
                'Tus-Resumable': this.tus_api_version,
                'Upload-Offset': new_offset,
            },
            status=204
        )
