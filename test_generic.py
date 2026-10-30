"""Generic-mode interval check: mirrors the JS constants in index.html exactly.
This checks interval propagation only. Group bases are generic assumptions,
NOT per-dish validation. One example passing does NOT validate the group.
"""
OIL_KCAL = 8.84
NA = 393.0
GEN_BASE = {
    "egg": ((140, 170), (9, 12), (100, 150)),
    "tofu": ((60, 90), (3, 5), (5, 15)),
    "pork": ((200, 280), (14, 22), (60, 90)),
    "chicken": ((155, 175), (3, 4.5), (60, 90)),
    "beef": ((180, 250), (8, 15), (65, 95)),
    "fish_shrimp": ((110, 160), (2, 6), (80, 150)),
    "leafy": ((20, 40), (0.2, 1), (10, 30)),
    "root_stem": ((50, 90), (0.2, 1), (10, 30)),
    "mushroom": ((25, 45), (0.3, 1), (5, 15)),
    "mixed_veg": ((30, 60), (0.5, 2), (15, 40)),
}
GEN_OIL = {"low": (3, 7), "regular": (7, 14), "heavy": (14, 25)}
GEN_SALT = {"light": (0, 0.5), "regular": (0.5, 1.5), "heavy": (1.5, 3)}
GEN_SOY_ML = {"light": (0, 5), "regular": (5, 15), "heavy": (15, 30)}
GEN_BOWL = {"small": (150, 250), "medium": (200, 350), "large": (300, 500)}

def generic(group, oil_level, salt_level, bowl):
    (klo, khi), (flo, fhi), (slo, shi) = GEN_BASE[group]
    g = GEN_BOWL[bowl]; o = GEN_OIL[oil_level]
    sg = GEN_SALT[salt_level]; sm = GEN_SOY_ML[salt_level]
    return {
        "grams": g,
        "kcal": (g[0]*klo/100 + o[0]*OIL_KCAL, g[1]*khi/100 + o[1]*OIL_KCAL),
        "fat_g": (g[0]*flo/100 + o[0], g[1]*fhi/100 + o[1]),
        "sodium_mg": (g[0]*slo/100 + sg[0]*NA + sm[0]*36.0,
                      g[1]*shi/100 + sg[1]*NA + sm[1]*56.4),
    }

def fmt(r): return f"{r[0]:.1f}–{r[1]:.1f}"

if __name__ == "__main__":
    cases = [
        ("stir-fry pork, regular oil, regular salt, medium bowl",
         "pork", "regular", "regular", "medium"),
        ("steamed fish, low oil, light salt, small bowl",
         "fish_shrimp", "low", "light", "small"),
        ("cold-mixed vegetable, low oil, light salt, medium bowl",
         "mixed_veg", "low", "light", "medium"),
        # extra propagation guards: same group, heavy oil/salt, large bowl
        ("braised pork, heavy oil, heavy salt, large bowl",
         "pork", "heavy", "heavy", "large"),
        ("steamed leafy vegetable, low oil, light salt, small bowl",
         "leafy", "low", "light", "small"),
    ]
    for name, *args in cases:
        r = generic(*args)
        for k in ("kcal", "fat_g", "sodium_mg"):
            assert r[k][0] <= r[k][1], (name, k, r[k])
        # FDA 2300 generic reference, non-personal
        pct = (r["sodium_mg"][0]/2300*100, r["sodium_mg"][1]/2300*100)
        print(f"{name}: grams {fmt(r['grams'])} g; kcal {fmt(r['kcal'])}; "
              f"fat {fmt(r['fat_g'])} g; sodium {fmt(r['sodium_mg'])} mg "
              f"({pct[0]:.0f}–{pct[1]:.0f}% of FDA 2300 mg generic ref)")
    print("ALL GENERIC INTERVAL CHECKS PROPAGATE (lo <= hi for every range).")
