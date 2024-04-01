import pandas as pd

file_path = '.../responses.csv'

column_names = ['Timestamp', 'date', 'event', 'name'] # new column names
df = pd.read_csv(file_path, header = 0, names=column_names) #import data

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
df['Date'] = pd.to_datetime(df['Date'], format='%a %dth %B')
df['Date'] = df['Date'].dt.strftime('%d-%m')

######### Create new output df #########

# Determine unique dates:
date_list = list(df['Date'].unique())


pivot_df = df.pivot_table(index='Date', columns='Event', values='name', aggfunc=lambda x: ', '.join(x))
pivot_df = pivot_df.sort_values(by='Date', ascending=False)
pivot_df = pivot_df.reset_index()
pivot_df.fillna("/", inplace=True)


# Save to csv
output_file_path = '.../output.xlsx'
pivot_df.to_excel(output_file_path, index=False)
