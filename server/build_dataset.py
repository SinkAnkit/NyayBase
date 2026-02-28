"""
NyayBase - Massive Dataset Builder v2
Generates 500+ items across all legal categories using Groq LLM
Builds on existing dataset, adds much more depth
"""

import json, time, os
from groq import Groq

client = Groq(api_key="os.environ.get("GROQ_API_KEY", "")")

def ask(prompt, retries=2):
    for attempt in range(retries + 1):
        try:
            r = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an Indian legal data expert. Output ONLY valid JSON. No backticks, no markdown, no commentary."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.15, max_tokens=7500
            )
            raw = r.choices[0].message.content.strip()
            if raw.startswith("```"):
                lines = raw.split("\n")
                raw = "\n".join(lines[1:-1] if lines[-1].strip().startswith("```") else lines[1:])
            try:
                return json.loads(raw)
            except:
                s = raw.index("[" if "[" in raw[:5] else "{")
                e = raw.rindex("]" if raw.rstrip()[-1] == "]" else "}") + 1
                return json.loads(raw[s:e])
        except Exception as ex:
            print(f"    Retry {attempt+1}: {str(ex)[:80]}")
            if attempt < retries: time.sleep(4)
    return None

# Load existing dataset
existing = {}
path = os.path.join(os.path.dirname(__file__), "legal_dataset.json")
if os.path.exists(path):
    with open(path) as f:
        existing = json.load(f)
    print(f"Loaded existing dataset with {sum(len(v) if isinstance(v,list) else 0 for v in existing.values())} items")

dataset = {k: list(v) if isinstance(v, list) else v for k, v in existing.items()}

# ─── 1. More Constitution Articles (expand to 50+) ───
print("\n[1/12] More Constitution Articles (Part IV, IVA, structural)...")
r = ask("""Generate JSON array of 25 Indian Constitution articles NOT in this list: 14,15,16,19,20,21,21A,22,23,25,32,38,39,39A,41,42,43,44,51A,72,110,123,124,136,141,142,226,227,300A,311.
Each: {"article": "243", "title": "Panchayat system", "part": "Part IX", "category": "Panchayats", "text": "Summary of the article text", "usage": "How this article is used in legal arguments", "landmark_case": "Relevant SC case with citation"}
Cover: Art 1-13, 40, 45-50, 73, 74, 112, 143, 200, 213, 243, 243A-O, 244, 246, 254, 265, 267, 282, 312, 324, 352, 356, 360, 368, 370, 371.
Output ONLY the array.""")
if r:
    dataset.setdefault("constitution", []).extend(r)
    print(f"    +{len(r)} articles (total: {len(dataset['constitution'])})")
time.sleep(3)

# ─── 2. More BNS Sections ───
print("[2/12] More BNS/Criminal Sections...")
r = ask("""Generate JSON array of 20 more BNS 2023 sections NOT already covered (murder, hurt, theft, robbery, rape, kidnapping, cheating, forgery, defamation, dowry death, cruelty, intimidation, dacoity, extortion, CBT, mischief, trespass, rioting, conspiracy, abetment).
Each: {"bns": "section", "ipc": "old section", "offence": "name", "punishment": "details", "cognizable": true/false, "bailable": true/false, "category": "category", "definition": "brief definition", "conviction_rate": 0.XX}
Cover: attempt to suicide, bigamy, stalking, voyeurism, acid attack, adulteration, counterfeiting, public nuisance, illegal assembly, wrongful confinement, criminal force, obscene acts online, hate speech, organized crime, hit and run, causing death by negligence, unnatural offences, sedition-equivalent, war against state.
Output ONLY the array.""")
if r:
    dataset.setdefault("bns_sections", []).extend(r)
    print(f"    +{len(r)} sections (total: {len(dataset['bns_sections'])})")
time.sleep(3)

# ─── 3. More Civil Sections ───
print("[3/12] More Civil/Special Law Sections...")
r = ask("""Generate JSON array of 25 more important sections from Indian civil/special laws.
Each: {"act": "Act Name", "section": "number", "title": "section title", "summary": "what it provides", "usage": "how used in cases"}
Cover: Hindu Succession Act (s.4,6,8,14,15,30), Muslim Personal Law (dissolution, maintenance), Special Marriage Act (s.4,13,27), Domestic Violence Act (s.2,3,12,18,19,20,22,23), POCSO Act (s.3,4,5,6,7,11,29,30), SC/ST Atrocity Act (s.3,14), RERA Act (s.3,4,7,11,12,18,31), Arbitration Act (s.7,8,9,11,34,36), Insolvency Code (s.5,7,9,10), Companies Act key sections (s.241,242).
Output ONLY the array.""")
if r:
    dataset.setdefault("civil_sections", []).extend(r)
    print(f"    +{len(r)} sections (total: {len(dataset['civil_sections'])})")
time.sleep(3)

