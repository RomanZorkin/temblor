import clickhouse_connect

client = clickhouse_connect.get_client(
    host='0.0.0.0',
    username='boba',
    password='123',
    port=8123,
    database='quake',
)