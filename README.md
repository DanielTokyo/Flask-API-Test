# Flask-API-Test
Just a basic Flask API test

This project is just meant as a practical (personal) way to get up and running with Python and Flask. I just took the guide found here (https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way) and adapted it to my own needs.

The API exposes functionality to add shopping lists and shopping list items.

I should probably have used Swagger to generate documentation, but for now it's necessary to use curl or a similar application to use the API. 

How to run
----------

1. Git clone this repository
2. Modify the .env file to point to your local DB server and set up a DB name (or set them manually if you're getting "\r" problems).
3. Create the empty DB
4. Create a virtual environment
5. Use pip to install the requirements (pip3 install -r requirements.txt)
6. Upgrade the DB to create the model's tables (python3 manage.py db upgrade)
7. You may now run the tests (python3 test_api.py)
8. You may also just run the app (flask run)

How to use
----------

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
