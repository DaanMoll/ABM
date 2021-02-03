import pandas as pd

# df = pd.read_csv('15')
# df2 = pd.read_csv('16')

# df.dropna(
#     axis=0,
#     how='any',
#     thresh=None,
#     subset=None,
#     inplace=True
# )

# df2.dropna(
#     axis=0,
#     how='any',
#     thresh=None,
#     subset=None,
#     inplace=True
# )

# merged1 = pd.concat([df, df2], ignore_index=True)

# merged2 = pd.concat([merged1, df3], ignore_index=True)

# merged3 = pd.concat([merged2, df4], ignore_index=True)

# merged3 = merged3.drop(columns=['Unnamed: 0'])

# merged3.to_csv("test.csv")

df = pd.read_csv('first14.csv')
df2 = pd.read_csv('last6.csv')

merged = pd.concat([df, df2], ignore_index=True)
merged = merged.drop(columns=['Unnamed: 0'])

merged.to_csv("data_daan.csv")