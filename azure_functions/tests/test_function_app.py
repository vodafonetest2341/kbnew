import unittest
from behave import given, when, then
from azure.functions import HttpRequest, HttpResponse
from function_app import getContent  # Import your Azure Function
import os


class __TestGetContentFunction__(unittest.TestCase):
    server_url = os.getenv("SERVER_URL")
    api_url = server_url + "api/getContent"

    def test_valid_container_pathpdf(self):
        # Mock the HttpRequest object with a valid container path
        req = HttpRequest(
            method="GET",
            url=self.api_url,
            params={"containerFilePath": "landing/sharepoint/Test.pdf"},
        )
        # Call the Azure Function
        response = getContent(req)
        # Assert that the response is an HttpResponse with status code 200
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)

        # Add more assertions to validate the response content if needed

    def test_valid_container_pathimage(self):
        # Mock the HttpRequest object with a valid container path
        req = HttpRequest(
            method="GET",
            url=self.api_url,
            params={"containerFilePath": "landing/sharepoint/Test.png"},
        )
        # Call the Azure Function
        response = getContent(req)
        # Assert that the response is an HttpResponse with status code 200
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)

        # Add more assertions to validate the response content if needed

    def test_valid_container_pathtxt(self):
        # Mock the HttpRequest object with a valid container path
        req = HttpRequest(
            method="GET",
            url=self.api_url,
            params={"containerFilePath": "landing/sharepoint/Test.txt"},
        )
        # Call the Azure Function
        response = getContent(req)
        # Assert that the response is an HttpResponse with status code 200
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)

        # Add more assertions to validate the response content if needed

    def test_valid_container_pathjson(self):
        # Mock the HttpRequest object with a valid container path
        req = HttpRequest(
            method="GET",
            url=self.api_url,
            params={"containerFilePath": "landing/sharepoint/Test.json"},
        )
        # Call the Azure Function
        response = getContent(req)
        # Assert that the response is an HttpResponse with status code 200
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)

        # Add more assertions to validate the response content if needed

    def test_invalid_container_path(self):
        # Mock the HttpRequest object with an invalid container path
        req = HttpRequest(
            method="GET",
            url=self.api_url,
            params={"containerFilePath": "landing1/sharepoint/Benefit_Options.pdf"},
        )
        # Call the Azure Function
        response = getContent(req)
        # Assert that the response is an HttpResponse with status code 404
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 404)

        # Add more assertions to validate the response content if needed

    # Add more test cases for different scenarios as needed


if __name__ == "__main__":
    unittest.main()