# ─── 4-9. More Landmark Cases (6 batches) ───
case_batches = [
    ("4/12", "Property & Real Estate", "15 real Indian Supreme Court property law cases. Cover: adverse possession, partition suits, specific performance, tenancy disputes, benami transactions, gift deeds, mortgage disputes, easement rights, joint family property, will disputes, title suits, injunction, land revenue."),
    ("5/12", "Criminal Law", "15 real Indian criminal law cases. Cover: bail, anticipatory bail, quashing of FIR, private defense, circumstantial evidence, dying declaration, confession, identification parade, forensic evidence, investigation procedure, witness protection, charge framing, acquittal, sentencing."),
    ("6/12", "Family & Matrimonial", "15 real Indian family law cases. Cover: mutual consent divorce, contested divorce, maintenance under S.125 CrPC, alimony, child custody, domestic violence, dowry harassment, restitution of conjugal rights, void/voidable marriages, NRI marriages, inter-faith marriages."),
    ("7/12", "Consumer, Labour & Service", "15 real Indian cases in consumer protection, labour law, and service matters. Cover: deficiency of service, medical negligence, insurance claims, unfair trade, wrongful termination, retrenchment, gratuity, provident fund, sexual harassment at workplace, equal pay, contract labour."),
    ("8/12", "Tax, Environment & IPR", "15 real Indian cases. Cover: income tax reassessment, GST disputes, transfer pricing, environmental clearance, pollution, mining, forest rights, trademark infringement, copyright fair use, patent validity, trade secrets."),
    ("9/12", "Constitutional & Writ", "15 landmark Indian constitutional cases post-2000. Cover: right to privacy, Aadhaar, Article 370, triple talaq, Section 377, NJAC, Sabarimala, demonetisation, electoral bonds, CAA challenges, EWS reservation, death penalty, internet shutdown, sedition."),
]

for label, topic, prompt in case_batches:
    print(f"[{label}] Landmark Cases: {topic}...")
    r = ask(f"""Generate JSON array of {prompt}
Each: {{"name": "full case name", "citation": "real citation", "year": YYYY, "court": "exact court", "type": "category", "facts": "2-3 sentence fact summary", "held": "what was decided", "principles": ["principle 1", "principle 2"], "impact": "significance", "result": "allowed/dismissed/partly allowed", "sections": ["relevant sections"]}}
REAL CASES ONLY with accurate citations. Output ONLY the array.""")
    if r:
        dataset.setdefault("landmark_cases_extra", []).extend(r)
        print(f"    +{len(r)} cases")
    time.sleep(3)

print(f"    Total extra cases: {len(dataset.get('landmark_cases_extra', []))}")

# ─── 10. Legal Procedures ───
print("[10/12] Legal Procedures & Processes...")
r = ask("""Generate JSON array of 15 common Indian legal procedures.
Each: {"name": "Filing a Civil Suit", "case_types": ["property", "contract"], "steps": [{"step": 1, "action": "Draft plaint", "details": "Must contain material facts, cause of action, relief claimed per Order VII CPC", "time": "1-2 weeks", "documents": ["Plaint", "Vakalatnama", "Court fee"]}], "typical_duration": "3-36 months", "court_fee": "Ad valorem", "limitations": "3 years from cause of action", "tips": ["Verify limitation before filing"]}
Cover: Civil suit, Criminal complaint (private), FIR filing, Bail application, Anticipatory bail, Cheque bounce complaint, Consumer complaint, RERA complaint, Motor accident claim, Divorce petition (mutual), Divorce petition (contested), Writ petition, RTI application, Appeal process, Arbitration initiation.
Output ONLY the array.""")
if r:
    dataset["legal_procedures"] = r
    print(f"    {len(r)} procedures")
time.sleep(3)

# ─── 11. Legal Maxims ───
print("[11/12] Legal Maxims & Principles...")
r = ask("""Generate JSON array of 30 important legal maxims used in Indian courts.
Each: {"maxim": "Audi alteram partem", "meaning": "Hear the other side", "language": "Latin", "application": "No one condemned unheard. Both parties must get fair hearing.", "example_case": "Maneka Gandhi v. Union of India (1978) 1 SCC 248", "used_in": ["Writ petitions", "Administrative law"]}
Cover maxims for natural justice, equity, criminal law, evidence, property, contract, statutory interpretation, constitutional law.
Output ONLY the array.""")
if r:
    dataset["legal_maxims"] = r
    print(f"    {len(r)} maxims")
time.sleep(3)

# ─── 12. Court-specific Data ───
print("[12/12] District Court Statistics...")
r = ask("""Generate JSON array of court statistics for 20 major Indian district courts/tribunals.
Each: {"name": "Saket District Court", "city": "New Delhi", "state": "Delhi", "type": "District Court", "total_judges": 45, "pending_cases": 85000, "annual_disposal": 35000, "avg_disposal_months": 18, "busiest_case_types": ["property", "criminal", "cheque_bounce"], "e_filing": true, "video_conferencing": true}
Cover major district courts: Tis Hazari, Saket, Patiala House, City Civil Mumbai, Esplanade Chennai, Bangalore City Civil, Hyderabad City Criminal, Kolkata, Pune, Ahmedabad, Lucknow, Jaipur, Chandigarh, and major tribunals: NCLAT, NCLT Mumbai, NCDRC, ITAT Delhi, NGT, CAT.
Output ONLY the array.""")
if r:
    dataset["district_courts"] = r
    print(f"    {len(r)} courts/tribunals")

# Save
with open(path, "w") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

total = sum(len(v) if isinstance(v, list) else 0 for v in dataset.values())
size = os.path.getsize(path)
print(f"\n=== DATASET COMPLETE ===")
print(f"Total items: {total}")
print(f"File size: {size/1024:.0f} KB")
for k, v in dataset.items():
    if isinstance(v, list):
        print(f"  {k}: {len(v)}")
