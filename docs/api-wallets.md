# Overview

This endpoint it's the representation of the **Wallet** model found in **[wallet/models.py](https://github.com/gdi3d/my_wallet/blob/master/wallet/models.py)**

[http://127.0.0.1:8000/api/v1/wallet/](http://127.0.0.1:8000/api/v1/wallet/)

There's also another endpoint that will return the total (the sum of all of transactions) of each wallet.

If you wish to know the balance of that wallet you need to sum the **initial_amount** for each wallet.

[http://127.0.0.1:8000/api/v1/wallet-total/](http://127.0.0.1:8000/api/v1/wallet-total/)


## Methods

* [GET](#get)
* [POST](#post)
* [PUT](#put)
* [DELETE](#delete)

You can try out all this methods using your browsing. Just open the url from above. Just remember to be logged in first.

### GET

Send GET request to [http://127.0.0.1:8000/api/v1/wallet/](http://127.0.0.1:8000/api/v1/wallet/)

It would return a JSON like this:

```
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

### POST

Send a POST request to [http://127.0.0.1:8000/api/v1/wallet/](http://127.0.0.1:8000/api/v1/wallet/) with this JSON data structure:

```
{
    "name": "My new wallet", 
    "initial_amount": "100.1234", 
    "note": "Savings account"
}
```

It will return a **201** status code if the wallet was created. And the created object like this:

```
{
	"id": 5,
    "name": "My new wallet", 
    "initial_amount": "100.1234", 
    "note": "Savings account"
}
```

### PUT

Send a PUT request to [http://127.0.0.1:8000/api/v1/wallet/ID/](http://127.0.0.1:8000/api/v1/wallet/ID/) with this JSON data structure:

```
{
	"id": 5,
    "name": "My new wallet", 
    "initial_amount": "200.1234", 
    "note": "Savings account"
}
```

It will return a **200** status code if the wallet was updated. And the updated object:

```
{
	"id": 5,
    "name": "My new wallet", 
    "initial_amount": "200.1234", 
    "note": "Savings account"
}
```

### DELETE

Send a DELETE request to [http://127.0.0.1:8000/api/v1/wallet/ID/](http://127.0.0.1:8000/api/v1/wallet/ID/)

It will return a **204** status code if the wallet was deleted

## Tests

You can read the test code at **[wallet/tests.py](https://github.com/gdi3d/my_wallet/blob/master/wallet/tests.py)**. Just take a look at the TestCase **WalletTestCase**
