"""
Token auth.
"""

from typing import Dict, Optional

from preset_cli.auth.main import Auth


class TokenAuth(Auth):  # pylint: disable=too-few-public-methods, abstract-method
    """
    Auth via a token.
    """

    def __init__(
        self,
        token: str,
        *,
        verify_ssl: bool = True,
        ca_bundle: Optional[str] = None,
    ):
        super().__init__(verify_ssl=verify_ssl, ca_bundle=ca_bundle)
        self.token = token

    def get_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}
