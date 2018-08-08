# Flask-API-Test
Just a basic Flask API test

This project is just meant as a practical (personal) way to get up and running with Python and Flask.

The API exposes functionality to add shopping lists and shopping list items.

I should probably have used Swagger to generate documentation, but for now it's necessary to use curl or a similar application to use the API. 

Some Examples
-------------

Add a new shopping list:
curl --header "Content-Type: application/json" --request POST --data '{"title":"New Shopping List","store":"BIC Camera"}' http://127.0.0.1:5000/shoppinglists/

Get existing shopping lists:
curl http://127.0.0.1:5000/shoppinglists/

Search a shopping list by title ("new"):
curl http://127.0.0.1:5000/shoppinglists/search/new

Add items:
curl --header "Content-Type: application/json" --request POST --data '{"name":"chocolates","quantity":3}' http://127.0.0.1:5000/shoppinglists/1/items/

See items in a shopping list:
curl http://127.0.0.1:5000/shoppinglists/1/items/