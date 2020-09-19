import os
import sys
from google.cloud import bigquery
from data.secrets import *

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd()+"/data/"+GOOGLE_APPLICATION_CREDENTIALS

# Construct a BigQuery client object.
client = bigquery.Client()

tablename = demoname = sys.argv[1].split('/')[-1].split('.')[0]

table_id = projectname+"."+datasetname+"."+tablename

job_config = bigquery.LoadJobConfig(
	source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
)

job_config.write_disposition = 'WRITE_TRUNCATE'

file_path = sys.argv[1]
with open(file_path, "rb") as source_file:
	job = client.load_table_from_file(source_file, table_id, job_config=job_config)

job.result()  # Waits for the job to complete.

table = client.get_table(table_id)  # Make an API request.
print(f"{tablename}: uploaded {table.num_rows} rows and {len(table.schema)} columns uploaded to {projectname}.{datasetname}")