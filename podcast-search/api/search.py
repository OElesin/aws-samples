import os
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import json
from pathlib import Path
import utils
import reranker
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title="Podcast Search API.",
    description="API for searching and retrieving podcast episodes from RSS feed",
    version="1.0.0"
)


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/episodes",
         response_model=Dict[str, List[Dict]],
         summary="Get all podcast episodes",
         description="Retrieves all podcast episodes from the RSS feed",
         response_description="List of podcast episodes",
         responses={
             200: {"description": "Successfully retrieved episodes"},
             500: {"description": "Internal server error"}
         })
async def get_all_episodes():
    try:
        episodes = utils.read_podcasts_json_file()
        return {"episodes": episodes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search",
          response_model=Dict[str, List[Dict]],
          summary="Search podcast episodes",
          description="Search for podcast episodes based on a query string matching title, content, or summary",
          response_description="List of matching podcast episodes",
          responses={
              200: {"description": "Successfully retrieved matching episodes"},
              500: {"description": "Internal server error"}
          })
async def search_episodes(q: str = 'learn about strategy', limit: int = 10):
    try:
        reranked_result = reranker.rerank_podcasts(q, limit)
        return {"results": reranked_result} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


app.mount("/", StaticFiles(directory="build", html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)