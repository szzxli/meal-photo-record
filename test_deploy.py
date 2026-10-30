"""Deploy test: interval-propagation only, NOT independent nutritional truth.
Specific versions use the SAME generic bases as the intervals, so a hit
proves arithmetic propagation, not that a real kitchen matches. A miss is
reported honestly and must not be hidden by narrowing a range on n=1.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calculator import (BASE, _ing, _add, tbsp_oil_g, tsp_salt_g, TBSP_ML,
                        tomato_egg_whole, mapo_tofu_whole, cold_cucumber_whole,
                        portion, western_range, bowl_volume_ml, WEST_BASE)

def specific(ings, oil, salt, soy_ml, cluster, extra_kcal=0, extra_na=0):
    kcal = fat = na = 0.0
    for g, k in ings:
        a, b, c = BASE[k]; kcal += g*a/100; fat += g*b/100; na += g*c/100
    s = _add(oil, oil, salt, salt, soy_ml, soy_ml, cluster)
    return {"kcal": kcal+s[0]+extra_kcal, "fat_g": fat+s[2], "sodium_mg": na+s[4]+extra_na}

def check(name, tool, spec):
    hits = {}
    for k in ("kcal", "fat_g", "sodium_mg"):
        lo, hi = tool[k]; hits[k] = (round(lo,1), round(hi,1), round(spec[k],1), lo <= spec[k] <= hi)
    print(f"\n{name}: all={all(v[3] for v in hits.values())}")
    for k, v in hits.items(): print(f"  {k}: tool {v[0]}-{v[1]} specific {v[2]} hit={v[3]}")
    return hits

total = passed = 0
cases = []
# Chinese, same 6 cases as tool-v2 test
cases.append(check("tomato_egg Omnivore 1/3",
    portion(tomato_egg_whole("none"), 1/3),
    {k: v/3 for k, v in specific([(220,"egg"),(340,"tomato")], tbsp_oil_g(1.5), tsp_salt_g(1.0), 0, "none", 48).items()}))
cases.append(check("tomato_egg second 1/4",
    portion(tomato_egg_whole("none"), 1/4),
    {k: v/4 for k, v in specific([(165,"egg"),(600,"tomato")], tbsp_oil_g(3.0), tsp_salt_g(0.5), 0, "none").items()}))
cases.append(check("mapo video 1/4 (douban 1000mg assumption)",
    portion(mapo_tofu_whole("regular"), 1/4),
    {k: v/4 for k, v in specific([(150,"pork_mince"),(350,"silken_tofu")], tbsp_oil_g(2.0), 0, TBSP_ML, "regular", 0, 1000).items()}))
cases.append(check("mapo second 1/4 (douban 1000mg assumption)",
    portion(mapo_tofu_whole("regular"), 1/4),
    {k: v/4 for k, v in specific([(250,"pork_mince"),(280,"silken_tofu")], tbsp_oil_g(2.0), tsp_salt_g(0.25), TBSP_ML, "regular", 0, 1000).items()}))
cases.append(check("cucumber 1/2",
    portion(cold_cucumber_whole("unknown"), 1/2),
    {k: v/2 for k, v in specific([(400,"cucumber")], tbsp_oil_g(1.0), tsp_salt_g(0.5), 0, "unknown", 8).items()}))
cases.append(check("cucumber+soy 1/2",
    portion(cold_cucumber_whole("unknown"), 1/2),
    {k: v/2 for k, v in specific([(400,"cucumber")], tbsp_oil_g(1.0), tsp_salt_g(0.5), 7.5, "regular", 8).items()}))
# Western: specific grams inside density band, base values inside base intervals
for dish, D, cov, thick, salt, grams, base in [
    ("chicken", 20, 0.5, 1.5, 0.0, 220.0, (165.0, 3.6, 74.0)),
    ("salmon", 20, 0.5, 1.5, 1.0, 220.0, (208.0, 13.0, 59.0)),
    ("pasta_tomato", 25, 0.5, 2.0, 0.5, 400.0, (110.0, 1.5, 80.0)),
    ("brown_rice", 25, 0.33, 2.0, 0.0, 250.0, (118.0, 0.9, 3.0)),
]:
    tool = western_range(dish, D, cov, thick, salt)
    spec = {"kcal": grams*base[0]/100, "fat_g": grams*base[1]/100,
            "sodium_mg": grams*base[2]/100 + salt*393.0}
    # check grams inside band
    print(f"\nwestern {dish}: volume {tool['volume_ml']:.1f} ml grams {tool['grams'][0]:.1f}-{tool['grams'][1]:.1f} specific_grams {grams} in_band={tool['grams'][0] <= grams <= tool['grams'][1]}")
    cases.append(check(f"western {dish}", tool, spec))
for c in cases:
    for v in c.values(): total += 1; passed += 1 if v[3] else 0
print(f"\nTOTAL: {passed}/{total} individual range checks hit")
print(f"Cases all-hit: {sum(1 for c in cases if all(v[3] for v in c.values()))}/{len(cases)}")
print("Bowl volumes (volume only, not nutrition):")
for label, D, Hlo, Hhi, dlo, dhi in [("tiger 11/5.5", 11, 5.5, 5.5, 6.0, 8.0), ("leaf 20/5-6", 20, 5.0, 6.0, 9.0, 14.0), ("beaded 21/8", 21, 8.0, 8.0, 10.0, 15.0)]:
    print(f"  {label}: {bowl_volume_ml(D,Hlo,dlo):.0f}-{bowl_volume_ml(D,Hhi,dhi):.0f} ml")
print("  shallow plate 25cm: area 490.9 sq cm, use plate method (area x coverage x thickness), not bowl volume")
