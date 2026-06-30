
import pandas as pd
import numpy as np
from unidecode import unidecode

def clean_columns(df):
  df.columns = [
    unidecode(col)
    for col in df.columns
  ]
  df.columns = df.columns\
    .str.lower()\
    .str.strip()\
    .str.replace(r"[^a-z0-9]+", "_", regex=True)\
    .str.rstrip("_")


  return df

def clean_num_col(df,col, threshold=0.8):

  # Only apply string replacements if the column is a string or object type
  if pd.api.types.is_object_dtype(df[col]):
  #or pd.api.types.is_string_dtype(df[col]):
    df[col] = df[col]\
    .astype(str)\
    .str.replace(r"\\[\\w+\\]", "", regex=True)\
    .str.replace("$", "", regex=False)\
    .str.replace(",", "", regex=False)

  converted = pd.to_numeric(
            df[col],
            errors="coerce"
        )
  ratio = converted.notna().mean()

  if ratio >= threshold:
    df[col] = converted

  return df[col]


def clean_num_df(df):
  df = df.copy()
  for col in df.columns:
    df[col] = clean_num_col(df,col, threshold=0.8)
  return df

def clean_date_col(df,col, threshold=0.8):
  converted = pd.to_datetime(
            df[col],
            errors="coerce"
        )
  ratio = converted.notna().mean()

  if ratio >= threshold:
    df[col] = converted

  return df[col]


def clean_date_df(df):
  df = df.copy()
  for col in df.columns:
    if df[col].dtype == "object":
      df[col] = clean_date_col(df,col, threshold=0.8)
  return df


def homogenizar_strings_df(df):
  df = df.copy()

  df = df.map(
    lambda x: unidecode(x)
    if isinstance(x, str)
    else x)

  for col in df.columns:
    if pd.api.types.is_string_dtype(df[col]) or df[col].dtype == "object":

      df[col] = df[col].astype("string")\
      .str.lower()\
      .str.strip()\
      .str.replace(r"[^a-z0-9]+", "_", regex=True)\
      .str.rstrip("_")
  return df


def homogenizar_strings_new(df, exclude_cols=None):

  df = df.copy()

  if exclude_cols is None:
        exclude_cols = []

  df = df.map(
        lambda x: unidecode(x)
        if isinstance(x, str)
        else x
    )

  for col in df.columns:
      if col in exclude_cols:
        continue

      if pd.api.types.is_string_dtype(df[col]) or df[col].dtype == "object":

        df[col] = (df[col]\
        .astype("string")\
        .str.lower()\
        .str.strip()\
        .str.replace(r"[^a-z0-9]+", "_", regex=True)\
        .str.rstrip("_"))

  return df
    

def clean_df(df):
  df = df.copy()
  df = clean_columns(df)
  df = clean_num_df(df)
  df = clean_date_df(df)
  #df = homogenizar_strings_df(df)
  return df


def replace_misiing_values(df,mis_val):
  df = df.copy()
  for col in df.columns:
    if pd.api.types.is_string_dtype(df[col]):
      df[col] = df[col].replace(mis_val,pd.NA)
  return df
