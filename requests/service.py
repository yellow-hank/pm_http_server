from flask import current_app
from errors import QueryNotFound
from datetime import datetime, timedelta

def get_prob_single_sensor(campus_id):
    try:
        # prevent circular import
        from flask_server import MONGO
        target_data = MONGO.db.pm_data
        
        days = 90
        half = timedelta(days=1)
        cur = datetime.utcnow()
        lower = cur - half * days
        
        recentData = list(target_data.find({
                '$and': [
                    {
                        'position': campus_id
                    },
                    {
                        'date': {
                            '$gte': lower
                            
                        }
                    }
                ]
        }))
        #recentData = list(target_data.find({}, { '_id': 0 }))
        
        green =[0]*24
        yellow = [0]*24
        orange = [0] *24
        red =[0]*24
        prob_list=[]
        '''
        loop_range = 100
        if(len(recentData) < loop_range):
            upper = len(recentData)-1
            lower = 0
        else:
            upper =len(recentData)-1
            lower = len(recentData) - loop_range
        '''
        for i in range(len(recentData)):
            pm25 = int(recentData[i]["pm25"])
            hour = int(recentData[i]["date"].hour)
            
            if(hour +8 >23):
                hour = hour - 16
            else:
                hour = hour + 8
            
            if(pm25 <= 20):
                green[hour] += 1
                
            elif (pm25 > 20 and pm25 <= 40):
                yellow[hour] += 1
                
            elif (pm25 > 40  and pm25 <= 60):
                orange[hour] += 1
                
            else:
                red[hour] += 1
                    
            
        for i in range(24):
            total = green[i] + yellow[i] + orange[i] + red[i]
            if(total == 0):
                total = 1
            prob_list.append({
                'hour' : i,
                'green': float(green[i])/total,
                'yellow': float(yellow[i])/total,
                'orange': float(orange[i])/total,
                'red': float(red[i])/total
            })
        
         
            
        # No data is found
        if len(recentData) == 0:
            raise QueryNotFound
        return prob_list
    except QueryNotFound as err:
        current_app.logger.info(err)
        # return the an empty arr
        return []