# """
# Handles read and write operations for datasave, and acts as the middle man between Python and the MySQL database
# """

# import mysql.connector
# import uuid
# import json

# # Default data for empty records
# default = {
#     "user_id" : None, # will be set later
#     "highscore" : 0,
#     "wave_no" : 0,
#     "money" : 500,
#     "grid" : None,
#     "health" : 100,
#     "contains_data" : False # indicator of whether data has actually been previously saved or not
# }

# try:
#     database = mysql.connector.connect(
#     host="127.0.0.1",
#     user="root",
#     password="password123!", # This has been done for simplification, and is not secure
#     database="IA_Datasave"
#     )
#     cursor = database.cursor()
# except Exception as e:
#     print(f"Failed to connect to database: {e}")


# def get_user_id(): # Uses MAC address as user id
#     return uuid.getnode()

# def get_user_data():
#     try:
#         user_id = get_user_id()
#         # Fetch user info using SELECT statement
#         cursor.execute(f"SELECT * FROM USERINFO WHERE user_id = {user_id}")
#         results = cursor.fetchall()
#         # Return default results if empty
#         if not results:
#             default["user_id"] = user_id
#             return default
        
#         # Reformat results into a dictionary
#         user_data = {
#             "user_id" : user_id,
#             "highscore" : results[0][1],
#             "wave_no" : results[0][2],
#             "money" : results[0][3],
#             "grid" : json.loads(results[0][4]),
#             "health" : results[0][5],
#             "contains_data" : True
#         }
#         # If data matches default values, mark as empty (excluding highscore)
#         if user_data["wave_no"] == 0 and user_data["health"] == 100 and (user_data["grid"] == None or not any(1 in row for row in user_data["grid"])):
#             user_data["contains_data"] = False
#         return user_data
#     except Exception as e:
#         # Handle error in retrieving data, and instead return empty data
#         print(f"Error while fetching user data: {e}")
#         default["user_id"] = user_id
#         return default

# def save_user_data(highscore, wave_no, money, grid, health):
#     try:
#         if grid:
#             # Convert grid into a saveable format
#             save_grid = []
#             for r in grid:
#                 row = []
#                 for x in r:
#                     if x == None: row.append(0)
#                     else: row.append(1)
#                 save_grid.append(row)
#             save_grid=json.dumps(save_grid)
#         else: save_grid = grid
#         # Check if user exits
#         user_id = get_user_id()
#         cursor.execute(f"SELECT * FROM USERINFO WHERE user_id = {user_id}")
#         user_found = cursor.fetchall()
#         if user_found: # Update data if user exits
#             update_query = """
#                 UPDATE USERINFO 
#                 SET highscore = %s, wave_no = %s, money = %s, grid = %s, health = %s
#                 WHERE user_id = %s
#             """
#             cursor.execute(update_query, (highscore, wave_no, money, save_grid, health, user_id))
#         else: # Insert new record if user does not exist
#             query = "INSERT INTO USERINFO VALUES (%s, %s, %s, %s, %s, %s)"
#             data = (user_id, highscore, wave_no, money, save_grid, health)
            
#             cursor.execute(query, data)
#         database.commit()
#     except Exception as e:
#         print(f"Error while saving data: {e}")