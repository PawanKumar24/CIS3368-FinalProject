from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# Establish a connection to the database
mydb = pymysql.connect(
  host = "localhost",
  user = "root",
  password = "",
  database = "Interstellar Cargo Transportation"
)

# mydb = pymysql.connect(
#   host = "cargodb.cluster-ro-cnw5dtvigwfx.eu-north-1.rds.amazonaws.com",
#   user = "admin",
#   password = "Htown.2022",
#   database = "CargoDB"
# )

#get all cargo items... 
@app.route('/cargo', methods=['GET'])
def get_cargo():
    try:
        # Open a cursor to execute SQL queries
        with mydb.cursor() as cursor:
            # Execute a SELECT SQL query
            sql = "SELECT * FROM cargo"
            cursor.execute(sql)

            # Fetch all the rows returned by the query
            rows = cursor.fetchall()
            
        return jsonify(rows)
    
    except Exception as e:
        # Return an error message if there's any exception
        print("Error occurred: ", e)
        return jsonify({'error ': str(e)})
    
    finally:
        mydb.close()

#create cargo items
@app.route('/cargo/add', methods=['POST'])
def add_cargo():
    try:
        # Parse request data
        data = request.get_json()
        weight = data['weight']
        cargotype = data['cargotype']
        departure = data['departure']
        arrival = data['arrival']
        shipid = data['shipid']

        # Insert new cargo entry into 'cargo' table
        cursor = mydb.cursor()
        sql = "INSERT INTO cargo (weight, cargotype, departure, arrival, shipid) VALUES (%s, %s, %s, %s, %s)"
        val = (weight, cargotype, departure, arrival, shipid)
        cursor.execute(sql, val)
        mydb.commit()

        # Return success message
        return jsonify({'message': 'Cargo added successfully!'})

    except pymysql.Error as error:
        # Handle database errors
        return jsonify({'error': str(error)})

    except KeyError as error:
        # Handle missing or incorrect data fields in request
        return jsonify({'error': f"Missing or incorrect data field: {str(error)}"})

    except Exception as error:
        # Handle all other errors
        return jsonify({'error': str(error)})

    finally:
        # Close database connection
        if 'conn' in locals() and mydb.is_connected():
            cursor.close()
            mydb.close()
            print("Database connection closed.")

#update cargo items
@app.route('/cargo/update/<int:id>', methods=['PUT'])
def update_cargo(id):
    # Get the request payload
    payload = request.json
    cursor = mydb.cursor()

    # Build the UPDATE query
    update_query = "UPDATE cargo SET "
    
    if 'weight' in payload:
        update_query += "weight = %s, "
    if 'cargotype' in payload:
        update_query += "cargotype = %s, "
    if 'departure' in payload:
        update_query += "departure = %s, "
    if 'arrival' in payload:
        update_query += "arrival = %s, "
    if 'shipid' in payload:
        update_query += "shipid = %s, "
        
    # Remove the last comma and space
    update_query = update_query[:-2]
    
    # Add the WHERE clause
    update_query += " WHERE id = %s"
    
    # Get the values from the payload
    values = list(payload.values())
    
    # Add the id to the end of the values list
    values.append(id)
    
    # Execute the query
    try:
        cursor.execute(update_query, values)
        mydb.commit()
        return {"message": "Cargo record updated successfully"}
    except Exception as e:
        print(e)
        mydb.rollback()
        return {"error": "Cargo record update failed"}
    finally:
        # Close the cursor and database connection
        cursor.close()
        mydb.close()

# Delete cargo by id
@app.route('/cargo/delete/<int:id>', methods=['DELETE'])
def delete_cargo(id):
    try:
        # Create a cursor object
        cur = mydb.cursor()

        # Execute the SQL query
        cur.execute("DELETE FROM cargo WHERE id=%s", (id,))

        # Commit the changes to the database
        mydb.commit()

        # Close the cursor and connection
        cur.close()

        # Return success message
        return jsonify({'message': 'Cargo with id {} deleted successfully.'.format(id)}), 200

    except Exception as e:
        # Roll back the transaction if there is an error
        mydb.rollback()

        # Close the cursor and connection
        cur.close()

        # Return error message
        return jsonify({'message': str(e)}), 500

#----------------------------------

@app.route('/captain', methods=['GET'])
def get_captain():
    try:
        # Open a cursor to execute SQL queries
        with mydb.cursor() as cursor:
            # Execute a SELECT SQL query
            sql = "SELECT * FROM captain"
            cursor.execute(sql)

            # Fetch all the rows returned by the query
            rows = cursor.fetchall()
            
        return jsonify(rows)
    
    except Exception as e:
        # Return an error message if there's any exception
        print("Error occurred: ", e)
        return jsonify({'error ': str(e)})

