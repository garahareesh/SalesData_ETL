import sqlite3
import pandas as pd
import json

class SalesDataETL:
    def __init__(self,db_name = 'sales_data.db'):
        self.db_name = db_name

    def extract_data(self,file_path,password = None):
        if file_path.endswith('xlsx'):
            return pd.read_excel(file_path)
        if file_path.endswith('csv'):
            return pd.read_csv(file_path)
    
    def transform_data(self,df,region_label):
        #total_sales
        print(df.columns)
        df['total_sales'] = df['QuantityOrdered'] * df['ItemPrice']
        df['region'] = region_label
        df.drop_duplicates(subset = ['OrderId'], inplace = True)
        print(df.columns)
        df['PromotionDiscount'] = df['PromotionDiscount'].apply(self.extract_amount).fillna(0)
        df['net_sale'] = df['total_sales']-df['PromotionDiscount']
        df = df[df['net_sale']>0]

        print(df)
        return df
    def extract_amount(self,promo_disc):
        if isinstance(promo_disc,str):
            try:
                promo_disc = json.loads(promo_disc)
            except json.JSONDecodeError:
                return 0
        return pd.to_numeric(promo_disc.get('Amount',0),errors = 'coerce')
    
    def load_data_to_db(self,df):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        #create sales_data table
        cursor.execute ('''
            CREATE TABLE IF NOT EXISTS sales_data(
            OrderId INTEGER PRIMARY KEY,
            OrderItemId INTEGER,
            QuantityOrdered INTEGER,
            ItemPrice REAL,
            total_sale REAL,
            region TEXT,
            net_sale REAL
            )
        ''')
        # load df into database
        df.to_sql('sales_data',conn,if_exists = 'replace', index = False)
        conn.commit()
        conn.close()
    def execute_etl(self,region_a,region_b):
        df_a = self.extract_data(region_a)
        df_b = self.extract_data(region_b)
        transform_df_a = self.transform_data(df_a,region_label = 'A')
        transform_df_b = self.transform_data(df_b,region_label = 'B')
        concat_df = pd.concat([transform_df_a,transform_df_b],ignore_index = True)
        self.load_data_to_db(concat_df)
        pass 
    
def main():
    etl = SalesDataETL()
    region_a = "order_region_a.xlsx"
    region_b = "order_region_b.xlsx"
    etl.execute_etl(region_a,region_b)
if __name__ == '__main__':
    main()