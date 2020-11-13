import pandas as pd
import random
import numpy as np

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
def clean_pop(df1,df2,State_ABBR):
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
    df_concat["State"] = State_ABBR
    return df_concat


# Function that merges population data with mortality data
def merge_mortalitypop(df_mortality, df_pop):
    df_pop["County"] = df_pop["County"].astype("string")
    df_pop["State"] = df_pop["State"].astype("string")
    df_mortality["County"] = df_mortality["County"].astype("string")
    df_mortality["State"] = df_mortality["State"].astype("string")
    merged = df_mortality.merge(df_pop,left_on=["Year", "County"],
                                right_on=["Year", "County"], how="right")
    merged = merged.drop(["State_x"], axis=1)
    merged = merged.rename(columns={"State_y": "State"})
    merged["Deaths"] = merged["Deaths"].apply(lambda l: l if not np.isnan(l) else np.random.randint(0, 9))
    merged["Mortality Rate"] = merged["Deaths"] / merged["Population"]
    return merged

