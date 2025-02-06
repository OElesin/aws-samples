# AI-Powered Podcast Search Application

This project is an AI-powered podcast search application that uses AWS Lambda and React to provide intelligent search results for podcasts.

The application consists of a serverless backend using AWS Lambda and a React-based frontend. It leverages the Cohere machine learning model to rerank search results, providing users with highly relevant podcast recommendations based on their search queries.

The search functionality is implemented as an AWS Lambda function that processes user queries, fetches podcast data, and uses the Cohere model to rank the results. The frontend is built with React and provides a user-friendly interface for searching and displaying podcast results.

## Repository Structure

```
.
├── lambda
│   └── search.py
└── src
    ├── App.js
    ├── components
    │   ├── SearchBar.js
    │   └── SearchResults.js
    └── styles
        ├── App.css
        ├── SearchBar.css
        └── SearchResults.css
```

### Key Files:

- `lambda/search.py`: AWS Lambda function for handling search queries and ranking results
- `src/App.js`: Main React component for the frontend application
- `src/components/SearchBar.js`: React component for the search input
- `src/components/SearchResults.js`: React component for displaying search results

## Usage Instructions

### Installation

Prerequisites:
- Node.js (v14 or later)
- npm (v6 or later)
- AWS CLI configured with appropriate permissions
- Python 3.8 or later (for Lambda function)

Steps:
1. Clone the repository
2. Install frontend dependencies:
   ```
   cd src
   npm install
   ```
3. Deploy the Lambda function:
   ```
   cd lambda
   aws lambda create-function --function-name podcast-search --runtime python3.8 --handler search.lambda_handler --zip-file fileb://search.zip --role <your-lambda-execution-role-arn>
   ```

### Getting Started

1. Start the React development server:
   ```
   cd src
   npm start
   ```
2. Open your browser and navigate to `http://localhost:3000`

### Configuration

- Update the AWS region in `lambda/search.py` if necessary:
  ```python
  bedrock = boto3.client(
      service_name='bedrock-runtime',
      region_name='us-east-1'
  )
  ```
- Modify the `mock_podcasts` list in `lambda/search.py` to include your actual podcast data or replace it with a database query.

### Common Use Cases

1. Searching for podcasts:
   - Enter a search query in the search bar
   - Click the "Search" button or press Enter
   - View the ranked list of podcast results

2. Playing a podcast:
   - Click the play button on a podcast card to open the audio URL in a new tab

### Integration Patterns

- The frontend communicates with the Lambda function through an API endpoint (`/api/search`).
- Ensure that the API Gateway is set up to trigger the Lambda function and that CORS is properly configured.

### Testing & Quality

To run frontend tests:
```
cd src
npm test
```

### Troubleshooting

1. Issue: Search results not loading
   - Check the browser console for error messages
   - Verify that the API endpoint is correctly configured in the frontend code
   - Ensure that the Lambda function has the necessary permissions to access AWS services

2. Issue: Lambda function timing out
   - Increase the Lambda function timeout in the AWS Console
   - Optimize the podcast data retrieval process

Debugging:
- Enable CloudWatch Logs for the Lambda function to view detailed execution logs
- Use `console.log()` statements in the React components for frontend debugging

## Data Flow

The data flow in this application follows these steps:

1. User enters a search query in the SearchBar component
2. The App component sends a POST request to the `/api/search` endpoint
3. The API Gateway triggers the Lambda function
4. The Lambda function processes the query:
   a. Fetches podcast data (currently using mock data)
   b. Uses the Cohere model to rerank the results
5. The ranked results are returned to the frontend
6. The App component updates its state with the search results
7. The SearchResults component renders the podcast cards

```
[User] -> [SearchBar] -> [App] -> [API Gateway] -> [Lambda]
                                                    |
                                                    v
                                               [Cohere Model]
                                                    |
                                                    v
[User] <- [SearchResults] <- [App] <- [API Gateway] <- [Lambda]
```

Note: The current implementation uses mock podcast data in the Lambda function. In a production environment, this would be replaced with a database query or an external API call to fetch real podcast data.