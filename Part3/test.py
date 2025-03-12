#!/usr/bin/python3
"""This module tests the User API endpoints"""

import unittest
from app import create_app
import uuid

class TestUserEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
        
        ### User        
        unique_email = f"{uuid.uuid4()}@example.com"
        response = cls.client.post("/api/v1/users/", json={
            "first_name": "John",
            "last_name": "Doe",
            "email": unique_email
        })
        cls.user = response.json
        
        ### Owner        
        unique_email = f"{uuid.uuid4()}@example.com"
        response = cls.client.post("/api/v1/users/", json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": unique_email
        })
        cls.owner = response.json
        
        ### Amenity
        response = cls.client.post("/api/v1/amenities/", json={
            "name": "Wi-Fi"
        })
        cls.amenity = response.json
        
        ### Owner Place
        response = cls.client.post("/api/v1/places/", json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": cls.owner.get("id"),
            "amenities": [
                cls.amenity.get("id")
            ]
        })
        cls.place = response.json
        
        ### Place Review
        response = cls.client.post("/api/v1/reviews/", json={
            "text": "Super cool!",
            "rating": 5,
            "user_id": cls.user.get("id"),
            "place_id": cls.place.get("id")
        })
        cls.review = response.json
        
        ### Place Review for Delete
        response = cls.client.post("/api/v1/reviews/", json={
            "text": "Great studio",
            "rating": 5,
            "user_id": cls.user.get("id"),
            "place_id": cls.place.get("id")
        })
        cls.review_delete = response.json
        
    def setUp(self):
        pass

#testing user
#create user
#success example

    def test_user_create(self):
        print("• User create success")
        response = self.client.post("/api/v1/users/", json={
            "first_name": "Peter",
            "last_name": "Parker",
            "email": "peter@parker.com"
        })
        self.new_user = response.json
        self.assertEqual(response.status_code, 201)
        print("Status code:", response.status_code)
        print(f"Json Response: {self.new_user}\n")
        
