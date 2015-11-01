# Reset Password

This endpoint is used to reset the user's account password

[http://127.0.0.1:8000/api/v1/auth/password/reset/](http://127.0.0.1:8000/api/v1/auth/password/reset/)

## Methods

* [POST](#post)

### POST

Send a POST request to [http://127.0.0.1:8000/api/v1/auth/password/reset/](http://127.0.0.1:8000/api/v1/auth/password/reset/) with this JSON data structure:

```
{
	"email": "somemail@host.com",
	"csrf": CSRF_HASH
}
```

It will return a **200** status code if the email is valid and even if there's no user with that email address:

```
{
    "success": "Password reset e-mail has been sent."
}
```

For more information about this behavior check out django docs:
https://docs.djangoproject.com/en/1.7/topics/auth/default/#django.contrib.auth.views.password_reset