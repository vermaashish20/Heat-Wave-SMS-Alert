import pandas as pd
from twilio.rest import Client


def detect_heatwaves(data, threshold=30, consecutive_days=3):
    data['heatwave'] = False
    count = 0

    for i in range(len(data)):
        if data['Temperature'][i] > threshold:
            count += 1
        else:
            count = 0

        if count >= consecutive_days:
            data.loc[i,'heatwave'] = True

    return data


def send_sms(to, message):
    #these are intentially wrong credentials
    account_sid = 'AC133rfdfjld3' # your twilio sid 
    auth_token = '343fdjflj3r' # your twilio auth token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_='+18053035966',
        to=to
    )

    print(f"Message sent to {to}: {message.sid}")


# Load historical temperature data from a CSV file
data = pd.read_csv('historical_temperature_data.csv')

# Apply heatwave detection
data = detect_heatwaves(data)

# Check for heatwaves and send notifications
for index, row in data.iterrows():
    if row['heatwave']:
        send_sms('+916354107123', f"Heatwave detected on {row['Date']} with temperature {row['Temperature']}°C.")
        #the mobile no. is intentially wrong