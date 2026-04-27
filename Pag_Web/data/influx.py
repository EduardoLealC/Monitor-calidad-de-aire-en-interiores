from influxdb_client import InfluxDBClient
from config import INFLUX_URL, TOKEN, ORG, BUCKET, DEVICE, FIELDS

def get_latest_values() -> dict:
    """Retorna el último valor de cada campo como {field: value}."""
    client = InfluxDBClient(url=INFLUX_URL, token=TOKEN, org=ORG)
    query_api = client.query_api()

    fields_flux = ", ".join(f'"{f}"' for f in FIELDS)
    query = f'''
    from(bucket: "{BUCKET}")
      |> range(start: -5m)
      |> filter(fn: (r) => r._measurement == "ambiente" and r.device == "{DEVICE}")
      |> filter(fn: (r) => contains(value: r._field, set: [{fields_flux}]))
      |> last()
    '''
    result = query_api.query(org=ORG, query=query)
    data = {}
    for table in result:
        for record in table.records:
            data[record.get_field()] = record.get_value()
    client.close()
    return data