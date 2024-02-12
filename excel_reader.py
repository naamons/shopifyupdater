
import pandas as pd
import configparser

def read_sku_map_from_excel(file_path, map_adjustment):
    df = pd.read_excel(file_path)
    if "Article code" in df.columns and "Price, USD" in df.columns:
        # Apply MAP Adjustment
        df["Price, USD"] = df["Price, USD"] / map_adjustment
        return df[["Article code", "Price, USD"]]
    else:
        raise ValueError("Excel file must contain 'Article Code' and 'Price, USD' columns")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    file_path = config['Filepaths']['excel_file_path']
    # Read the MAP adjustment factor from the config file
    map_adjustment = float(config['Prices']['map_adjustment'])
    print(read_sku_map_from_excel(file_path, map_adjustment))