#create user
#unsuccess examples

    def test_user_create_unsuccess(self):
        print("• User create: without required value")
        response = self.client.post("/api/v1/users/", json={
            "first_name": "",
            "last_name": "Parker",
            "email": "peter@email.com"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "First name is required"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

        print("• User create: first_name/last_name more than 50 chars")
        response = self.client.post("/api/v1/users/", json={
            "first_name": "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz",
            "last_name": "Parker",
            "email": "peter@email.com"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "First name is too long"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• User create: invalid type value")
        response = self.client.post("/api/v1/users/", json={
            "first_name": 35,
            "last_name": "Parker",
            "email": "peter@email.com"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "First name must be a string"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• User create: invalid email format")
        response = self.client.post("/api/v1/users/", json={
            "first_name": "Pater",
            "last_name": "Paker",
            "email": "peterparkercom"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Email is not valid"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

        print("• User create: already registered email")
        invalid_email = self.owner.get("email")
        response = self.client.post("/api/v1/users/", json={
            "first_name": "Peter",
            "last_name": "Parker",
            "email": invalid_email
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Email already registered"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

#get user
#success example

    def test_users_get(self):
        print("• Users get all")
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, 200)
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

        print("• User get by ID")
        user_id = self.user.get("id")
        response = self.client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

#get user
#unsuccess example

    def test_users_get_unsuccess(self):
        print("• User get by invalid ID")
        response = self.client.get("/api/v1/users/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

#update user
#success example

    def test_user_update(self):     
        print("• User update success")
        response = self.client.put(f"/api/v1/users/{self.user["id"]}", json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@email.com"
        })
        self.assertEqual(response.status_code, 201)
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

#update user
#unsuccess examples

    def test_user_update_unsuccess(self):
        print("• User update: without required value")
        response = self.client.put(f"/api/v1/users/{self.user["id"]}", json={
            "first_name": "",
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "First name is required"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• User update: first_name/last_name more than 50 chars")
        response = self.client.put(f"/api/v1/users/{self.user["id"]}", json={
            "first_name": "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz",
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "First name is too long"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• User update: invalid value type")
        response = self.client.put(f"/api/v1/users/{self.user["id"]}", json={
            "first_name": 35,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "First name must be a string"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• User update: with invalid email format")
        response = self.client.put(f"/api/v1/users/{self.user["id"]}", json={
            "email": "johndoeemailcom"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Email is not valid"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• User update: with email already registered")
        invalid_email = self.owner.get("email")
        response = self.client.put(f"/api/v1/users/{self.user["id"]}", json={
            "email": invalid_email
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Email already registered by another user"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
         
        print("• User update: with invalid user id")
        response = self.client.put("/api/v1/users/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", json={
            "email": "johndoe@email.com"
        })   
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'message': 'User not found'})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
#testing Amenities
#create amenity
#success example

    def test_amenities_create(self):
        print("• Amenity create success")
        response =  self.client.post("/api/v1/amenities/", json={
            "name": "Garage"
        })
        self.new_amenity = response.json
        self.assertEqual(response.status_code, 201)
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
#create amenity
#unsuccess example

    def test_amenities_create_unsuccess(self):
        print("• Amenity create: without name")
        response =  self.client.post("/api/v1/amenities/", json={
            "name": ""
        })
        self.new_amenity = response.json
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Name is required"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Amenity create: name is not a string")
        response =  self.client.post("/api/v1/amenities/", json={
            "name": 32
        })
        self.new_amenity = response.json
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Name is invalid"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Amenity create: name more the 50 chars")
        response =  self.client.post("/api/v1/amenities/", json={
            "name": "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
        })
        self.new_amenity = response.json
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Name is too long"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Amenity create: name already registered")
        response =  self.client.post("/api/v1/amenities/", json={
            "name": "Wi-Fi"
        })
        self.new_amenity = response.json
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Amenity already registered"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
#Get amenity
#success example

    def test_amenities_get(self):
        print("• Amenities get all")
        response =  self.client.get("/api/v1/amenities/")
        self.assertEqual(response.status_code, 200)
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Amenity get by id")
        response =  self.client.get(f"/api/v1/amenities/{self.amenity.get("id")}")
        self.assertEqual(response.status_code, 200)
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
#Get amenity
#unsuccess example

    def test_amenities_get_unsuccess(self):
        print("• Amenity get by invalid id")
        response =  self.client.get("/api/v1/amenities/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "Amenity not found"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

#Update amenity
#success example

    def test_amenities_update(self):
        print("• Amenity update successfully")
        response =  self.client.put(f"/api/v1/amenities/{self.amenity.get("id")}", json={
            "name": "Swimming Pool"
        })
        self.new_amenity = response.json
        self.assertEqual(response.status_code, 200)
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
#Update amenity
#unsuccess example

    def test_amenities_update_unsuccess(self):
        print("• Amenity update: name is required")
        response =  self.client.put(f"/api/v1/amenities/{self.amenity.get("id")}", json={
            "name": ""
        })
        self.new_amenity = response.json
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Name is required"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Amenity update: name has invalid type")
        response =  self.client.put(f"/api/v1/amenities/{self.amenity.get("id")}", json={
            "name": 35
        })
        self.new_amenity = response.json
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Name is invalid"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Amenity update: name is more tha 50 chars")
        response =  self.client.put(f"/api/v1/amenities/{self.amenity.get("id")}", json={
            "name": "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
        })
        self.new_amenity = response.json
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Name is too long"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Amenity update: not found")
        response =  self.client.put("/api/v1/amenities/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", json={
            "name": "Swimming Pool"
        })
        self.new_amenity = response.json
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "Amenity not found"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
    
#testing Places
#create place
#success example

    def test_places_create(self):
        print("• Place create success")
        response = self.client.post("/api/v1/places/", json={
            "title": "Cool Studio",
            "description": "Super place with great view",
            "price": 80,
            "latitude": 56.7749,
            "longitude": 88.4194,
            "owner_id": self.user.get("id"),
            "amenities": [
                self.amenity.get("id")
            ]
        })
        self.new_place = response.json
        self.assertEqual(response.status_code, 201)
        print("Status code:", response.status_code)
        print(f"Json Response: {self.new_place}\n")
        
#create place
#unsuccess example

    def test_places_create_unsuccess(self):
        print("• Place create: without required value")
        response = self.client.post("/api/v1/places/", json={
            "title": "",
            "description": "Big and nice house",
            "price": 280,
            "latitude": 36.7749,
            "longitude": 98.4194,
            "owner_id": self.user.get("id")
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Title is required"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

        print("• Place create: title more than 100 chars")
        response = self.client.post("/api/v1/places/", json={
            "title": "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz",
            "description": "Big and nice house",
            "price": 280,
            "latitude": 36.7749,
            "longitude": 98.4194,
            "owner_id": self.user.get("id")
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Title is too long"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Place create: with an invalid type value")
        response = self.client.post("/api/v1/places/", json={
            "title": 35,
            "description": "Big and nice house",
            "price": 280,
            "latitude": 36.7749,
            "longitude": 98.4194,
            "owner_id": self.user.get("id")
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Title value is not valid"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

        print("• Place create: with out of range value")
        response = self.client.post("/api/v1/places/", json={
            "title": "Cool Studio",
            "description": "Super place with great view",
            "price": -80,
            "latitude": 56.7749,
            "longitude": 88.4194,
            "owner_id": self.user.get("id")
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Price must be a positive number"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Place create: with a not existing amenity")
        response = self.client.post("/api/v1/places/", json={
            "title": "Cool Studio",
            "description": "Super place with great view",
            "price": 80,
            "latitude": 56.7749,
            "longitude": 88.4194,
            "owner_id": self.user.get("id"),
            "amenities": ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"]
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Invalid amenities: ['xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx']"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Place create: with a not existing user")
        response = self.client.post("/api/v1/places/", json={
            "title": "Cool Studio",
            "description": "Super place with great view",
            "price": 80,
            "latitude": 56.7749,
            "longitude": 88.4194,
            "owner_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Invalid user"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

#get place
#success example

    def test_places_get(self):
        print("• Places get all")
        response = self.client.get("/api/v1/places/")
        self.assertEqual(response.status_code, 200)
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
    
        print("• Place get by ID")
        response = self.client.get(f"/api/v1/places/{self.place.get("id")}")
        self.assertEqual(response.status_code, 200)
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

#get place
#unsuccess example

    def test_places_get_unsuccess(self):
        print("• Place get by invalid ID")
        response = self.client.get("/api/v1/places/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "Place not found"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")


#put place
#success example

    def test_places_update(self):     
        print("• Place update success")
        response = self.client.put(f"/api/v1/places/{self.place["id"]}", json={
            "price": 150,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Place updated successfully"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

#put place
#unsuccess examples

    def test_places_update_unsuccess(self):
        print("• Place update: without a required value")
        response = self.client.put(f"/api/v1/places/{self.place.get("id")}", json={
            "title": "",
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Title is required"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

        print("• Place update: title more than 100 chars")
        response = self.client.put(f"/api/v1/places/{self.place.get("id")}", json={
            "title": "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Title is too long"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Place update: with an invalid value type")
        response = self.client.put(f"/api/v1/places/{self.place.get("id")}", json={
            "title": 35,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Title value is not valid"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Place update: value out of range")
        response = self.client.put(f"/api/v1/places/{self.place.get("id")}", json={
            "price": -80,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Price must be a positive number"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Place update: not existing amenity")
        response = self.client.put(f"/api/v1/places/{self.place.get("id")}", json={
            "amenities": ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"]
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Invalid amenities: ['xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx']"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Place update: update owner")
        response = self.client.put(f"/api/v1/places/{self.place.get("id")}", json={
            "owner_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Owner can not be modified"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Place update by invalid ID")
        response = self.client.get("/api/v1/places/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", json={
            "price": 150
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "Place not found"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

        
#testing review
#create review
#success example
        
    def test_reviews_create(self):
        print("• Review create success")
        response = self.client.post("/api/v1/reviews/", json={
            "text": "Nice house for a weekend!",
            "rating": 5,
            "user_id": self.user.get("id"),
            "place_id": self.place.get("id")
        })
        self.assertEqual(response.status_code, 201)
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

#create review
#unsuccess

    def test_reviews_create_unsuccess(self):
        print("• Review create: without required value")
        response = self.client.post("/api/v1/reviews/", json={
            "text": "",
            "rating": 5,
            "user_id": self.user.get("id"),
            "place_id": self.place.get("id")
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Text is required"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Review create: with an invalid value type")
        response = self.client.post("/api/v1/reviews/", json={
            "text": 35,
            "rating": 5,
            "user_id": self.user.get("id"),
            "place_id": self.place.get("id")
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Text is not valid"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Review create: with rating out of range")
        response = self.client.post("/api/v1/reviews/", json={
            "text": "Nice house for a weekend!",
            "rating": 7,
            "user_id": self.user.get("id"),
            "place_id": self.place.get("id")
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Rating must be between 1 and 5"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Review create: with place ID invalid value")
        response = self.client.post("/api/v1/reviews/", json={
            "text": "Nice house for a weekend!",
            "rating": 5,
            "user_id": self.user.get("id"),
            "place_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Invalid place"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Review create: with user ID invalid value")
        response = self.client.post("/api/v1/reviews/", json={
            "text": "Nice house for a weekend!",
            "rating": 5,
            "user_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "place_id": self.place.get("id")
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Invalid user"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

#get review
#success example

    def test_reviews_get(self):
        print("• Reviews get all")
        response = self.client.get("/api/v1/reviews/")
        self.assertEqual(response.status_code, 200)
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
    
        print("• Review get by ID")
        response = self.client.get(f"/api/v1/reviews/{self.review.get("id")}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': self.review.get("id"), 'place_id': self.place.get("id"), 'rating': 5, 'text': 'Super cool!', 'user_id': self.user.get("id")})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Review by place ID")
        response = self.client.get(f"/api/v1/places/{self.place.get("id")}/reviews")
        self.assertEqual(response.status_code, 200)
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

#get review
#unsuccess examples

    def test_reviews_get_unsuccess(self):
        print("• Review get by invalid ID")
        response = self.client.get("/api/v1/reviews/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "Review not found"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Review by invalid place ID")
        response = self.client.get(f"/api/v1/places/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/reviews")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "Place not found"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

#Update review
#success example

    def test_reviews_update(self):      
        print("• Review update success")
        response = self.client.put(f"/api/v1/reviews/{self.review.get("id")}", json={
            "text": "Not so cool",
            "rating": 3
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Review updated successfully"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

#Update review
#unsuccess examples

    def test_reviews_update_unsuccess(self):
        print("• Review update: without required value")
        response = self.client.put(f"/api/v1/reviews/{self.review.get("id")}", json={
            "text": ""
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Text is required"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Review update: with an invalid value type")
        response = self.client.put(f"/api/v1/reviews/{self.review.get("id")}", json={
            "text": 35
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Text is not valid"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Review update: with rating out of range")
        response = self.client.put(f"/api/v1/reviews/{self.review.get("id")}", json={
            "rating": 7
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Rating must be between 1 and 5"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Review update: with place ID invalid value")
        response = self.client.put(f"/api/v1/reviews/{self.review.get("id")}", json={
            "place_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Forbidden input values"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Review update: with user ID invalid value")
        response = self.client.put(f"/api/v1/reviews/{self.review.get("id")}", json={
            "user_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Forbidden input values"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")
        
        print("• Review update by invalid ID")
        response = self.client.get("/api/v1/reviews/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", json={
            "rating": 3
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "Review not found"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

#delete review
#success example

    def test_reviews_delete(self):
        print("• Delete review")
        response = self.client.delete(f"/api/v1/reviews/{self.review_delete.get("id")}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Review deleted successfully"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

#unsuccess example

    def test_reviews_delete_unsuccess(self):
        print("• Delete review")
        response = self.client.delete("/api/v1/reviews/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "Review not found"})
        print("Status code:", response.status_code)
        print(f"Json Response: {response.json}\n")

if __name__ == '__main__':
    unittest.main()