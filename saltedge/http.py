import base64
import json
import time
from enum import Enum
from typing import Any, Iterator

import requests
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

from saltedge.logging import log


class SaltedgeHttpClient:
    def __init__(
        self, app_id, secret, private_key: bytes, password: str = None
    ):
        self.app_id = app_id
        self.secret = secret

        # with open(private_path, "rb") as private_key:
        self._private_key = serialization.load_pem_private_key(
            private_key, password=password, backend=default_backend()
        )

    class HttpMethod(Enum):
        GET = "GET"
        POST = "POST"
        DELETE = "DELETE"

    @classmethod
    def verify(
        cls, public_key_data: bytes, message: bytes, signature: str
    ) -> bool:
        """
        Verifies the signature on a message.
        :param public_key_data: Bytes, The public key to use to verify the signature.
        :param message: Bytes, The message to verify.
        :param signature: String, The signature on the message.
        :return:
        """
        public_key = serialization.load_pem_public_key(
            public_key_data, backend=default_backend()
        )

        try:
            public_key.verify(
                base64.b64decode(signature),
                message,
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
            return True
        except InvalidSignature as e:
            log.error(
                "Invalid signature: %s",
                e,
                exc_info=True,
                extra={"signature": signature, "_message": message},
            )
            return False

    def get(self, url, query_params: dict = None) -> Iterator[dict]:
        return self._request(
            self.HttpMethod.GET, url, query_params=query_params
        )

    def post(
        self, url, query_params: dict = None, payload: dict = None
    ) -> Iterator[dict]:
        return self._request(
            self.HttpMethod.GET.POST,
            url,
            query_params=query_params,
            payload=payload,
        )

    def delete(self, url, query_params: dict = None) -> dict:
        return next(
            self._request(
                self.HttpMethod.DELETE, url, query_params=query_params
            )
        )

    def _sign(self, message):
        """
        Signs a message.
        :param message: string, Message to be signed.
        :return: string, The signature of the message for the given key.
        """
        return base64.b64encode(
            self._private_key.sign(
                bytes(message.encode("utf8")),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
        )

    def _generate_signature(
        self, method: str, expire: str, url: str, payload: str | None = None
    ) -> str:
        """
        Generates base64 encoded SHA256 signature of the string given params, signed with the client's private key.
        :param method: Uppercase method of the HTTP request. Example: GET, POST, PATCH, PUT, DELETE, etc.;
        :param expire: request expiration time as a UNIX timestamp in UTC timezone. The Recommended value is 1 minute from now. The maximum value is 1 hour from now.
        :param url: The full requested URL, with all its complementary parameters;
        :param payload: the request post body. Should be left empty if it is a GET request, or the body is empty;
        :return: base64 encoded SHA1 signature
        """
        message = "{expire}|{method}|{url}|".format(
            expire=expire, method=method, url=url
        )

        if payload:
            message += "{payload}".format(payload=payload)

        signature = self._sign(message)
        return signature.decode("utf8")

    def _generate_headers(
        self, method: HttpMethod, url: str, payload: str | None
    ) -> dict:
        expire = self._expires_at(minutes=1)

        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Expires-at": expire,
            "App-id": self.app_id,
            "Secret": self.secret,
            "Signature": self._generate_signature(
                method.value.upper(), expire, url, payload
            ),
        }
        return headers

    def _expires_at(self, hours=0, minutes=0, seconds=0):
        return str(time.time() + hours * 3600 + minutes * 60 + seconds)

    def _make_single_http_request(
        self,
        method: HttpMethod,
        url: str,
        params: dict[str, Any],
        payload: dict = None,
    ) -> dict:
        log.debug("Fetching %s. Params: %s", url, params)
        serialized_payload = json.dumps(payload) if payload else None
        query_params = (
            "?" + "&".join([f"{k}={v}" for k, v in params.items()])
            if params
            else ""
        )
        headers: dict = self._generate_headers(
            method, url + query_params, serialized_payload
        )
        response = requests.request(
            method=method.value,
            params=params,
            url=url,
            headers=headers,
            data=serialized_payload,
        )
        if response.status_code >= 400:
            msg = f"Request to {url} exited with code {response.status_code}"
            log.error(msg)
            try:
                payload = response.json()
                msg = payload["error"]
            except Exception as e:
                log.warning("No error class defined in payload: %s", str(e))
            raise Exception(msg)
        return response.json()

    def _request(
        self,
        method: HttpMethod,
        url: str,
        payload: dict = None,
        query_params: dict = None,
    ) -> Iterator[dict]:

        resp: dict = self._make_single_http_request(
            method, url, query_params, payload
        )
        yield resp

        while "meta" in resp and resp["meta"]["next_id"]:
            query_params |= {"from_id": resp["meta"]["next_id"]}
            resp = self._make_single_http_request(
                method, url, query_params, payload
            )
            yield resp
