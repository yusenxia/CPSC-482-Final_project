import pandas as pd

df = pd.read_csv("game_analytics.csv")

print("Original shape:", df.shape)

df = df.dropna(subset=["appid", "name"])

text_columns = [
    "genre_primary",
    "developer",
    "publisher",
    "publisher_tier",
    "tags",
    "pc_req_min",
    "pc_req_rec"
]

for col in text_columns:
    df[col] = df[col].fillna("Unknown")

numeric_columns_zero = [
    "price_initial",
    "price_final",
    "discount_percent",
    "owners_min",
    "owners_max",
    "owners_midpoint",
    "positive_reviews",
    "negative_reviews",
    "ccu",
    "peak_ccu",
    "required_age",
    "languages_count",
    "achievement_count",
    "dlc_count"
]

for col in numeric_columns_zero:
    df[col] = df[col].fillna(0)

boolean_columns = [
    "is_early_access",
    "is_free",
    "steam_deck"
]

for col in boolean_columns:
    df[col] = df[col].fillna(False)

df["controller_support"] = df["controller_support"].fillna("Unknown")

df["appid"] = df["appid"].astype(int)

int_columns = [
    "owners_min",
    "owners_max",
    "owners_midpoint",
    "positive_reviews",
    "negative_reviews",
    "ccu",
    "peak_ccu",
    "required_age",
    "languages_count",
    "achievement_count",
    "dlc_count"
]

for col in int_columns:
    df[col] = df[col].astype(int)

float_columns = [
    "price_initial",
    "price_final",
    "discount_percent"
]

for col in float_columns:
    df[col] = df[col].astype(float)

df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

df["release_year"] = df["release_date"].dt.year

df["release_date"] = df["release_date"].dt.strftime("%Y-%m-%d")

df["total_reviews"] = df["positive_reviews"] + df["negative_reviews"]

df["positive_review_percent"] = df.apply(
    lambda row: round((row["positive_reviews"] / row["total_reviews"]) * 100, 2)
    if row["total_reviews"] > 0 else 0,
    axis=1
)

df["negative_review_percent"] = df.apply(
    lambda row: round((row["negative_reviews"] / row["total_reviews"]) * 100, 2)
    if row["total_reviews"] > 0 else 0,
    axis=1
)

df["game_type"] = df["is_free"].apply(
    lambda x: "Free-to-play" if x == True else "Paid"
)

df["has_discount"] = df["discount_percent"].apply(
    lambda x: True if x > 0 else False
)

df["has_achievements"] = df["achievement_count"].apply(
    lambda x: True if x > 0 else False
)

before_dedup = df.shape[0]

df["name_clean"] = df["name"].astype(str).str.strip().str.lower()

df = df.sort_values(
    by=["total_reviews", "peak_ccu", "owners_midpoint"],
    ascending=[False, False, False]
)

df = df.drop_duplicates(subset=["name_clean"], keep="first")

df = df.drop(columns=["name_clean"])

after_dedup = df.shape[0]

print("Rows before duplicate removal:", before_dedup)
print("Rows after duplicate removal:", after_dedup)
print("Duplicate rows removed:", before_dedup - after_dedup)

df = df.drop(columns=["pc_req_min", "pc_req_rec"], errors="ignore")

df.to_csv("cleaned_game_analytics.csv", index=False, encoding="utf-8")

print("Cleaned shape:", df.shape)
print("Cleaned file saved as cleaned_game_analytics.csv")
print(df.head())