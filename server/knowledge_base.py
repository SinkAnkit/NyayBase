"""
NyayBase - Expanded Indian Legal Knowledge Base
10+ case types, all Indian states/UTs, comprehensive legal data
"""

CASE_TYPES = {
    "property_dispute": {
        "name": "Property Dispute",
        "description": "Civil disputes involving ownership, possession, boundaries, and title of immovable property",
        "relevant_acts": ["Transfer of Property Act, 1882", "Indian Registration Act, 1908", "Specific Relief Act, 1963", "Limitation Act, 1963"],
        "avg_win_rate": 0.42, "avg_duration_months": 48, "duration_range": [18, 120],
        "court_stats": {
            "District Court": {"avg_months": 36, "win_rate": 0.40},
            "High Court": {"avg_months": 24, "win_rate": 0.38},
            "Supreme Court": {"avg_months": 18, "win_rate": 0.35}
        },
        "common_winning_arguments": [
            {"argument": "Valid registered sale deed with consideration paid", "strength": 0.92, "section": "Section 54, Transfer of Property Act 1882", "description": "A registered sale deed is the strongest evidence of property transfer.", "success_rate": 0.88},
            {"argument": "Continuous and uninterrupted possession for 12+ years (Adverse Possession)", "strength": 0.85, "section": "Section 65, Limitation Act 1963", "description": "Continuous, open, hostile possession for over 12 years can establish ownership.", "success_rate": 0.72},
            {"argument": "Clear chain of title documents from original owner", "strength": 0.88, "section": "Section 110, Indian Evidence Act 1872", "description": "An unbroken chain of title deeds significantly strengthens the claim.", "success_rate": 0.80},
            {"argument": "Revenue records showing plaintiff as owner", "strength": 0.75, "section": "State Revenue Laws", "description": "Revenue records serve as strong corroborative evidence.", "success_rate": 0.65},
            {"argument": "Fraud or misrepresentation in defendant's acquisition", "strength": 0.70, "section": "Section 17, Indian Contract Act 1872", "description": "Transfer obtained through fraud can be declared void.", "success_rate": 0.60},
        ],
        "landmark_cases": [
            {"case_name": "Suraj Lamp & Industries v. State of Haryana", "citation": "(2012) 1 SCC 656", "court": "Supreme Court of India", "year": 2012, "outcome": "GPA sales declared invalid", "summary": "Only registered sale deeds effect valid transfer of immovable property.", "key_principle": "GPA sales are illegal; only registered sale deeds are valid"},
            {"case_name": "S.P. Chengalvaraya Naidu v. Jagannath", "citation": "(1994) 1 SCC 1", "court": "Supreme Court of India", "year": 1994, "outcome": "Decree set aside", "summary": "Fraud vitiates all proceedings.", "key_principle": "Decrees obtained by fraud are void"},
            {"case_name": "Ravinder Kaur Grewal v. Manjit Kaur", "citation": "(2019) 8 SCC 729", "court": "Supreme Court of India", "year": 2019, "outcome": "Reaffirmed Suraj Lamp", "summary": "Immovable property can only be transferred through registered instruments.", "key_principle": "Registered instruments are the only valid means of property transfer"},
            {"case_name": "Karnataka Board of Wakf v. Government of India", "citation": "(2004) 10 SCC 779", "court": "Supreme Court of India", "year": 2004, "outcome": "Title established", "summary": "Party in possession with revenue records has stronger presumption.", "key_principle": "Possession with revenue records creates strong presumption of ownership"},
            {"case_name": "Hemaji Waghaji Jat v. Bhikhabhai Khengarbhai", "citation": "(2009) 16 SCC 517", "court": "Supreme Court of India", "year": 2009, "outcome": "Adverse possession upheld", "summary": "12 years of continuous hostile possession confers title.", "key_principle": "Adverse possession is legally valid"},
        ],
        "mediation_factors": {"recommended": True, "success_rate": 0.65, "avg_settlement_time_months": 6, "reasoning": "Property disputes often involve family. Mediation preserves relationships and is faster."}
    },
    "cheque_bounce": {
        "name": "Cheque Bounce (NI Act Section 138)",
        "description": "Criminal complaint for dishonour of cheque for insufficiency of funds",
        "relevant_acts": ["Negotiable Instruments Act, 1881 (Sections 138-142)", "Code of Criminal Procedure, 1973", "Indian Evidence Act, 1872"],
        "avg_win_rate": 0.68, "avg_duration_months": 18, "duration_range": [6, 36],
        "court_stats": {
            "Magistrate Court": {"avg_months": 12, "win_rate": 0.70},
            "Sessions Court (Appeal)": {"avg_months": 8, "win_rate": 0.55},
            "High Court (Revision)": {"avg_months": 12, "win_rate": 0.45}
        },
        "common_winning_arguments": [
            {"argument": "Legally enforceable debt with demand notice served within 30 days", "strength": 0.95, "section": "Section 138, NI Act", "description": "The complainant must prove cheque was issued for debt, dishonoured, and demand notice sent within 30 days.", "success_rate": 0.85},
            {"argument": "Statutory presumption under Section 139 shifts burden to accused", "strength": 0.90, "section": "Section 139, NI Act", "description": "Court PRESUMES cheque was issued for consideration. Burden is on accused.", "success_rate": 0.82},
            {"argument": "Accused failed to reply to statutory demand notice within 15 days", "strength": 0.88, "section": "Section 138(c), NI Act", "description": "Non-response to demand notice strengthens complainant's case.", "success_rate": 0.80},
            {"argument": "Cheque signature matches accused's specimen signature", "strength": 0.85, "section": "Section 118, NI Act", "description": "Every negotiable instrument is presumed to be made for consideration.", "success_rate": 0.78},
            {"argument": "Complaint filed within statutory limitation period", "strength": 0.80, "section": "Section 142, NI Act", "description": "Complaint must be filed within 30 days of cause of action.", "success_rate": 0.90},
        ],
        "landmark_cases": [
            {"case_name": "Bir Singh v. Mukesh Kumar", "citation": "(2019) 4 SCC 197", "court": "Supreme Court of India", "year": 2019, "outcome": "Jurisdiction clarified", "summary": "Complaint can be filed where payee's bank is located.", "key_principle": "Post-amendment: complaint at payee bank's location"},
            {"case_name": "Meters and Instruments v. Kanchan Mehta", "citation": "(2018) 1 SCC 560", "court": "Supreme Court of India", "year": 2018, "outcome": "Summary trial recommended", "summary": "Cheque bounce cases should use summary trial procedure.", "key_principle": "Summary trials and technology should expedite S.138 cases"},
            {"case_name": "Kusum Ingots v. Pennar Peterson", "citation": "(2000) 2 SCC 745", "court": "Supreme Court of India", "year": 2000, "outcome": "Notice requirements clarified", "summary": "Demand notice is mandatory prerequisite.", "key_principle": "Demand notice must comply strictly with S.138"},
            {"case_name": "Dashrath Rupsingh Rathod v. State of Maharashtra", "citation": "(2014) 9 SCC 129", "court": "Supreme Court of India", "year": 2014, "outcome": "Jurisdiction ruling", "summary": "S.138 complaints filed where cheque dishonoured.", "key_principle": "Jurisdiction at drawee bank location"},
            {"case_name": "Expeditious Trial of S.138 Cases (Suo Motu)", "citation": "(2021) SCC OnLine SC 325", "court": "Supreme Court of India", "year": 2021, "outcome": "Fast-tracking directions", "summary": "Comprehensive directions for fast-tracking cheque bounce cases.", "key_principle": "Technology-driven fast-tracking mandated"},
        ],
        "mediation_factors": {"recommended": True, "success_rate": 0.72, "avg_settlement_time_months": 3, "reasoning": "Fundamentally about recovering money. Lok Adalat is highly effective."}
    },
    "motor_accident": {
        "name": "Motor Accident Claims",
        "description": "Compensation claims for injuries or death from motor vehicle accidents",
        "relevant_acts": ["Motor Vehicles Act, 1988", "Motor Vehicles (Amendment) Act, 2019", "Indian Fatal Accidents Act, 1855"],
        "avg_win_rate": 0.78, "avg_duration_months": 24, "duration_range": [8, 48],
        "court_stats": {
            "MACT Tribunal": {"avg_months": 18, "win_rate": 0.80},
            "High Court (Appeal)": {"avg_months": 12, "win_rate": 0.65},
            "Supreme Court": {"avg_months": 18, "win_rate": 0.55}
        },
        "common_winning_arguments": [
            {"argument": "Structured multiplier method (Sarla Verma formula)", "strength": 0.95, "section": "Section 166, MV Act 1988", "description": "Multiplier table uses victim's age and income for just compensation.", "success_rate": 0.90},
            {"argument": "No-fault liability compensation", "strength": 0.88, "section": "Section 140, MV Act 1988", "description": "Fixed compensation without proving negligence.", "success_rate": 0.95},
            {"argument": "FIR and charge sheet establish negligent driving", "strength": 0.85, "section": "Section 281, BNS 2023", "description": "Police records strongly support compensation claim.", "success_rate": 0.82},
            {"argument": "Future loss of income and amenities of life", "strength": 0.82, "section": "Section 166, MV Act", "description": "Courts add compensation for future earning loss and quality of life.", "success_rate": 0.78},
            {"argument": "Insurance company liable regardless of policy conditions", "strength": 0.80, "section": "Section 149, MV Act 1988", "description": "Insurer must pay victim first, then recover from insured.", "success_rate": 0.85},
        ],
        "landmark_cases": [
            {"case_name": "Sarla Verma v. Delhi Transport Corp.", "citation": "(2009) 6 SCC 121", "court": "Supreme Court of India", "year": 2009, "outcome": "Multiplier table established", "summary": "Definitive multiplier table for calculating compensation.", "key_principle": "Standardized multiplier for fair compensation"},
            {"case_name": "National Insurance v. Pranay Sethi", "citation": "(2017) 16 SCC 680", "court": "Supreme Court of India", "year": 2017, "outcome": "Enhanced framework", "summary": "Standardized conventional damages and 40% future prospects addition.", "key_principle": "40% future prospects addition upheld"},
            {"case_name": "Reshma Kumari v. Madan Mohan", "citation": "(2013) 9 SCC 65", "court": "Supreme Court of India", "year": 2013, "outcome": "Sarla Verma affirmed", "summary": "Multiplier based on deceased's age, not claimant's.", "key_principle": "Multiplier based on deceased's age"},
            {"case_name": "Nagappa v. Gurudayal Singh", "citation": "(2003) 2 SCC 274", "court": "Supreme Court of India", "year": 2003, "outcome": "Just compensation upheld", "summary": "Tribunal has discretion for just and fair compensation.", "key_principle": "No restriction on Tribunal's power"},
            {"case_name": "Jai Prakash v. National Insurance Co.", "citation": "(2010) 2 SCC 607", "court": "Supreme Court of India", "year": 2010, "outcome": "Interim compensation mandated", "summary": "MACT should grant interim compensation quickly.", "key_principle": "Interim compensation during pendency"},
        ],
        "mediation_factors": {"recommended": False, "success_rate": 0.35, "avg_settlement_time_months": 4, "reasoning": "Tribunal awards are generally higher. Mediation not recommended unless urgent funds needed."}
    },
    "divorce": {
        "name": "Divorce & Matrimonial Disputes",
        "description": "Divorce petitions, maintenance claims, custody battles, domestic violence complaints",
        "relevant_acts": ["Hindu Marriage Act, 1955", "Special Marriage Act, 1954", "Protection of Women from Domestic Violence Act, 2005", "Hindu Adoption and Maintenance Act, 1956"],
        "avg_win_rate": 0.55, "avg_duration_months": 30, "duration_range": [6, 60],
        "court_stats": {
            "Family Court": {"avg_months": 24, "win_rate": 0.55},
            "High Court (Appeal)": {"avg_months": 12, "win_rate": 0.45},
            "Supreme Court": {"avg_months": 18, "win_rate": 0.35}
        },
        "common_winning_arguments": [
            {"argument": "Cruelty (mental or physical) as ground for divorce", "strength": 0.88, "section": "Section 13(1)(ia), Hindu Marriage Act", "description": "Continuous cruelty is the most common and successful ground for divorce.", "success_rate": 0.75},
            {"argument": "Mutual consent with agreed terms", "strength": 0.98, "section": "Section 13B, Hindu Marriage Act", "description": "Mutual consent divorce is fastest and has near-100% success rate.", "success_rate": 0.99},
            {"argument": "Desertion for continuous period of 2+ years", "strength": 0.80, "section": "Section 13(1)(ib), Hindu Marriage Act", "description": "Abandonment without reasonable cause for 2 years.", "success_rate": 0.70},
            {"argument": "Right to maintenance based on earning disparity", "strength": 0.85, "section": "Section 125, CrPC / Section 144, BNSS", "description": "Wife entitled to maintenance proportional to husband's income.", "success_rate": 0.80},
            {"argument": "Child's welfare as paramount in custody decisions", "strength": 0.90, "section": "Guardians and Wards Act, 1890", "description": "Best interest of child is the overriding consideration.", "success_rate": 0.85},
        ],
        "landmark_cases": [
            {"case_name": "Shilpa Sailesh v. Varun Sreenivasan", "citation": "(2023) SCC OnLine SC 544", "court": "Supreme Court of India", "year": 2023, "outcome": "SC can grant divorce directly", "summary": "Supreme Court can exercise Article 142 to grant divorce even without mutual consent.", "key_principle": "SC can dissolve irretrievably broken marriages"},
            {"case_name": "K. Srinivas Rao v. D.A. Deepa", "citation": "(2013) 5 SCC 226", "court": "Supreme Court of India", "year": 2013, "outcome": "Mental cruelty defined", "summary": "Mental cruelty need not be physical; sustained anguish qualifies.", "key_principle": "Mental cruelty is a valid ground"},
            {"case_name": "Roxann Sharma v. Arun Sharma", "citation": "(2015) 8 SCC 318", "court": "Supreme Court of India", "year": 2015, "outcome": "Mother's right for young children", "summary": "Mother normally gets custody of children below 5 years.", "key_principle": "Tender years doctrine favors mother"},
            {"case_name": "Rajnesh v. Neha", "citation": "(2021) 2 SCC 324", "court": "Supreme Court of India", "year": 2021, "outcome": "Maintenance guidelines", "summary": "Comprehensive guidelines for determining maintenance amounts.", "key_principle": "Standardized maintenance calculation criteria"},
            {"case_name": "Naveen Kohli v. Neelu Kohli", "citation": "(2006) 4 SCC 558", "court": "Supreme Court of India", "year": 2006, "outcome": "Irretrievable breakdown", "summary": "Marriage broken beyond repair should be dissolved.", "key_principle": "Irretrievable breakdown as ground for divorce"},
        ],
        "mediation_factors": {"recommended": True, "success_rate": 0.45, "avg_settlement_time_months": 4, "reasoning": "Mediation can resolve maintenance and custody amicably. Courts mandate mediation attempt first."}
    },
    "consumer_complaint": {
        "name": "Consumer Complaints",
        "description": "Deficiency in service, defective products, unfair trade practices, insurance claim denials",
        "relevant_acts": ["Consumer Protection Act, 2019", "Insurance Regulatory and Development Authority Act, 1999"],
        "avg_win_rate": 0.62, "avg_duration_months": 12, "duration_range": [3, 24],
        "court_stats": {
            "District Consumer Forum": {"avg_months": 8, "win_rate": 0.65},
            "State Consumer Commission": {"avg_months": 10, "win_rate": 0.55},
            "National Consumer Commission": {"avg_months": 14, "win_rate": 0.45}
        },
        "common_winning_arguments": [
            {"argument": "Deficiency in service with documentary proof", "strength": 0.90, "section": "Section 2(11), Consumer Protection Act 2019", "description": "Any fault or imperfection in quality or manner of service performance.", "success_rate": 0.82},
            {"argument": "Unfair trade practice or misleading advertisement", "strength": 0.85, "section": "Section 2(47), Consumer Protection Act 2019", "description": "False claims about goods or services quality, price, or benefits.", "success_rate": 0.75},
            {"argument": "Medical negligence with expert opinion", "strength": 0.78, "section": "Section 2(11), Consumer Protection Act 2019", "description": "Doctors and hospitals bound by standard of reasonable care.", "success_rate": 0.65},
            {"argument": "Insurance claim wrongfully repudiated", "strength": 0.82, "section": "IRDA Regulations", "description": "Insurance companies cannot deny claims without valid grounds.", "success_rate": 0.78},
            {"argument": "Product liability for manufacturing defect", "strength": 0.80, "section": "Section 84-87, Consumer Protection Act 2019", "description": "Manufacturer liable for harm caused by defective products.", "success_rate": 0.72},
        ],
        "landmark_cases": [
            {"case_name": "Indian Medical Association v. V.P. Shantha", "citation": "(1995) 6 SCC 651", "court": "Supreme Court of India", "year": 1995, "outcome": "Medical services are consumer services", "summary": "Medical profession falls within ambit of Consumer Protection Act.", "key_principle": "Doctors can be sued for consumer negligence"},
            {"case_name": "Lucknow Development Auth. v. M.K. Gupta", "citation": "(1994) 1 SCC 243", "court": "Supreme Court of India", "year": 1994, "outcome": "Housing deficiency", "summary": "Government bodies providing services are covered under CPA.", "key_principle": "Public authorities liable as service providers"},
            {"case_name": "Ambrish Kumar Shukla v. Ferrero India", "citation": "2023 NCDRC Order", "court": "National Consumer Commission", "year": 2023, "outcome": "Misleading advertising", "summary": "Misleading health claims on food packaging constitute unfair trade practice.", "key_principle": "False advertising is actionable under CPA"},
            {"case_name": "Spring Meadows Hospital v. Harjol Ahluwalia", "citation": "(1998) 4 SCC 39", "court": "Supreme Court of India", "year": 1998, "outcome": "Hospital vicariously liable", "summary": "Hospital liable for negligence of its doctors/staff.", "key_principle": "Vicarious liability of hospitals"},
            {"case_name": "Branch Manager, Bajaj Allianz v. Dalbir Kaur", "citation": "(2020) SC", "court": "Supreme Court of India", "year": 2020, "outcome": "Insurance claim upheld", "summary": "Technicalities cannot be used to deny genuine insurance claims.", "key_principle": "Insurance claims should not be rejected on technicalities"},
        ],
        "mediation_factors": {"recommended": True, "success_rate": 0.55, "avg_settlement_time_months": 2, "reasoning": "Companies often prefer settlement to avoid negative publicity and lengthy litigation."}
    },
    "criminal_offense": {
        "name": "Criminal Offences (IPC/BNS)",
        "description": "Theft, assault, fraud, forgery, criminal intimidation, cybercrime, dowry harassment",
        "relevant_acts": ["Bharatiya Nyaya Sanhita, 2023 (BNS)", "Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)", "Bharatiya Sakshya Adhiniyam, 2023 (BSA)", "Information Technology Act, 2000"],
        "avg_win_rate": 0.45, "avg_duration_months": 36, "duration_range": [12, 84],
        "court_stats": {
            "Magistrate Court": {"avg_months": 18, "win_rate": 0.50},
            "Sessions Court": {"avg_months": 24, "win_rate": 0.45},
            "High Court (Appeal)": {"avg_months": 18, "win_rate": 0.35},
            "Supreme Court": {"avg_months": 18, "win_rate": 0.30}
        },
        "common_winning_arguments": [
            {"argument": "Prosecution proved guilt beyond reasonable doubt", "strength": 0.90, "section": "Section 4, BSA 2023", "description": "Criminal conviction requires proof beyond reasonable doubt.", "success_rate": 0.55},
            {"argument": "FIR filed promptly with consistent statements", "strength": 0.82, "section": "Section 173, BNSS 2023", "description": "Prompt FIR with no contradictions strengthens prosecution case.", "success_rate": 0.70},
            {"argument": "Strong forensic and electronic evidence", "strength": 0.88, "section": "Section 63, BSA 2023", "description": "Digital evidence including CCTV, phone records, electronic documents.", "success_rate": 0.75},
            {"argument": "Bail denied due to flight risk or evidence tampering", "strength": 0.75, "section": "Section 480, BNSS 2023", "description": "Court may deny bail if accused likely to flee or influence witnesses.", "success_rate": 0.60},
            {"argument": "Quashing of FIR due to no prima facie case", "strength": 0.70, "section": "Section 528, BNSS 2023", "description": "High Court can quash FIR if allegations don't constitute an offence.", "success_rate": 0.50},
        ],
        "landmark_cases": [
            {"case_name": "Arnesh Kumar v. State of Bihar", "citation": "(2014) 8 SCC 273", "court": "Supreme Court of India", "year": 2014, "outcome": "Arrest guidelines", "summary": "Police must follow guidelines before arresting in cases with punishment < 7 years.", "key_principle": "No automatic arrest for bailable offences"},
            {"case_name": "Lalita Kumari v. State of UP", "citation": "(2014) 2 SCC 1", "court": "Supreme Court of India", "year": 2014, "outcome": "Mandatory FIR registration", "summary": "Police must register FIR for cognizable offences without preliminary inquiry.", "key_principle": "FIR registration is mandatory for cognizable offences"},
            {"case_name": "Satender Kumar Antil v. CBI", "citation": "(2022) 10 SCC 51", "court": "Supreme Court of India", "year": 2022, "outcome": "Bail reform", "summary": "Bail is the rule, jail is the exception. Guidelines for bail in various categories.", "key_principle": "Default rule of bail unless compelling reasons"},
            {"case_name": "Shreya Singhal v. Union of India", "citation": "(2015) 5 SCC 1", "court": "Supreme Court of India", "year": 2015, "outcome": "Section 66A struck down", "summary": "Section 66A of IT Act found unconstitutional for being vague.", "key_principle": "Online speech restrictions must be precise and narrow"},
            {"case_name": "K.A. Abbas v. Union of India", "citation": "AIR 1971 SC 481", "court": "Supreme Court of India", "year": 1971, "outcome": "Free speech", "summary": "Pre-censorship standards must not be vague or arbitrary.", "key_principle": "Restrictions on speech must be narrowly tailored"},
        ],
        "mediation_factors": {"recommended": False, "success_rate": 0.25, "avg_settlement_time_months": 3, "reasoning": "Criminal cases generally cannot be mediated except compoundable offences under Section 359 BNSS."}
    },
    "labor_employment": {
        "name": "Labour & Employment Disputes",
        "description": "Wrongful termination, unpaid wages, workplace harassment, PF/ESI disputes, industrial disputes",
        "relevant_acts": ["Industrial Disputes Act, 1947", "Payment of Wages Act, 1936", "Employees Provident Fund Act, 1952", "Sexual Harassment of Women at Workplace Act, 2013", "Code on Wages, 2019"],
        "avg_win_rate": 0.58, "avg_duration_months": 24, "duration_range": [6, 48],
        "court_stats": {
            "Labour Court": {"avg_months": 18, "win_rate": 0.60},
            "Industrial Tribunal": {"avg_months": 20, "win_rate": 0.55},
            "High Court": {"avg_months": 12, "win_rate": 0.45}
        },
        "common_winning_arguments": [
            {"argument": "Retrenchment without following Section 25F procedure", "strength": 0.90, "section": "Section 25F, Industrial Disputes Act", "description": "Employer must give 1 month notice and pay retrenchment compensation.", "success_rate": 0.85},
            {"argument": "Termination without domestic inquiry is illegal", "strength": 0.88, "section": "Standing Orders / Employment Contract", "description": "Employee must be given opportunity to be heard before termination.", "success_rate": 0.80},
            {"argument": "Non-payment of statutory dues (PF/ESI/Gratuity)", "strength": 0.92, "section": "EPF Act 1952, ESI Act 1948", "description": "Employer statutory obligations for PF and ESI contributions.", "success_rate": 0.88},
            {"argument": "Workplace sexual harassment complaint under POSH Act", "strength": 0.80, "section": "Sexual Harassment Act, 2013", "description": "Employer must constitute ICC and investigate complaints.", "success_rate": 0.70},
            {"argument": "Equal pay for equal work", "strength": 0.78, "section": "Code on Wages, 2019", "description": "No discrimination in wages for same or similar work.", "success_rate": 0.65},
        ],
        "landmark_cases": [
            {"case_name": "Vishaka v. State of Rajasthan", "citation": "(1997) 6 SCC 241", "court": "Supreme Court of India", "year": 1997, "outcome": "Sexual harassment guidelines", "summary": "Established mandatory guidelines for preventing workplace sexual harassment.", "key_principle": "Employers must prevent and address sexual harassment"},
            {"case_name": "Workmen of Dimakuchi Tea Estate v. Management", "citation": "(1958) SCR 1156", "court": "Supreme Court of India", "year": 1958, "outcome": "Retrenchment norms", "summary": "Last in, first out principle for retrenchment.", "key_principle": "LIFO principle in retrenchment"},
            {"case_name": "Delhi Transport Corp. v. DTC Mazdoor Congress", "citation": "(1991) Supp 1 SCC 600", "court": "Supreme Court of India", "year": 1991, "outcome": "Right to livelihood", "summary": "Right to livelihood is part of Article 21 right to life.", "key_principle": "Termination must follow due process as right to livelihood"},
            {"case_name": "Hari Nandan Prasad v. Employer", "citation": "(1965) 1 LLJ 728", "court": "Supreme Court of India", "year": 1965, "outcome": "Natural justice", "summary": "Principles of natural justice must be followed in disciplinary action.", "key_principle": "Audi alteram partem in employment termination"},
            {"case_name": "SAIL v. National Union Waterfront Workers", "citation": "(2001) 7 SCC 1", "court": "Supreme Court of India", "year": 2001, "outcome": "Contract labour regularization", "summary": "Abolition of contract labour does not automatically regularize workers.", "key_principle": "Contract workers not automatically regularized"},
        ],
        "mediation_factors": {"recommended": True, "success_rate": 0.60, "avg_settlement_time_months": 3, "reasoning": "Conciliation officers are mandated before industrial disputes go to court."}
    },
    "cyber_crime": {
        "name": "Cyber Crime & IT Disputes",
        "description": "Online fraud, hacking, identity theft, data breach, social media crimes, defamation online",
        "relevant_acts": ["Information Technology Act, 2000", "IT (Amendment) Act, 2008", "Bharatiya Nyaya Sanhita, 2023", "Personal Data Protection Act, 2023"],
        "avg_win_rate": 0.40, "avg_duration_months": 24, "duration_range": [8, 48],
        "court_stats": {
            "Cyber Crime Cell / Magistrate": {"avg_months": 12, "win_rate": 0.45},
            "Sessions Court": {"avg_months": 18, "win_rate": 0.40},
            "High Court": {"avg_months": 15, "win_rate": 0.35}
        },
        "common_winning_arguments": [
            {"argument": "Electronic evidence preserved with proper certificate", "strength": 0.92, "section": "Section 63, BSA 2023", "description": "Electronic evidence must be accompanied by certificate for admissibility.", "success_rate": 0.80},
            {"argument": "Unauthorized access / hacking proved through digital forensics", "strength": 0.85, "section": "Section 43, IT Act 2000", "description": "Accessing computer without permission attracts civil and criminal liability.", "success_rate": 0.70},
            {"argument": "Identity theft with financial loss documented", "strength": 0.80, "section": "Section 66C, IT Act 2000", "description": "Using another person's electronic signature or identity.", "success_rate": 0.65},
            {"argument": "Online defamation with traceable IP/account", "strength": 0.75, "section": "Section 356, BNS 2023", "description": "Defamatory content published online with identifiable source.", "success_rate": 0.60},
            {"argument": "Data breach by company due to negligence", "strength": 0.78, "section": "Section 43A, IT Act / DPDPA 2023", "description": "Companies must implement reasonable security practices for data.", "success_rate": 0.65},
        ],
        "landmark_cases": [
            {"case_name": "Shreya Singhal v. Union of India", "citation": "(2015) 5 SCC 1", "court": "Supreme Court of India", "year": 2015, "outcome": "Section 66A struck down", "summary": "Vague provisions criminalizing online speech are unconstitutional.", "key_principle": "Free speech online cannot be vaguely restricted"},
            {"case_name": "Shafhi Mohammad v. State of HP", "citation": "(2018) 2 SCC 801", "court": "Supreme Court of India", "year": 2018, "outcome": "Electronic evidence standards", "summary": "S.65B certificate requirement for electronic evidence clarified.", "key_principle": "Electronic evidence requires proper certification"},
            {"case_name": "Arjun Panditrao Khotkar v. Kailash Kushanrao", "citation": "(2020) 7 SCC 1", "court": "Supreme Court of India", "year": 2020, "outcome": "S.65B certificate mandatory", "summary": "Certificate under Section 65B is mandatory for electronic evidence.", "key_principle": "No electronic evidence without proper S.65B certificate"},
            {"case_name": "K.S. Puttaswamy v. Union of India", "citation": "(2017) 10 SCC 1", "court": "Supreme Court of India", "year": 2017, "outcome": "Right to privacy", "summary": "Right to privacy is a fundamental right under Article 21.", "key_principle": "Privacy is a fundamental right"},
            {"case_name": "Avnish Bajaj v. State (Bazee.com)", "citation": "(2008) 150 DLT 769", "court": "Delhi High Court", "year": 2008, "outcome": "Intermediary liability", "summary": "Platform intermediaries not automatically liable for user content.", "key_principle": "Intermediary safe harbour depends on knowledge"},
        ],
        "mediation_factors": {"recommended": False, "success_rate": 0.20, "avg_settlement_time_months": 3, "reasoning": "Cyber crimes are criminal in nature. Financial fraud cases may be settled but hacking/identity theft generally go to trial."}
    },
    "tax_dispute": {
        "name": "Tax Disputes (Income Tax / GST)",
        "description": "Income tax assessments, GST disputes, tax evasion proceedings, penalty appeals",
        "relevant_acts": ["Income Tax Act, 1961", "Central Goods and Services Tax Act, 2017", "Taxation Laws (Amendment) Act, 2021"],
        "avg_win_rate": 0.52, "avg_duration_months": 30, "duration_range": [12, 60],
        "court_stats": {
            "Commissioner (Appeals)": {"avg_months": 12, "win_rate": 0.50},
            "ITAT / Appellate Authority": {"avg_months": 18, "win_rate": 0.55},
            "High Court": {"avg_months": 18, "win_rate": 0.48},
            "Supreme Court": {"avg_months": 24, "win_rate": 0.40}
        },
        "common_winning_arguments": [
            {"argument": "Assessment order passed without proper opportunity of hearing", "strength": 0.88, "section": "Section 144, Income Tax Act", "description": "Taxpayer must be given adequate opportunity before assessment.", "success_rate": 0.80},
            {"argument": "Addition based on suspicion without corroborative evidence", "strength": 0.85, "section": "Section 69, Income Tax Act", "description": "Income additions must be supported by concrete evidence, not mere suspicion.", "success_rate": 0.75},
            {"argument": "GST Input Tax Credit wrongfully denied", "strength": 0.82, "section": "Section 16, CGST Act 2017", "description": "ITC cannot be denied on mere technical grounds if conditions substantially met.", "success_rate": 0.72},
            {"argument": "Reassessment notice beyond limitation period", "strength": 0.90, "section": "Section 149, Income Tax Act", "description": "Reassessment notices must comply with strict time limits.", "success_rate": 0.85},
            {"argument": "Penalty deleted for reasonable cause and bona fide belief", "strength": 0.78, "section": "Section 273B, Income Tax Act", "description": "Penalty not imposable if reasonable cause shown for non-compliance.", "success_rate": 0.70},
        ],
        "landmark_cases": [
            {"case_name": "Ashish Agarwal v. Union of India", "citation": "(2022) 9 SCC 176", "court": "Supreme Court of India", "year": 2022, "outcome": "Reassessment notices", "summary": "Old reassessment notices under S.148 converted to new regime.", "key_principle": "Reassessment must follow new procedure post-2021 amendment"},
            {"case_name": "Principal CIT v. NRA Iron & Steel", "citation": "(2019) SCC", "court": "Supreme Court of India", "year": 2019, "outcome": "Bogus purchases", "summary": "Assessee must prove genuineness of purchase transactions.", "key_principle": "Onus on assessee to prove transaction genuineness"},
            {"case_name": "Vodafone International v. Union of India", "citation": "(2012) 6 SCC 613", "court": "Supreme Court of India", "year": 2012, "outcome": "Retrospective taxation struck", "summary": "India cannot tax indirect transfers retrospectively.", "key_principle": "Tax laws should not operate retrospectively to create liability"},
            {"case_name": "CIT v. Reliance Petroproducts", "citation": "(2010) 322 ITR 158", "court": "Supreme Court of India", "year": 2010, "outcome": "No penalty for claim", "summary": "Making a legal claim that is disallowed does not attract penalty.", "key_principle": "No penalty for bona fide claims subsequently disallowed"},
            {"case_name": "Safari Retreats v. CCGST", "citation": "(2019) SCC", "court": "Supreme Court of India", "year": 2019, "outcome": "ITC for construction", "summary": "Input tax credit available for construction of commercial immovable property for letting.", "key_principle": "ITC available when construction is for business purposes"},
        ],
        "mediation_factors": {"recommended": True, "success_rate": 0.50, "avg_settlement_time_months": 6, "reasoning": "Vivad se Vishwas scheme and advance dispute resolution reduce litigation burden."}
    },
    "ipr_dispute": {
        "name": "Intellectual Property Disputes",
        "description": "Trademark infringement, copyright violations, patent disputes, trade secret misappropriation",
        "relevant_acts": ["Trade Marks Act, 1999", "Copyright Act, 1957", "Patents Act, 1970", "Designs Act, 2000", "IT Act, 2000"],
        "avg_win_rate": 0.55, "avg_duration_months": 24, "duration_range": [6, 48],
        "court_stats": {
            "Commercial Court": {"avg_months": 18, "win_rate": 0.55},
            "High Court (IP Division)": {"avg_months": 15, "win_rate": 0.50},
            "Supreme Court": {"avg_months": 18, "win_rate": 0.40}
        },
        "common_winning_arguments": [
            {"argument": "Prior registered trademark with continuous use", "strength": 0.92, "section": "Section 28, Trade Marks Act", "description": "Registered trademark holder has exclusive right to use the mark.", "success_rate": 0.85},
            {"argument": "Deceptive similarity causing consumer confusion", "strength": 0.85, "section": "Section 29, Trade Marks Act", "description": "Infringement if mark is deceptively similar causing public confusion.", "success_rate": 0.78},
            {"argument": "Copyright subsists in original literary/artistic work", "strength": 0.88, "section": "Section 13, Copyright Act", "description": "Original work receives automatic copyright protection.", "success_rate": 0.80},
            {"argument": "Patent specification sufficiently disclosed invention", "strength": 0.80, "section": "Section 10, Patents Act", "description": "Complete specification must fully describe the invention.", "success_rate": 0.70},
            {"argument": "Interim injunction to prevent irreparable harm", "strength": 0.85, "section": "Order 39, CPC", "description": "Courts grant interim injunctions to prevent ongoing IP infringement.", "success_rate": 0.75},
        ],
        "landmark_cases": [
            {"case_name": "Cadila Healthcare v. Cadila Pharmaceuticals", "citation": "(2001) 5 SCC 73", "court": "Supreme Court of India", "year": 2001, "outcome": "Deceptive similarity test", "summary": "Laid down parameters for testing deceptive similarity in pharma.", "key_principle": "Stricter similarity test for pharmaceutical trademarks"},
            {"case_name": "Yahoo Inc v. Akash Arora", "citation": "(1999) IIAD Delhi 229", "court": "Delhi High Court", "year": 1999, "outcome": "Domain name infringement", "summary": "Domain names are entitled to same protection as trademarks.", "key_principle": "Domain names protected as trademarks"},
            {"case_name": "Eastern Book Co. v. D.B. Modak", "citation": "(2008) 1 SCC 1", "court": "Supreme Court of India", "year": 2008, "outcome": "Copyright in judgments", "summary": "Raw text of judgments has no copyright but editorial additions do.", "key_principle": "Creativity required for copyright, not mere skill"},
            {"case_name": "Novartis AG v. Union of India", "citation": "(2013) 6 SCC 1", "court": "Supreme Court of India", "year": 2013, "outcome": "Evergreening rejected", "summary": "Section 3(d) prevents evergreening of pharmaceutical patents.", "key_principle": "No patent for mere modification without enhanced efficacy"},
            {"case_name": "Bayer Corporation v. Natco Pharma", "citation": "IPAB Order 2012", "court": "IPAB", "year": 2012, "outcome": "Compulsory license granted", "summary": "First compulsory license in India for cancer drug Nexavar.", "key_principle": "Compulsory licenses for affordable access to essential drugs"},
        ],
        "mediation_factors": {"recommended": True, "success_rate": 0.55, "avg_settlement_time_months": 4, "reasoning": "IP disputes often resolved through licensing agreements or consent terms."}
    },
    "land_acquisition": {
        "name": "Land Acquisition & Compensation",
        "description": "Government land acquisition, compensation disputes, rehabilitation claims under RFCTLARR Act",
        "relevant_acts": ["Right to Fair Compensation and Transparency in Land Acquisition Act, 2013", "National Highways Act, 1956", "Land Acquisition Act, 1894 (legacy)"],
        "avg_win_rate": 0.65, "avg_duration_months": 36, "duration_range": [12, 72],
        "court_stats": {
            "Reference Court": {"avg_months": 24, "win_rate": 0.70},
            "High Court": {"avg_months": 18, "win_rate": 0.55},
            "Supreme Court": {"avg_months": 18, "win_rate": 0.50}
        },
        "common_winning_arguments": [
            {"argument": "Market value significantly higher than offered compensation", "strength": 0.90, "section": "Section 26, RFCTLARR Act 2013", "description": "Compensation must reflect market value with solatium.", "success_rate": 0.82},
            {"argument": "Multiplier factor applicable for rural land", "strength": 0.88, "section": "First Schedule, RFCTLARR Act", "description": "Rural land entitled to multiplier up to 2x based on distance.", "success_rate": 0.80},
            {"argument": "Social Impact Assessment not conducted", "strength": 0.85, "section": "Section 4, RFCTLARR Act 2013", "description": "SIA is mandatory before acquisition. Non-compliance voids acquisition.", "success_rate": 0.78},
            {"argument": "Consent of affected families not obtained (for PPP projects)", "strength": 0.82, "section": "Section 2(2), RFCTLARR Act 2013", "description": "70-80% consent required for private/PPP projects.", "success_rate": 0.75},
            {"argument": "Comparable sale deeds showing higher market value", "strength": 0.88, "section": "Section 26, RFCTLARR Act", "description": "Recent sale deeds of nearby similar land prove higher market rate.", "success_rate": 0.82},
        ],
        "landmark_cases": [
            {"case_name": "Indore Development Authority v. Manoharlal", "citation": "(2020) 8 SCC 129", "court": "Supreme Court of India", "year": 2020, "outcome": "Lapse of acquisition", "summary": "If possession not taken within 5 years, acquisition lapses.", "key_principle": "Land acquisition proceedings lapse without timely possession"},
            {"case_name": "Pune Municipal Corp. v. Harakchand Solanki", "citation": "(2014) 3 SCC 183", "court": "Supreme Court of India", "year": 2014, "outcome": "Enhanced compensation", "summary": "SC enhanced compensation using comparable sale method.", "key_principle": "Market value determined by comparable sales"},
            {"case_name": "Shaji v. State of Kerala", "citation": "(2023) SCC", "court": "Supreme Court of India", "year": 2023, "outcome": "SIA mandatory", "summary": "Social Impact Assessment cannot be bypassed.", "key_principle": "SIA is a mandatory prerequisite to acquisition"},
            {"case_name": "Chhaju Ram v. State of Rajasthan", "citation": "(2006) SCC", "court": "Supreme Court of India", "year": 2006, "outcome": "Solatium upheld", "summary": "Solatium of 30% on market value is the right of landowner.", "key_principle": "Solatium is a statutory right, not discretionary"},
            {"case_name": "NHAI v. Hanumanthaiah", "citation": "(2019) SCC", "court": "Supreme Court of India", "year": 2019, "outcome": "Highway acquisition compensation", "summary": "Compensation under NH Act must also be just and fair.", "key_principle": "Highway acquisition must meet fair compensation standards"},
        ],
        "mediation_factors": {"recommended": True, "success_rate": 0.45, "avg_settlement_time_months": 8, "reasoning": "Negotiation with government on compensation amount. Direct settlement avoids years of litigation."}
    },
    "writ_petition": {
        "name": "Writ Petition / Constitutional Remedy",
        "description": "Challenging government action, fundamental rights violations, habeas corpus, mandamus, certiorari",
        "relevant_acts": ["Constitution of India (Articles 32, 226)", "Right to Information Act, 2005", "Administrative Tribunals Act, 1985"],
        "avg_win_rate": 0.35, "avg_duration_months": 12, "duration_range": [1, 36],
        "court_stats": {
            "High Court (Article 226)": {"avg_months": 8, "win_rate": 0.35},
            "Supreme Court (Article 32)": {"avg_months": 12, "win_rate": 0.30}
        },
        "common_winning_arguments": [
            {"argument": "Violation of Article 14 (Right to Equality)", "strength": 0.85, "section": "Article 14, Constitution", "description": "State action is arbitrary, discriminatory, and violates equal protection.", "success_rate": 0.65},
            {"argument": "Violation of Article 21 (Right to Life and Liberty)", "strength": 0.90, "section": "Article 21, Constitution", "description": "Broad right covering livelihood, dignity, privacy, health, education.", "success_rate": 0.70},
            {"argument": "Government action without following natural justice", "strength": 0.88, "section": "Principles of Natural Justice", "description": "Audi alteram partem - right to be heard before adverse action.", "success_rate": 0.75},
            {"argument": "Action ultra vires the parent statute", "strength": 0.82, "section": "Administrative Law Principles", "description": "Government exceeded powers granted by the enabling statute.", "success_rate": 0.65},
            {"argument": "Unreasonable delay causing prejudice", "strength": 0.75, "section": "Article 226, Constitution", "description": "Inordinate delay by government in processing applications.", "success_rate": 0.60},
        ],
        "landmark_cases": [
            {"case_name": "Maneka Gandhi v. Union of India", "citation": "(1978) 1 SCC 248", "court": "Supreme Court of India", "year": 1978, "outcome": "Expanded Article 21", "summary": "Right to life includes right to live with dignity. Procedure must be fair.", "key_principle": "Procedure established by law must be just, fair, and reasonable"},
            {"case_name": "Kesavananda Bharati v. State of Kerala", "citation": "(1973) 4 SCC 225", "court": "Supreme Court of India", "year": 1973, "outcome": "Basic structure doctrine", "summary": "Parliament cannot amend basic structure of Constitution.", "key_principle": "Basic structure of Constitution is inviolable"},
            {"case_name": "S.R. Bommai v. Union of India", "citation": "(1994) 3 SCC 1", "court": "Supreme Court of India", "year": 1994, "outcome": "President's rule limitations", "summary": "Article 356 is subject to judicial review.", "key_principle": "Judicial review of Presidential proclamations"},
            {"case_name": "Navtej Singh Johar v. Union of India", "citation": "(2018) 10 SCC 1", "court": "Supreme Court of India", "year": 2018, "outcome": "Section 377 struck", "summary": "Consensual homosexual acts decriminalized.", "key_principle": "Constitutional morality prevails over social morality"},
            {"case_name": "Internet Freedom Foundation v. Union of India", "citation": "(2020) SC", "court": "Supreme Court of India", "year": 2020, "outcome": "Internet shutdown limits", "summary": "Indefinite internet shutdowns violate fundamental rights.", "key_principle": "Internet access linked to freedom of expression"},
        ],
        "mediation_factors": {"recommended": False, "success_rate": 0.15, "avg_settlement_time_months": 2, "reasoning": "Writ petitions challenge government action on constitutional grounds. These require judicial pronouncement, not mediation."}
    },
    "custom": {
        "name": "Custom / Other Case Type",
        "description": "Any case type not listed above - the AI will analyze based on general legal principles",
        "relevant_acts": ["Constitution of India", "Code of Civil Procedure, 1908", "Bharatiya Nagarik Suraksha Sanhita, 2023", "Indian Evidence Act / BSA 2023"],
        "avg_win_rate": 0.45, "avg_duration_months": 24, "duration_range": [6, 60],
        "court_stats": {
            "Trial Court": {"avg_months": 18, "win_rate": 0.45},
            "High Court": {"avg_months": 15, "win_rate": 0.40},
            "Supreme Court": {"avg_months": 18, "win_rate": 0.35}
        },
        "common_winning_arguments": [
            {"argument": "Strong documentary evidence supporting the claim", "strength": 0.90, "section": "Indian Evidence Act / BSA 2023", "description": "Documentary evidence is prioritized over oral testimony.", "success_rate": 0.80},
            {"argument": "Principles of natural justice followed", "strength": 0.85, "section": "Administrative / Constitutional Law", "description": "Right to fair hearing and reasoned decision.", "success_rate": 0.75},
            {"argument": "Timely filing within limitation period", "strength": 0.88, "section": "Limitation Act, 1963", "description": "Case filed within prescribed limitation period.", "success_rate": 0.85},
            {"argument": "Precedent from similar cases established", "strength": 0.80, "section": "Article 141, Constitution", "description": "Supreme Court decisions binding on all courts.", "success_rate": 0.70},
            {"argument": "Balance of convenience and irreparable harm", "strength": 0.75, "section": "Order 39, CPC", "description": "Interim relief warranted to prevent irreparable injury.", "success_rate": 0.65},
        ],
        "landmark_cases": [
            {"case_name": "Vishaka v. State of Rajasthan", "citation": "(1997) 6 SCC 241", "court": "Supreme Court of India", "year": 1997, "outcome": "Guidelines established", "summary": "SC filled legislative vacuum by laying down binding guidelines.", "key_principle": "Courts can create law when legislature fails to act"},
            {"case_name": "MC Mehta v. Union of India", "citation": "(1987) 1 SCC 395", "court": "Supreme Court of India", "year": 1987, "outcome": "Absolute liability", "summary": "Industries causing hazardous substances leaks have absolute liability.", "key_principle": "Absolute liability for hazardous industries"},
            {"case_name": "DK Basu v. State of West Bengal", "citation": "(1997) 1 SCC 416", "court": "Supreme Court of India", "year": 1997, "outcome": "Arrest guidelines", "summary": "11 mandatory requirements for lawful arrest to prevent custodial abuse.", "key_principle": "Detailed guidelines for police arrest procedures"},
            {"case_name": "Olga Tellis v. Bombay Municipal Corp.", "citation": "(1985) 3 SCC 545", "court": "Supreme Court of India", "year": 1985, "outcome": "Right to livelihood", "summary": "Right to livelihood is part of right to life under Article 21.", "key_principle": "Eviction of pavement dwellers requires due process"},
            {"case_name": "Bachan Singh v. State of Punjab", "citation": "(1980) 2 SCC 684", "court": "Supreme Court of India", "year": 1980, "outcome": "Death penalty guidelines", "summary": "Death sentence only in rarest of rare cases.", "key_principle": "Rarest of rare doctrine for capital punishment"},
        ],
        "mediation_factors": {"recommended": True, "success_rate": 0.40, "avg_settlement_time_months": 4, "reasoning": "ADR mechanisms encouraged by courts across all civil matters under Section 89 CPC."}
    }
}

