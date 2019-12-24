import requests
import base64


class APIException(Exception):
    def __init__(self, message: str = "", status_code: int = -1) -> None:
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return repr("[ERROR:%d] %s" % (self.status_code, self.message))


class Cscart:
    def __init__(self, domain: str, email: str, api_key: str,
                 version: int = 1) -> None:
        self.version = version

        self.url_base = domain + self._api_prefix()

        self.authorization = "Basic " + base64.b64encode(
            f"{email}:{api_key}".encode("utf-8")).decode("utf-8")

        self.headers = {"authorization": self.authorization}

    def _api_prefix(self) -> str:
        if self.version == 1:
            return "/api"
        elif self.version == 2:
            return "/api2"
        else:
            raise APIException("NOT FOUND version[%d]" % (self.version))

    def _url(self, api: str) -> str:
        return self.url_base + api

    def _check_response(self, req: requests.Response,
                        success_status_code: int,
                        error_message: str) -> requests.Response:
        if req.status_code == success_status_code:
            return req
        else:
            raise APIException(error_message, req.status_code)

    def _get(self, api: str) -> requests.Response:
        url = self._url(api)
        req = requests.get(url, headers=self.headers)
        return self._check_response(req, 200, "GET "+url)

    def _delete(self, api: str) -> requests.Response:
        url = self._url(api)
        req = requests.delete(url, headers=self.headers)
        return self._check_response(req, 204, "DELETE "+url)

    def _post(self, api: str, data: dict) -> requests.Response:
        url = self._url(api)
        req = requests.post(url, data=data, headers=self.headers)
        return self._check_response(req, 201, "CREATE "+url)

    def _put(self, api: str, data: dict) -> requests.Response:
        url = self._url(api)
        req = requests.put(url, data=data, headers=self.headers)
        return self._check_response(req, 200, "UPDATE "+url)

    def get_orders(self) -> dict:
        api = "/orders"
        return self._get(api).json()

    def get_order(self, order_id: str) -> dict:
        api = "/orders/" + order_id
        return self._get(api).json()

    def delete_order(self, order_id: str) -> None:
        api = "/orders/" + order_id
        self._delete(api)


if __name__ == "__main__":
    c = Cscart(domain="http://clothingfan.com",
               email="mywebadmin@admin.com",
               api_key="v21AY99014bJ76133UZhgCl46AB66G07")
