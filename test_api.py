# test_api.py
import unittest
import os
import json
from app import create_app, db

class ShoppingListTestCase(unittest.TestCase):
    """This class represents the shoppinglist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.shoppinglist1 = {'title':'Food', 'store':'Maruetsu'}
        self.shoppinglist2 = {'title':'Toiletry', 'store':'Gyomu'}
        self.shoppinglist3 = {'title':'Cleaning stuff', 'store':'Don Quijote'}
        self.shoppinglist4 = {'title':'Other stuff', 'store':'Gyomu'}
        self.item1 = {'name':'Apples', 'quantity':3}
        self.item2 = {'name':'Water', 'quantity':2}
        self.item3 = {'name':'Detergent', 'quantity':4}
        self.item4 = {'name':'Shampoo', 'quantity':1}
        self.item5 = {'name':'Brushes', 'quantity':10}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_shoppinglist_creation(self):
        """Test API can create a shoppinglist (POST request)"""
        res = self.client().post('/shoppinglists/', data=self.shoppinglist1)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Food', str(res.data))

    def test_api_can_get_all_shoppinglists(self):
        """Test API can get a shoppinglist (GET request)."""
        res = self.client().post('/shoppinglists/', data=self.shoppinglist1)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/shoppinglists/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Food', str(res.data))

    def test_api_can_get_shoppinglist_by_id(self):
        """Test API can get a single shoppinglist by using it's id."""
        res = self.client().post('/shoppinglists/', data=self.shoppinglist1)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().get('/shoppinglists/{}'.format(result_in_json['id']))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Food', str(res.data))

    def test_api_can_get_shoppinglist_by_title(self):
        """Test API can get a single shoppinglist by using it's title."""
        res = self.client().post('/shoppinglists/', data=self.shoppinglist2)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/shoppinglists/', data=self.shoppinglist3)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/shoppinglists/', data=self.shoppinglist4)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/shoppinglists/search/stuff')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json.loads(res.data.decode('utf-8'))), 2)
        self.assertIn('stuff', str(res.data))
        res = self.client().get('/shoppinglists/search/other')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json.loads(res.data.decode('utf-8'))), 1)
        self.assertIn('other', str(res.data).lower())
        res = self.client().get('/shoppinglists/search/notintitle')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json.loads(res.data.decode('utf-8'))), 0)

    def test_shoppinglist_can_be_edited(self):
        """Test API can edit an existing shoppinglist. (PUT request)"""
        res = self.client().post('/shoppinglists/', data=self.shoppinglist2)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().put('/shoppinglists/{}'.format(result_in_json['id']), data=self.shoppinglist3)
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/shoppinglists/{}'.format(result_in_json['id']))
        self.assertIn('Cleaning', str(results.data))

    def test_shoppinglist_deletion(self):
        """Test API can delete an existing shoppinglist. (DELETE request)."""
        res = self.client().post('/shoppinglists/',data=self.shoppinglist2)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().delete('/shoppinglists/{}'.format(result_in_json['id']))
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        res = self.client().get('/shoppinglists/1')
        self.assertEqual(res.status_code, 404)
    
    def test_api_can_add_items(self):
        """Test API can add items to an existing shoppinglist."""
        res = self.client().post('/shoppinglists/', data=self.shoppinglist1)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().post(
            '/shoppinglists/{}/items/'.format(result_in_json['id']), data=self.item1)
        self.assertEqual(res.status_code, 201)
        res = self.client().post(
            '/shoppinglists/{}/items/'.format(result_in_json['id']), data=self.item2)
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
            '/shoppinglists/{}/items/'.format(result_in_json['id']))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json.loads(res.data.decode('utf-8'))), 2)
        self.assertIn('water', str(res.data).lower())

    def test_api_can_add_item_quantities(self):
        """Test API can add the item quantities when items to an existing shoppinglist."""
        res = self.client().post('/shoppinglists/', data=self.shoppinglist1)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().post(
            '/shoppinglists/{}/items/'.format(result_in_json['id']), data=self.item1)
        self.assertEqual(res.status_code, 201)
        res = self.client().post(
            '/shoppinglists/{}/items/'.format(result_in_json['id']), data=self.item1)
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
            '/shoppinglists/{}/items/'.format(result_in_json['id']))
        self.assertEqual(res.status_code, 200)
        jsondata = json.loads(res.data.decode('utf-8'))
        self.assertEqual(len(jsondata), 1)
        total = jsondata[0].get('quantity')
        self.assertEqual(total, self.item1['quantity'] * 2)
        self.assertIn('apples', str(res.data).lower())

    def test_shoppinglistitem_deletion(self):
        """Test API can delete an existing shoppinglist's item. (DELETE request)."""
        res = self.client().post('/shoppinglists/', data=self.shoppinglist2)
        self.assertEqual(res.status_code, 201)
        listid = json.loads(res.data.decode('utf-8').replace("'", "\""))['id']
        res = self.client().post(
            '/shoppinglists/{}/items/'.format(listid), data=self.item1)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().delete('/shoppinglists/{}/items/{}'.format(listid, result_in_json['id']))
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        res = self.client().get('/shoppinglists/{}/items/{}'.format(listid, result_in_json['id']))
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
