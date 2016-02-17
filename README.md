# My Wallet
My Wallet it's a personal project that follows the principle of **eat your own dog food**.

The purpose of the app is to keep track of your transactions for differents accounts, like bank accounts, wallets, socks or any weird place you want.
It uses [Django](https://www.djangoproject.com/) on the backend and [Django Rest Framework](http://www.django-rest-framework.org/) on top of it to provide a nice RESTful interface.

Includes a nice responsive html website to play with it.

## Installation
I would recommend to install it using [Virtual Environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/) (and [virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvwrapper) that provides autocomplete features).  

Install:
```
mkvirtualenv my_wallet
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

## Documentation
You can access to the documentation on [http://my-wallet.readthedocs.org/en/latest/](http://my-wallet.readthedocs.org/en/latest/)

or using mkdocs:
```
mkdocs serve
```
and then open [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

For more info about mkdocs read [mkdocs](http://www.mkdocs.org/)