import requests
import json
import sqlite3

# open the database connection
conn = sqlite3.connect('customer_orders.db')
c = conn.cursor()

# empty the tables
c.execute("DELETE FROM line_items")
c.execute("DELETE FROM orders")
c.execute("DELETE FROM customer")

conn.commit()

# load the json data
with open('orders.json') as f:
    order_data = json.load(f)

    # Using the API add the currency exchange rate
    for order in order_data:
        r = requests.get('https://api.exchangeratesapi.io/' + str(order.get('created_at'))[0:10] + '?base=USD')
        daily_rate = json.loads(r.text).get('rates').get('CAD')
        order['currency_rate'] = daily_rate
        print(order)

        # dump the data along with currency rate into JSON file
        # with open('orders_exchange.json', 'w') as outfile:
        #   json.dump(order_data, outfile)

        # check whether the customer already exists in sqlite DB
        c.execute('SELECT * FROM customer WHERE id = ?', (order.get('customer').get('id'),))
        rows = c.fetchall()

        # insert customers
        if len(rows) == 0:
            c.execute("INSERT INTO customer VALUES (?,?,?)",
                      (order.get('customer').get('id'), order.get('customer').get('name'),
                       order.get('customer').get('email')))

        # insert orders
        c.execute("INSERT INTO orders VALUES (?,?,?,?,?)",
                  (order.get('id'), order.get('customer').get('id'), order.get('total_price'), order.get('created_at'),
                   order.get('currency_rate')))

        # insert line items
        for line_item in order.get('line_items'):
            c.execute("INSERT INTO line_items VALUES (?,?,?,?,?,?)",
                      (line_item.get('id'), line_item.get('product_id'), line_item.get('product_sku'),
                       line_item.get('product_name'), line_item.get('price'), order.get('id')))

        conn.commit()

conn.close()
