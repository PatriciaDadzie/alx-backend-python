#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient class.
"""

from unittest import TestCase
from parameterized import parameterized
from unittest.mock import patch
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

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, test_payload)

    @patch.object(GithubOrgClient, "org", new_callable=dict)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url returns the repos_url from org payload.
        """
        expected_url = "https://api.github.com/orgs/testorg/repos"
        mock_org.update({"repos_url": expected_url})

        client = GithubOrgClient("testorg")
        result = client._public_repos_url

        self.assertEqual(result, expected_url)


if __name__ == "__main__":
    import unittest
    unittest.main()
