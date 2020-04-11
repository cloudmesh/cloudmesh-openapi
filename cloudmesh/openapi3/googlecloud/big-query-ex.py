from google.cloud import bigquery


# def __init__(self, filepath=None, dataset="Dataset_1", table="Table1", client=bigquery.Client()):
#     self.filepath = filepath
#     self.dataset = dataset
#     self.table = table
#     self.client = client
class Google:

    def pushFileBQ(dataset):

        client = bigquery.Client()
        filename = '/Users/andrewgoldfarb/Desktop/test-data/data/flavors.csv'
        dataset_id = dataset
        table_id = "my_table"
        
        dataset_ref = client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.CSV
        job_config.skip_leading_rows = 1
        job_config.autodetect = True

        with open(filename, "rb") as source_file:
            job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

        job.result()  # Waits for table load to complete.

        print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))
