
import unittest
from unittest.mock import Mock, patch
import json

from collection import news
from sentiment_analyzer import analyzer
from parquet import base

class TestAutoForexTrading(unittest.TestCase):

    def setUp(self):
        # Setup any common resources or configurations needed for tests.
        pass

    def tearDown(self):
        # Clean up any resources or configurations after each test.
        pass

class TestGetNews(unittest.TestCase):

    @patch('requests.get')
    @patch('json.loads')
    def test_get_news(self, mock_json_loads, mock_requests_get):
        # Set up your mocks and expected values
        with open('./collection/.config.json') as config_file:
            api_keys = json.load(config_file)['news_api_keys']
        query = 'USD'
        mock_json_loads.return_value = {'articles': [{'title': 'Article 1'}]}
        response = Mock()
        response.json.return_value = {'articles': [{'title': 'Article 1'}]}
        mock_requests_get.return_value = response

        # Run the function
        result = news.get_news(api_keys, query)

        # Check if the function returns the expected result
        self.assertEqual(result, [{'title': 'Article 1', 'tag': 'USD'}])

class TestSaveToJson(unittest.TestCase):

    def test_save_to_json(self):
        # Set up some test data
        articles = [{'title': 'Article 1', 'tag': 'tag1'}, {'title': 'Article 2', 'tag': 'tag2'}]

        # Run the function
        news.save_to_json('test.json', articles)

        # Read the file and check if the content is as expected
        with open('test.json', 'r') as f:
            file_content = f.readlines()

        expected_content = ['{"title": "Article 1", "tag": "tag1"}\n', '{"title": "Article 2", "tag": "tag2"}\n']
        self.assertEqual(file_content, expected_content)

    # Add more test functions for other functions you want to test

class TestSentimentAnalysisWithTextBlob(unittest.TestCase):

    def test_positive_sentiment(self):
        content = "I love this product! It's amazing."
        sentiment_score = analyzer.analyze_sentiment_with_textblob(content)
        self.assertTrue(sentiment_score > 6)  # Expecting a positive sentiment score

    def test_negative_sentiment(self):
        content = "This is the worst service ever."
        sentiment_score = analyzer.analyze_sentiment_with_textblob(content)
        self.assertTrue(sentiment_score < 4)  # Expecting a negative sentiment score

    def test_neutral_sentiment(self):
        content = "It's neither good nor bad."
        sentiment_score = analyzer.analyze_sentiment_with_textblob(content)
        self.assertAlmostEqual(sentiment_score, 5, delta=1)  # Expecting a neutral sentiment score

    def test_empty_input(self):
        content = ""
        sentiment_score = analyzer.analyze_sentiment_with_textblob(content)
        self.assertEqual(sentiment_score, 0)  # Expecting a score of 0 for empty input

class TestSentimentAnalysisWithHuggingFace(unittest.TestCase):

    def test_positive_sentiment(self):
        content = "I love this product! It's amazing."
        sentiment_score = analyzer.analyze_sentiment_with_hugging_face(content)
        self.assertTrue(sentiment_score > 6)  # Expecting a positive sentiment score

    def test_negative_sentiment(self):
        content = "This is the worst service ever."
        sentiment_score = analyzer.analyze_sentiment_with_hugging_face(content)
        self.assertTrue(sentiment_score < 4)  # Expecting a negative sentiment score

    def test_neutral_sentiment(self):
        content = "It's neither good nor bad."
        sentiment_score = analyzer.analyze_sentiment_with_hugging_face(content)
        self.assertAlmostEqual(sentiment_score, 5, delta=1)  # Expecting a neutral sentiment score

    def test_empty_input(self):
        content = ""
        sentiment_score = analyzer.analyze_sentiment_with_hugging_face(content)
        self.assertEqual(sentiment_score, 0)  # Expecting a score of 0 for empty input

class TestAnalyzeSentiment(unittest.TestCase):

    def test_valid_data(self):
        #known data
        test_data = [{}]
         
        analyzer.analyze_sentiment(test_data)

        # Check that the output file is created and has the expected content

    def test_missing_content(self):
        # Test 'content' is missing
        test_data = [{"title": "Sample Title", "description": "Sample Description"}]

        analyzer.analyze_sentiment(test_data)

        # Check that the function handles missing content and writes an error message

    def test_empty_data(self):
        # empty dataset
        test_data = []

        analyzer.analyze_sentiment(test_data)

        # Check that the function handles empty data and writes an error message


if __name__ == '__main__':
    unittest.main()
