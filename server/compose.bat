set INFLUXDB_HTTP_AUTH_ENABLED='true' docker run -p 8086:8086 -e INFLUXDB_DB='iotdb' -e INFLUXDB_ADMIN_USER='miniproject1_user' -e INFLUXDB_ADMIN_PASSWORD='miniproject1_pass' influxdb:1.8.10

docker run -p 3000:3000 grafana/grafana:10.2.0