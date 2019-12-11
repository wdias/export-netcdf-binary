import logging
from flask import Blueprint, request, Response, stream_with_context
import requests
from datetime import datetime, timedelta

bp = Blueprint('ascii_grid', __name__)
logger = logging.getLogger(__name__)

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
ADAPTER_GRID = 'http://adapter-grid.default.svc.cluster.local'


@bp.route('/export/netcdf/binary/<string:timeseries_id>/<string:request_name>', methods=['GET'])
def get_export_netcdf_binary(timeseries_id: str, request_name: str):
    assert timeseries_id, 'Timeseries ID should be provided'
    assert request_name.endswith('.nc'), 'Request file name should ends with .nc'
    start = request.args.get('start')
    assert start, 'start date time should be provide'
    start_time = datetime.strptime(start, DATE_TIME_FORMAT)
    end = request.args.get('end')
    if end:
        end_time = datetime.strptime(end, DATE_TIME_FORMAT)
    else:
        end_time = start_time + timedelta(hours=24)
    query_string = f"start={start}&end={end_time.strftime(DATE_TIME_FORMAT)}"
    logger.info(f'>> {timeseries_id}, {request_name}, {query_string}')

    # Solution via: 1. https://stackoverflow.com/a/5166423/1461060
    # combining 2. https://stackoverflow.com/a/39217788/1461060
    return Response(requests.get(f'{ADAPTER_GRID}/timeseries/{timeseries_id}/{request_name}?{query_string}', stream=True), direct_passthrough=True, mimetype='application/x-netcdf4')

    # Solution by: ``. https://stackoverflow.com/a/16696317/1461060
    # 2. http://flask.pocoo.org/docs/1.0/patterns/streaming/#streaming-with-context
    # def generate():
    #     with requests.get(f'{ADAPTER_GRID}/timeseries/{timeseries_id}/{request_name}', stream=True) as r:
    #         for chunk in r.iter_content(chunk_size=1024):
    #             if chunk:  # filter out keep-alive new chunks
    #                 yield chunk
    #
    # return Response(stream_with_context(generate()), direct_passthrough=True)
