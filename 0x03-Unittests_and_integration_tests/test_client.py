#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient class.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected repos URL."""
        test_payload = {"repos_url": "http://fake.url/repos"}

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
        ) as mock_org:
            mock_org.return_value = test_payload

            client = GithubOrgClient("test_org")
            result = client._public_repos_url

            self.assertEqual(result, "http://fake.url/repos")
            mock_org.assert_called_once()

    def test_public_repos(self):
        """Test GithubOrgClient.public_repos with mocked payload and URL."""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]

        with patch("client.get_json", return_value=test_payload) as mock_get_json:
            with patch.object(
                GithubOrgClient,
                "_public_repos_url",
                new_callable=PropertyMock,
            ) as mock_repos_url:
                mock_repos_url.return_value = "http://fake.url"

                client = GithubOrgClient("test_org")
                result = client.public_repos()

                self.assertEqual(result, ["repo1", "repo2", "repo3"])
                mock_repos_url.assert_called_once()
                mock_get_json.assert_called_once_with("http://fake.url")
