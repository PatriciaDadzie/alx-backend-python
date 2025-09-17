#!/usr/bin/env python3
"""
Tests for client.py:
- unit tests for GithubOrgClient using patch decorators and context managers
- integration tests using fixtures and parameterized_class
"""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock, PropertyMock

import client
from client import GithubOrgClient
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([("google",), ("abc",)])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json: Mock):
        expected = {"login": org_name}
        mock_get_json.return_value = expected
        gh = GithubOrgClient(org_name)
        self.assertEqual(gh.org, expected)
        mock_get_json.assert_called_once_with(GithubOrgClient.ORG_URL.format(org=org_name))

    def test_public_repos_url(self):
        gh = GithubOrgClient("test_org")
        fake_org = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock, return_value=fake_org):
            self.assertEqual(gh._public_repos_url, fake_org["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: Mock):
        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = repos_payload
        gh = GithubOrgClient("test_org")
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock, return_value="fake-url"):
            repos = gh.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_get_json.assert_called_once()
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock, return_value="fake-url"):
            mock_get_json.reset_mock()
            mock_get_json.return_value = repos_payload
            apache_repos = gh.public_repos(license="apache-2.0")
            self.assertEqual(apache_repos, ["repo2"])
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: dict, license_key: str, expected: bool):
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)

@parameterized_class(("org_payload", "repos_payload", "expected_repos", "apache2_repos"), [(fixtures.org_payload, fixtures.repos_payload, fixtures.expected_repos, fixtures.apache2_repos)])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using fixtures"""

    @classmethod
    def setUpClass(cls):
        # mocked responses for requests.get(...).json()
        org_resp = Mock()
        org_resp.json.return_value = cls.org_payload
        repos_resp = Mock()
        repos_resp.json.return_value = cls.repos_payload

        def get_side_effect(url, *args, **kwargs):
            if url.endswith("/repos") or "/repos" in url:
                return repos_resp
            return org_resp

        # patch top-level requests.get so utils.get_json receives the mock
        cls.get_patcher = patch("requests.get", side_effect=get_side_effect)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        gh = GithubOrgClient("whatever")
        self.assertEqual(sorted(gh.public_repos()), sorted(self.expected_repos))

    def test_public_repos_with_license(self):
        gh = GithubOrgClient("whatever")
        self.assertEqual(sorted(gh.public_repos(license="apache-2.0")), sorted(self.apache2_repos))
