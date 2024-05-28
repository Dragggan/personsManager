from flask import request, jsonify
from config import app, db
from models import Contact


@app.route("/persons", methods=["GET"])
def get_context():
    persons = Contact.query.all()
    persons_objects = map(lambda x: x.to_json(), persons)
    json_persons = list(persons_objects)
    return jsonify({"persons": json_persons})


@app.route("/add_person",methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    
    if not first_name or not last_name or not email:
        return ( jsonify({"please include first name, last and email"}) ,400)

    new_person = Contact(first_name=first_name,last_name=last_name,email=email)
    try:
        db.session.add(new_person)
        db.session.commit()
        print(' new_person==>',new_person);
    except Exception as e:
        return (jsonify({"messageeeee": str(e) }), 400)
    
    return (jsonify({"message":f"User {first_name}, {last_name} created"}),201)



@app.route("/update_contact<int:user_id>",methods=["PATCH"])
def update_persons(user_id):
    contact = Contact.query.get(user_id)
    
    if not contact:
        return jsonify({"mesage":"user not found"}),404

    data = request.json
    contact.first_name = data.get("firstName",contact.first_name)    
    contact.last_name = data.get("lastName",contact.last_name)    
    contact.email = data.get("email",contact.email)    
    
    db.session.commit()
    return jsonify({"message":"user updated!"}),201
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
