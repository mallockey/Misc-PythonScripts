import csv
from twilio.rest import Client
from datetime import datetime

twilio_sid = ''
twilio_token = ''
twilio_number = ''
to_number = ''

upcoming_birthdays = False
today_date = datetime.now()

with open('Birthdays.csv', mode='r') as csv_file:
  csv_reader = csv.DictReader(csv_file)
  send_string = ''
  for row in csv_reader:
    current_birthday = datetime.strptime(f'{row["Day"]}/{today_date.year}', f'%m/%d/%Y' )
    difference_in_days = (current_birthday - today_date).days
    if difference_in_days < 0:
      continue #The birthday has passed
    if difference_in_days < 30:
      upcoming_birthdays = True
      send_string += f'{row["Name"]} birthday is coming up on {row["Day"]}, '

if len(send_string) > 0:
  send_string = send_string[0: len(send_string) - 2]
  client = Client(twilio_sid, twilio_token)
  try:
    message = client.messages.create(
      to = to_number,
      from_= twilio_number,
      body = send_string
    )
  except:
    print("There was an error sending the message") 
  
  print("Message sent successfully!")
else:
  print("There are no birthdays coming up in the next 30 days") 


