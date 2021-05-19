from flask import flash
from flask_bcrypt import Bcrypt
import re

from flask_app import app
from ..config.mysqlconnection import connectToMySQL
from ..model import user


class Recipe: 
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data["description"]
        self.instruction = data["instruction"]
        self.prep = data["prep"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        if 'user' in data:
            self.user = data['user']


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id =%(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        ## GIVES YOU ACCESS TO THE USER INFO VIA THE USER_ID THAT MADE THE RECIPE
        results_data = {
            'id': results[0]['id'],
            'name': results[0]['name'],
            'description': results[0]['description'],
            'instruction': results[0]['instruction'],
            'prep': results[0]['prep'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
            'user': user.User.get_by_id({"id": results[0]['user_id']})
        }

        return cls(results_data)

    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes(user_id, name, description, instruction, prep, created_at, updated_at) VALUES (%(user_id)s, %(name)s, %(description)s,%(instruction)s,%(prep)s, NOW(), NOW());"
        print(query)
        recipe_id = connectToMySQL("recipes_schema").query_db(query,data)
        print (recipe_id)

        return recipe_id

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s,prep = %(prep)s, updated_at = NOW() WHERE id = %(id)s;"
        print(query)
        recipe_id = connectToMySQL("recipes_schema").query_db(query,data)
        print (recipe_id)

        return recipe_id


    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        recipe_id = connectToMySQL("recipes_schema").query_db(query,data)
        print (recipe_id)

    @staticmethod
    def validator(post_data):
        is_valid = True

        if len(post_data['name']) < 2:
            flash("Recipe name must be at least 2 characters")
            is_valid = False

        if len(post_data['description']) < 2:
            flash("Description must be at least 2 characters")
            is_valid = False

        if len(post_data['instruction']) < 2:
            flash("Instructions must be at least 2 characters")
            is_valid = False


        return is_valid