# -------------------------------------------------------------
# Import Flask and required modules
# -------------------------------------------------------------
from flask import Flask, request, jsonify

# -------------------------------------------------------------
# Create Flask app
# -------------------------------------------------------------
app = Flask(__name__)
data=0
# -------------------------------------------------------------
# GET Request Example
# -------------------------------------------------------------
@app.get("/get-example")
def get_example():
    return jsonify({
        "status": "success",
        "method": "GET",
        "message": "This is a GET response"
    })

# -------------------------------------------------------------
# GET with Query Parameters
# -------------------------------------------------------------
@app.get("/user")
def get_user():
    user_id = request.args.get("id")
    user_name = request.args.get("name")

    return jsonify({
        "status": "success",
        "method": "GET with Query Params",
        "id": user_id,
        "name": user_name
    })

# -------------------------------------------------------------
# POST Request Example
# -------------------------------------------------------------
@app.post("/create")
def create_user():
    data = request.get_json() # Read JSON body
    return jsonify({
        "status": "success",
        "method": "POST",
        "received_data": data
    })

# -------------------------------------------------------------
# PUT Request Example
# -------------------------------------------------------------
@app.put("/update/<int:user_id>")
def update_user(user_id):
    update_data = request.get_json()
    return jsonify({
        "status": "success",
        "method": "PUT",
        "user_id": user_id,
        "updated_fields": update_data
    })

# -------------------------------------------------------------
# DELETE Request Example
# -------------------------------------------------------------
@app.delete("/delete/<int:user_id>")
def delete_user(user_id):
    return jsonify({
        "status": "success",
        "method": "DELETE",
        "deleted_user_id": user_id
    })

# -------------------------------------------------------------
# Start Server
# -------------------------------------------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)