#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import base64


class APIException(Exception):
    """Cscart API 异常类"""
    def __init__(self, message: str = "", status_code: int = -1) -> None:
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return repr("[ERROR:%d] %s" % (self.status_code, self.message))


class Cscart:
    """Cscart API 客户端"""
    def __init__(self, domain: str, email: str, api_key: str,
                 api_version: int = 1) -> None:
        """初始化Cscart API客户端

        :domain: cscart域名
        :email: 管理员email
        :api_key: API KEY
        :api_version: API版本(默认为1)
        :returns: None

        """
        self.api_version = api_version

        self.url_base = domain + self._api_prefix(self.api_version)

        self.authorization = "Basic " + base64.b64encode(
            f"{email}:{api_key}".encode("utf-8")).decode("utf-8")

        self.headers = {
            "authorization": self.authorization,
        }

    def _api_prefix(self, api_version) -> str:
        """获取api URL的前缀

        :api_version: API版本
        :returns: api URL前缀

        """
        if api_version == 1:
            return "/api"
        elif api_version == 2:
            return "/api2"
        else:
            raise APIException("NOT FOUND API version[%d]" % (self.api_version))

    def _url(self, api: str) -> str:
        """拼接出完整的api URL

        :api: 操作部分的API
        :returns: 完整的api URL

        """
        return self.url_base + api

    def _check_response(self, r: requests.Response, success_status_code: int,
                        error_message: str) -> requests.Response:
        """检查响应是否是成功执行

        :r: HTTP响应
        :success_status_code: 响应成功的HTTP代码
        :error_message: 响应失败时要显示的错误信息
        :returns: HTTP响应

        """
        if r.status_code == success_status_code:
            return r
        else:
            raise APIException(error_message, r.status_code)

    def _get(self, api: str) -> requests.Response:
        """发送GET请求

        :api: 目标api
        :returns: HTTP响应

        """
        url = self._url(api)
        r = requests.get(url, headers=self.headers)
        return self._check_response(r, 200, "GET " + url)

    def _delete(self, api: str) -> requests.Response:
        """发送DELETE请求

        :api: 目标api
        :returns: HTTP响应

        """
        url = self._url(api)
        r = requests.delete(url, headers=self.headers)
        return self._check_response(r, 204, "DELETE " + url)

    def _post(self, api: str, data: dict) -> requests.Response:
        """发送POST请求

        :api: 目标api
        :data: 请求中附带的数据
        :returns: HTTP响应

        """
        url = self._url(api)
        self.headers.update({'Content-Type': 'application/json'})
        r = requests.post(url, json=data, headers=self.headers)
        del self.headers['Content-Type']
        return self._check_response(r, 201, "CREATE " + url)

    def _put(self, api: str, data: dict) -> requests.Response:
        """发送PUT请求

        :api: 目标api
        :data: 请求中附带的数据
        :returns: HTTP响应

        """
        url = self._url(api)
        self.headers.update({'Content-Type': 'application/json'})
        r = requests.put(url, json=data, headers=self.headers)
        del self.headers['Content-Type']
        return self._check_response(r, 200, "UPDATE " + url)

    def get_orders(self,
            page: int = 1,
            items_per_page: int = 10,
            sort_by: str = "date",
            sort_order: str = "desc",
            status: str = "",
            user_id: str = "",
            company_id: str = "",
            email: str = "",
            invoice_id: str = "",
            credit_memo_id: str = "") -> dict:
        """获取订单列表

        :page: 当前页数
        :items_per_page: 每页显示数量
        :sort_by: 排序关键字
        :sort_order: 排序顺序
        :status: 按订单状态筛选
        :user_id: 按用户id筛选
        :company_id: 按公司ID筛选
        :email: 按电子邮件筛选
        :invoice_id: 按发票ID筛选
        :credit_memo_id: 按信用卡备忘录ID筛选
        :returns: 订单列表

        """
        sort_order_list = ['asc', 'desc']
        status_list = ['P', 'C', 'O', 'F', 'D', 'B', 'I', 'Y']

        params = dict()
        params['page'] = str(page)
        params['items_per_page'] = str(items_per_page)
        params['sort_by'] = sort_by
        if sort_order in sort_order_list:
            params['sort_order'] = sort_order
        else:
            raise APIException("sort_order must in %a" % (sort_order_list))
        if len(status) > 0:
            if status in status_list:
                params['status'] = status
            else:
                raise APIException("status must in %a" % (status_list))
        if len(user_id) > 0:
            params['user_id'] = user_id
        if len(company_id) > 0:
            params['company_id'] = company_id
        if len(email) > 0:
            params['email'] = email
        if len(invoice_id) > 0:
            params['invoice_id'] = invoice_id
        if len(credit_memo_id) > 0:
            params['credit_memo_id'] = credit_memo_id

        api = "/orders?" + '&'.join(["%s=%s" % (k, v) for k, v in params.items()])
        return self._get(api).json()

    def get_order(self, order_id: str) -> dict:
        """获取订单

        :order_id: 订单ID
        :returns: 订单详细信息

        """
        api = "/orders/" + order_id
        return self._get(api).json()

    def delete_order(self, order_id: str) -> None:
        """删除订单

        :order_id: 订单ID
        :returns: None

        """
        api = "/orders/" + order_id
        self._delete(api)

    def create_order(self, company_id: str, data: dict) -> dict:
        """创建订单

        :company_id: 单用户都用1
        :data: 订单信息
        :returns: order_id

        """
        api = "/stores/%s/orders" % (company_id)
        return self._post(api, data).json()

    def update_order(self, order_id: str, data: dict) -> dict:
        """更新订单

        :order_id: 订单ID
        :data: 订单信息
        :returns: order_id

        """
        api = "/orders/" + order_id
        return self._put(api, data).json()

    def get_product(self, product_id: str, data: dict) -> dict:
        """获取产品信息

        :product_id: 产品ID
        :returns: 产品详细信息

        """
        api = "/products/" + product_id
        return self._get(api).json()

    def update_order_status(self, order_id: str, new_status: str) -> dict:
        """更新订单状态

        :order_id: 订单ID
        :new_status: 订单新状态
        :returns: order_id

        """
        data = {
                "status": new_status,
                "notify_user": "1",
                "notify_department": "1",
                "notify_vendor": "1"
                }
        return self.update_order(order_id, data)

if __name__ == "__main__":
    import os

    domain = os.environ['DOMAIN']
    email = os.environ['EMAIL']
    api_key = os.environ['API_KEY']

    c = Cscart(domain, email, api_key)

    # test update order status
    print(c.get_product('10939', None))

    #test get orders
    #print(c.get_orders(status='P'))

    # test get
    #print(c.get_order('1210818'))

    # test delete
    #print(c.delete_order('xxxxxx'))

    # test create
    #data = {
        #"user_id": "6993",
        #"shipping_id": "4",
        #"payment_id": "21",
        #"products": {
            #"205693": {
                #"amount": "1"
            #}
        #}
    #}
    #print(c.create_order("1", data))

    # test update
    #data = {
            #"status": "O"
    #}
    #print(c.update_order('1210826', data))
