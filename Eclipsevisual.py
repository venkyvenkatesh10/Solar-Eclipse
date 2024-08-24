import pandas as pd
import matplotlib.pyplot as plt

# Load the merged data file
file_path = r'C:\Users\venka\Desktop\Solar Eclipse\eclipse_subscriber_data_merged.csv'
save_path = r'C:\Users\venka\Desktop\Solar Eclipse'

# Ensure the DataFrame is loaded
df = pd.read_csv(file_path)

# Inspect the data to ensure it's loaded correctly
print(df.head())
print(df.columns)

# Plotting the data
plt.figure(figsize=(10, 6))
plt.bar(df['destination_city_csv'], df['merge_duration'])
plt.xlabel('City')
plt.ylabel('Duration (hours)')
plt.title('Merge Duration by City')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



