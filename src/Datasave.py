"""
Handles read and write operations for datasave. 
Persistent data is stored locally in a .txt file, which can be read and written
"""

# Default data for empty records
default = {
    "highscore" : 0,
    "wave_no" : 0,
    "money" : 500,
    "grid" : None,
    "health" : 100,
    "contains_data" : False # indicator of whether data has actually been previously saved or not
}

def save_user_data(highscore, wave_no, money, grid, health):
    try: 
        # Convert grid to proper format
        if grid: 
            save_grid = ""
            for row in grid:
                for x in row:
                    if x == None: save_grid += "0" # indicates empty
                    else: save_grid += "1" # indicates full
                save_grid += "_" # indicates new line

        # Save data to txt
        with open("save.txt", "w") as f:
            f.write(f"{highscore}\n{wave_no}\n{money}\n{save_grid}\n{health}")
    except Exception as e:
        print(f"Error while saving data: {e}")

def get_user_data():
    data = default
    try: 
        with open("save.txt", "r") as f:
            lines = f.readlines()
            if not lines:
                return default

            for i, line in enumerate(lines):
                if i == 0: data["highscore"] = int(line)
                if i == 1: data["wave_no"] = int(line)
                if i == 2: data["money"] = int(line)
                if i == 3 and line != "None":     
                    grid = []
                    row = []
                    for x in list(line):
                        if x == "_": 
                            grid.append(row)
                            row = []
                        elif x != "\n": 
                            row.append(int(x))
                    data["grid"] = grid
                if i == 4: data["health"] = int(line)
            
            if data["wave_no"] != 0 or data["health"] != 100 or (data["grid"] != None and any(1 in row for row in data["grid"])):
                data["contains_data"] = True
    except Exception as e:
        print(f"Error while fetching user data: {e}")
    return data