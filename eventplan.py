import pandas as pd
from datetime import datetime

######### Import csv file  #########

input_file_path = 'Responses.xlsx' 

column_names = ['Timestamp', 'date', 'event', 'name']
df = pd.read_excel(input_file_path, header = 0, names=column_names) 

######### Prepare df for work #########

# Expand df to get rid of multiple entries in event column
df = df.assign(Event=df['event'].str.split(', ')).explode('Event')

# Shortens the event title by removing " - X€"
df['Event'] = df['Event'].str.split('–').str[0]
# Keep initials of event (also removes parentheses)
#df['Event'] = df['Event'].apply(lambda x: ''.join(word[0] for word in x.split() if word[0].isalpha()))

# Expand df to get rid of multiple entries in date column
df = df.assign(Date=df['date'].str.split(', ')).explode('Date')

# get rid of date and timestamp column
df = df.drop(columns=['date', 'Timestamp', 'event'])

# Convert date to normal date form
current_year = datetime.now().year
# Convert dates and include the current year
df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%a %dth %B').replace(year=current_year)).dt.strftime('%d-%m-%y')
######### Create new output df #########

pivot_df = df.pivot_table(index='Date', columns='Event', values='name', aggfunc=lambda x: ', '.join(x))
pivot_df.index = pd.to_datetime(pivot_df.index, format='%d-%m-%y')
pivot_df = pivot_df.sort_index(ascending=True)

pivot_df.fillna("/", inplace=True)
pivot_df.index = pivot_df.index.date

######### Save to csv  #########

output_file_path = 'output.xlsx'
pivot_df.to_excel(output_file_path, index=True)
