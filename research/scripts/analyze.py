#!/usr/bin/env python3
"""从分面数据计算核心指标（判决书同口径）。用法: python3 research/scripts/analyze.py"""
import json, pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
J = json.load(open(BASE / "data/facets/2026-08-15_judgments.json"))
S, F, DV = J["sets"], J["facets"], J["derived"]
NB, NE, NO = S["B_baseline"]["total"], S["E_equity"]["total"], S["E_option"]["total"]
UNION = DV["union_equity_option"]

def pct(fs, grp, key, n):
    return F[fs][grp].get(key, 0) / n * 100

print("=" * 72)
print("口径：案由=劳动争议、人事争议 且 文书类型=判决书（分子分母同口径）")
print("=" * 72)
print(f"基线 劳动争议判决书          {NB:>10,}")
print(f"含『股权激励』              {NE:>10,}")
print(f"含『期权』                  {NO:>10,}")
print(f"两者交集                    {S['I_equity_option']['total']:>10,}   重叠率 {S['I_equity_option']['total']/NE*100:.1f}%")
print(f"并集（容斥）                {UNION:>10,}   ← 真实规模，单关键词会漏掉约一半")

print(f"\n【0】稀有度")
for name, n in [("严格口径(股权激励)", NE), ("宽口径(并集)", UNION)]:
    print(f"  {name:<20} {n/NB*10000:5.2f}‱   每 {NB//n:,} 件劳动争议判决中 1 件"
          f"   律师办100件/年 → {NB/n/100:.1f} 年遇到 1 件")

print("\n【1】审级分布")
print(f"{'':10}{'股权激励':>10}{'基线':>10}{'倍数':>8}")
for lv in ["基层法院", "中级法院", "高级法院"]:
    a, b = pct("E_equity", "法院层级", lv, NE), pct("B_baseline", "法院层级", lv, NB)
    print(f"{lv:10}{a:>9.1f}%{b:>9.1f}%{a/b:>8.2f}x")

print("\n【2】地域集中度")
print(f"{'':10}{'股权激励':>10}{'基线':>10}{'倍数':>8}")
te = tb = 0
for p in ["北京市", "上海市", "广东省", "江苏省", "浙江省"]:
    a, b = pct("E_equity", "地域", p, NE), pct("B_baseline", "地域", p, NB)
    print(f"{p:10}{a:>9.1f}%{b:>9.1f}%{a/b:>8.2f}x")
    if p in ("北京市", "上海市", "广东省"):
        te, tb = te + a, tb + b
print(f"{'北上广合计':10}{te:>9.1f}%{tb:>9.1f}%{te/tb:>8.2f}x")

print("\n【3】相对占比趋势（比值消除文书公开率偏差）")
print(f"{'年份':<7}{'股权激励':>9}{'基线':>10}{'万分比':>9}{'vs2019':>9}")
base = None
for y in [str(x) for x in range(2016, 2027)]:
    e = F["E_equity"]["裁判年份"].get(y, 0)
    b = F["B_baseline"]["裁判年份"].get(y, 0)
    if not b: continue
    r = e / b * 10000
    if y == "2019": base = r
    tail = "  ←不完整年" if y == "2026" else ""
    rel = f"{r/base:.2f}x" if base else "—"
    print(f"{y:<7}{e:>9,}{b:>10,}{r:>9.2f}{rel:>9}{tail}")
print("=" * 72)