# All Indian jurisdictions - every state, UT, and major High Courts
JURISDICTIONS = {
    "Delhi": {"name": "Delhi (Delhi HC)", "speed_factor": 0.90},
    "Mumbai": {"name": "Mumbai (Bombay HC)", "speed_factor": 0.85},
    "Bangalore": {"name": "Bengaluru (Karnataka HC)", "speed_factor": 1.0},
    "Chennai": {"name": "Chennai (Madras HC)", "speed_factor": 0.95},
    "Kolkata": {"name": "Kolkata (Calcutta HC)", "speed_factor": 1.1},
    "Hyderabad": {"name": "Hyderabad (Telangana HC)", "speed_factor": 1.0},
    "Pune": {"name": "Pune (Bombay HC - Bench)", "speed_factor": 1.05},
    "Ahmedabad": {"name": "Ahmedabad (Gujarat HC)", "speed_factor": 1.1},
    "Lucknow": {"name": "Lucknow (Allahabad HC - Bench)", "speed_factor": 1.2},
    "Allahabad": {"name": "Allahabad (Allahabad HC)", "speed_factor": 1.25},
    "Jaipur": {"name": "Jaipur (Rajasthan HC)", "speed_factor": 1.15},
    "Chandigarh": {"name": "Chandigarh (Punjab & Haryana HC)", "speed_factor": 0.95},
    "Kochi": {"name": "Kochi (Kerala HC)", "speed_factor": 0.90},
    "Patna": {"name": "Patna (Patna HC)", "speed_factor": 1.3},
    "Guwahati": {"name": "Guwahati (Gauhati HC)", "speed_factor": 1.15},
    "Bhopal": {"name": "Bhopal (Madhya Pradesh HC)", "speed_factor": 1.15},
    "Jabalpur": {"name": "Jabalpur (MP HC - Principal Seat)", "speed_factor": 1.2},
    "Nagpur": {"name": "Nagpur (Bombay HC - Bench)", "speed_factor": 1.1},
    "Cuttack": {"name": "Cuttack (Orissa HC)", "speed_factor": 1.2},
    "Ranchi": {"name": "Ranchi (Jharkhand HC)", "speed_factor": 1.25},
    "Bilaspur": {"name": "Bilaspur (Chhattisgarh HC)", "speed_factor": 1.2},
    "Shimla": {"name": "Shimla (Himachal Pradesh HC)", "speed_factor": 1.0},
    "Nainital": {"name": "Nainital (Uttarakhand HC)", "speed_factor": 1.1},
    "Jodhpur": {"name": "Jodhpur (Rajasthan HC - Bench)", "speed_factor": 1.15},
    "Srinagar": {"name": "Srinagar (J&K and Ladakh HC)", "speed_factor": 1.3},
    "Jammu": {"name": "Jammu (J&K and Ladakh HC - Bench)", "speed_factor": 1.3},
    "Amaravati": {"name": "Amaravati (Andhra Pradesh HC)", "speed_factor": 1.1},
    "Imphal": {"name": "Imphal (Manipur HC)", "speed_factor": 1.2},
    "Shillong": {"name": "Shillong (Meghalaya HC)", "speed_factor": 1.15},
    "Kohima": {"name": "Kohima (Gauhati HC - Bench)", "speed_factor": 1.2},
    "Agartala": {"name": "Agartala (Tripura HC)", "speed_factor": 1.15},
    "Aizawl": {"name": "Aizawl (Gauhati HC - Bench)", "speed_factor": 1.2},
    "Itanagar": {"name": "Itanagar (Gauhati HC - Bench)", "speed_factor": 1.25},
    "Gangtok": {"name": "Gangtok (Sikkim HC)", "speed_factor": 1.1},
    "PortBlair": {"name": "Port Blair (Calcutta HC Circuit)", "speed_factor": 1.3},
    "Panaji": {"name": "Panaji (Bombay HC - Goa Bench)", "speed_factor": 1.0},
    "Thiruvananthapuram": {"name": "Thiruvananthapuram (Kerala HC)", "speed_factor": 0.95},
    "Madurai": {"name": "Madurai (Madras HC - Bench)", "speed_factor": 1.0},
    "Aurangabad": {"name": "Aurangabad (Bombay HC - Bench)", "speed_factor": 1.1},
    "Supreme_Court": {"name": "Supreme Court of India (New Delhi)", "speed_factor": 0.80},
    "Other": {"name": "Other Jurisdiction", "speed_factor": 1.1}
}
