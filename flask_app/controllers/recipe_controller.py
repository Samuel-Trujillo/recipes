from flask import render_template, request, redirect, session
from flask_bcrypt import Bcrypt   
from flask_app import app
from ..model.recipe import Recipe
from ..model.user import User

bcrypt = Bcrypt(app)


@app.route("/dashboard")
def dashboard():
    if "uuid" not in session:
        return redirect("/")

    ###ALLOWS YOU TO ACCESS USER DATA THROUGHOUT THE ROUTES INPUT
    logged_user = User.get_by_id({"id": session['uuid']})

    return render_template("dashboard.html", user = logged_user)


@app.route('/create')
def new_recipe_form():
    if "uuid" not in session:
        return redirect("/")

    logged_user = User.get_by_id({"id": session['uuid']})

    return render_template('create.html', user = logged_user)

@app.route('/create_math', methods = ['POST'])
def create_new_recipe():
    if not Recipe.validator(request.form):
        return redirect('/create')

    print(request.form)
    data = {
        "user_id": session['uuid'],
        "name": request.form['name'],
        "description": request.form['description'],
        "instruction": request.form['instruction'],
        "prep": request.form['prep']
    }
    Recipe.create_recipe(data)

    return redirect('/dashboard')


@app.route('/update/<int:id>')
def update_recipe_form(id):
    if "uuid" not in session:
        return redirect("/")
    
    edit_recipe = Recipe.get_one({"id": id})
    logged_user = User.get_by_id({"id": session['uuid']})

    return render_template("update.html", recipe = edit_recipe, user = logged_user)


@app.route('/update_math/<int:id>', methods = ['POST'])
def update_recipe(id):
    if not Recipe.validator(request.form):
        return redirect('/create')

    print(request.form)
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instruction": request.form['instruction'],
        "prep": request.form['prep'],
        "id": id
    }
    Recipe.update(data)

    return redirect('/dashboard')


@app.route('/view_recipe/<int:id>')
def show_recipe(id):
    if "uuid" not in session:
        return redirect("/")
    
    viewing_recipe = Recipe.get_one({"id": id})

    return render_template("view.html", recipe = viewing_recipe)



@app.route('/delete/<int:id>')
def delete_recipe(id):
    Recipe.delete({"id": id})


    return redirect("/dashboard")