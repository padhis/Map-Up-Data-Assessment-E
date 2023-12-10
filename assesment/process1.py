import pandas as pd

file_path = 'C:/Users/ADMIN/Downloads/MapUp-Data-Assessment-E-main/MapUp-Data-Assessment-E-main/evaluation_data/input/raw_data.parquet'

df = pd.read_parquet(file_path)

df.info()

df['timestamp'] = pd.to_datetime(df['timestamp'])

df.info()

df.sort_values(by = ['unit', 'timestamp'], inplace = True)

df['time_diff'] = df.groupby('unit')['timestamp'].diff()

threshold = pd.Timedelta(hours = 7)

df['new_trip'] = df['time_diff'] > threshold
df.new_trip.value_counts()

df['trip_number'] = df.groupby('unit')['new_trip'].cumsum()

output = 'C:/Users/ADMIN/Downloads/MapUp-Data-Assessment-E-main/MapUp-Data-Assessment-E-main/evaluation_data/output'


for (unit, trip_number), trip_df in df.groupby(['unit', 'trip_number']):
        output_file_path = f"{output}/{unit}_{trip_number}.csv"
        trip_df[['latitude', 'longitude', 'timestamp']].to_csv(output_file_path, index=False)


