import json
import os
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd


def _period_frequency(period):
    return {"month": "M", "quarter": "Q", "year": "Y"}[period]

def _period_window(period, end_date):
    if period == "quarter":
        current = pd.Period(end_date, freq='Q')
        if current.end_time == end_date: return current - 1, end_date
        return (current - 1).start_time, (current - 1).end_time
    elif period == "year":
        current = pd.Period(end_date, freq='Y')
        if current.end_time == end_date: return current - 1, end_date
        return (current - 1).start_time, (current - 1).end_time
    elif period == "month":
        current = pd.Period(end_date, freq='M')
        if current.end_time == end_date: return current - 1, end_date
        return (current - 1).start_time, (current - 1).end_time

def _range_start_date(range_key, history_start, end_range):
    end_date = end_range.normalize()
    if range_key == "last-6-months": return (end_date - pd.DateOffset(months=6)).normalize()
    if range_key == "last-year": return (end_date - pd.DateOffset(years=1)).normalize()
    if range_key == "last-3-years": return (end_date - pd.DateOffset(years=3)).normalize()
    if range_key == "last-6-years": return (end_date - pd.DateOffset(years=6)).normalize()
    if range_key == "last-10-years": return (end_date - pd.DateOffset(years=10)).normalize()
    if range_key == "all-data": return history_start

def _has_any_category(value, terms):
    normalized = {item.strip().lower() for item in str(value).split(",") if item.strip()}
    return any(term.strip().lower() in normalized for term in terms)

