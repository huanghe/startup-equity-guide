#!/usr/bin/env python3
"""从分面数据计算核心指标。用法: python3 scripts/analyze.py"""
import json, pathlib

D = pathlib.Path(__file__).resolve().parent.parent / "data/facets/2026-08-15_core.json"
q = {x["id"]: x for x in json.load(open(D))["queries"]}
E, B = q["P_equity_labor"], q["B_labor_all"]

def share(f, group, key, total):
    return f["facets"][group].get(key, 0) / total * 100

print("=" * 66)
print(f"股权激励∩劳动争议 = {E['total']:,}    劳动争议基线 = {B['total']:,}")
print(f"占比 = {E['total']/B['total']*10000:.2f} 万分之  (每 {B['total']//E['total']:,} 件中 1 件)")

print("\n【1】审级分布 —— 这类案子有多爱打二审")
print(f"{'':10}{'股权激励':>12}{'普通劳动争议':>14}{'倍数':>8}")
for lv in ["基层法院", "中级法院", "高级法院"]:
    a, b = share(E, "法院层级", lv, E["total"]), share(B, "法院层级", lv, B["total"])
    print(f"{lv:10}{a:>11.1f}%{b:>13.1f}%{a/b:>8.2f}x")

print("\n【2】地域集中度")
print(f"{'':10}{'股权激励':>12}{'普通劳动争议':>14}{'倍数':>8}")
tot_e = tot_b = 0
for p in ["北京市", "上海市", "广东省", "江苏省", "浙江省"]:
    a, b = share(E, "地域", p, E["total"]), share(B, "地域", p, B["total"])
    print(f"{p:10}{a:>11.1f}%{b:>13.1f}%{a/b:>8.2f}x")
    if p in ("北京市", "上海市", "广东省"):
        tot_e, tot_b = tot_e + a, tot_b + b
print(f"{'北上广合计':10}{tot_e:>11.1f}%{tot_b:>13.1f}%{tot_e/tot_b:>8.2f}x")

print("\n【3】相对占比的年度趋势 —— 用比值消掉'文书公开率下降'的偏差")
print(f"{'年份':<8}{'股权激励':>10}{'劳动争议':>12}{'万分比':>10}{'相对2019':>10}")
base = None
for y in [str(x) for x in range(2016, 2027)]:
    e = E["facets"]["裁判年份"].get(y, 0)
    b = B["facets"]["裁判年份"].get(y, 0)
    if not b:
        continue
    r = e / b * 10000
    if y == "2019":
        base = r
    rel = f"{r/base:.2f}x" if base else "-"
    star = "  ←不完整年" if y == "2026" else ""
    print(f"{y:<8}{e:>10,}{b:>12,}{r:>10.2f}{rel:>10}{star}")

print("\n【4】文书类型（⚠ 存在关键词命中偏差，不可直接作结论）")
for t in ["判决书", "裁定书", "调解书"]:
    a, b = share(E, "文书类型", t, E["total"]), share(B, "文书类型", t, B["total"])
    print(f"  {t:6} 股权激励 {a:5.1f}%   基线 {b:5.1f}%")
print("  → 调解书需全文命中'股权激励'才被计入，而调解书通常不载明争议细节，")
print("    因此该差异主要由检索方式造成，不能解读为'这类案子调解不了'。")
print("=" * 66)
