# Getting Started (In progress...)

## Installation
I would recommend to install it using [Virtual Environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/) (and [virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvwrapper) that provides autocomplete features).  

Install:
```
mkvirtualenv my_wallet
workon my_wallet
mkdir my_wallet
cd my_wallet
git clone https://github.com/gdi3d/my_wallet .
pip install -r requirements.txt
./local_server.sh
```
Now open your browser at:

[http://127.0.0.1:8000](http://127.0.0.1:8000) and login using:

**username:** demo  
**password:** demo

The data, using the local environment (setted by local_server.sh), is saved using sqlite as a database.

---

## Apps
My wallets it's divided into 3 apps

* [API](#api)
* [Wallet](#wallet)
* [Website](#website)

## API
The api app it's very simple and has only one file **urls.py**.

The only function of this app is to expose API urls of others applications. This way I can handle all my API url routing in one place
and if I ever need to change it to some other path, like **api/v2/**, I just change it over there.

## Wallet
All the models, views and serializers of the project.

## Website
A web interface to use the application based mostly on javascript.

You can take a look at **website/static/js/wallet.js** for more info. 

Each view is represented by a singleton that handles all the CRUD operations by talking to the API

Components used:

* [Bootstrap](http://getbootstrap.com/)
* [jQuery](https://jquery.com/)
* [jQuery Numeric](http://www.texotela.co.uk/code/jquery/numeric/)
* [jQuery Cookie](https://github.com/carhartl/jquery-cookie)
* [accounting](http://openexchangerates.github.io/accounting.js)
* [jQuery Simple Pagination](http://flaviusmatis.github.com/simplePagination.js/)
* [Knockout](http://knockoutjs.com/index.html)
* [Knockout Mapping Plugin](http://knockoutjs.com/documentation/plugins-mapping.html)

---

## API EndPoints
My wallet has several endpoints that you can use

### Items
Returns all the items on the transactions for the current user in all the wallets.

It's the representation of the Items model on **wallet/models.py**

Api Response example:

**GET /api/v1/items/**
```
HTTP 200 OK
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS

{
    "count": 2, 
    "next": null, 
    "previous": null, 
    "results": [
        {
            "id": 134, 
            "category": {
                "id": 41, 
                "name": "Freelance Work"
            }, 
            "amount": "120.0000", 
            "note": "Bugfix", 
            "pending": false
        }, 
        {
            "id": 135, 
            "category": {
                "id": 2, 
                "name": "Food"
            }, 
            "amount": "-50.0000", 
            "note": "Dinner", 
            "pending": false
        }
    ]
}
```
For more info on this endpoint check [http://127.0.0.1:8000/api/v1/items/](http://127.0.0.1:8000/api/v1/items/)

### Transactions
Returns all the transactions for the current user in all wallets

It's the representation of the Transaction model on **wallet/models.py**

Api response example:

**GET api/v1/transactions**
```
HTTP 200 OK
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS

{
    "count": 2, 
    "next": null, 
    "previous": null, 
    "results": [
        {
            "id": 88, 
            "item": {
                "id": 134, 
                "category": {
                    "id": 41, 
                    "name": "Freelance Work"
                }, 
                "amount": "120.0000", 
                "note": "Bugfix", 
                "pending": false
            }, 
            "wallet": {
                "id": 8, 
                "name": "Bank account", 
                "initial_amount": "500.0000", 
                "note": "My first account"
            }, 
            "date": "2015-03-14"
        }, 
        {
            "id": 89, 
            "item": {
                "id": 135, 
                "category": {
                    "id": 2, 
                    "name": "Food"
                }, 
                "amount": "-50.0000", 
                "note": "Dinner", 
                "pending": false
            }, 
            "wallet": {
                "id": 8, 
                "name": "Bank account", 
                "initial_amount": "500.0000", 
                "note": "My first account"
            }, 
            "date": "2015-03-14"
        }
    ]
}
```
For more info on this endpoint check [http://127.0.0.1:8000/api/v1/transactions/](http://127.0.0.1:8000/api/v1/transactions/)

### Transactions Total
Returns the total amount of a transactions search

Api response example:

**GET api/v1/transactions-total**
```
HTTP 200 OK
Content-Type: application/json
Vary: Accept
Allow: GET, HEAD, OPTIONS

{
    "total": "70.00"
}
```
For more documentation on this endpoint check [http://127.0.0.1:8000/api/v1/transactions-total/](http://127.0.0.1:8000/api/v1/transactions-total/)

### Category
Returns all the categories for the current user

It's the representation of the Category model on **wallet/models.py**

Api response example:

**GET api/v1/category**
```
HTTP 200 OK
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS

{
    "count": 6, 
    "next": null, 
    "previous": null, 
    "results": [
        {
            "id": 2, 
            "name": "Food"
        }, 
        {
            "id": 41, 
            "name": "Freelance Work"
        }, 
        {
            "id": 3, 
            "name": "Gas"
        }
        ...
    ]
}
```
For more documentation on this endpoint check [http://127.0.0.1:8000/api/v1/category/](http://127.0.0.1:8000/api/v1/category/)

### Wallet
Returns all the wallets for the current user

It's the representation of the Wallet model on **wallet/models.py**

Api response example:

**GET api/v1/wallet**
```
HTTP 200 OK
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS

{
    "count": 1, 
    "next": null, 
    "previous": null, 
    "results": [
        {
            "id": 8, 
            "name": "Bank account", 
            "initial_amount": "500.0000", 
            "note": "My first account"
        }
    ]
}
```
For more documentation on this endpoint check [http://127.0.0.1:8000/api/v1/wallet/](http://127.0.0.1:8000/api/v1/wallet/)

### Wallet Total
Returns the balance of each wallet for the current user

It's the representation of the Wallet model on **wallet/models.py**

Api response example:

**GET api/v1/wallet-total**
```
HTTP 200 OK
Content-Type: application/json
Vary: Accept
Allow: GET, HEAD, OPTIONS

{
    "count": 1, 
    "next": null, 
    "previous": null, 
    "results": [
        {
            "wallet": {
                "id": 8, 
                "name": "Bank account", 
                "initial_amount": "500.0000", 
                "note": "My first account"
            }, 
            "total": "70.0000"
        }
    ]
}
```
For more documentation on this endpoint check [http://127.0.0.1:8000/api/v1/wallet-total/](http://127.0.0.1:8000/api/v1/wallet-total/)