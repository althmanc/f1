import boto3
import pandas as pd
import io
import time

athena = boto3.client('athena', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')

# Ver detalhes do driver_number 38
query = """
SELECT driver_number, full_name, meeting_name, start_year, final_position
FROM pitwall_silver.fact_race_wide 
WHERE session_type = 'Race' AND driver_number = 38
"""

print("Executando query...")
response = athena.start_query_execution(
    QueryString=query,
    QueryExecutionContext={'Database': 'pitwall_silver'},
    ResultConfiguration={'OutputLocation': 's3://handson-datalake-prd/athena-results/'}
)
query_id = response['QueryExecutionId']

while True:
    status = athena.get_query_execution(QueryExecutionId=query_id)
    state = status['QueryExecution']['Status']['State']
    if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
        break
    time.sleep(0.5)

print(f"Status: {state}")

if state == 'SUCCEEDED':
    output = status['QueryExecution']['ResultConfiguration']['OutputLocation']
    bucket = output.split('/')[2]
    key = '/'.join(output.split('/')[3:])
    obj = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    print(df.to_string())
else:
    error = status['QueryExecution']['Status'].get('StateChangeReason', 'Unknown')
    print(f"Erro: {error}")
