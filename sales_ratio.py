import pandas as pd

df = pd.read_csv("Data/cleaned_data.csv", low_memory=False)
assessed_values = df['Assessed Value'].tolist()[:10]
sale_amounts = df['Sale Amount'].tolist()[:10]
ratios = df['Sales Ratio'].tolist()[:10]

for assessed, sale, ratio in zip(assessed_values, sale_amounts, ratios):
    print("assessed: ", assessed)
    print("sale: ", sale)
    print("my ratio: ", assessed / sale)
    print("ratio: ", ratio)
