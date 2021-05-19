from flask import flash
from flask_bcrypt import Bcrypt
import re
from ..model import recipe

from flask_app import app
from ..config.mysqlconnection import connectToMySQL

bcrypt = Bcrypt(app)

class User: 
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.recipes = []


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL("recipes_schema").query_db(query,data)

        user = cls(results[0])
        if results[0]['recipes.id'] != None:
            for row in results:
                row_data = {
                    'id': row['recipes.id'],
                    'name': row['name'],
                    'description': row['description'],
                    'instruction': row['instruction'],
                    'prep': row['prep'],
                    'created_at': row['recipes.created_at'],
                    'updated_at': row ['recipes.updated_at'],
                }
                user.recipes.append(recipe.Recipe(row_data))

        
        return user


    @classmethod
    def create(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"

        user_id = connectToMySQL("recipes_schema").query_db(query,data)

        return user_id

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("recipes_schema").query_db(query,data)

        return cls(results[0]) if len(results) > 0 else None


    @staticmethod
    def register_validator(post_data):
        is_valid = True
        
        if len(post_data['first_name']) < 2:
            flash('first name must be more than 2 characters')
            is_valid = False
        
        if len(post_data['last_name']) < 2:
            flash('last name must be more than 2 characters')
            is_valid = False
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']): 
                flash("Invalid email address!")
                is_valid = False
        else:
            user= User.get_by_email({"email": post_data['email']})
            if user:
                flash("email is already in use")
                is_valid = False
        
        if len(post_data['password']) < 4:
            flash('password must be more than 4 characters')
            is_valid = False
        
        if post_data['password'] != post_data['confirm_password']:
            flash('passwords must match')
            is_valid = False
            

        return is_valid


    @staticmethod
    def login_validator(post_data):
        user = User.get_by_email({"email": post_data['email']})

        if not user:
            flash ("invalid credentials")
            return False
        
        if not bcrypt.check_password_hash(user.password, post_data['password']): 
            flash("invalid credentials")
            return False

        return True