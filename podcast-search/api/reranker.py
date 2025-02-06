import boto3
import json
import random
from utils import read_podcasts_json_file, read_podcasts_json_files
region = 'us-west-2'

bedrock_agent_runtime = boto3.client('bedrock-agent-runtime',region_name='us-west-2')

modelId = "cohere.rerank-v3-5:0"
model_package_arn = f"arn:aws:bedrock:{region}::foundation-model/{modelId}"


def rerank_podcasts(text_query, num_results):
    """
    """
    podcasts = random.choices(list(read_podcasts_json_files()), k=1000)
    podcasts_sources = prepare_text_sources(podcasts)
    response = bedrock_agent_runtime.rerank(
        queries=[
            {
                "type": "TEXT",
                "textQuery": {
                    "text": text_query
                }
            }
        ],
        sources=podcasts_sources,
        rerankingConfiguration={
            "type": "BEDROCK_RERANKING_MODEL",
            "bedrockRerankingConfiguration": {
                "numberOfResults": num_results,
                "modelConfiguration": {
                    "modelArn": model_package_arn,
                }
            }
        }
    )
    ranked_search_results = sort_podcasts_by_rerank(podcasts, response['results'])
    return ranked_search_results


def prepare_text_sources(podcasts):
    """
    """
    sources = []
    for text_source in podcasts:
        sources.append({
            "type": "INLINE",
            "inlineDocumentSource": {
                "type": "JSON",
                "jsonDocument": text_source
            },

        })
    return sources


def sort_podcasts_by_rerank(podcasts, rerank_results):
    """
    """
    podcasts_reranked = []
    for result in rerank_results:
        podcasts_reranked.append(podcasts[int(result['index'])])
    return podcasts_reranked