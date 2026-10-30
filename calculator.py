"""Deploy calculator: range-only, no photo recognition, no diagnosis.
Chinese logic is copied from tool-v2/calculator_v2.py (same constants, same
whole-pot intervals). Western logic is new for this deploy, using interval
bases (not single points) and plate volume x density band, both labelled
assumptions, not weighed values.

Conversions, explicit: 1 tbsp = 15 ml; 1 tsp = 5 ml; oil 0.92 g/ml;
salt 1 tsp = 5.7 g; salt sodium 393 mg/g; oil 8.84 kcal/g.
Soy cluster mg/ml: regular 56.4, reduced-salt 36.0, unknown 36.0-56.4, none 0.
Generic reference: FDA daily sodium 2300 mg, generic, non-personal,
non-medical. Base values are generic assumptions, not lab values for a
specific kitchen; tests check interval propagation only.
"""
import math

TBSP_ML = 15.0
TSP_ML = 5.0
OIL_G_PER_ML = 0.92
SALT_G_PER_TSP = 5.7
SALT_NA_MG_PER_G = 393.0
OIL_KCAL_PER_G = 8.84
SOY_MG_PER_ML = {"regular": (56.4, 56.4), "reduced_salt": (36.0, 36.0),
                  "unknown": (36.0, 56.4), "none": (0.0, 0.0)}

def tbsp_oil_g(t): return t * TBSP_ML * OIL_G_PER_ML
def tsp_salt_g(t): return t * SALT_G_PER_TSP
def bowl_volume_ml(D, H, d):
    R, r = D / 2.0, d / 2.0
    return math.pi * H / 3.0 * (R * R + R * r + r * r)

BASE = {"egg": (155.0, 11.0, 124.0), "tomato": (18.0, 0.2, 5.0),
        "pork_mince": (242.0, 18.0, 65.0), "silken_tofu": (55.0, 2.7, 7.0),
        "cucumber": (15.0, 0.1, 2.0)}

def _ing(lo, hi, k):
    a, b, c = BASE[k]
    return (lo*a/100, hi*a/100, lo*b/100, hi*b/100, lo*c/100, hi*c/100)

def _add(oil_lo, oil_hi, salt_lo, salt_hi, soy_lo, soy_hi, cluster):
    return (oil_lo*OIL_KCAL_PER_G, oil_hi*OIL_KCAL_PER_G, oil_lo, oil_hi,
            salt_lo*SALT_NA_MG_PER_G + soy_lo*SOY_MG_PER_ML[cluster][0],
            salt_hi*SALT_NA_MG_PER_G + soy_hi*SOY_MG_PER_ML[cluster][1])

def tomato_egg_whole(soy="none"):
    e = _ing(150, 240, "egg"); t = _ing(300, 720, "tomato")
    s = _add(tbsp_oil_g(1.5), tbsp_oil_g(3.0), tsp_salt_g(0.5), tsp_salt_g(1.0), 0, 0, soy)
    return {"kcal": (e[0]+t[0]+s[0], e[1]+t[1]+s[1]+48),
            "fat_g": (e[2]+t[2]+s[2], e[3]+t[3]+s[3]),
            "sodium_mg": (e[4]+t[4]+s[4], e[5]+t[5]+s[5])}

def mapo_tofu_whole(soy="unknown"):
    m = _ing(150, 250, "pork_mince"); f = _ing(280, 400, "silken_tofu")
    oil = tbsp_oil_g(2.0)
    s = _add(oil, oil, 0, tsp_salt_g(0.25), TBSP_ML, TBSP_ML, soy)
    return {"kcal": (m[0]+f[0]+s[0], m[1]+f[1]+s[1]+16),
            "fat_g": (m[2]+f[2]+s[2], m[3]+f[3]+s[3]),
            "sodium_mg": (m[4]+f[4]+s[4]+500, m[5]+f[5]+s[5]+1500)}

def cold_cucumber_whole(soy="unknown"):
    c = _ing(320, 480, "cucumber"); oil = tbsp_oil_g(1.0); salt = tsp_salt_g(0.5)
    s = _add(oil, oil, salt, salt, 0, 7.5, soy)
    return {"kcal": (c[0]+s[0], c[1]+s[1]+8),
            "fat_g": (c[2]+s[2], c[3]+s[3]),
            "sodium_mg": (c[4]+s[4], c[5]+s[5])}

CHINESE = {"tomato_egg": tomato_egg_whole, "mapo_tofu": mapo_tofu_whole,
           "cold_cucumber": cold_cucumber_whole}

def portion(w, share):
    return {k: (v[0]*share, v[1]*share) for k, v in w.items()}

# Western: base intervals per 100 g, unsalted (kcal, fat, sodium).
WEST_BASE = {
    "chicken": ((155.0, 175.0), (3.0, 4.5), (60.0, 90.0)),
    "salmon": ((190.0, 220.0), (11.0, 15.0), (50.0, 70.0)),
    "pasta_tomato": ((90.0, 130.0), (1.0, 2.0), (5.0, 150.0)),
    "brown_rice": ((110.0, 125.0), (0.8, 1.0), (1.0, 5.0)),
}
DENSITY = (0.8, 1.1)  # g/ml, assumption band, not weighed

def plate_volume_ml(D, coverage, thickness):
    return math.pi * (D/2.0)**2 * coverage * thickness

def western_range(dish, D, coverage, thickness, salt_g):
    vol = plate_volume_ml(D, coverage, thickness)
    glo, ghi = vol * DENSITY[0], vol * DENSITY[1]
    (klo, khi), (flo, fhi), (slo, shi) = WEST_BASE[dish]
    salt_na = salt_g * SALT_NA_MG_PER_G
    return {"volume_ml": vol, "grams": (glo, ghi),
            "kcal": (glo*klo/100, ghi*khi/100),
            "fat_g": (glo*flo/100, ghi*fhi/100),
            "sodium_mg": (glo*slo/100 + salt_na, ghi*shi/100 + salt_na)}

if __name__ == "__main__":
    for name, fn in [("tomato_egg", tomato_egg_whole), ("mapo_tofu", mapo_tofu_whole), ("cold_cucumber", cold_cucumber_whole)]:
        w = fn()
        print(name, w)
    print("western chicken 20cm/0.5/1.5cm/0g salt:", western_range("chicken", 20, 0.5, 1.5, 0))
    print("tiger bowl 11/5.5, d 4.95-7.7:", bowl_volume_ml(11, 5.5, 4.95), bowl_volume_ml(11, 5.5, 7.7))
