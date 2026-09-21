from pathlib import Path
import numpy as np
import pandas as pd

RAW = Path("data/raw/financials_2016_2025_raw.csv")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(RAW)
if df.empty:
    raise SystemExit("원천 데이터가 없습니다.")

MAP = {
"revenue":["매출액","수익(매출액)"], "gross_profit":["매출총이익"],
"operating_income":["영업이익","영업이익(손실)"], "net_income":["당기순이익","당기순이익(손실)"],
"assets":["자산총계"], "current_assets":["유동자산"],
"cash":["현금및현금성자산"], "receivables":["매출채권"], "inventory":["재고자산"],
"liabilities":["부채총계"], "current_liabilities":["유동부채"], "equity":["자본총계"],
"cfo":["영업활동 현금흐름","영업활동으로 인한 현금흐름"],
}
records=[]
for year, sub in df.groupby(df["bsns_year"].astype(str)):
    rec={"year":int(year)}
    for key,names in MAP.items():
        x=sub[sub["account_nm"].isin(names)]
        if not x.empty:
            value = x.iloc[0]["thstrm_amount"]
            rec[key] = pd.to_numeric(value, errors="coerce")
        else:
            rec[key] = np.nan
    records.append(rec)
out=pd.DataFrame(records).sort_values("year")
out["avg_assets"]=(out["assets"]+out["assets"].shift(1))/2
out["avg_equity"]=(out["equity"]+out["equity"].shift(1))/2
out["revenue_growth"]=out["revenue"].pct_change()
out["gross_margin"]=out["gross_profit"]/out["revenue"]
out["operating_margin"]=out["operating_income"]/out["revenue"]
out["net_margin"]=out["net_income"]/out["revenue"]
out["roa"]=out["net_income"]/out["avg_assets"]
out["roe"]=out["net_income"]/out["avg_equity"]
out["current_ratio"]=out["current_assets"]/out["current_liabilities"]
out["debt_ratio"]=out["liabilities"]/out["equity"]
out["equity_ratio"]=out["equity"]/out["assets"]
out["cfo_net_income"]=out["cfo"]/out["net_income"]
out["total_asset_turnover"]=out["revenue"]/out["avg_assets"]
out.to_csv(OUT/"sk_hynix_financial_analysis_2016_2025.csv",index=False,encoding="utf-8-sig")
out.to_json(OUT/"sk_hynix_financial_analysis_2016_2025.json",orient="records",force_ascii=False,indent=2)
print(out.tail())
