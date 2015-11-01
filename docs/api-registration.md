# Registration

This endpoint is used for creating new users

[http://127.0.0.1:8000/api/v1/rest-auth/registration/](http://127.0.0.1:8000/api/v1/rest-auth/registration/)

## Methods

* [POST](#post)

### POST

Send a POST request to [http://127.0.0.1:8000/api/v1/rest-auth/registration/](http://127.0.0.1:8000/api/v1/rest-auth/registration/) with this JSON data structure:

```
{
    "username": "john",
	"password1": "mysuperpassword",
	"password2": "mysuperpassword",
	"email": "somemail@host.com",
	"csrfmiddlewaretoken": CSRF_HASH
}
```

It will return a **201** status code if the user was created. And the created object like this:

```
{
    "username": "john", 
    "email": "somemail@host.com", 
    "first_name": "", 
    "last_name": ""
}
```

***You don't need the **csrfmiddlewaretoken** field if you try to create an account using the form shown on the endpoint page***