import pandas as pd

# Load the CSV and JSON files into DataFrames
csv_path = r'C:\Users\venka\Desktop\Solar Eclipse\eclipse_subscriber_data_with_links.csv'
json_path = r'C:\Users\venka\Desktop\Solar Eclipse\eclipse_subscriber_data_with_times.json'

csv_df = pd.read_csv(csv_path)
json_df = pd.read_json(json_path, lines=True)

# Convert 'eclipse_time' in both DataFrames to datetime format
csv_df['eclipse_time'] = pd.to_datetime(csv_df['eclipse_time'], errors='coerce')
json_df['eclipse_time'] = pd.to_datetime(json_df['eclipse_time'], errors='coerce')

# Merge the DataFrames on 'subscriber_id' and 'eclipse_time', keeping all columns but avoiding duplication
merged_df = pd.merge(csv_df, json_df, on=['subscriber_id', 'eclipse_time'], how='outer', suffixes=('_csv', '_json'))

# Calculate total eclipse data usage (eclipse upstream + eclipse downstream)
merged_df['total_eclipse_data_usage'] = merged_df['eclipse_upstream_data'] + merged_df['eclipse_downstream_data']

# Calculate total data usage (upstream + downstream) for each record
merged_df['total_data_usage'] = merged_df['data_usage_upstream'] + merged_df['data_usage_downstream']

# Calculate average data usage
merged_df['average_data_usage'] = merged_df['total_data_usage'] / len(merged_df)

# Example merge duration calculation (assuming arrival_time and start_time are in datetime format)
merged_df['merge_duration'] = (pd.to_datetime(merged_df['arrival_time']) - pd.to_datetime(merged_df['start_time'])).dt.total_seconds() / 3600.0

# Display all columns in the final merged DataFrame
print("Columns in the final merged DataFrame:")
print(merged_df.columns)

# Optionally, you can display the first few rows of the DataFrame to inspect the data
print("\nSample data from the merged DataFrame:")
print(merged_df.head())

# Save the resulting DataFrame to a new CSV file
output_path = r'C:\Users\venka\Desktop\Solar Eclipse\eclipse_subscriber_data_merged.csv'
merged_df.to_csv(output_path, index=False)

print(f"\nMerged data saved to {output_path}")
