# API
As mentioned before, the API is based on [Django Rest Framework](http://www.django-rest-framework.org/)

Django uses a csrfmiddlewaretoken cookie that needs to be send with ALL non read operations (POST, PUT, DEL)

This makes using curl very uncomfortable to use, so we are going to use [Django Test Client](https://docs.djangoproject.com/en/1.7/topics/testing/tools/) for testing the api

## Login
My Wallet uses [Django Rest Auth](https://github.com/Tivix/django-rest-auth) to manage authentication and registration process.

You can read the documentation on [http://django-rest-auth.readthedocs.org/en/latest/](http://django-rest-auth.readthedocs.org/en/latest/)

___Note: The base path has been changed from /rest-auth/ to /auth/___

Let's login and save the cookie so we can keep playing around with the api afterwards.

Open a console and paste this:

**Remember to activate your env if you installed my_wallet using Virtual Environments as mentioned on the [Installation Steps](getting-started#installation)**

```
./shell_local_server.sh
```

This will open a python console. Paste this to test the login endpoint:

```
from django.test import Client
c = Client()
r = c.post('/api/v1/auth/login/', {'username':'demo','password':'demo'})
```

Now let's check what happend:

```
r.status_code
```
will return `200` if login was ok


```
r.context
```
will return something like: `{"key":"67c11eec636c7d900c3cb7693ae0b6cf65629109"}`

And that's it, we are logged in!

---

## Registration
It's not implemented yet... yeap, it's sucks I know.

Use the admin area [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to manage this for now

----

## Reset password
It's not implemented yet... yeap, it's sucks I know.

Use the admin area [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to manage this for now

---

## Items

It's the representation of the Items model on **wallet/models.py**

You can call it using this methods: **GET, POST, HEAD, OPTIONS**


### GET
Returns all the items on the transactions for the current user in all the wallets.

Let's try it:

Open a python console

```
./shell_local_server.sh
```

Once it's open:
```
from django.test import Client
c = Client()
r = c.get('/api/v1/items/')
```

Try `r.status_code`, it should return `200` if everything it's ok.

To access the data returned by the api type `r.content`, it should return something like

```
'{"count":2,"next":null,"previous":null,"results":[{"id":134,"category":{"id":41,"name":"Freelance Work"},"amount":"120.0000","note":"Bugfix"},{"id":135,"category":{"id":2,"name":"Food"},"amount":"-50.0000","note":"Dinner"}]}'
```

Ok. This is great but we can get a nicer representation by just using our browser.

Open [http://127.0.0.1:8000/api/v1/items/](http://127.0.0.1:8000/api/v1/items/)

___Remember you need to be logged in. If you're not just, go to [website](http://127.0.0.1:8000/) or [admin area](http://127.0.0.1:8000/admin/) and login with user/pass: demo/demo and then return to the api url. Otherwise you'll get a nasty 500 error___

Api Html Response example:

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

And now we also have a nice form to create or edit items. 

You can edit the items by adding the **item id** at the end of the url like this [http://127.0.0.1:8000/api/v1/items/135/](http://127.0.0.1:8000/api/v1/items/135/)

### POST

To add a new item just send a POST to the url **/api/v1/items/* with following json structure:

```
{
    "category_id": INTEGER, 
    "amount": DECIMAL, 
    "note": STRING
}
```

We can take advantage of the OPTIONS method and examine the endpoint more deeply without having to read the code

Open your browser on [http://127.0.0.1:8000/api/v1/items/](http://127.0.0.1:8000/api/v1/items/) (remember to be logged in) and click the **OPTIONS** button. You should see this:

```
HTTP 200 OK
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS

{
    "name": "Item List", 
    "description": "Viewing and editing items.\n\nNo filters options.", 
    "renders": [
        "application/json", 
        "text/html"
    ], 
    "parses": [
        "application/json", 
        "application/x-www-form-urlencoded", 
        "multipart/form-data"
    ], 
    "actions": {
        "POST": {
            "id": {
                "type": "integer", 
                "required": false, 
                "read_only": true, 
                "label": "ID"
            }, 
            "category": {
                "type": "field", 
                "required": false, 
                "read_only": true, 
                "label": "Category"
            }, 
            "category_id": {
                "type": "integer", 
                "required": false, 
                "read_only": false, 
                "label": "Category id"
            }, 
            "amount": {
                "type": "decimal", 
                "required": true, 
                "read_only": false, 
                "label": "Amount"
            }, 
            "note": {
                "type": "string", 
                "required": false, 
                "read_only": false, 
                "label": "Note"
            }
        }
    }
}
```

Here you can see that the field **category_id** is an **integer** type and is **not required**.

You can also notice that we have two fields related to categories: **category** and **category_id** and that the main difference between them is that we use **category** on **GET** request, that give us the category object, and **category_id** when creating a new item object.

Let's try to add a new item using the api. We can try it on our browser, using the form that Django Rest Framework gives us, or using a python shell like this:

Open a python console

___IMPORTANT: You need to be logged in. If you're not, read the [Login](#login) steps and then come back___

```
./shell_local_server.sh
```

Once it's open:
```
from django.test import Client
c = Client()
data = {'category_id':2, 'amount': 9.5432, 'note':"Hey! i'm testing this api"}
r = c.post('/api/v1/items/')
```

Try `r.status_code`, it should return `201` if the item was created.

To access the data returned by the api type `r.content`, it should return something like

```
'{"id":137,"category":{"id":2,"name":"Food"},"amount":"9.5432","note":"Hey! i\'m testing this api"}'
```
----

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