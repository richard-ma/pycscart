import requests
import base64
import json

if __name__ == "__main__":

    # get order_ids

    domain = "http://clothingfan.com/api"
    email = "mywebadmin@admin.com"
    api_key = "v21AY99014bJ76133UZhgCl46AB66G07"

    authorization = "Basic " + base64.b64encode(
                f"{email}:{api_key}".encode("utf-8")
    ).decode("utf-8")
    headers = {"authorization": authorization}

    api = "/orders"
    url = domain + api

    order_ids = list()
    params = dict()
    page = 1
    items_per_page = 10
    total_items = 100

    params['page'] = page

    while page * items_per_page < total_items:
        req = requests.get(url, params=params, headers=headers)
        if req.status_code == 200:
            print("[%d/%d] success" % (page * items_per_page, total_items))
            data = req.json()

            orders = data['orders']
            for order in orders:
                order_ids.append(order['order_id'])
            params = data['params']

            page += 1
            items_per_page = int(params['items_per_page'])
            total_items = int(params['total_items'])
        else:
            print("failed")
            break


    api = "/orders/"
    orders = dict()
    idx = 1
    with open("order.dat", "w") as f:
        for order_id in order_ids:
            url = domain + api + str(order_id)
            req = requests.get(url, headers=headers)
            data = req.json()
            f.write(json.dumps(data))
            f.write("\n")
            print("%d/%d" % (idx, len(order_ids)))
            idx += 1
