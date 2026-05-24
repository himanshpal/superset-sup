"""
Mechanisms for authentication and authorization for Superset instances.
"""

from typing import Dict, Optional

from yarl import URL

from preset_cli.auth.token import TokenAuth


class SupersetJWTAuth(TokenAuth):  # pylint: disable=abstract-method
    """
    Auth to Superset via JWT token.
    """

    def __init__(
        self,
        token: str,
        baseurl: URL,
        *,
        verify_ssl: bool = True,
        ca_bundle: Optional[str] = None,
    ):
        super().__init__(token, verify_ssl=verify_ssl, ca_bundle=ca_bundle)
        self.baseurl = baseurl

    def get_csrf_token(self, jwt: str) -> str:
        """
        Get a CSRF token.
        """
        response = self.session.get(
            self.baseurl / "api/v1/security/csrf_token",  # type: ignore
            headers={"Authorization": f"Bearer {jwt}"},
        )
        response.raise_for_status()
        payload = response.json()
        return payload["result"]

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "X-CSRFToken": self.get_csrf_token(self.token),
        }


class UsernamePasswordAuth(SupersetJWTAuth):  # pylint: disable=too-few-public-methods
    """
    Auth to Superset via username/password.

    Uses Superset's /api/v1/security/login endpoint to get a JWT token,
    then inherits JWT authentication behavior from SupersetJWTAuth.
    """

    def __init__(
        self,
        baseurl: URL,
        username: str,
        password: Optional[str] = None,
        *,
        verify_ssl: bool = True,
        ca_bundle: Optional[str] = None,
    ):
        super().__init__("", baseurl, verify_ssl=verify_ssl, ca_bundle=ca_bundle)

        self.baseurl = baseurl
        self.username = username
        self.password = password
        self.token = self.auth()

    def auth(self) -> str:
        """
        Login to Superset using username/password and return access token.
        Uses /api/v1/security/login endpoint.
        """
        payload = {
            "username": self.username,
            "password": self.password,
            "provider": "db",
        }

        response = self.session.post(
            self.baseurl / "api/v1/security/login",  # type: ignore
            json=payload,
        )
        response.raise_for_status()
        payload = response.json()

        return payload["access_token"]
