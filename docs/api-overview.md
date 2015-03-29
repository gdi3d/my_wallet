# Overview

As mentioned before, the API is based on [Django Rest Framework](http://www.django-rest-framework.org/)

Django uses a csrfmiddlewaretoken cookie that needs to be send with ALL non read operations (POST, PUT, DEL)

You can also play and explore the API using your web browser, just remember to be logged in first.

For this you can go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and login using this credentials:

**username**: demo
**password**: demo

Or use the admin [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) with the same credentials

## EndPoints

* [Login](api-login.md)
* [Registration](api-registration.md)
* [Reset Password](api-reset-password.md)
* Transactions
* Transactions Total
* Wallets
* Wallets Total
* Category
