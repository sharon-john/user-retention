import csv 
import time
import sys

DAY_1, DAY_15 = 1, 15

class UserData:
    def __init__(self):
        """ 
        curr_day_users maintains all the users seen in the current day
        seen_user_ids map to store user_id -> (origin_day, number of days seen)
        These two structures maintain the user_ids of the consecutive user as well as their duration
        If a user leaves for a day, they would be removed from the map. 
        """
        self.seen_user_ids = dict()
        self.curr_day_users = set()
    
    def update_user_map(self):
        new_user_map = dict()
        for key in self.curr_day_users.intersection(self.seen_user_ids):  
            #if a user_id was seen today and yesterday, it is consecutive
            #removes users who were not seen today, must treat as new user
            new_user_map[key] = self.seen_user_ids[key]
        
        self.seen_user_ids = new_user_map
        self.curr_day_users = set()

"""
create dict of dicts of the form {1: {1-14},...14: {1-14}}   
each outer key holds the day and each key within it holds the N_consecutive_users
"""
def initialize_day_counts():
    consecutive_day_users = dict()   
    for i in range(DAY_1,DAY_15):            
        consecutive_day_users[i] = dict()
        for j in range(DAY_1,DAY_15):
            consecutive_day_users[i][j] = 0
    return consecutive_day_users
            
def main():    
    consecutive_day_users = initialize_day_counts()  #dict of dicts data structure    
    user_data = UserData()
    
    try:
        csv_file = sys.argv[1]
    except:
        print("No valid CSV provided!")
    
    with open(csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        curr_day, last_seen_day = 0, 0   
            
        for row in csv_reader:
            curr_day = int(time.gmtime(int(row[0])).tm_mday)  #convert epoch to datetime and extract day
            user_id = str(row[1]) 
            
            if curr_day == last_seen_day + 1:  #epoch has crossed to next day, manage id and maps 
                user_data.update_user_map()  
            
            if user_id not in user_data.curr_day_users:  #first epoch sighting in this day for this user_id
                if user_id in user_data.seen_user_ids.keys():  #previously seen user
                    first_seen_day, n_days_seen = user_data.seen_user_ids[user_id]
                    n_days_seen += 1               # seen for one more consecutive day 
                    user_data.seen_user_ids[user_id] = (first_seen_day, n_days_seen)  #update record in map  
                    consecutive_day_users[first_seen_day][n_days_seen - 1] -= 1  
                    #Ex: user_playing_2_days becomes user_playing_3_days, so decrement 2 and increment 3 
                    consecutive_day_users[first_seen_day][n_days_seen] += 1     
                    
                else:
                    user_data.seen_user_ids[user_id] = (curr_day,1)  #set first_seen_day and num_consecutive is 1 
                    consecutive_day_users[curr_day][1] += 1
            
            user_data.curr_day_users.add(user_id)
            last_seen_day = curr_day
     
    """
    output printing logic, retrieves all the counts from dict of dicts
    """
    output = []
    for key in consecutive_day_users.keys():
        line = f"{key}"
        for i in range(DAY_1,DAY_15):
            line += f",{consecutive_day_users[key][i]}"
        output.append(line)
    print("\n".join(output))
            
if __name__ == "__main__":
    main()