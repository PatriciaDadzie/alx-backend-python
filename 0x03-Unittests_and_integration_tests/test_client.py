#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient class.
"""

from unittest import TestCase
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and get_json is called once with the expected URL.
        """
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, test_payload)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns the expected list of repos,
        and that _public_repos_url and get_json are each called once.
        """
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = "http://fake.url"

            client = GithubOrgClient("test_org")
            result = client.public_repos()

            # Validate results
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            # Ensure mocks were called correctly
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://fake.url")


if __name__ == "__main__":
    import unittest
    unittest.main()
