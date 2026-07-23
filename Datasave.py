"""
Handles read and write operations for datasave, and acts as the middle man between Python and the MySQL database
"""

import mysql.connector
import uuid
import json

database = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="W@ff13$(:!",
  database="IA_Datasave"
)
cursor = database.cursor()

def get_user_id(): # Uses MAC address as user id
    return uuid.getnode()

def get_user_data():
    user_id = get_user_id()
    # Fetch user info using SELECT statement
    cursor.execute(f"SELECT * FROM USERINFO WHERE user_id = {user_id}")
    results = cursor.fetchall()
    # Return default results if empty
    if not results:
        return {
            "user_id" : user_id,
            "highscore" : 0,
            "wave_no" : 0,
            "money" : 500,
            "grid" : None,
            "health" : 100
        }
    # Reformat results into a dictionary
    return {
        "user_id" : user_id,
        "highscore" : results[0][1],
        "wave_no" : results[0][2],
        "money" : results[0][3],
        "grid" : json.loads(results[0][4]),
        "health" : results[0][5]
    }

def save_user_data(highscore, wave_no, money, grid, health):
    print("saving")
    print(grid)
    if grid:
        print("convert")
        # Convert grid into a saveable format
        save_grid = []
        for r in grid:
            row = []
            for x in r:
                if x == None: row.append(0)
                else: row.append(1)
            save_grid.append(row)
        save_grid=json.dumps(save_grid)
    else: save_grid = grid
    print(save_grid)
    # Check if user exits
    user_id = get_user_id()
    cursor.execute(f"SELECT * FROM USERINFO WHERE user_id = {user_id}")
    user_found = cursor.fetchall()
    if user_found: # Update data if user exits
        update_query = """
            UPDATE USERINFO 
            SET highscore = %s, wave_no = %s, money = %s, grid = %s, health = %s
            WHERE user_id = %s
        """
        cursor.execute(update_query, (highscore, wave_no, money, save_grid, user_id, health))
    else: # Insert new record if user does not exist
        query = "INSERT INTO USERINFO VALUES (%s, %s, %s, %s, %s, %s)"
        data = (user_id, highscore, wave_no, money, save_grid, health)
        
        cursor.execute(query, data)
    print("committing")
    database.commit()
    print("committed")