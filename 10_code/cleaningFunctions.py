import pandas as pd

# Function that cleans overdose mortality data
# state_abbr must be capitalized
def clean_mortality(df, State_Abbr):
    df[["County1", "State"]] = df.County.str.split(", ", expand=True)
    df = df[df["State"] == State_Abbr]
    df = df.drop(["Notes", "County", "County Code", "Year Code"], axis=1)
    df = df.rename(columns={"County1": "County"})
    df = df[(df["Drug/Alcohol Induced Cause Code"] == "D1") | (df["Drug/Alcohol Induced Cause Code"] == "D2") | (df["Drug/Alcohol Induced Cause Code"] == "D4") | (df["Drug/Alcohol Induced Cause Code"] == "D9")]
    df["Deaths"] = df["Deaths"].astype(float)
    df = df.groupby(["Year", "State", "County"], as_index=False).sum()
    df["Year"] = df["Year"].astype(int)
    return df


# Function that cleans population data by state
def clean_pop(df1,df2):
    df1 = df1.drop(["Unnamed: 1", 2000, 2001, 2002, "Unnamed: 12", "Unnamed: 13"], axis=1)
    df1 = df1.rename(columns={"Unnamed: 0": "County"})
    df2 = df2.drop(["Census", "Estimates Base", 2016, 2017, 2018, 2019], axis=1)
    df2 = df2.rename(columns={"Unnamed: 0": "County"})
    df1.drop(df1.head(1).index, inplace=True)
    df1.drop(df1.tail(8).index, inplace=True)
    df2.drop(df2.head(1).index, inplace=True)
    df2.drop(df2.tail(5).index, inplace=True)
    df1["County"] = df1["County"].str[1:]
    df2["County"] = df2["County"].str[1:]
    df1 = df1.melt(id_vars=["County"])
    df1 = df1.rename(columns={"variable": "Year", "value": "Population"})
    df1 = df1.groupby(["Year", "County"], as_index=False).sum()
    df2 = df2.melt(id_vars=["County"])
    df2 = df2.rename(columns={"variable": "Year", "value": "Population"})
    df2 = df2.groupby(["Year", "County"], as_index=False).sum()
    df2[["County1", "State"]] = df2.County.str.split(", ", expand=True)
    df2 = df2.drop(["County", "State"], axis=1)
    df2 = df2.rename(columns={"County1": "County"})
    df_concat = pd.concat([df1,df2],ignore_index=True)
    return df_concat


# Function that merges population data with mortality data
def merge_mortalitypop(df_mortality, df_pop):
    merged = df_mortality.merge(df_pop, how="left")
    merged["Mortality Rate"] = merged["Deaths"] / merged["Population"]
    return merged


# Function that groups dataframe by year, and calculate the total death and total population
def calc_avg_mortality(df1, df2, df3):
    df1 = df1.groupby('Year', as_index=False).sum()[['Year', 'Deaths', 'Population']]
    df2 = df2.groupby('Year', as_index=False).sum()[['Year', 'Deaths', 'Population']]
    df3 = df3.groupby('Year', as_index=False).sum()[['Year', 'Deaths', 'Population']]

    df = pd.concat([df1, df2, df3], ignore_index=True)
    df = df.groupby('Year', as_index=False).sum()
    df['Avg Mortality Rate'] = df['Deaths'] / df['Population']
    return df