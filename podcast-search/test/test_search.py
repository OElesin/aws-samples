from fastapi import HTTPException
from fastapi.testclient import TestClient
from api.search import app, parse_rss_feed
from api.search import parse_rss_feed
from podcast_search.api.search import app, SearchQuery, parse_rss_feed
from podcast_search.api.search import app, parse_rss_feed
from search import parse_rss_feed
from unittest.mock import patch
from unittest.mock import patch, MagicMock
import pytest
import xml.etree.ElementTree as ET

client = TestClient(app)

class TestSearch:

    def test_get_all_episodes_empty_feed(self, monkeypatch):
        """
        Test that get_all_episodes returns an empty list when the RSS feed contains no episodes.
        """
        def mock_parse_rss_feed():
            return []

        monkeypatch.setattr("podcast_search.lambda.search.parse_rss_feed", mock_parse_rss_feed)

        response = client.get("/episodes")
        assert response.status_code == 200
        assert response.json() == {"episodes": []}

    def test_get_all_episodes_file_not_found(self, monkeypatch):
        """
        Test that get_all_episodes raises an HTTPException when the RSS file is not found.
        """
        def mock_parse_rss_feed():
            raise FileNotFoundError("RSS file not found")

        monkeypatch.setattr("podcast_search.lambda.search.parse_rss_feed", mock_parse_rss_feed)

        response = client.get("/episodes")
        assert response.status_code == 500
        assert "Error parsing RSS feed: RSS file not found" in response.json()["detail"]

    def test_get_all_episodes_invalid_xml(self, monkeypatch):
        """
        Test that get_all_episodes raises an HTTPException when the RSS file contains invalid XML.
        """
        def mock_parse_rss_feed():
            raise ET.ParseError("Invalid XML")

        monkeypatch.setattr("podcast_search.lambda.search.parse_rss_feed", mock_parse_rss_feed)

        response = client.get("/episodes")
        assert response.status_code == 500
        assert "Error parsing RSS feed: Invalid XML" in response.json()["detail"]

    def test_get_all_episodes_missing_channel(self, monkeypatch):
        """
        Test that get_all_episodes raises an HTTPException when the RSS feed is missing the channel element.
        """
        def mock_parse_rss_feed():
            raise ValueError("No channel element found in RSS feed")

        monkeypatch.setattr("podcast_search.lambda.search.parse_rss_feed", mock_parse_rss_feed)

        response = client.get("/episodes")
        assert response.status_code == 500
        assert "Error parsing RSS feed: No channel element found in RSS feed" in response.json()["detail"]

    @patch('lambda.search.parse_rss_feed')
    def test_get_all_episodes_success(self, mock_parse_rss_feed):
        """
        Test that get_all_episodes returns all episodes successfully
        """
        # Mock the parse_rss_feed function to return a list of episodes
        mock_episodes = [
            {
                "title": "Episode 1",
                "summary": "Summary 1",
                "episodeType": "full",
                "image": "image1.jpg",
                "content": "Content 1",
                "player": "player1.mp3"
            },
            {
                "title": "Episode 2",
                "summary": "Summary 2",
                "episodeType": "full",
                "image": "image2.jpg",
                "content": "Content 2",
                "player": "player2.mp3"
            }
        ]
        mock_parse_rss_feed.return_value = mock_episodes

        # Make a GET request to the /episodes endpoint
        response = client.get("/episodes")

        # Assert the response status code is 200 (OK)
        assert response.status_code == 200

        # Assert the response JSON contains the expected episodes
        assert response.json() == {"episodes": mock_episodes}

        # Verify that parse_rss_feed was called once
        mock_parse_rss_feed.assert_called_once()

    def test_get_all_episodes_unexpected_error(self, monkeypatch):
        """
        Test that get_all_episodes raises an HTTPException when an unexpected error occurs.
        """
        def mock_parse_rss_feed():
            raise Exception("Unexpected error")

        monkeypatch.setattr("podcast_search.lambda.search.parse_rss_feed", mock_parse_rss_feed)

        response = client.get("/episodes")
        assert response.status_code == 500
        assert "Unexpected error" in response.json()["detail"]

    def test_parse_rss_feed_file_not_found(self):
        """
        Test parsing RSS feed with file not found error.
        """
        with patch('xml.etree.ElementTree.parse', side_effect=FileNotFoundError("File not found")):
            with pytest.raises(HTTPException) as exc_info:
                parse_rss_feed()
            
            assert exc_info.value.status_code == 500
            assert "Error parsing RSS feed: File not found" in str(exc_info.value.detail)

    def test_parse_rss_feed_missing_elements(self):
        """
        Test parsing RSS feed with missing elements in items.
        """
        mock_xml_content = '''
        <rss>
            <channel>
                <item>
                    <title>Test Episode</title>
                </item>
            </channel>
        </rss>
        '''
        
        with patch('xml.etree.ElementTree.parse') as mock_parse:
            mock_tree = MagicMock()
            mock_root = ET.fromstring(mock_xml_content)
            mock_tree.getroot.return_value = mock_root
            mock_parse.return_value = mock_tree
            
            result = parse_rss_feed()
            
            assert len(result) == 1
            assert result[0]['title'] == 'Test Episode'
            assert result[0]['summary'] is None
            assert result[0]['episodeType'] is None
            assert result[0]['image'] is None
            assert result[0]['content'] is None
            assert result[0]['player'] is None

    def test_parse_rss_feed_no_channel(self):
        """
        Test parse_rss_feed when the RSS feed has no channel element.
        """
        mock_xml = """
        <?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
        </rss>
        """
        
        with patch('xml.etree.ElementTree.parse') as mock_parse:
            mock_tree = ET.ElementTree(ET.fromstring(mock_xml))
            mock_parse.return_value = mock_tree
            
            with pytest.raises(HTTPException) as exc_info:
                parse_rss_feed()
            
            assert exc_info.value.status_code == 500
            assert "No channel element found in RSS feed" in str(exc_info.value.detail)

    def test_parse_rss_feed_no_channel_2(self):
        """
        Test parsing RSS feed with no channel element.
        """
        mock_xml_content = '<rss></rss>'
        
        with patch('xml.etree.ElementTree.parse') as mock_parse:
            mock_tree = MagicMock()
            mock_root = ET.fromstring(mock_xml_content)
            mock_tree.getroot.return_value = mock_root
            mock_parse.return_value = mock_tree
            
            with pytest.raises(HTTPException) as exc_info:
                parse_rss_feed()
            
            assert exc_info.value.status_code == 500
            assert "No channel element found in RSS feed" in str(exc_info.value.detail)

    def test_parse_rss_feed_successful(self):
        """
        Test successful parsing of RSS feed with valid channel and items.
        """
        mock_xml_content = '''
        <rss>
            <channel>
                <item>
                    <title>Test Episode</title>
                    <summary>Test Summary</summary>
                    <episodeType>full</episodeType>
                    <image>http://example.com/image.jpg</image>
                    <content:encoded xmlns:content="http://purl.org/rss/1.0/modules/content/">Test Content</content:encoded>
                    <player>http://example.com/player</player>
                </item>
            </channel>
        </rss>
        '''
        
        with patch('xml.etree.ElementTree.parse') as mock_parse:
            mock_tree = MagicMock()
            mock_root = ET.fromstring(mock_xml_content)
            mock_tree.getroot.return_value = mock_root
            mock_parse.return_value = mock_tree
            
            result = parse_rss_feed()
            
            assert len(result) == 1
            assert result[0]['title'] == 'Test Episode'
            assert result[0]['summary'] == 'Test Summary'
            assert result[0]['episodeType'] == 'full'
            assert result[0]['image'] == 'http://example.com/image.jpg'
            assert result[0]['content'] == 'Test Content'
            assert result[0]['player'] == 'http://example.com/player'

    def test_parse_rss_feed_with_empty_channel(self, mocker):
        """
        Test parse_rss_feed with an XML file that has an empty channel element.
        """
        mock_tree = mocker.Mock()
        mock_root = mocker.Mock()
        mock_channel = mocker.Mock()
        mock_channel.findall.return_value = []
        mock_root.find.return_value = mock_channel
        mock_tree.getroot.return_value = mock_root
        mocker.patch('xml.etree.ElementTree.parse', return_value=mock_tree)

        result = parse_rss_feed("empty_channel.xml")
        assert result == []

    def test_parse_rss_feed_with_empty_file(self):
        """
        Test parse_rss_feed with an empty XML file.
        """
        with pytest.raises(HTTPException) as exc_info:
            parse_rss_feed("empty.xml")
        assert exc_info.value.status_code == 500
        assert "Error parsing RSS feed" in str(exc_info.value.detail)

    def test_parse_rss_feed_with_incorrect_type(self):
        """
        Test parse_rss_feed with an incorrect input type.
        """
        with pytest.raises(TypeError):
            parse_rss_feed(123)

    def test_parse_rss_feed_with_invalid_xml(self):
        """
        Test parse_rss_feed with an invalid XML file.
        """
        with pytest.raises(HTTPException) as exc_info:
            parse_rss_feed("invalid.xml")
        assert exc_info.value.status_code == 500
        assert "Error parsing RSS feed" in str(exc_info.value.detail)

    def test_parse_rss_feed_with_missing_item_elements(self, mocker):
        """
        Test parse_rss_feed with an XML file that has missing item elements.
        """
        mock_tree = mocker.Mock()
        mock_root = mocker.Mock()
        mock_channel = mocker.Mock()
        mock_item = mocker.Mock()
        mock_item.find.return_value = None
        mock_channel.findall.return_value = [mock_item]
        mock_root.find.return_value = mock_channel
        mock_tree.getroot.return_value = mock_root
        mocker.patch('xml.etree.ElementTree.parse', return_value=mock_tree)

        result = parse_rss_feed("missing_elements.xml")
        assert result == [{'title': None, 'summary': None, 'episodeType': None, 'image': None, 'content': None, 'player': None}]

    def test_parse_rss_feed_with_no_channel_element(self, mocker):
        """
        Test parse_rss_feed with an XML file that has no channel element.
        """
        mock_tree = mocker.Mock()
        mock_root = mocker.Mock()
        mock_root.find.return_value = None
        mock_tree.getroot.return_value = mock_root
        mocker.patch('xml.etree.ElementTree.parse', return_value=mock_tree)

        with pytest.raises(HTTPException) as exc_info:
            parse_rss_feed("no_channel.xml")
        assert exc_info.value.status_code == 500
        assert "No channel element found in RSS feed" in str(exc_info.value.detail)

    def test_parse_rss_feed_with_nonexistent_file(self):
        """
        Test parse_rss_feed with a nonexistent file.
        """
        with pytest.raises(HTTPException) as exc_info:
            parse_rss_feed("nonexistent.xml")
        assert exc_info.value.status_code == 500
        assert "Error parsing RSS feed" in str(exc_info.value.detail)

    def test_search_episodes_empty_query(self):
        """
        Test search_episodes with an empty query string.
        """
        response = client.post("/search", json={"query": ""})
        assert response.status_code == 200
        assert response.json() == {"results": []}

    def test_search_episodes_invalid_query_type(self):
        """
        Test search_episodes with an invalid query type (not a string).
        """
        response = client.post("/search", json={"query": 123})
        assert response.status_code == 422

    def test_search_episodes_missing_query(self):
        """
        Test search_episodes with a missing query parameter.
        """
        response = client.post("/search", json={})
        assert response.status_code == 422

    def test_search_episodes_no_results(self, monkeypatch):
        """
        Test search_episodes when no results are found.
        """
        def mock_parse_rss_feed():
            return [{"title": "Unrelated Episode", "content": "No matching content", "summary": "No match here"}]

        monkeypatch.setattr("podcast-search.lambda.search.parse_rss_feed", mock_parse_rss_feed)
        
        response = client.post("/search", json={"query": "nonexistent"})
        assert response.status_code == 200
        assert response.json() == {"results": []}

    @patch('podcast_search.lambda.search.parse_rss_feed')
    def test_search_episodes_returns_matching_results(self, mock_parse_rss_feed):
        """
        Test that search_episodes returns matching results when given a valid query
        """
        # Mock the parse_rss_feed function to return test data
        mock_parse_rss_feed.return_value = [
            {"title": "Test Episode 1", "content": "This is test content", "summary": "Test summary"},
            {"title": "Another Episode", "content": "More content", "summary": "Another summary"},
            {"title": "Third Episode", "content": "Even more content", "summary": "Third summary"}
        ]

        # Create a test query
        query = SearchQuery(query="test")

        # Make a POST request to the /search endpoint
        response = client.post("/search", json=query.dict())

        # Check that the response status code is 200 (OK)
        assert response.status_code == 200

        # Check that the response contains the expected results
        expected_results = [
            {"title": "Test Episode 1", "content": "This is test content", "summary": "Test summary"}
        ]
        assert response.json() == {"results": expected_results}

        # Verify that parse_rss_feed was called
        mock_parse_rss_feed.assert_called_once()

    def test_search_episodes_special_characters(self):
        """
        Test search_episodes with special characters in the query.
        """
        response = client.post("/search", json={"query": "!@#$%^&*()"})
        assert response.status_code == 200
        assert response.json() == {"results": []}

    def test_search_episodes_sql_injection_attempt(self):
        """
        Test search_episodes with a potential SQL injection attempt.
        """
        response = client.post("/search", json={"query": "'; DROP TABLE episodes; --"})
        assert response.status_code == 200
        assert response.json() == {"results": []}

    def test_search_episodes_very_long_query(self):
        """
        Test search_episodes with an extremely long query string.
        """
        long_query = "a" * 10000  # Very long query
        response = client.post("/search", json={"query": long_query})
        assert response.status_code == 200
        assert response.json() == {"results": []}

    def test_search_episodes_xml_parsing_error(self, monkeypatch):
        """
        Test search_episodes when XML parsing fails.
        """
        def mock_parse_rss_feed():
            raise Exception("XML parsing error")

        monkeypatch.setattr("podcast-search.lambda.search.parse_rss_feed", mock_parse_rss_feed)
        
        response = client.post("/search", json={"query": "test"})
        assert response.status_code == 500
        assert "XML parsing error" in response.json()["detail"]