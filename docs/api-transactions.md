# Overview

This endpoint it's the representation of the **Transaction** model found in **[wallet/models.py](https://github.com/gdi3d/my_wallet/blob/master/wallet/models.py)**

[http://127.0.0.1:8000/api/v1/transactions/](http://127.0.0.1:8000/api/v1/transactions/)

There's another endpoint for transactions that will return the total amount for a transaction set.

[http://127.0.0.1:8000/api/v1/transactions-total/](http://127.0.0.1:8000/api/v1/transactions-total/)

## Methods

* [GET](#get)
* [POST](#post)
* [PUT](#put)
* [DELETE](#delete)

You can try out all this methods using your browsing. Just open the url from above. Just remember to be logged in first.

### GET

Send GET request to [http://127.0.0.1:8000/api/v1/transactions/](http://127.0.0.1:8000/api/v1/transactions/)

It would return a JSON like this:

```
{
    "count": 2, 
    "next": null, 
    "previous": null, 
    "results": [
        {
            "id": 88, 
            "item": {
                "id": 134, 
                "category": null, 
                "amount": "120.0000", 
                "note": "Bugfix eal"
            }, 
            "wallet": {
                "id": 8, 
                "name": "Bank account", 
                "initial_amount": "500.0000", 
                "note": "My first account"
            }, 
            "date": "2015-03-14"
        }, 
        ...
    ]
}
```

### POST

Send a POST request to [http://127.0.0.1:8000/api/v1/transactions/](http://127.0.0.1:8000/api/v1/transactions/) with this JSON data structure:

```
 {
    "item": {
    	"category_id": 1, 
    	"amount": "9.5432", 
    	"note":"Hey! i'm creating a transaction"
   	},
    "date": "2015/01/01",
    "wallet_id": 1            
}
```

It will return a **201** status code if the transaction was created. And the created object like this:

```
{
	"item": {
	    "category": {"name": "category", 'id': 1}, 
	    "amount": "9.5432", 
	    "note": "Hey! i'm creating a transaction",
	    'id': 1,
	},
	"date": "2015-01-01",
	"wallet": {
	    "id": 1,
	    "name": "wallet",
	    "initial_amount": "1.1234", 
	    "note": "Some note"
	},
	"id": 1
}
```

### PUT

Send a PUT request to [http://127.0.0.1:8000/api/v1/transactions/ID/](http://127.0.0.1:8000/api/v1/transactions/ID/) with this JSON data structure:

```
 {
    "item": {
    	"category_id": 1, 
    	"amount": "9.5432", 
    	"note":"Hey! i'm updating a transaction"
   	},
    "date": "2015/01/01",
    "wallet_id": 1,
    "id": 1          
}
```

It will return a **200** status code if the transaction was updated. And the updated object:

```
{
	"item": {
	    "category": {"name": "category", 'id': 1}, 
	    "amount": "9.5432", 
	    "note": "Hey! i'm updating a transaction",
	    'id': 1,
	},
	"date": "2015-01-01",
	"wallet": {
	    "id": 1,
	    "name": "wallet",
	    "initial_amount": "1.1234", 
	    "note": "Some note"
	},
	"id": 1
}
```

### DELETE

Send a DELETE request to [http://127.0.0.1:8000/api/v1/transactions/ID/](http://127.0.0.1:8000/api/v1/transactions/ID/)

It will return a **204** status code if the transaction was deleted

## Tests

You can read the test code at **[wallet/tests.py](https://github.com/gdi3d/my_wallet/blob/master/wallet/tests.py)**. Just take a look at the TestCase **TransactionTestCase**
