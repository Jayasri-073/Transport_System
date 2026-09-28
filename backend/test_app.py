import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

os.environ["ADMIN_USERNAME"] = "test-admin"
os.environ["ADMIN_PASSWORD"] = "test-password"
os.environ["ADMIN_TOKEN_SECRET"] = "test-token-secret"
sys.path.insert(0, str(Path(__file__).resolve().parent))

import app as transport_app


class TransportApiTests(unittest.TestCase):
    def setUp(self):
        self.upload_dir = tempfile.TemporaryDirectory()
        transport_app.UPLOAD_FOLDER = Path(self.upload_dir.name)
        self.client = transport_app.create_app().test_client()

    def tearDown(self):
        self.upload_dir.cleanup()

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_dashboard_data_is_available(self):
        response = self.client.get("/api/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["success"])

    def test_client_route_serves_the_react_application(self):
        response = self.client.get("/dashboard")
        try:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"<div id=\"root\">", response.data)
        finally:
            response.close()

    def test_upload_requires_admin_token(self):
        self.assertEqual(self.client.post("/api/upload-csv").status_code, 401)

    def test_login_and_reject_non_csv_upload(self):
        login = self.client.post("/api/admin/login", json={"username": "test-admin", "password": "test-password"})
        self.assertEqual(login.status_code, 200)
        token = login.get_json()["token"]
        response = self.client.post(
            "/api/upload-csv",
            headers={"Authorization": f"Bearer {token}"},
            data={"file": (io.BytesIO(b"not,csv"), "not-a-csv.txt")},
        )
        self.assertEqual(response.status_code, 400)

    def test_admin_login_cors_preflight_allows_the_vercel_origin(self):
        response = self.client.options(
            "/api/admin/login",
            headers={
                "Origin": "https://transport-system-cgshok610-transport-system.vercel.app",
                "Access-Control-Request-Method": "POST",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Access-Control-Allow-Origin"),
            "https://transport-system-cgshok610-transport-system.vercel.app",
        )


if __name__ == "__main__":
    unittest.main()
