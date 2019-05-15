import logging
from flask import Blueprint, request, Response, stream_with_context
import requests

bp = Blueprint('ascii_grid', __name__)
logger = logging.getLogger(__name__)

ADAPTER_GRID = 'http://adapter-grid.default.svc.cluster.local'


@bp.route('/export/netcdf/binary/<string:timeseries_id>/<string:request_name>', methods=['GET'])
def get_export_netcdf_binary(timeseries_id: str, request_name: str):
    assert timeseries_id, 'Timeseries ID should be provided'
    assert request_name.endswith('.nc'), 'Request file name should ends with .nc'
    logger.info(f'>> {timeseries_id}, {request_name}')

    # Solution via: 1. https://stackoverflow.com/a/5166423/1461060
    # combining 2. https://stackoverflow.com/a/39217788/1461060
    return Response(requests.get(f'{ADAPTER_GRID}/timeseries/{timeseries_id}/{request_name}', stream=True), direct_passthrough=True, mimetype='application/x-netcdf4')

    # Solution by: ``. https://stackoverflow.com/a/16696317/1461060
    # 2. http://flask.pocoo.org/docs/1.0/patterns/streaming/#streaming-with-context
    # def generate():
    #     with requests.get(f'{ADAPTER_GRID}/timeseries/{timeseries_id}/{request_name}', stream=True) as r:
    #         for chunk in r.iter_content(chunk_size=1024):
    #             if chunk:  # filter out keep-alive new chunks
    #                 yield chunk
    #
    # return Response(stream_with_context(generate()), direct_passthrough=True)
