import os
import json

from flask import current_app, url_for
from flask_babelex import gettext as _

from .base import BaseTestCase

from opac_schema.v1 import models

FIXTURES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


class RestAPIJournalTestCase(BaseTestCase):
    def load_json_fixture(self, filename):
        with open(os.path.join(FIXTURES_PATH, filename)) as f:
            return json.load(f)

    def setUp(self):
        self.journal_dict = self.load_json_fixture("journal_payload.json")

    def test_add_journal_by_api(self):
        with current_app.app_context():
            with self.client as client:
                response = client.post(
                    url_for("restapi.journal"),
                    data=json.dumps(self.journal_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'{"failed":false,"id":"1678-4464"}\n')

    def test_add_journal_by_api_without_data(self):
        with current_app.app_context():
            with self.client as client:
                response = client.post(
                    url_for("restapi.journal"),
                    data=json.dumps({}),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 500)
            self.assertEqual(
                response.data,
                b'{"error":"The journal is mandatory to mount the URL","failed":true}\n',
            )

    def test_add_journal_by_api_without_id(self):
        del self.journal_dict["id"]

        with current_app.app_context():
            with self.client as client:
                response = client.post(
                    url_for("restapi.journal"),
                    data=json.dumps(self.journal_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )
            self.assertEqual(response.status_code, 500)
            self.assertEqual(
                response.data,
                b'{"error":"ValidationError (Journal:None) (Field is required: [\'_id\', \'jid\'])","failed":true}\n',
            )

    def test_add_journal_by_api_with_wrong_data(self):
        del self.journal_dict["status_history"][0]["date"]

        with current_app.app_context():
            with self.client as client:
                response = client.post(
                    url_for("restapi.journal"),
                    data=json.dumps(self.journal_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )
            self.assertEqual(response.status_code, 500)
            self.assertEqual(
                response.data,
                b'{"error":"ValidationError (Journal:1678-4464) (since.cannot parse date \\"\\": [\'timeline\'])","failed":true}\n',
            )


class RestAPIIssueTestCase(BaseTestCase):
    def load_json_fixture(self, filename):
        with open(os.path.join(FIXTURES_PATH, filename)) as f:
            return json.load(f)

    def setUp(self):
        self.journal_dict = self.load_json_fixture("journal_payload.json")
        self.issue_dict = self.load_json_fixture("issue_payload.json")

    def test_add_issue_by_api(self):
        with current_app.app_context():
            # journal
            with self.client as client:
                response = client.post(
                    url_for("restapi.journal"),
                    data=json.dumps(self.journal_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'{"failed":false,"id":"1678-4464"}\n')

            # issue
            with self.client as client:
                response = client.post(
                    url_for("restapi.issue")
                    + "?journal_id="
                    + self.journal_dict.get("id"),
                    data=json.dumps(self.issue_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.data, b'{"failed":false,"id":"1678-4464-1998-v29-n3"}\n'
            )

    def test_add_issue_by_api_without_data(self):
        with current_app.app_context():
            # journal
            with self.client as client:
                response = client.post(
                    url_for("restapi.journal"),
                    data=json.dumps(self.journal_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'{"failed":false,"id":"1678-4464"}\n')

            # issue
            with self.client as client:
                response = client.post(
                    url_for("restapi.issue")
                    + "?journal_id="
                    + self.journal_dict.get("id"),
                    data=json.dumps({}),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.data, b'{"error":"\'id\'","failed":true}\n')

    def test_add_issue_by_api_without_journal_id(self):
        with current_app.app_context():
            # journal
            with self.client as client:
                response = client.post(
                    url_for("restapi.journal"),
                    data=json.dumps(self.journal_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'{"failed":false,"id":"1678-4464"}\n')

            # issue
            with self.client as client:
                response = client.post(
                    url_for("restapi.issue"),
                    data=json.dumps({}),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.data, b'{"error":"missing param journal_id","failed":true}\n'
            )


class RestAPIAricleTestCase(BaseTestCase):
    def load_json_fixture(self, filename):
        with open(os.path.join(FIXTURES_PATH, filename)) as f:
            return json.load(f)

    def setUp(self):
        self.journal_dict = self.load_json_fixture("journal_payload.json")
        self.issue_dict = self.load_json_fixture("issue_payload.json")
        self.article_dict = self.load_json_fixture("article_payload.json")

    def test_add_article_by_api(self):
        with current_app.app_context():
            # journal
            with self.client as client:
                response = client.post(
                    url_for("restapi.journal"),
                    data=json.dumps(self.journal_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'{"failed":false,"id":"1678-4464"}\n')

            # issue
            with self.client as client:
                response = client.post(
                    url_for("restapi.issue")
                    + "?journal_id="
                    + self.journal_dict.get("id"),
                    data=json.dumps(self.issue_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.data, b'{"failed":false,"id":"1678-4464-1998-v29-n3"}\n'
            )

            # article
            with self.client as client:
                response = client.post(
                    # Using query string to send the params:
                    # ``issue_id``, ``article_id``, ``order``, ``article_url``,
                    url_for("restapi.article")
                    + "?issue_id=%s&article_id=%s&order=%s&article_url=%s"
                    % (
                        self.issue_dict.get("id"),
                        "id_test",
                        1,
                        "http://minio.scielo.org/documentstore/example.xml",
                    ),
                    data=json.dumps(self.article_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'{"failed":false,"id":"id_test"}\n')

            # check if the article is in database
            self.assertTrue(models.Article.objects.get(_id="id_test"))

    def test_add_article_by_api_without_data(self):
        with current_app.app_context():
            # journal
            with self.client as client:
                response = client.post(
                    url_for("restapi.journal"),
                    data=json.dumps(self.journal_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'{"failed":false,"id":"1678-4464"}\n')

            # issue
            with self.client as client:
                response = client.post(
                    url_for("restapi.issue")
                    + "?journal_id="
                    + self.journal_dict.get("id"),
                    data=json.dumps(self.issue_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.data, b'{"failed":false,"id":"1678-4464-1998-v29-n3"}\n'
            )

            # article
            with self.client as client:
                response = client.post(
                    # Using query string to send the params:
                    # ``issue_id``, ``article_id``, ``order``, ``article_url``,
                    url_for("restapi.article")
                    + "?issue_id=%s&article_id=%s&order=%s&article_url=%s"
                    % (
                        self.issue_dict.get("id"),
                        "id_test",
                        1,
                        "http://minio.scielo.org/documentstore/example.xml",
                    ),
                    data=json.dumps({}),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'{"failed":false,"id":"id_test"}\n')
            
            # check if the article is in database
            self.assertTrue(models.Article.objects.get(_id="id_test"))

    def test_add_article_by_api_without_issue_id(self):
        with current_app.app_context():
            # journal
            with self.client as client:
                response = client.post(
                    url_for("restapi.journal"),
                    data=json.dumps(self.journal_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'{"failed":false,"id":"1678-4464"}\n')

            # issue
            with self.client as client:
                response = client.post(
                    url_for("restapi.issue")
                    + "?journal_id="
                    + self.journal_dict.get("id"),
                    data=json.dumps(self.issue_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.data, b'{"failed":false,"id":"1678-4464-1998-v29-n3"}\n'
            )

            # article
            with self.client as client:
                response = client.post(
                    # Using query string to send the params:
                    # ``issue_id``, ``article_id``, ``order``, ``article_url``,
                    url_for("restapi.article")
                    + "?article_id=%s&order=%s&article_url=%s"
                    % (
                        "id_test",
                        1,
                        "http://minio.scielo.org/documentstore/example.xml",
                    ),
                    data=json.dumps(self.article_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.data, b'{"error":"missing param issue_id","failed":true}\n')
            
            # check if the article is in database
            with self.assertRaises(models.Article.DoesNotExist):
                models.Article.objects.get(_id="id_test")

    def test_add_article_by_api_without_article_id(self):
        with current_app.app_context():
            # journal
            with self.client as client:
                response = client.post(
                    url_for("restapi.journal"),
                    data=json.dumps(self.journal_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'{"failed":false,"id":"1678-4464"}\n')

            # issue
            with self.client as client:
                response = client.post(
                    url_for("restapi.issue")
                    + "?journal_id="
                    + self.journal_dict.get("id"),
                    data=json.dumps(self.issue_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.data, b'{"failed":false,"id":"1678-4464-1998-v29-n3"}\n'
            )

            # article
            with self.client as client:
                response = client.post(
                    # Using query string to send the params:
                    # ``issue_id``, ``article_id``, ``order``, ``article_url``,
                    url_for("restapi.article")
                    + "?issue_id=%s&order=%s&article_url=%s"
                    % (
                        self.issue_dict.get("id"),
                        1,
                        "http://minio.scielo.org/documentstore/example.xml",
                    ),
                    data=json.dumps({}),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.data, b'{"error":"missing param article_id","failed":true}\n')
            
            # check if the article is in database
            with self.assertRaises(models.Article.DoesNotExist):
                models.Article.objects.get(_id="id_test")

    def test_add_article_by_api_without_order(self):
        with current_app.app_context():
            # journal
            with self.client as client:
                response = client.post(
                    url_for("restapi.journal"),
                    data=json.dumps(self.journal_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'{"failed":false,"id":"1678-4464"}\n')

            # issue
            with self.client as client:
                response = client.post(
                    url_for("restapi.issue")
                    + "?journal_id="
                    + self.journal_dict.get("id"),
                    data=json.dumps(self.issue_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.data, b'{"failed":false,"id":"1678-4464-1998-v29-n3"}\n'
            )

            # article
            with self.client as client:
                response = client.post(
                    # Using query string to send the params:
                    # ``issue_id``, ``article_id``, ``order``, ``article_url``,
                    url_for("restapi.article")
                    + "?issue_id=%s&article_id=%s&article_url=%s"
                    % (
                        self.issue_dict.get("id"),
                        "id_test",
                        "http://minio.scielo.org/documentstore/example.xml",
                    ),
                    data=json.dumps(self.article_dict),
                    follow_redirects=True,
                    content_type="application/json",
                )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.data, b'{"error":"missing param order","failed":true}\n')
            
            # check if the article is in database
            with self.assertRaises(models.Article.DoesNotExist):
                models.Article.objects.get(_id="id_test")