def main():
    DATA_PATH = Path("data/games.csv")
    PRECOMP_DIR = Path("data")

    df = pd.read_csv(DATA_PATH, low_memory=False)
    df["Release date"] = pd.to_datetime(df["Release date"], errors="coerce")
    

    explore_df = df.copy()
    bounds = explore_df["Estimated owners"].fillna("").astype(str).str.extract(r"(?P<lower>\d+)\s*-\s*(?P<upper>\d+)")
    explore_df["Owners lower"] = pd.to_numeric(bounds["lower"], errors="coerce")
    explore_df["Owners upper"] = pd.to_numeric(bounds["upper"], errors="coerce")
    explore_df["Income"] = explore_df.get("Estimated_Income", 0)
    explore_df["Positive ratings"] = explore_df.get("Positive_Pct", 0)
    explore_df["Negative ratings"] = explore_df.get("Negative_Pct", 0)
    
    def tokenize(value):
        if not value: return []
        return [part.strip().lower() for part in str(value).split(",") if part.strip()]
    
    explore_df["_genres_tokens"] = explore_df["Genres"].fillna("").apply(tokenize)
    explore_df["_categories_tokens"] = explore_df["Categories"].fillna("").apply(tokenize)
    explore_df["_tags_tokens"] = explore_df["Tags"].fillna("").apply(tokenize)
    
    explore_df.to_parquet(PRECOMP_DIR / "explore_optimized.parquet")


    overview_df = df.copy()
    END_RANGE = overview_df['Release date'].max()
    history_start_date = overview_df["Release date"].min().normalize()
    
    genre_lists = overview_df["Genres"].fillna("").astype(str).apply(
        lambda value: [genre.strip() for genre in value.split(",") if genre.strip()]
    )
    overview_df["Genre list"] = genre_lists
    overview_df["Genre count"] = genre_lists.apply(len)
    overview_df["Market value base"] = overview_df["Owner midpoint"].fillna(0) * overview_df["Price"].fillna(0)
    overview_df["Purchased copies base"] = overview_df["Owner midpoint"].fillna(0)
    
    genres = ["All genres"] + sorted(list(set([g for sublist in genre_lists for g in sublist])))
    
    overview_timeseries = {"month": {}, "quarter": {}, "year": {}}
    overview_metrics = {}
    overview_pies = {}

    exploded = overview_df[overview_df["Genre count"] > 0].explode("Genre list")
    exploded["Market value"] = exploded["Market value base"] / exploded["Genre count"]
    exploded["Purchased copies"] = exploded["Purchased copies base"] / exploded["Genre count"]

    for period in ["month", "quarter", "year"]:
        freq = _period_frequency(period)
        
        # Total
        total_p = overview_df.copy()
        total_p["Release date"] = total_p["Release date"].dt.to_period(freq).dt.to_timestamp()
        
        market_total = total_p.groupby("Release date")["Market value base"].sum().reset_index()
        market_total.rename(columns={"Market value base": "Market value"}, inplace=True)
        
        purchased_total = total_p.groupby("Release date")["Purchased copies base"].sum().reset_index()
        purchased_total.rename(columns={"Purchased copies base": "Purchased copies"}, inplace=True)
        
        df_all = pd.merge(market_total, purchased_total, on="Release date", how="outer").fillna(0)
        df_all = df_all[(df_all["Market value"] > 0) | (df_all["Purchased copies"] > 0)].sort_values("Release date")
        
        overview_timeseries[period]["All genres"] = {
            "Release date": df_all["Release date"].dt.strftime("%Y-%m-%d").tolist(),
            "Market value": df_all["Market value"].tolist(),
            "Purchased copies": df_all["Purchased copies"].tolist()
        }
        
        exploded_p = exploded.copy()
        exploded_p["Release date"] = exploded_p["Release date"].dt.to_period(freq).dt.to_timestamp()
        
        grouped_market = exploded_p.groupby(["Release date", "Genre list"])["Market value"].sum().reset_index()
        grouped_purchased = exploded_p.groupby(["Release date", "Genre list"])["Purchased copies"].sum().reset_index()
        
        for genre in genres:
            if genre == "All genres": continue
            g_market = grouped_market[grouped_market["Genre list"] == genre]
            g_purchased = grouped_purchased[grouped_purchased["Genre list"] == genre]
            
            df_g = pd.merge(g_market, g_purchased, on=["Release date", "Genre list"], how="outer").fillna(0)
            df_g = df_g[(df_g["Market value"] > 0) | (df_g["Purchased copies"] > 0)].sort_values("Release date")
            
            overview_timeseries[period][genre] = {
                "Release date": df_g["Release date"].dt.strftime("%Y-%m-%d").tolist(),
                "Market value": df_g["Market value"].tolist(),
                "Purchased copies": df_g["Purchased copies"].tolist()
            }

    years = sorted(overview_df["Release date"].dropna().dt.year.unique().astype(int).tolist(), reverse=True)
    years = [y for y in years if 1997 <= y <= 2026]

    for genre in genres:
        overview_metrics[genre] = {}
        overview_pies[genre] = {}
        
        if genre == "All genres":
            g_df = overview_df.copy()
        else:
            mask = overview_df["Genre list"].apply(lambda x: genre in x)
            g_df = overview_df[mask].copy()
            
        for period in ["month", "quarter", "year"]:
            overview_metrics[genre][period] = {}
            start_date, end_date = _period_window(period, END_RANGE)
            prev_start, prev_end = _period_window(period, start_date)
            
            filtered = g_df[(g_df["Release date"] >= start_date) & (g_df["Release date"] < end_date)]
            prev_filtered = g_df[(g_df["Release date"] >= prev_start) & (g_df["Release date"] < prev_end)]
            
            def get_metrics(df_sub):
                owners = df_sub["Owner midpoint"].fillna(0)
                prices = df_sub["Price"].fillna(0)
                market_value = (owners * prices).sum()
                purchased_copies = owners.sum()
                average_playtime = df_sub["Average playtime forever"].mean(skipna=True)
                peak_ccu = df_sub["Peak CCU"].max(skipna=True)
                return {
                    "games_released": len(df_sub),
                    "market_value": float(market_value),
                    "purchased_copies": float(purchased_copies),
                    "average_playtime": float(0 if pd.isna(average_playtime) else average_playtime),
                    "peak_ccu": float(0 if pd.isna(peak_ccu) else peak_ccu)
                }

            overview_metrics[genre][period]["current_period"] = get_metrics(filtered)
            overview_metrics[genre][period]["previous_period"] = get_metrics(prev_filtered)

        for year in years:
            pie_start = pd.to_datetime(f"{year}-01-01")
            pie_end = pd.to_datetime(f"{year + 1}-01-01")
            pie_df = g_df[(g_df["Release date"] >= pie_start) & (g_df["Release date"] < pie_end)]
            
            cat_series = pie_df["Categories"].fillna("").astype(str)
            sp_terms = {"Single-player"}
            mp_terms = {"Multi-player", "PvP", "Online PvP", "Remote Play Together", "Cross-Platform Multiplayer", "MMO", "LAN PvP"}
            coop_terms = {"Co-op", "Remote Play Together", "Online Co-op", "Shared/Split Screen Co-op", "LAN Co-op"}
            
            game_type_values = [
                int(cat_series.apply(lambda v: _has_any_category(v, sp_terms)).astype(bool).sum()),
                int(cat_series.apply(lambda v: _has_any_category(v, mp_terms)).astype(bool).sum()),
                int(cat_series.apply(lambda v: _has_any_category(v, coop_terms)).astype(bool).sum()),
            ]
            
            windows = pie_df["Windows"].fillna(False).astype(bool)
            linux_col = pie_df["Linux"].fillna(False).astype(bool)
            mac = pie_df["Mac"].fillna(False).astype(bool)
            platform_values = [
                int((windows & ~linux_col & ~mac).sum()),
                int((windows & linux_col & mac).sum()),
                int((windows & linux_col & ~mac).sum()),
                int((windows & ~linux_col & mac).sum()),
            ]
            
            ctrl_terms = {"Full controller support", "Partial controller support", "Tracked Controller Support"}
            ctrl_supported = cat_series.apply(lambda v: _has_any_category(v, ctrl_terms)).astype(bool)
            controller_values = [int(ctrl_supported.sum()), int((~ctrl_supported).sum())]
            
            vr_terms = {"VR Only", "VR Supported", "VR Support", "SteamVR Collectibles"}
            vr_supported = cat_series.apply(lambda v: _has_any_category(v, vr_terms)).astype(bool)
            vr_values = [int(vr_supported.sum()), int((~vr_supported).sum())]
            
            overview_pies[genre][str(year)] = {
                "game_type": game_type_values,
                "platform": platform_values,
                "controller": controller_values,
                "vr": vr_values
            }

    with open(PRECOMP_DIR / "overview_precomputed.json", "w") as f:
        json.dump({
            "timeseries": overview_timeseries,
            "metrics": overview_metrics,
            "pies": overview_pies
        }, f)



    try:
        with open(PRECOMP_DIR / "insights_precomputed.json", 'r') as f:
            insights_data = json.load(f)
    except FileNotFoundError:
        insights_data = {}

    for genre in genres:
        if genre == "All genres": continue
        
        if genre not in insights_data:
            insights_data[genre] = {}
            
        mask = overview_df["Genres"].fillna("").astype(str).str.contains(genre, case=False, regex=False)
        df_target = overview_df[mask].copy()

        radar_metrics = ['Price', 'Positive_Pct', 'DLC count', 'Achievements', 'Average playtime forever']
        df_percentiles = pd.DataFrame()
        for col in radar_metrics:
            if col in df_target.columns:
                df_percentiles[col] = df_target[col].rank(pct=True, method='max') * 100
            else:
                df_percentiles[col] = 0

        df_percentiles['Peak CCU'] = pd.to_numeric(df_target.get('Peak CCU', 0), errors='coerce').fillna(0).values
        df_percentiles['Estimated_Income'] = pd.to_numeric(df_target.get('Estimated_Income', 0), errors='coerce').fillna(0).values

        niche_median_profile = df_percentiles[radar_metrics].median()
        
        top_cutoff_marker1 = df_percentiles['Peak CCU'].quantile(0.90) if not df_percentiles.empty else 0
        leaderboard_profile1 = df_percentiles[df_percentiles['Peak CCU'] >= top_cutoff_marker1][radar_metrics].median() if not df_percentiles.empty else pd.Series(0, index=radar_metrics)

        top_cutoff_marker2 = df_percentiles['Estimated_Income'].quantile(0.90) if not df_percentiles.empty else 0
        leaderboard_profile2 = df_percentiles[df_percentiles['Estimated_Income'] >= top_cutoff_marker2][radar_metrics].median() if not df_percentiles.empty else pd.Series(0, index=radar_metrics)

        niche_values = niche_median_profile.fillna(0).tolist() + [niche_median_profile.fillna(0).tolist()[0]] if not niche_median_profile.empty else []
        leader_values1 = leaderboard_profile1.fillna(0).tolist() + [leaderboard_profile1.fillna(0).tolist()[0]] if not leaderboard_profile1.empty else []
        leader_values2 = leaderboard_profile2.fillna(0).tolist() + [leaderboard_profile2.fillna(0).tolist()[0]] if not leaderboard_profile2.empty else []
        
        insights_data[genre]["radar"] = {
            "niche_values": niche_values,
            "leader_values1": leader_values1,
            "leader_values2": leader_values2
        }

        df_violin = df_target[df_target['Average playtime forever'] > 0].copy()
        df_violin['Playtime_Hours'] = df_violin['Average playtime forever'] / 60
        if not df_violin.empty:
            df_violin = df_violin[df_violin['Playtime_Hours'] <= df_violin['Playtime_Hours'].quantile(0.95)]
        
        q40 = df_violin['Price'].quantile(0.40) if not df_violin.empty else 0
        q80 = df_violin['Price'].quantile(0.80) if not df_violin.empty else 0
        if q40 == q80 and not df_violin.empty:
            q40 = df_violin['Price'].median() * 0.7
            q80 = df_violin['Price'].median() * 1.3

        def tier_assigner(price):
            if price == 0: return "Free"
            elif price <= q40: return f"Budget<br>(Under ${q40:.2f})"
            elif price <= q80: return f"Mid-tier<br>(${q40:.2f} - ${q80:.2f})"
            else: return f"Premium<br>(Above ${q80:.2f})"

        df_violin['Price_Tier'] = df_violin['Price'].apply(tier_assigner) if not df_violin.empty else []
        
        global_order = ["Free", f"Budget<br>(Under ${q40:.2f})", f"Mid-tier<br>(${q40:.2f} - ${q80:.2f})", f"Premium<br>(Above ${q80:.2f})"]
        
        violins_playtime = []
        for tier_name in global_order:
            sub_df = df_violin[df_violin['Price_Tier'] == tier_name] if not df_violin.empty else pd.DataFrame()
            if not sub_df.empty:
                violins_playtime.append({
                    "tier_name": tier_name,
                    "y": sub_df["Playtime_Hours"].tolist()
                })

        df_income = df_target[df_target.get('Estimated_Income', 0) > 0].copy()
        if not df_income.empty:
            df_income = df_income[df_income['Estimated_Income'] <= df_income['Estimated_Income'].quantile(0.95)]
        
        df_income['Price_Tier'] = df_income['Price'].apply(tier_assigner) if not df_income.empty else []
        income_order = [tier for tier in global_order if tier != "Free"]
        
        violins_income = []
        for tier_name in income_order:
            sub_df = df_income[df_income['Price_Tier'] == tier_name] if not df_income.empty else pd.DataFrame()
            if not sub_df.empty:
                violins_income.append({
                    "tier_name": tier_name,
                    "y": sub_df["Estimated_Income"].tolist()
                })

        insights_data[genre]["violins"] = {
            "global_order": global_order,
            "income_order": income_order,
            "playtime_data": violins_playtime,
            "income_data": violins_income
        }

    with open(PRECOMP_DIR / "insights_precomputed.json", "w") as f:
        json.dump(insights_data, f)

if __name__ == "__main__":
    main()
