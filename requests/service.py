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
        #print (date_time)
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

        # if len(pmdata) == 0:
        #         raise QueryNotFound
        return specific_time_data
    except QueryNotFound as err:
        current_app.logger.info(err)
        # return the an empty arr
        return []


def get_one_month_data(campus_id):
    try:
        # prevent circular import
        from flask_server import MONGO
        target_data = MONGO.db.pm_data
        half_day = timedelta(days=1)
        half_hour = timedelta(hours=1)
        #use utc because mongo use utc 
        now = datetime.utcnow()
        one_month_data=[]
        
        for i in range(24):
            one_month_data.append([])
            
        for day in range(2,32):
            one_day_pm25 = []
            one_day_count = []
            for i in range(24):
                one_day_pm25.append(0)
                one_day_count.append(0)

            lower = now.replace(hour = 16,minute = 0, second = 0) 
            upper = now.replace(hour = 16,minute = 0, second = 0) 
            lower = lower- half_day * day 
            upper = upper- half_day * (day-1) 
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

            for i in range(len(pmdata)):
                pm25 = int(pmdata[i]["pm25"])
                hour = int(pmdata[i]["date"].hour)
                hour +=8
                if(hour > 23):
                    hour-=24
                one_day_pm25[hour]+=pm25
                one_day_count[hour]+=1

            for i in range(24):
                if(one_day_count[i] == 0):
                    one_month_data[i].append(float(one_day_pm25[i]))
                else:
                    one_month_data[i].append(float(one_day_pm25[i])/one_day_count[i])

        return one_month_data
    except QueryNotFound as err:
        current_app.logger.info(err)
        # return the an empty arr
        return []

# this one is for drawing splom cart about time ,pm25,humidity
def get_one_day_data(campus_id):
    try:
        # prevent circular import
        from flask_server import MONGO
        target_data = MONGO.db.pm_data
        half_day = timedelta(days=1)
        half_hour = timedelta(hours=1)
        #use utc because mongo use utc 
        now = datetime.utcnow()
        one_day_data=[]
        one_day_data_pm25 = []
        one_day_data_humidity = []

        
        
        for time in range(24):
            lower = now.replace(hour = 16,minute = 0, second = 0) 
            upper = now.replace(hour = 17,minute = 0, second = 0) 
            lower = lower- half_day * 2 + time * half_hour
            upper = upper- half_day * 2 + time * half_hour
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

            sum_pm25 = 0
            sum_humidity = 0
            for i in pmdata:
                sum_pm25 +=i["pm25"]
                sum_humidity +=i["humidity"]
            
            #Change time format to "Year-Month-day Hour:minute:second"
            

            if(len(pmdata) == 0):
                one_day_data_pm25.append(float(sum_pm25))
                one_day_data_humidity.append(float(sum_humidity))
            else:
                one_day_data_pm25.append(float(sum_pm25)/len(pmdata))
                one_day_data_humidity.append(float(sum_humidity)/len(pmdata))
        one_day_data.append(
            {
                'pm25':one_day_data_pm25,
                'humidity': one_day_data_humidity
            }
        )
        return one_day_data
    except QueryNotFound as err:
        current_app.logger.info(err)
        # return the an empty arr
        return []

