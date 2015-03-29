# Login

My Wallet uses [Django Rest Auth](https://github.com/Tivix/django-rest-auth) to manage authentication and registration process.

You can read the documentation on [http://django-rest-auth.readthedocs.org/en/latest/](http://django-rest-auth.readthedocs.org/en/latest/)

___Note: The base path has been changed from /rest-auth/ to /auth/___

[http://127.0.0.1:8000/api/v1/auth/login](http://127.0.0.1:8000/api/v1/auth/login)

To login send a POST with this JSON:

```
{
	'username': 'demo'
	'password': 'demo'
}
```

will return something like: 

`{"key":"67c11eec636c7d900c3cb7693ae0b6cf65629109"}`

And that's it, we have a valid session to work!