from flask import current_app
from errors import QueryNotFound
from datetime import datetime, timedelta

def get_prob_single_sensor(campus_id):
    try:
        # prevent circular import
        from flask_server import MONGO
        target_data = MONGO.db.pm_data
        '''
        days = 90
        half = timedelta(days=1)
        cur = datetime.utcnow()
        lower = cur - half * days
        '''
        str = '2019-11-26 00:00:00'
        date_time = datetime.strptime(str,'%Y-%m-%d %H:%M:%S')
        
        recentData = list(target_data.find({
                '$and': [
                    {
                        'position': campus_id
                    },
                    {
                        'date': {
                            '$gte': date_time
                            
                        }
                    }
                ]
        }))
        #recentData = list(target_data.find({}, { '_id': 0 }))
        print (date_time)
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

def get_specific_time_data(campus_id):
    try:
        # prevent circular import
        from flask_server import MONGO
        target_data = MONGO.db.pm_data
        half = timedelta(days=1)
        #use utc because mongo use utc 
        now = datetime.utcnow()
        time_range=[8,12,18]
        specific_time_data = []
        for day in range(1,4):
            for time in range(3):
                lower = now.replace(hour = time_range[time]-8, minute = 0, second = 0) 
                upper = now.replace(hour = time_range[time]-7, minute = 0, second = 0) 
                lower -= half * day
                upper -= half * day
                

                

                pmdata = list(target_data.find({
                            '$and': [
                                {
                                    'position': campus_id
                                },
                                {
                                    'date': {
                                        '$gte': lower,
                                        '$lte': upper
                                    }
                                }
                            ]
                    }))

                sum = 0
                for i in pmdata:
                    sum +=i["pm25"]
                
                #Change time format to "Year-Month-day Hour:minute:second"
                taiwan_aware = lower.replace(hour = time_range[time], minute = 0, second = 0).strftime("%Y-%m-%d %H:%M:%S")

                if(len(pmdata) == 0):
                    specific_time_data.append({
                        "pm25":float(sum),
                        "date":taiwan_aware
                    })
                else:
                    specific_time_data.append({
                        "pm25":float(sum)/len(pmdata),
                        "date": taiwan_aware
                    })

        if len(pmdata) == 0:
                raise QueryNotFound
        return specific_time_data
    except QueryNotFound as err:
        current_app.logger.info(err)
        # return the an empty arr
        return []