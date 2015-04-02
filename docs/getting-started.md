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

### API
The api app it's very simple and has only one file **urls.py**.

The only function of this app is to expose API urls of others applications. This way I can handle all my API url routing in one place
and if I ever need to change it to some other path, like **api/v2/**, I just change it over there.

### Wallet
All the models, views and serializers of the project.

### Website
A web interface to use the application based mostly on javascript.

You can take a look at **website/static/js/wallet.js** for more info. 

Each view is represented by a singleton class that handles all the CRUD operations by talking to the API and UI actions.

Components used:

* [Bootstrap](http://getbootstrap.com/)
* [jQuery](https://jquery.com/)
* [jQuery Numeric](http://www.texotela.co.uk/code/jquery/numeric/)
* [jQuery Cookie](https://github.com/carhartl/jquery-cookie)
* [accounting](http://openexchangerates.github.io/accounting.js)
* [jQuery Simple Pagination](http://flaviusmatis.github.com/simplePagination.js/)
* [Knockout](http://knockoutjs.com/index.html)
* [Knockout Mapping Plugin](http://knockoutjs.com/documentation/plugins-mapping.html)