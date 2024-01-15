import pandas as pd
import numpy as np

df = pd.read_excel("115.xlsx")
print(df)

def divide_and_add(row, column_name):
    try:
        value = float(row[column_name])
        row[column_name + '_Лево'] = value / 4
        row[column_name + '_Право'] = value / 4
    except ValueError:
        row[column_name + '_Лево'] = None
        row[column_name + '_Право'] = None
    return row

df['Расстояние'] = pd.to_numeric(df['Расстояние'], errors='coerce')
df['Расстояние'] = df['Расстояние'] / 2

df = df.apply(lambda row: divide_and_add(row, 'Насыпь'), axis=1)
df = df.apply(lambda row: divide_and_add(row, 'Выемка'), axis=1)
df = df.apply(lambda row: divide_and_add(row, 'Кюветы'), axis=1)
df = df.apply(lambda row: divide_and_add(row, 'Присыпные\nобочины'), axis=1)


duplicated_df = pd.DataFrame(columns=df.columns)

for i in range(0, len(df), 2):
    duplicated_df = pd.concat([duplicated_df, df.iloc[i:i+2], df.iloc[i:i+2]])


duplicated_df = duplicated_df.drop(['Насыпь', 'Выемка', 'Кюветы', 'Присыпные\nобочины'], axis=1)


duplicated_df['Пикетаж'] = None


piketage_values = []
current_value = 0

for index, row in duplicated_df.iterrows():
    if index % 2 == 0:
        piketage_values.append(f'{current_value // 100}+{current_value % 100:02d}.000')
        current_value += 10
    else:
        piketage_values.append(None)

duplicated_df['Пикетаж'] = piketage_values


try:
    with pd.ExcelWriter('вырезка2.xlsx', engine='openpyxl') as writer:
        duplicated_df.to_excel(writer, index=False, sheet_name='Sheet1')
except IndexError:
    with pd.ExcelWriter('вырезка2.xlsx') as writer:
        duplicated_df.to_excel(writer, index=False, sheet_name='Sheet1')