# API to insert data into the 'captain' table
@app.route('/captain/add', methods=['POST'])
def add_captain():
    cursor = mydb.cursor()
    try:
        # Extracting data from the request body
        data = request.get_json()
        firstname = data['firstname']
        lastname = data['lastname']
        rank = data['rank']
        homeplanet = data['homeplanet']
        
        # Inserting the data into the 'captain' table
        query = "INSERT INTO captain (firstname, lastname, rank, homeplanet) VALUES (%s, %s, %s, %s)"
        values = (firstname, lastname, rank, homeplanet)
        cursor.execute(query, values)
        mydb.commit()

        return jsonify({"message": "Captain added successfully!"}), 200

    except Exception as e:
        print("Error occurred: ", e)
        return jsonify({"message": "Unable to add captain."}), 500

@app.route('/captain/update/<int:id>', methods=['PUT'])
def update_captain(id):
    try:
        # Get the request body
        request_data = request.json
        
        # Get the connection cursor
        cursor = mydb.cursor()

        # Update the captain details
        update_query = "UPDATE captain SET "
        for key in request_data:
            update_query += f"{key} = '{request_data[key]}', "
        update_query = update_query[:-2]
        update_query += f" WHERE id = {id}"
        cursor.execute(update_query)
        mydb.commit()

        # Close the cursor
        cursor.close()

        # Return success message
        return {"message": "Captain details updated successfully."}

    except Exception as e:
        # Rollback the transaction if any error occurs
        mydb.rollback()
        return {"error": f"An error occurred while updating the captain details: {str(e)}"}

# Delete captain by id
@app.route('/captain/delete/<int:id>', methods=['DELETE'])
def delete_captain(id):
    try:
        # Create a cursor object
        cur = mydb.cursor()

        # Execute the SQL query
        cur.execute("DELETE FROM captain WHERE id=%s", (id,))

        # Commit the changes to the database
        mydb.commit()

        # Close the cursor and connection
        cur.close()

        # Return success message
        return jsonify({'message': 'Captain with id {} deleted successfully.'.format(id)}), 200

    except Exception as e:
        # Roll back the transaction if there is an error
        mydb.rollback()

        # Close the cursor and connection
        cur.close()

        # Return error message
        return jsonify({'message': str(e)}), 500

#------------------------------------------------------

@app.route('/spaceship', methods=['GET'])
def get_spaceShip():
    try:
        # Open a cursor to execute SQL queries
        with mydb.cursor() as cursor:
            # Execute a SELECT SQL query
            sql = "SELECT * FROM spaceship"
            cursor.execute(sql)

            # Fetch all the rows returned by the query
            rows = cursor.fetchall()
            
        return jsonify(rows)
    
    except Exception as e:
        # Return an error message if there's any exception
        print("Error occurred: ", e)
        return jsonify({'error ': str(e)})

@app.route('/spaceship/add', methods=['POST'])
def create_spaceship():
    cursor = mydb.cursor()
    maxweight = request.json['maxweight']
    captainid = request.json['captainid']
    sql = "INSERT INTO spaceship (maxweight, captainid) VALUES (%s, %s)"
    val = (maxweight, captainid)
    try:
        cursor.execute(sql, val)
        mydb.commit()
        return jsonify({"message": "Spaceship created successfully."}), 201
    except pymysql.Error as err:
        mydb.rollback()
        return jsonify({"message": "Error creating spaceship: " + str(err)}), 400

@app.route('/spaceship/update/<int:id>', methods=['PUT'])
def update_spaceship(id):
    try:
        # Get the request body
        request_data = request.json

        # Get the connection cursor
        cursor = mydb.cursor()

        # Update the spaceship details
        update_query = "UPDATE spaceship SET "
        for key in request_data:
            update_query += f"{key} = '{request_data[key]}', "
        update_query = update_query[:-2]
        update_query += f" WHERE id = {id}"
        cursor.execute(update_query)
        mydb.commit()

        # Close the cursor
        cursor.close()

        # Return success message
        return {"message": "Spaceship details updated successfully."}

    except Exception as e:
        # Rollback the transaction if any error occurs
        mydb.rollback()
        return {"error": f"An error occurred while updating the spaceship details: {str(e)}"}

# Delete spaceship by id
@app.route('/spaceship/delete/<int:id>', methods=['DELETE'])
def delete_spaceship(id):
    try:
        # Create a cursor object
        cur = mydb.cursor()

        # Execute the SQL query
        cur.execute("DELETE FROM spaceship WHERE id=%s", (id,))

        # Commit the changes to the database
        mydb.commit()

        # Close the cursor and connection
        cur.close()

        # Return success message
        return jsonify({'message': 'Spaceship with id {} deleted successfully.'.format(id)}), 200

    except Exception as e:
        # Roll back the transaction if there is an error
        mydb.rollback()

        # Close the cursor and connection
        cur.close()

        # Return error message
        return jsonify({'message': str(e)}), 500


if __name__ == '__main__':
  app.run()
