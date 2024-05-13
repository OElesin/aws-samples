import argparse
import boto3

def start_ingestion_job(data_source_id, knowledge_base_id, region_name='us-east-1'):
    """
    Starts an ingestion job for a Bedrock knowledge base.

    Args:
        data_source_id (str): The ID of the data source to ingest.
        knowledge_base_id (str): The ID of the knowledge base to ingest the data into.
        region_name (str, optional): The AWS region to use. Defaults to 'us-east-1'.

    Returns:
        dict: The response from the Bedrock agent service.
    """
    bedrock_agent = boto3.client('bedrock-agent', region_name=region_name)

    response = bedrock_agent.start_ingestion_job(
        dataSourceId=data_source_id.split('|')[1],
        knowledgeBaseId=knowledge_base_id
    )

    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start a Bedrock ingestion job')
    parser.add_argument('--data-source-id', '-d', required=True, help='The ID of the data source to ingest')
    parser.add_argument('--knowledge-base-id', '-k', required=True, help='The ID of the knowledge base to ingest the data into')
    parser.add_argument('--region', default='us-east-1', help='The AWS region to use')
    args = parser.parse_args()

    response = start_ingestion_job(
        args.data_source_id,
        args.knowledge_base_id,
        args.region
    )

    print(response)
