"""
Mechanisms for authentication and authorization.
"""

from typing import Any, Dict, Optional, Union

from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class Auth:  # pylint: disable=too-few-public-methods
    """
    An authentication/authorization mechanism.
    """

    def __init__(
        self,
        verify_ssl: bool = True,
        ca_bundle: Optional[str] = None,
    ):
        self.session = Session()
        # SSL verification config:
        # - verify_ssl=False  -> skip cert verification entirely (insecure)
        # - ca_bundle=PATH    -> verify against the given CA bundle (recommended for
        #                       internal CAs / self-hosted Superset behind a private CA)
        # - default           -> verify against requests' bundled (certifi) CAs
        self.verify: Union[bool, str] = False if not verify_ssl else (ca_bundle or True)
        self.session.verify = self.verify
        self.session.hooks["response"].append(self.reauth)

        retries = Retry(
            total=3,  # max retries count
            backoff_factor=1,  # delay factor between attempts
            respect_retry_after_header=True,
        )

        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def get_headers(self) -> Dict[str, str]:
        """
        Return headers for auth.
        """
        return {}

    def auth(self) -> None:
        """
        Perform authentication, fetching JWT tokens, CSRF tokens, cookies, etc.
        """
        raise NotImplementedError("Must be implemented for reauthorizing")

    # pylint: disable=invalid-name, unused-argument
    def reauth(self, r: Response, *args: Any, **kwargs: Any) -> Response:
        """
        Catch 401 and re-auth.
        """
        if r.status_code != 401:
            return r

        # Prevent infinite recursion by temporarily disabling the hook
        hooks = self.session.hooks
        self.session.hooks = {"response": []}

        try:
            self.auth()
        except NotImplementedError:
            self.session.hooks = hooks
            return r
        except Exception:
            # If auth fails, restore hooks and return the 401 response
            self.session.hooks = hooks
            return r

        self.session.headers.update(self.get_headers())
        r.request.headers.update(self.get_headers())

        try:
            # Retry without triggering hooks again. Honour the session's verify
            # setting rather than hardcoding verify=False (previous behaviour
            # silently disabled TLS verification on every reauth, which is
            # exactly what we don't want).
            retry_response = self.session.send(r.request, verify=self.verify)
            return retry_response
        finally:
            # Restore the hooks
            self.session.hooks = hooks
