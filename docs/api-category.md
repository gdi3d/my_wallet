# Overview

This endpoint it's the representation of the **Category** model found in **[wallet/models.py](https://github.com/gdi3d/my_wallet/blob/master/wallet/models.py)**

[http://127.0.0.1:8000/api/v1/category/](http://127.0.0.1:8000/api/v1/category/)

## Methods

* [GET](#get)
* [POST](#post)
* [PUT](#put)
* [DELETE](#delete)

You can try out all this methods using your browsing. Just open the url from above. Just remember to be logged in first.

### GET

Send GET request to [http://127.0.0.1:8000/api/v1/category/](http://127.0.0.1:8000/api/v1/category/)

It would return a JSON like this:

```
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
        }, 
        ...
    ]
}
```

### POST

Send a POST request to [http://127.0.0.1:8000/api/v1/category/](http://127.0.0.1:8000/api/v1/category/) with this JSON data structure:

```
{
    "name": "My new Category"
}
```

It will return a **201** status code if the category was created. And the created object like this:

```
{
	"id": 9,
    "name": "My new Category"
}
```

### PUT

Send a PUT request to [http://127.0.0.1:8000/api/v1/category/ID/](http://127.0.0.1:8000/api/v1/category/ID/) with this JSON data structure:

```
{
	"id": 9,
    "name": "My new Category updated!"
}
```

It will return a **200** status code if the category was updated. And the updated object:

```
{
	"id": 9,
    "name": "My new Category updated!"
}
```

### DELETE

Send a DELETE request to [http://127.0.0.1:8000/api/v1/category/ID/](http://127.0.0.1:8000/api/v1/category/ID/)

It will return a **204** status code if the category was deleted

## Tests

You can read the test code at **[wallet/tests.py](https://github.com/gdi3d/my_wallet/blob/master/wallet/tests.py)**. Just take a look at the TestCase **CategoryTestCase**
