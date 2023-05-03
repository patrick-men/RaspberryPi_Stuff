# Weather Notification

This Script uses the openweathermap API to get a forecast. The .json is then broken down into a short weather forecast of the day.
Using Pushbullet it is then send to my phone, as a push notification.
To automate the process, crontab schedules it to run every morning at 5.55am (right before the 6am forecast).
