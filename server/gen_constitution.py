"""
Generate ALL Constitution articles 1-370 using 70B model with rate limit management
"""

import json, time, os
from groq import Groq

client = Groq(api_key="os.environ.get("GROQ_API_KEY", "")")

def ask(prompt, retries=3):
    for attempt in range(retries + 1):
        try:
            r = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Indian Constitution expert. Output ONLY valid JSON array. No markdown."},
                          {"role": "user", "content": prompt}],
                temperature=0.1, max_tokens=6000)
            raw = r.choices[0].message.content.strip()
            if raw.startswith("```"):
                raw = "\n".join(raw.split("\n")[1:])
                if raw.rstrip().endswith("```"): raw = raw.rstrip()[:-3]
            try: return json.loads(raw)
            except:
                s, e = raw.index("["), raw.rindex("]") + 1
                return json.loads(raw[s:e])
        except Exception as ex:
            wait = 15 * (attempt + 1)
            print(f"    Retry {attempt+1} (wait {wait}s): {str(ex)[:60]}")
            if attempt < retries: time.sleep(wait)
    return []

path = os.path.join(os.path.dirname(__file__), "legal_dataset.json")
with open(path) as f:
    dataset = json.load(f)

# Generate in focused batches
batches = [
    ("Part I: Union & Territory (1-4)", "1,2,3,4"),
    ("Part II: Citizenship (5-11)", "5,6,7,8,9,10,11"),
    ("Part III: Fundamental Rights A (12-18)", "12,13,14,15,16,17,18"),
    ("Part III: Fundamental Rights B (19-24)", "19,20,21,21A,22,23,24"),
    ("Part III: Religious/Cultural/Educational Rights (25-30)", "25,26,27,28,29,30"),
    ("Part III: Right to Constitutional Remedies (31A-35)", "31A,31B,31C,32,33,34,35"),
    ("Part IV: DPSP A (36-43B)", "36,37,38,39,39A,40,41,42,43,43A,43B"),
    ("Part IV: DPSP B (44-51)", "44,45,46,47,48,48A,49,50,51"),
    ("Part IVA: Fundamental Duties + President (51A-61)", "51A,52,53,54,55,56,57,58,59,60,61"),
    ("VP, PM, Council (62-75)", "62,63,64,65,66,67,68,69,70,71,72,73,74,75"),
    ("AG, Parliament structure (76-88)", "76,77,78,79,80,81,82,83,84,85,86,87,88"),
    ("Parliament officers & procedures (89-100)", "89,90,91,92,93,94,95,96,97,98,99,100"),
    ("Parliament disqualification & bills (101-111)", "101,102,103,104,105,106,107,108,109,110,111"),
    ("Budget & financial (112-122)", "112,113,114,115,116,117,118,119,120,121,122"),
    ("Supreme Court (123-135)", "123,124,124A,125,126,127,128,129,130,131,132,133,134,134A,135"),
    ("Supreme Court powers (136-147)", "136,137,138,139,139A,140,141,142,143,144,144A,145,146,147"),
    ("CAG & Governor (148-162)", "148,149,150,151,152,153,154,155,156,157,158,159,160,161,162"),
    ("State Executive (163-171)", "163,164,165,166,167,168,169,170,171"),
    ("State Legislature procedures (172-189)", "172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189"),
    ("State Legislature bills (190-212)", "190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212"),
    ("High Courts (213-226)", "213,214,215,216,217,218,219,220,221,222,223,224,224A,225,226"),
    ("High Courts & subordinate courts (227-237)", "227,228,228A,229,230,231,233,233A,234,235,236,237"),
    ("Union Territories (238-241)", "238,239,239A,239AA,239AB,239B,240,241"),
    ("Panchayats (243-243O)", "243,243A,243B,243C,243D,243E,243F,243G,243H,243I,243J,243K,243L,243M,243N,243O"),
    ("Municipalities (243P-243ZJ)", "243P,243Q,243R,243S,243T,243U,243V,243W,243X,243Y,243Z,243ZA,243ZB,243ZC,243ZD,243ZE,243ZF,243ZG"),
    ("Tribal & Legislative Relations (244-254)", "244,244A,245,246,246A,247,248,249,250,251,252,253,254"),
    ("Centre-State relations (255-263)", "255,256,257,258,258A,260,261,262,263"),
    ("Finance & Taxation (264-275)", "264,265,266,267,268,269,269A,270,271,272,273,274,275"),
    ("Finance continued (276-290A)", "276,277,278,279,279A,280,281,282,283,284,285,286,287,288,289,290,290A"),
    ("Property & Rights (291-300A)", "292,293,294,295,296,297,298,299,300,300A"),
    ("Trade & Services (301-311)", "301,302,303,304,305,306,307,308,309,310,311"),
    ("PSC & Public Services (312-323B)", "312,312A,315,316,317,318,319,320,321,322,323,323A,323B"),
    ("Elections (324-329A)", "324,325,326,327,328,329,329A"),
    ("Reservations SC/ST/OBC (330-342A)", "330,331,332,333,334,335,336,337,338,338A,338B,339,340,341,342,342A"),
    ("Official Language (343-351)", "343,344,345,346,347,348,349,350,350A,350B,351"),
    ("Emergency Provisions (352-360)", "352,353,354,355,356,357,358,359,360"),
    ("Miscellaneous & Amendment (361-370)", "361,361A,362,363,363A,365,366,367,368,369,370"),
    ("Special State provisions & Transitional (371-395)", "371,371A,371B,371C,371D,371E,371F,371G,371H,371I,371J,372,372A,373,374,375,392,393,394,395"),
]

all_articles = []

for i, (label, article_list) in enumerate(batches):
    print(f"[{i+1}/{len(batches)}] {label}...")
    prompt = f"""Generate JSON array for these Indian Constitution Articles: {article_list}
Each: {{"article":"number","title":"title","part":"Part","category":"category","text":"accurate 1-2 sentence summary of provision","usage":"legal usage context","landmark_case":"SC case citation if important, else empty"}}
Include ALL listed articles. Output ONLY JSON array."""
    result = ask(prompt)
    if result:
        all_articles.extend(result)
        print(f"    +{len(result)} (total: {len(all_articles)})")
    else:
        print(f"    FAILED")
    time.sleep(12)

# Deduplicate
seen = {}
for a in all_articles:
    seen[str(a.get("article", ""))] = a

dataset["constitution"] = list(seen.values())

with open(path, "w") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

total = sum(len(v) if isinstance(v, list) else 0 for v in dataset.values())
print(f"\n=== DONE: {len(seen)} unique articles, {total} total items, {os.path.getsize(path)/1024:.0f} KB ===")
