from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    #returns the list of pictures stored in the data variable
    #jsonify is used to convert the data list into a JSON response
    return jsonify(data),200
######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture),200
    return jsonify({"message": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
"""
You will first need to extract the picture data from the request body and then append it to the data list.
If a picture with the id already exists, 
send an HTTP code of 302 back to 
the user with a message of {"Message": "picture with id {picture['id']} already present"}.
"""
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()
    pic_id = new_picture.get("id")
    for pic in data:
        if pic == new_picture:
            msg = f"picture with id {pic_id} already present"
            return jsonify({"Message": msg}),302

    data.append(new_picture)
    return jsonify(new_picture), 201
    
######################################################################
# UPDATE A PICTURE
######################################################################
"""
You will first need to extract the picture data from the request body.
You will then find the picture in the data list. 
If the picture exists, you will update it with the incoming request.
If the picture does not exist, 
you will send back a status of 404 with a message {"message": "picture not found"}.
"""
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture =request.get_json() #data
    for pic in data:
        if pic["id"] == id:
            pic.update(picture)
            return jsonify(pic), 200
    return jsonify({"message": "picture not found"}), 404

    
######################################################################
# DELETE A PICTURE
######################################################################
"""
You will first extract the id from the URL.
Next, traverse the data list to find the picture by id. 
If the picture exists, you will delete the item from the list 
and return an empty body with a status of HTTP_204_NO_CONTENT.
If the picture does not exist, 
you will send back a status of 404 with a message {"message": "picture not found"}.
"""
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for pic in data:
        if pic["id"] == id:
            data.remove(pic)
            return '',204
    return jsonify({"message": "picture not found"}), 404

