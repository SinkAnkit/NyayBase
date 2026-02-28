"""
NyayBase — Indian Courts Database
Comprehensive database of Indian courts with search functionality.
"""

COURTS = [
    # ═══════════════════════════════════════
    # HIGH COURTS (All 25)
    # ═══════════════════════════════════════
    {"name": "Supreme Court of India", "type": "supreme_court", "city": "New Delhi", "state": "Delhi", "pincode": "110001", "address": "Tilak Marg, New Delhi - 110001", "lat": 28.6225, "lng": 77.2400, "phone": "011-23388922", "hours": "Mon-Fri: 10:30 AM - 4:00 PM", "website": "https://main.sci.gov.in", "helpline": "011-23388942"},

    # High Courts
    {"name": "Delhi High Court", "type": "high_court", "city": "New Delhi", "state": "Delhi", "pincode": "110003", "address": "Sher Shah Road, New Delhi - 110003", "lat": 28.6353, "lng": 77.2413, "phone": "011-23384604", "hours": "Mon-Fri: 10:30 AM - 4:00 PM", "website": "https://delhihighcourt.nic.in", "helpline": "011-23386492"},
    {"name": "Bombay High Court", "type": "high_court", "city": "Mumbai", "state": "Maharashtra", "pincode": "400032", "address": "Fort, Mumbai - 400032", "lat": 18.9271, "lng": 72.8318, "phone": "022-22660571", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://bombayhighcourt.nic.in", "helpline": "022-22620956"},
    {"name": "Madras High Court", "type": "high_court", "city": "Chennai", "state": "Tamil Nadu", "pincode": "600104", "address": "High Court Buildings, Chennai - 600104", "lat": 13.0826, "lng": 80.2870, "phone": "044-25301346", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://hcmadras.tn.nic.in", "helpline": "044-25361989"},
    {"name": "Calcutta High Court", "type": "high_court", "city": "Kolkata", "state": "West Bengal", "pincode": "700001", "address": "Government Place West, Kolkata - 700001", "lat": 22.5726, "lng": 88.3503, "phone": "033-22484022", "hours": "Mon-Fri: 10:30 AM - 4:00 PM", "website": "https://calcuttahighcourt.gov.in", "helpline": "033-22484461"},
    {"name": "Karnataka High Court", "type": "high_court", "city": "Bengaluru", "state": "Karnataka", "pincode": "560001", "address": "Ambedkar Veedhi, Bengaluru - 560001", "lat": 12.9781, "lng": 77.5922, "phone": "080-22868264", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://karnatakajudiciary.kar.nic.in", "helpline": "080-22868100"},
    {"name": "Gujarat High Court", "type": "high_court", "city": "Ahmedabad", "state": "Gujarat", "pincode": "380009", "address": "Sola, Ahmedabad - 380060", "lat": 23.0684, "lng": 72.5169, "phone": "079-27682046", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://gujarathighcourt.nic.in", "helpline": "079-27680025"},
    {"name": "Rajasthan High Court", "type": "high_court", "city": "Jodhpur", "state": "Rajasthan", "pincode": "342001", "address": "High Court Campus, Jodhpur - 342001", "lat": 26.2905, "lng": 73.0238, "phone": "0291-2636104", "hours": "Mon-Fri: 10:00 AM - 4:30 PM", "website": "https://hcraj.nic.in", "helpline": "0291-2636100"},
    {"name": "Allahabad High Court", "type": "high_court", "city": "Prayagraj", "state": "Uttar Pradesh", "pincode": "211001", "address": "High Court Road, Prayagraj - 211001", "lat": 25.4358, "lng": 81.8463, "phone": "0532-2623579", "hours": "Mon-Fri: 10:00 AM - 4:30 PM", "website": "https://www.allahabadhighcourt.in", "helpline": "0532-2623500"},
    {"name": "Patna High Court", "type": "high_court", "city": "Patna", "state": "Bihar", "pincode": "800001", "address": "Bailey Road, Patna - 800001", "lat": 25.6143, "lng": 85.1265, "phone": "0612-2223004", "hours": "Mon-Fri: 10:00 AM - 4:30 PM", "website": "https://patnahighcourt.gov.in", "helpline": "0612-2223006"},
    {"name": "Punjab and Haryana High Court", "type": "high_court", "city": "Chandigarh", "state": "Punjab/Haryana", "pincode": "160001", "address": "Sector 1, Chandigarh - 160001", "lat": 30.7574, "lng": 76.7724, "phone": "0172-2744100", "hours": "Mon-Fri: 10:00 AM - 4:30 PM", "website": "https://phhc.gov.in", "helpline": "0172-2744000"},
    {"name": "Kerala High Court", "type": "high_court", "city": "Kochi", "state": "Kerala", "pincode": "682031", "address": "High Court of Kerala, Ernakulam, Kochi - 682031", "lat": 9.9663, "lng": 76.2815, "phone": "0484-2562541", "hours": "Mon-Fri: 10:00 AM - 4:30 PM", "website": "https://highcourtofkerala.nic.in", "helpline": "0484-2393789"},
    {"name": "Telangana High Court", "type": "high_court", "city": "Hyderabad", "state": "Telangana", "pincode": "500066", "address": "Gachibowli, Hyderabad - 500032", "lat": 17.4241, "lng": 78.3382, "phone": "040-23448478", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://tshc.gov.in", "helpline": "040-23448000"},
    {"name": "Andhra Pradesh High Court", "type": "high_court", "city": "Amaravati", "state": "Andhra Pradesh", "pincode": "522503", "address": "Nelapadu, Amaravati - 522503", "lat": 16.5153, "lng": 80.5181, "phone": "0866-2974573", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://aphc.gov.in", "helpline": "0866-2974500"},
    {"name": "Madhya Pradesh High Court", "type": "high_court", "city": "Jabalpur", "state": "Madhya Pradesh", "pincode": "482001", "address": "High Court Campus, Jabalpur - 482001", "lat": 23.1749, "lng": 79.9416, "phone": "0761-2621650", "hours": "Mon-Fri: 10:00 AM - 4:30 PM", "website": "https://mphc.gov.in", "helpline": "0761-2621600"},
    {"name": "Jharkhand High Court", "type": "high_court", "city": "Ranchi", "state": "Jharkhand", "pincode": "834002", "address": "Dhurwa, Ranchi - 834004", "lat": 23.3639, "lng": 85.3145, "phone": "0651-2480285", "hours": "Mon-Fri: 10:00 AM - 4:30 PM", "website": "https://jharkhandhighcourt.nic.in", "helpline": "0651-2480200"},
    {"name": "Chhattisgarh High Court", "type": "high_court", "city": "Bilaspur", "state": "Chhattisgarh", "pincode": "495001", "address": "Bodri, Bilaspur - 495001", "lat": 22.0886, "lng": 82.1379, "phone": "07752-246060", "hours": "Mon-Fri: 10:00 AM - 4:30 PM", "website": "https://highcourt.cg.gov.in", "helpline": "07752-246000"},
    {"name": "Uttarakhand High Court", "type": "high_court", "city": "Nainital", "state": "Uttarakhand", "pincode": "263001", "address": "High Court Premises, Nainital - 263001", "lat": 29.3803, "lng": 79.4636, "phone": "05942-235239", "hours": "Mon-Fri: 10:00 AM - 4:30 PM", "website": "https://highcourtofuttarakhand.gov.in", "helpline": "05942-235200"},
    {"name": "Himachal Pradesh High Court", "type": "high_court", "city": "Shimla", "state": "Himachal Pradesh", "pincode": "171001", "address": "High Court Road, Shimla - 171001", "lat": 31.1048, "lng": 77.1734, "phone": "0177-2804425", "hours": "Mon-Fri: 10:00 AM - 4:30 PM", "website": "https://hphighcourt.nic.in", "helpline": "0177-2804400"},
    {"name": "Orissa High Court", "type": "high_court", "city": "Cuttack", "state": "Odisha", "pincode": "753002", "address": "Cantonment Road, Cuttack - 753002", "lat": 20.4625, "lng": 85.8830, "phone": "0671-2304059", "hours": "Mon-Fri: 10:00 AM - 4:30 PM", "website": "https://orissahighcourt.nic.in", "helpline": "0671-2304000"},
    {"name": "Gauhati High Court", "type": "high_court", "city": "Guwahati", "state": "Assam", "pincode": "781001", "address": "Panbazar, Guwahati - 781001", "lat": 26.1851, "lng": 91.7522, "phone": "0361-2735541", "hours": "Mon-Fri: 10:00 AM - 4:00 PM", "website": "https://ghconline.gov.in", "helpline": "0361-2735500"},
    {"name": "Jammu & Kashmir High Court", "type": "high_court", "city": "Srinagar", "state": "J&K", "pincode": "190001", "address": "Janipur, Jammu / Srinagar", "lat": 34.0837, "lng": 74.7973, "phone": "0191-2545820", "hours": "Mon-Fri: 10:00 AM - 4:00 PM", "website": "https://jkhighcourt.nic.in", "helpline": "0191-2545800"},
    {"name": "Tripura High Court", "type": "high_court", "city": "Agartala", "state": "Tripura", "pincode": "799001", "address": "High Court Complex, Agartala - 799001", "lat": 23.8315, "lng": 91.2868, "phone": "0381-2326587", "hours": "Mon-Fri: 10:00 AM - 4:00 PM", "website": "https://thc.nic.in", "helpline": "0381-2326500"},
    {"name": "Meghalaya High Court", "type": "high_court", "city": "Shillong", "state": "Meghalaya", "pincode": "793001", "address": "Lachumiere, Shillong - 793001", "lat": 25.5788, "lng": 91.8933, "phone": "0364-2224308", "hours": "Mon-Fri: 10:00 AM - 4:00 PM", "website": "https://meghalayahighcourt.nic.in", "helpline": "0364-2224300"},
    {"name": "Manipur High Court", "type": "high_court", "city": "Imphal", "state": "Manipur", "pincode": "795001", "address": "Chingmeirong, Imphal - 795001", "lat": 24.8074, "lng": 93.9513, "phone": "0385-2451050", "hours": "Mon-Fri: 10:00 AM - 4:00 PM", "website": "https://highcourtofmanipur.nic.in", "helpline": "0385-2451000"},
    {"name": "Sikkim High Court", "type": "high_court", "city": "Gangtok", "state": "Sikkim", "pincode": "737101", "address": "High Court Complex, Gangtok - 737101", "lat": 27.3314, "lng": 88.6138, "phone": "03592-202688", "hours": "Mon-Fri: 10:00 AM - 4:00 PM", "website": "https://hcs.gov.in", "helpline": "03592-202600"},

    # ═══════════════════════════════════════
    # DISTRICT COURTS (Major Cities)
    # ═══════════════════════════════════════
    {"name": "Tis Hazari Courts Complex", "type": "district_court", "city": "New Delhi", "state": "Delhi", "pincode": "110054", "address": "Tis Hazari, Delhi - 110054", "lat": 28.6640, "lng": 77.2249, "phone": "011-23919090", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/delhi", "helpline": "011-23919090"},
    {"name": "Patiala House Courts", "type": "district_court", "city": "New Delhi", "state": "Delhi", "pincode": "110001", "address": "India Gate Circle, New Delhi - 110001", "lat": 28.6167, "lng": 77.2375, "phone": "011-23383437", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/delhi", "helpline": "011-23383437"},
    {"name": "Saket District Court", "type": "district_court", "city": "New Delhi", "state": "Delhi", "pincode": "110017", "address": "Saket, New Delhi - 110017", "lat": 28.5225, "lng": 77.2141, "phone": "011-26523044", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/delhi", "helpline": "011-26523044"},
    {"name": "Karkardooma Courts Complex", "type": "district_court", "city": "New Delhi", "state": "Delhi", "pincode": "110032", "address": "Karkardooma, Delhi - 110032", "lat": 28.6597, "lng": 77.3052, "phone": "011-22375032", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/delhi", "helpline": "011-22375032"},
    {"name": "Dwarka Courts Complex", "type": "district_court", "city": "New Delhi", "state": "Delhi", "pincode": "110075", "address": "Sector 10, Dwarka, New Delhi - 110075", "lat": 28.5830, "lng": 77.0379, "phone": "011-28041815", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/delhi", "helpline": "011-28041815"},
    {"name": "City Civil Court Mumbai", "type": "district_court", "city": "Mumbai", "state": "Maharashtra", "pincode": "400001", "address": "Dhobi Talao, Fort, Mumbai - 400001", "lat": 18.9402, "lng": 72.8312, "phone": "022-22620170", "hours": "Mon-Sat: 10:00 AM - 5:30 PM", "website": "https://districts.ecourts.gov.in/mumbai", "helpline": "022-22620170"},
    {"name": "Esplanade Court Mumbai", "type": "district_court", "city": "Mumbai", "state": "Maharashtra", "pincode": "400001", "address": "MG Road, Fort, Mumbai - 400001", "lat": 18.9353, "lng": 72.8363, "phone": "022-22621855", "hours": "Mon-Sat: 10:00 AM - 5:30 PM", "website": "https://districts.ecourts.gov.in/mumbai", "helpline": "022-22621855"},
    {"name": "Chennai City Civil Court", "type": "district_court", "city": "Chennai", "state": "Tamil Nadu", "pincode": "600001", "address": "George Town, Chennai - 600001", "lat": 13.0900, "lng": 80.2861, "phone": "044-25260105", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/chennai", "helpline": "044-25260105"},
    {"name": "City Civil Court Bengaluru", "type": "district_court", "city": "Bengaluru", "state": "Karnataka", "pincode": "560009", "address": "Nrupathunga Road, Bengaluru - 560009", "lat": 12.9764, "lng": 77.5878, "phone": "080-22862254", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/bengaluru", "helpline": "080-22862254"},
    {"name": "City Civil Court Ahmedabad", "type": "district_court", "city": "Ahmedabad", "state": "Gujarat", "pincode": "380001", "address": "Bhadra, Ahmedabad - 380001", "lat": 23.0225, "lng": 72.5714, "phone": "079-25507573", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/ahmedabad", "helpline": "079-25507573"},
    {"name": "Kolkata City Civil Court", "type": "district_court", "city": "Kolkata", "state": "West Bengal", "pincode": "700001", "address": "B.B.D. Bagh, Kolkata - 700001", "lat": 22.5631, "lng": 88.3460, "phone": "033-22485422", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/kolkata", "helpline": "033-22485422"},
    {"name": "City Civil Court Hyderabad", "type": "district_court", "city": "Hyderabad", "state": "Telangana", "pincode": "500002", "address": "Nampally, Hyderabad - 500001", "lat": 17.3850, "lng": 78.4867, "phone": "040-24612847", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/hyderabad", "helpline": "040-24612847"},
    {"name": "District Court Pune", "type": "district_court", "city": "Pune", "state": "Maharashtra", "pincode": "411001", "address": "Shivajinagar, Pune - 411005", "lat": 18.5313, "lng": 73.8453, "phone": "020-25510148", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/pune", "helpline": "020-25510148"},
    {"name": "District Court Jaipur", "type": "district_court", "city": "Jaipur", "state": "Rajasthan", "pincode": "302001", "address": "MI Road, Jaipur - 302001", "lat": 26.9124, "lng": 75.7873, "phone": "0141-2568812", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/jaipur", "helpline": "0141-2568812"},
    {"name": "District Court Lucknow", "type": "district_court", "city": "Lucknow", "state": "Uttar Pradesh", "pincode": "226001", "address": "Collectorganj, Lucknow - 226001", "lat": 26.8505, "lng": 80.9463, "phone": "0522-2206411", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/lucknow", "helpline": "0522-2206411"},
    {"name": "District Court Chandigarh", "type": "district_court", "city": "Chandigarh", "state": "Punjab/Haryana", "pincode": "160017", "address": "Sector 43, Chandigarh - 160017", "lat": 30.7267, "lng": 76.7580, "phone": "0172-2700027", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/chandigarh", "helpline": "0172-2700027"},
    {"name": "District Court Indore", "type": "district_court", "city": "Indore", "state": "Madhya Pradesh", "pincode": "452001", "address": "MG Road, Indore - 452001", "lat": 22.7196, "lng": 75.8577, "phone": "0731-2430082", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/indore", "helpline": "0731-2430082"},
    {"name": "District Court Bhopal", "type": "district_court", "city": "Bhopal", "state": "Madhya Pradesh", "pincode": "462001", "address": "TT Nagar, Bhopal - 462003", "lat": 23.2332, "lng": 77.4183, "phone": "0755-2551735", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/bhopal", "helpline": "0755-2551735"},
    {"name": "District Court Nagpur", "type": "district_court", "city": "Nagpur", "state": "Maharashtra", "pincode": "440001", "address": "Civil Lines, Nagpur - 440001", "lat": 21.1497, "lng": 79.0806, "phone": "0712-2561283", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/nagpur", "helpline": "0712-2561283"},
    {"name": "District Court Thiruvananthapuram", "type": "district_court", "city": "Thiruvananthapuram", "state": "Kerala", "pincode": "695001", "address": "Fort, Thiruvananthapuram - 695023", "lat": 8.4957, "lng": 76.9605, "phone": "0471-2471590", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/thiruvananthapuram", "helpline": "0471-2471590"},
    {"name": "District Court Coimbatore", "type": "district_court", "city": "Coimbatore", "state": "Tamil Nadu", "pincode": "641018", "address": "Avanashi Road, Coimbatore - 641018", "lat": 11.0168, "lng": 76.9558, "phone": "0422-2300460", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/coimbatore", "helpline": "0422-2300460"},
    {"name": "District Court Visakhapatnam", "type": "district_court", "city": "Visakhapatnam", "state": "Andhra Pradesh", "pincode": "530002", "address": "Court Junction, Visakhapatnam - 530002", "lat": 17.7209, "lng": 83.3025, "phone": "0891-2564522", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/visakhapatnam", "helpline": "0891-2564522"},
    {"name": "District Court Patna", "type": "district_court", "city": "Patna", "state": "Bihar", "pincode": "800001", "address": "Gardanibagh, Patna - 800001", "lat": 25.6093, "lng": 85.1376, "phone": "0612-2230651", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/patna", "helpline": "0612-2230651"},
    {"name": "District Court Guwahati", "type": "district_court", "city": "Guwahati", "state": "Assam", "pincode": "781001", "address": "Pan Bazar, Guwahati - 781001", "lat": 26.1803, "lng": 91.7453, "phone": "0361-2731422", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/guwahati", "helpline": "0361-2731422"},
    {"name": "District Court Bhubaneswar", "type": "district_court", "city": "Bhubaneswar", "state": "Odisha", "pincode": "751001", "address": "Unit-3, Bhubaneswar - 751001", "lat": 20.2732, "lng": 85.8338, "phone": "0674-2531422", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/bhubaneswar", "helpline": "0674-2531422"},

    # Tier-2/3 District Courts
    {"name": "District Court Varanasi", "type": "district_court", "city": "Varanasi", "state": "Uttar Pradesh", "pincode": "221002", "address": "Sigra, Varanasi - 221002", "lat": 25.3176, "lng": 82.9739, "phone": "0542-2222100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/varanasi", "helpline": "0542-2222100"},
    {"name": "District Court Kanpur", "type": "district_court", "city": "Kanpur", "state": "Uttar Pradesh", "pincode": "208001", "address": "Nana Rao Park, Kanpur - 208001", "lat": 26.4499, "lng": 80.3319, "phone": "0512-2301000", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/kanpur", "helpline": "0512-2301000"},
    {"name": "District Court Agra", "type": "district_court", "city": "Agra", "state": "Uttar Pradesh", "pincode": "282001", "address": "Agra Fort, Agra - 282001", "lat": 27.1767, "lng": 78.0081, "phone": "0562-2260100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/agra", "helpline": "0562-2260100"},
    {"name": "District Court Meerut", "type": "district_court", "city": "Meerut", "state": "Uttar Pradesh", "pincode": "250001", "address": "Collectorate, Meerut - 250001", "lat": 28.9845, "lng": 77.7064, "phone": "0121-2640100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/meerut", "helpline": "0121-2640100"},
    {"name": "District Court Gorakhpur", "type": "district_court", "city": "Gorakhpur", "state": "Uttar Pradesh", "pincode": "273001", "address": "Civil Lines, Gorakhpur - 273001", "lat": 26.7606, "lng": 83.3732, "phone": "0551-2334100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/gorakhpur", "helpline": "0551-2334100"},
    {"name": "District Court Surat", "type": "district_court", "city": "Surat", "state": "Gujarat", "pincode": "395001", "address": "Nanpura, Surat - 395001", "lat": 21.1702, "lng": 72.8311, "phone": "0261-2424100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/surat", "helpline": "0261-2424100"},
    {"name": "District Court Vadodara", "type": "district_court", "city": "Vadodara", "state": "Gujarat", "pincode": "390001", "address": "Raopura, Vadodara - 390001", "lat": 22.3072, "lng": 73.1812, "phone": "0265-2426100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/vadodara", "helpline": "0265-2426100"},
    {"name": "District Court Rajkot", "type": "district_court", "city": "Rajkot", "state": "Gujarat", "pincode": "360001", "address": "Court Road, Rajkot - 360001", "lat": 22.3039, "lng": 70.8022, "phone": "0281-2232100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/rajkot", "helpline": "0281-2232100"},
    {"name": "District Court Mysuru", "type": "district_court", "city": "Mysuru", "state": "Karnataka", "pincode": "570001", "address": "Nazarbad, Mysuru - 570010", "lat": 12.3051, "lng": 76.6551, "phone": "0821-2443100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/mysuru", "helpline": "0821-2443100"},
    {"name": "District Court Mangaluru", "type": "district_court", "city": "Mangaluru", "state": "Karnataka", "pincode": "575001", "address": "Balmatta, Mangaluru - 575001", "lat": 12.8714, "lng": 74.8431, "phone": "0824-2440100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/mangaluru", "helpline": "0824-2440100"},
    {"name": "District Court Hubli-Dharwad", "type": "district_court", "city": "Hubli", "state": "Karnataka", "pincode": "580029", "address": "Court Circle, Hubli - 580029", "lat": 15.3647, "lng": 75.1240, "phone": "0836-2262100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/dharwad", "helpline": "0836-2262100"},
    {"name": "District Court Madurai", "type": "district_court", "city": "Madurai", "state": "Tamil Nadu", "pincode": "625001", "address": "Collectorate, Madurai - 625001", "lat": 9.9252, "lng": 78.1198, "phone": "0452-2341100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/madurai", "helpline": "0452-2341100"},
    {"name": "District Court Salem", "type": "district_court", "city": "Salem", "state": "Tamil Nadu", "pincode": "636001", "address": "Court Road, Salem - 636001", "lat": 11.6643, "lng": 78.1460, "phone": "0427-2313100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/salem", "helpline": "0427-2313100"},
    {"name": "District Court Tiruchirappalli", "type": "district_court", "city": "Tiruchirappalli", "state": "Tamil Nadu", "pincode": "620017", "address": "Collectorate, Tiruchirappalli - 620017", "lat": 10.7905, "lng": 78.7047, "phone": "0431-2460100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/tiruchirappalli", "helpline": "0431-2460100"},
    {"name": "District Court Dehradun", "type": "district_court", "city": "Dehradun", "state": "Uttarakhand", "pincode": "248001", "address": "Court Road, Dehradun - 248001", "lat": 30.3165, "lng": 78.0322, "phone": "0135-2712100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/dehradun", "helpline": "0135-2712100"},
    {"name": "District Court Raipur", "type": "district_court", "city": "Raipur", "state": "Chhattisgarh", "pincode": "492001", "address": "Collectorate, Raipur - 492001", "lat": 21.2514, "lng": 81.6296, "phone": "0771-2234100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/raipur", "helpline": "0771-2234100"},
    {"name": "District Court Ranchi", "type": "district_court", "city": "Ranchi", "state": "Jharkhand", "pincode": "834001", "address": "Main Road, Ranchi - 834001", "lat": 23.3441, "lng": 85.3096, "phone": "0651-2200100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/ranchi", "helpline": "0651-2200100"},
    {"name": "District Court Jamshedpur", "type": "district_court", "city": "Jamshedpur", "state": "Jharkhand", "pincode": "831001", "address": "Sakchi, Jamshedpur - 831001", "lat": 22.8046, "lng": 86.2029, "phone": "0657-2426100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/jamshedpur", "helpline": "0657-2426100"},
    {"name": "District Court Goa (Panaji)", "type": "district_court", "city": "Panaji", "state": "Goa", "pincode": "403001", "address": "Altinho, Panaji - 403001", "lat": 15.4989, "lng": 73.8278, "phone": "0832-2225100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/goa", "helpline": "0832-2225100"},
    {"name": "District Court Amritsar", "type": "district_court", "city": "Amritsar", "state": "Punjab", "pincode": "143001", "address": "Court Road, Amritsar - 143001", "lat": 31.6340, "lng": 74.8723, "phone": "0183-2566100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/amritsar", "helpline": "0183-2566100"},
    {"name": "District Court Ludhiana", "type": "district_court", "city": "Ludhiana", "state": "Punjab", "pincode": "141001", "address": "Court Complex, Ludhiana - 141001", "lat": 30.9010, "lng": 75.8573, "phone": "0161-2401100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/ludhiana", "helpline": "0161-2401100"},
    {"name": "District Court Shimla", "type": "district_court", "city": "Shimla", "state": "Himachal Pradesh", "pincode": "171001", "address": "The Ridge, Shimla - 171001", "lat": 31.1048, "lng": 77.1734, "phone": "0177-2658100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/shimla", "helpline": "0177-2658100"},
    {"name": "District Court Kota", "type": "district_court", "city": "Kota", "state": "Rajasthan", "pincode": "324001", "address": "Nayapura, Kota - 324001", "lat": 25.2138, "lng": 75.8648, "phone": "0744-2451100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/kota", "helpline": "0744-2451100"},
    {"name": "District Court Udaipur", "type": "district_court", "city": "Udaipur", "state": "Rajasthan", "pincode": "313001", "address": "Surajpole, Udaipur - 313001", "lat": 24.5854, "lng": 73.7125, "phone": "0294-2528100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/udaipur", "helpline": "0294-2528100"},
    {"name": "District Court Ajmer", "type": "district_court", "city": "Ajmer", "state": "Rajasthan", "pincode": "305001", "address": "Court Road, Ajmer - 305001", "lat": 26.4499, "lng": 74.6399, "phone": "0145-2620100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/ajmer", "helpline": "0145-2620100"},
    {"name": "District Court Nashik", "type": "district_court", "city": "Nashik", "state": "Maharashtra", "pincode": "422001", "address": "Old Agra Road, Nashik - 422001", "lat": 19.9975, "lng": 73.7898, "phone": "0253-2570100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/nashik", "helpline": "0253-2570100"},
    {"name": "District Court Aurangabad", "type": "district_court", "city": "Aurangabad", "state": "Maharashtra", "pincode": "431001", "address": "Kranti Chowk, Aurangabad - 431001", "lat": 19.8762, "lng": 75.3433, "phone": "0240-2334100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/aurangabad", "helpline": "0240-2334100"},
    {"name": "District Court Gwalior", "type": "district_court", "city": "Gwalior", "state": "Madhya Pradesh", "pincode": "474001", "address": "Lashkar, Gwalior - 474001", "lat": 26.2183, "lng": 78.1828, "phone": "0751-2340100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/gwalior", "helpline": "0751-2340100"},
    {"name": "District Court Ujjain", "type": "district_court", "city": "Ujjain", "state": "Madhya Pradesh", "pincode": "456001", "address": "Collectorate, Ujjain - 456001", "lat": 23.1793, "lng": 75.7849, "phone": "0734-2554100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/ujjain", "helpline": "0734-2554100"},
    {"name": "District Court Siliguri", "type": "district_court", "city": "Siliguri", "state": "West Bengal", "pincode": "734001", "address": "Hill Cart Road, Siliguri - 734001", "lat": 26.7271, "lng": 88.3953, "phone": "0353-2535100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/siliguri", "helpline": "0353-2535100"},
    {"name": "District Court Kochi", "type": "district_court", "city": "Kochi", "state": "Kerala", "pincode": "682011", "address": "Ernakulam, Kochi - 682011", "lat": 9.9816, "lng": 76.2999, "phone": "0484-2394100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/ernakulam", "helpline": "0484-2394100"},
    {"name": "District Court Kozhikode", "type": "district_court", "city": "Kozhikode", "state": "Kerala", "pincode": "673001", "address": "Court Road, Kozhikode - 673001", "lat": 11.2588, "lng": 75.7804, "phone": "0495-2366100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/kozhikode", "helpline": "0495-2366100"},
    {"name": "District Court Jammu", "type": "district_court", "city": "Jammu", "state": "J&K", "pincode": "180001", "address": "Janipur, Jammu - 180001", "lat": 32.7266, "lng": 74.8570, "phone": "0191-2571100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/jammu", "helpline": "0191-2571100"},
    {"name": "District Court Srinagar", "type": "district_court", "city": "Srinagar", "state": "J&K", "pincode": "190001", "address": "Lal Chowk, Srinagar - 190001", "lat": 34.0837, "lng": 74.7973, "phone": "0194-2477100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/srinagar", "helpline": "0194-2477100"},
    {"name": "District Court Cuttack", "type": "district_court", "city": "Cuttack", "state": "Odisha", "pincode": "753001", "address": "Court Station, Cuttack - 753001", "lat": 20.4625, "lng": 85.8830, "phone": "0671-2610100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/cuttack", "helpline": "0671-2610100"},
    {"name": "District Court Gaya", "type": "district_court", "city": "Gaya", "state": "Bihar", "pincode": "823001", "address": "Collectorate, Gaya - 823001", "lat": 24.7955, "lng": 84.9994, "phone": "0631-2220100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/gaya", "helpline": "0631-2220100"},
    {"name": "District Court Muzaffarpur", "type": "district_court", "city": "Muzaffarpur", "state": "Bihar", "pincode": "842001", "address": "Court Road, Muzaffarpur - 842001", "lat": 26.1209, "lng": 85.3647, "phone": "0621-2240100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/muzaffarpur", "helpline": "0621-2240100"},
    {"name": "District Court Imphal", "type": "district_court", "city": "Imphal", "state": "Manipur", "pincode": "795001", "address": "Lamphel, Imphal - 795004", "lat": 24.8074, "lng": 93.9513, "phone": "0385-2220100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/imphal", "helpline": "0385-2220100"},
    {"name": "District Court Agartala", "type": "district_court", "city": "Agartala", "state": "Tripura", "pincode": "799001", "address": "Court Compound, Agartala - 799001", "lat": 23.8315, "lng": 91.2868, "phone": "0381-2315100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/agartala", "helpline": "0381-2315100"},
    {"name": "District Court Shillong", "type": "district_court", "city": "Shillong", "state": "Meghalaya", "pincode": "793001", "address": "Jail Road, Shillong - 793001", "lat": 25.5788, "lng": 91.8933, "phone": "0364-2222100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/shillong", "helpline": "0364-2222100"},
    {"name": "District Court Gangtok", "type": "district_court", "city": "Gangtok", "state": "Sikkim", "pincode": "737101", "address": "MG Marg, Gangtok - 737101", "lat": 27.3314, "lng": 88.6138, "phone": "03592-202100", "hours": "Mon-Sat: 10:00 AM - 5:00 PM", "website": "https://districts.ecourts.gov.in/gangtok", "helpline": "03592-202100"},

    # ===================================
    # CONSUMER FORUMS (Major Cities)
    # ===================================
    {"name": "National Consumer Disputes Redressal Commission (NCDRC)", "type": "consumer_forum", "city": "New Delhi", "state": "Delhi", "pincode": "110001", "address": "Janpath, New Delhi - 110001", "lat": 28.6281, "lng": 77.2180, "phone": "011-23782815", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://ncdrc.nic.in", "helpline": "1800-11-4000"},
    {"name": "Delhi State Consumer Commission", "type": "consumer_forum", "city": "New Delhi", "state": "Delhi", "pincode": "110002", "address": "ITO, New Delhi - 110002", "lat": 28.6283, "lng": 77.2495, "phone": "011-23379188", "hours": "Mon-Fri: 10:30 AM - 4:00 PM", "website": "https://confonet.nic.in", "helpline": "011-23379188"},
    {"name": "Delhi District Consumer Forum (Central)", "type": "consumer_forum", "city": "New Delhi", "state": "Delhi", "pincode": "110054", "address": "Tis Hazari Complex, Delhi - 110054", "lat": 28.6645, "lng": 77.2254, "phone": "011-23968451", "hours": "Mon-Fri: 10:30 AM - 4:00 PM", "website": "https://confonet.nic.in", "helpline": "011-23968451"},
    {"name": "Maharashtra State Consumer Commission", "type": "consumer_forum", "city": "Mumbai", "state": "Maharashtra", "pincode": "400020", "address": "Churchgate, Mumbai - 400020", "lat": 18.9341, "lng": 72.8267, "phone": "022-22017948", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://confonet.nic.in", "helpline": "022-22017948"},
    {"name": "Mumbai District Consumer Forum (South)", "type": "consumer_forum", "city": "Mumbai", "state": "Maharashtra", "pincode": "400051", "address": "Bandra East, Mumbai - 400051", "lat": 19.0596, "lng": 72.8411, "phone": "022-26407744", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://confonet.nic.in", "helpline": "022-26407744"},
    {"name": "Tamil Nadu State Consumer Commission", "type": "consumer_forum", "city": "Chennai", "state": "Tamil Nadu", "pincode": "600002", "address": "Egmore, Chennai - 600002", "lat": 13.0756, "lng": 80.2618, "phone": "044-28192570", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://confonet.nic.in", "helpline": "044-28192570"},
    {"name": "Karnataka State Consumer Commission", "type": "consumer_forum", "city": "Bengaluru", "state": "Karnataka", "pincode": "560027", "address": "Basavanagudi, Bengaluru - 560004", "lat": 12.9441, "lng": 77.5720, "phone": "080-26600786", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://confonet.nic.in", "helpline": "080-26600786"},
    {"name": "Gujarat State Consumer Commission", "type": "consumer_forum", "city": "Ahmedabad", "state": "Gujarat", "pincode": "380006", "address": "Usmanpura, Ahmedabad - 380014", "lat": 23.0412, "lng": 72.5609, "phone": "079-27541480", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://confonet.nic.in", "helpline": "079-27541480"},
    {"name": "West Bengal State Consumer Commission", "type": "consumer_forum", "city": "Kolkata", "state": "West Bengal", "pincode": "700001", "address": "Salt Lake, Kolkata - 700091", "lat": 22.5768, "lng": 88.4138, "phone": "033-23345700", "hours": "Mon-Fri: 10:30 AM - 4:00 PM", "website": "https://confonet.nic.in", "helpline": "033-23345700"},
    {"name": "Telangana State Consumer Commission", "type": "consumer_forum", "city": "Hyderabad", "state": "Telangana", "pincode": "500004", "address": "Abids, Hyderabad - 500001", "lat": 17.3924, "lng": 78.4753, "phone": "040-24756462", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://confonet.nic.in", "helpline": "040-24756462"},
    {"name": "Rajasthan State Consumer Commission", "type": "consumer_forum", "city": "Jaipur", "state": "Rajasthan", "pincode": "302005", "address": "C-Scheme, Jaipur - 302005", "lat": 26.9070, "lng": 75.7869, "phone": "0141-2222035", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://confonet.nic.in", "helpline": "0141-2222035"},
    {"name": "UP State Consumer Commission", "type": "consumer_forum", "city": "Lucknow", "state": "Uttar Pradesh", "pincode": "226001", "address": "Hazratganj, Lucknow - 226001", "lat": 26.8508, "lng": 80.9448, "phone": "0522-2623003", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://confonet.nic.in", "helpline": "0522-2623003"},
    {"name": "Kerala State Consumer Commission", "type": "consumer_forum", "city": "Thiruvananthapuram", "state": "Kerala", "pincode": "695004", "address": "Vazhuthacaud, Thiruvananthapuram - 695014", "lat": 8.5052, "lng": 76.9630, "phone": "0471-2326155", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://confonet.nic.in", "helpline": "0471-2326155"},
    {"name": "Punjab State Consumer Commission", "type": "consumer_forum", "city": "Chandigarh", "state": "Punjab", "pincode": "160019", "address": "Sector 19, Chandigarh - 160019", "lat": 30.7423, "lng": 76.7690, "phone": "0172-2725057", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://confonet.nic.in", "helpline": "0172-2725057"},
    {"name": "Pune District Consumer Forum", "type": "consumer_forum", "city": "Pune", "state": "Maharashtra", "pincode": "411001", "address": "Shivajinagar, Pune - 411005", "lat": 18.5287, "lng": 73.8466, "phone": "020-25532310", "hours": "Mon-Fri: 10:30 AM - 4:30 PM", "website": "https://confonet.nic.in", "helpline": "020-25532310"},
]

# Aliases for common city name variations
CITY_ALIASES = {
    "bangalore": "bengaluru", "bombay": "mumbai", "madras": "chennai",
    "calcutta": "kolkata", "trivandrum": "thiruvananthapuram",
    "allahabad": "prayagraj", "benares": "varanasi", "banaras": "varanasi",
    "vizag": "visakhapatnam", "noida": "new delhi", "gurgaon": "new delhi",
    "gurugram": "new delhi", "faridabad": "new delhi", "ghaziabad": "new delhi",
    "navi mumbai": "mumbai", "thane": "mumbai", "greater noida": "new delhi",
    "mysore": "bengaluru", "mangalore": "bengaluru", "hubli": "bengaluru",
    "cochin": "kochi", "ernakulam": "kochi", "calicut": "kochi",
    "pondicherry": "chennai", "puducherry": "chennai", "madurai": "chennai",
    "dehradun": "nainital", "haridwar": "nainital", "rishikesh": "nainital",
    "panaji": "mumbai", "goa": "mumbai", "margao": "mumbai",
    "raipur": "bilaspur", "durg": "bilaspur", "bhilai": "bilaspur",
    "kanpur": "lucknow", "agra": "prayagraj", "meerut": "new delhi",
    "varanasi": "prayagraj", "gorakhpur": "prayagraj",
    "surat": "ahmedabad", "vadodara": "ahmedabad", "rajkot": "ahmedabad",
    "ludhiana": "chandigarh", "amritsar": "chandigarh", "jalandhar": "chandigarh",
    "panchkula": "chandigarh", "mohali": "chandigarh",
    "ranchi": "ranchi", "jamshedpur": "ranchi", "dhanbad": "ranchi",
    "gwalior": "jabalpur", "ujjain": "indore",
    "siliguri": "kolkata", "durgapur": "kolkata", "asansol": "kolkata",
    "nashik": "mumbai", "aurangabad": "mumbai", "solapur": "pune",
    "kota": "jaipur", "udaipur": "jodhpur", "ajmer": "jaipur",
    "bhopal": "bhopal", "jabalpur": "jabalpur",
}

# Pincode first 2 digits → approximate center lat/lng for fallback
PINCODE_REGION = {
    "11": (28.6, 77.2), "12": (28.4, 77.0), "13": (28.9, 77.5),  # Delhi/Haryana
    "14": (30.9, 75.8), "15": (31.5, 75.3), "16": (30.7, 76.8),  # Punjab/Chandigarh
    "17": (31.1, 77.2), "18": (32.2, 76.3),  # HP/J&K
    "19": (34.1, 74.8),  # Kashmir
    "20": (26.8, 81.0), "21": (25.4, 81.8), "22": (26.4, 80.3),  # UP
    "23": (27.2, 79.4), "24": (26.9, 75.8), "25": (28.6, 79.4),  # UP
    "26": (27.9, 78.1), "27": (26.4, 83.4), "28": (26.8, 80.9),  # UP
    "30": (26.9, 75.8), "31": (27.2, 76.6), "32": (26.3, 73.0),  # Rajasthan
    "33": (27.6, 75.1), "34": (26.5, 74.6),  # Rajasthan
    "36": (23.2, 72.6), "37": (22.3, 70.8), "38": (23.0, 72.6),  # Gujarat
    "39": (21.2, 72.8), "40": (19.0, 72.8), "41": (18.5, 73.8),  # Maharashtra
    "42": (19.8, 75.3), "43": (20.0, 73.8), "44": (21.1, 79.0),  # Maharashtra
    "45": (22.7, 75.9), "46": (23.3, 77.4), "47": (23.2, 79.9),  # MP
    "48": (23.2, 79.9), "49": (22.1, 82.1),  # MP/CG
    "50": (17.4, 78.5), "51": (17.0, 79.6), "52": (16.5, 80.6),  # Telangana/AP
    "53": (17.7, 83.3), "56": (13.0, 77.6), "57": (15.4, 75.0),  # AP/Karnataka
    "58": (16.5, 75.7), "59": (14.7, 74.3),  # Karnataka
    "60": (13.1, 80.3), "61": (10.8, 79.0), "62": (9.9, 78.1),  # TN
    "63": (11.0, 77.0), "64": (10.5, 76.3),  # TN
    "67": (11.2, 75.8), "68": (9.6, 76.6), "69": (8.5, 77.0),  # Kerala
    "70": (22.6, 88.4), "71": (22.6, 88.0), "72": (23.5, 87.3),  # WB
    "73": (23.0, 88.5), "74": (24.1, 88.3), "75": (20.3, 85.8),  # WB/Odisha
    "76": (20.5, 84.0), "77": (19.3, 84.8),  # Odisha
    "78": (26.1, 91.7), "79": (23.8, 91.3),  # NE India
    "80": (25.6, 85.1), "81": (25.3, 87.0), "82": (24.8, 85.0),  # Bihar
    "83": (23.3, 85.3), "84": (25.6, 85.1),  # Jharkhand/Bihar
    "85": (25.6, 85.1),  # Bihar
}

import math

def _haversine(lat1, lon1, lat2, lon2):
    """Distance in km between two GPS coordinates."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def _find_nearest(lat, lng, state=None):
    """Find nearest courts: 2 HCs (same-state first) + 5 DCs + 3 CFs."""
    distances = []
    for court in COURTS:
        if court.get("lat") and court.get("lng"):
            d = _haversine(lat, lng, court["lat"], court["lng"])
            distances.append((d, court))
    distances.sort(key=lambda x: x[0])

    hcs = [(d, c) for d, c in distances if c["type"] in ("high_court", "supreme_court")]
    dcs = [(d, c) for d, c in distances if c["type"] == "district_court"]
    cfs = [(d, c) for d, c in distances if c["type"] == "consumer_forum"]

    # Prioritize same-state HC if state is known
    picked_hcs = []
    if state:
        sl = state.lower()
        same_state = [c for d, c in hcs if sl in c["state"].lower() or c["state"].lower() in sl]
        if same_state:
            picked_hcs.append(same_state[0])
    # Fill remaining HC slots from nearest
    for d, c in hcs:
        if c not in picked_hcs:
            picked_hcs.append(c)
        if len(picked_hcs) >= 2:
            break

    result = list(picked_hcs)
    for d, c in dcs[:5]:
        result.append(c)
    for d, c in cfs[:3]:
        result.append(c)
    return result


def _geocode(query):
    """Geocode a location using Nominatim. Returns (lat, lng, state)."""
    import urllib.request
    import json as _json

    search = f"{query}, India"
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(search)}&format=json&limit=1&countrycodes=in&addressdetails=1"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "NyayBase/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = _json.loads(resp.read().decode())
            if data and len(data) > 0:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                state = data[0].get("address", {}).get("state", "")
                return lat, lon, state
    except Exception:
        pass
    return None, None, None


import urllib.parse

def search_courts(query: str) -> dict:
    """
    Search courts by city/town/village/pincode.
    Uses Nominatim geocoding for ANY location, then finds nearest courts.
    """
    if not query or not query.strip():
        return {"courts": [], "is_nearest": False}

    q = query.strip().lower()
    q_resolved = CITY_ALIASES.get(q, q)

    # Try exact match first (city/state/pincode in database)
    results = []
    for court in COURTS:
        city_lower = court["city"].lower()
        state_lower = court["state"].lower()
        pin = court["pincode"]

        if q.isdigit() and (pin == q or pin.startswith(q)):
            results.append(court)
            continue
        if q_resolved in city_lower or city_lower in q_resolved:
            results.append(court)
            continue
        if q_resolved in state_lower:
            results.append(court)
            continue
        if q in court["name"].lower():
            results.append(court)
            continue

    search_lat, search_lng = None, None

    if results:
        lats = [c["lat"] for c in results if c.get("lat")]
        lngs = [c["lng"] for c in results if c.get("lng")]
        if lats and lngs:
            search_lat = sum(lats) / len(lats)
            search_lng = sum(lngs) / len(lngs)

        type_order = {"supreme_court": 0, "high_court": 1, "district_court": 2, "consumer_forum": 3}
        results.sort(key=lambda c: type_order.get(c["type"], 9))
        return {"courts": results, "is_nearest": False, "search_lat": search_lat, "search_lng": search_lng}

    # No exact match — geocode the location
    lat, lng, geo_state = _geocode(query)

    # Fallback: pincode region table
    if lat is None and q.isdigit() and len(q) >= 2:
        prefix = q[:2]
        if prefix in PINCODE_REGION:
            lat, lng = PINCODE_REGION[prefix]
            geo_state = None

    # Last fallback: center of India
    if lat is None:
        lat, lng = 22.0, 78.0
        geo_state = None

    search_lat, search_lng = lat, lng
    results = _find_nearest(lat, lng, state=geo_state)

    type_order = {"supreme_court": 0, "high_court": 1, "district_court": 2, "consumer_forum": 3}
    results.sort(key=lambda c: type_order.get(c["type"], 9))
    return {"courts": results, "is_nearest": True, "search_lat": search_lat, "search_lng": search_lng}


