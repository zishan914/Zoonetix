"""
Disease treatment database for ZOONETIX.
Contains medication info, dosage, precautions for each detected disease.
DISCLAIMER: This is AI-assisted information. Always consult a licensed veterinarian.
"""

from typing import Dict, List


class TreatmentInfo:
    def __init__(
        self,
        disease: str,
        symptoms: str,
        medications: List[Dict[str, str]],
        dosage_guide: str,
        administration: str,
        precautions: List[str],
        vet_urgency: str,
        recovery_time: str,
        home_care: str,
        prevention: str,
        disclaimer: str = "Always consult a licensed veterinarian before administering any medication.",
    ):
        self.disease = disease
        self.symptoms = symptoms
        self.medications = medications
        self.dosage_guide = dosage_guide
        self.administration = administration
        self.precautions = precautions
        self.vet_urgency = vet_urgency
        self.recovery_time = recovery_time
        self.home_care = home_care
        self.prevention = prevention
        self.disclaimer = disclaimer

    def to_dict(self) -> dict:
        return {
            "disease": self.disease,
            "symptoms": self.symptoms,
            "medications": self.medications,
            "dosage_guide": self.dosage_guide,
            "administration": self.administration,
            "precautions": self.precautions,
            "vet_urgency": self.vet_urgency,
            "recovery_time": self.recovery_time,
            "home_care": self.home_care,
            "prevention": self.prevention,
            "disclaimer": self.disclaimer,
        }


TREATMENT_DB: Dict[str, TreatmentInfo] = {
    "Eye Infection": TreatmentInfo(
        disease="Eye Infection",
        symptoms="Redness, swelling, discharge (watery/pus), squinting, excessive tearing, rubbing eyes, cloudiness in cornea.",
        medications=[
            {"name": "Ciprofloxacin Eye Drops", "type": "Antibiotic drops", "purpose": "Bacterial infection"},
            {"name": "Tobramycin Ophthalmic", "type": "Antibiotic ointment", "purpose": "Broad-spectrum bacterial coverage"},
            {"name": "Artificial Tears (Carboxymethylcellulose)", "type": "Lubricant", "purpose": "Soothing & flushing debris"},
        ],
        dosage_guide="""
• Ciprofloxacin/Tobramycin: 1-2 drops in affected eye every 6-8 hours for 7-10 days.
• For ointment: ¼ inch strip inside lower eyelid every 8-12 hours.
• Dosage varies by animal size — small breeds/cats use lower end, large breeds upper end.
""",
        administration="""
1. Clean eye gently with sterile saline or warm water.
2. Tilt head slightly back, pull down lower eyelid.
3. Apply drops/ointment WITHOUT touching the eye surface.
4. Allow animal to blink to spread medication.
5. Wash hands before & after.
""",
        precautions=[
            "Do NOT use steroid drops without vet prescription — can worsen ulcers.",
            "Separate infected animals to prevent contagious spread.",
            "Complete full antibiotic course even if symptoms improve.",
            "Avoid direct sunlight if eye is sensitive.",
        ],
        vet_urgency="Visit vet within 24-48 hours. Immediate if eye is bulging, severely clouded, or animal is in pain.",
        recovery_time="5-10 days with proper treatment. Chronic cases may take 2-3 weeks.",
        home_care="Keep eye area clean with warm compress 2-3 times daily. Use Elizabethan collar to prevent rubbing.",
        prevention="Regular eye cleaning, avoid dusty environments, check for foreign bodies, vaccinate against infectious causes.",
    ),

    "Fungal Infection": TreatmentInfo(
        disease="Fungal Infection",
        symptoms="Circular bald patches, scaly/crusty skin, redness, itching, musty odor, brittle hair, pustules around lesions.",
        medications=[
            {"name": "Itraconazole", "type": "Oral antifungal", "purpose": "Systemic fungal infections (ringworm, etc.)"},
            {"name": "Terbinafine", "type": "Oral/Topical antifungal", "purpose": "Dermatophyte infections"},
            {"name": "Miconazole Cream 2%", "type": "Topical cream", "purpose": "Localized skin fungus"},
            {"name": "Clotrimazole Spray", "type": "Topical spray", "purpose": "Widespread lesions"},
        ],
        dosage_guide="""
• Itraconazole: 5-10 mg/kg orally once daily for 4-6 weeks.
• Terbinafine: 10-20 mg/kg orally once daily OR apply cream twice daily.
• Topical creams/sprays: Apply thin layer to affected area 2 times daily for 2-4 weeks.
""",
        administration="""
1. Wear gloves — many fungal infections are ZOONOTIC (spread to humans).
2. Clip hair around lesions before applying topical medication.
3. Clean area with antiseptic solution, let dry.
4. Apply medication extending 2cm beyond visible lesion.
5. For oral meds: give with fatty food to improve absorption.
""",
        precautions=[
            "HIGHLY CONTAGIOUS to humans and other animals — wear gloves & mask.",
            "Wash bedding, toys, brushes in hot water with antifungal disinfectant.",
            "Isolate infected animal.",
            "Do NOT stop treatment early — fungi persist even after symptoms fade.",
        ],
        vet_urgency="Visit vet for confirmation (Wood's lamp exam or fungal culture). Treat within 3-5 days.",
        recovery_time="2-6 weeks typically. Deep infections may need 8+ weeks.",
        home_care="Daily bathing with medicated shampoo (ketoconazole/chlorhexidine) 2-3 times per week. Sun exposure helps kill spores.",
        prevention="Avoid damp environments, disinfect grooming tools, isolate new animals before introducing, boost immune system with good nutrition.",
    ),

    "Mange in Dog": TreatmentInfo(
        disease="Mange in Dog (Sarcoptic/Demodectic)",
        symptoms="Intense itching, hair loss (ears, elbows, belly), red inflamed skin, thick crusty lesions, foul odor, skin thickening.",
        medications=[
            {"name": "Ivermectin", "type": "Antiparasitic (oral/injectable)", "purpose": "Kills sarcoptic mites"},
            {"name": "Selamectin (Revolution)", "type": "Topical spot-on", "purpose": "Broad-spectrum parasite control"},
            {"name": "Amitraz Dip (Mitaban)", "type": "Topical dip", "purpose": "Demodectic mange"},
            {"name": "Lime Sulfur Dip", "type": "Topical dip", "purpose": "Soothes skin & kills mites"},
        ],
        dosage_guide="""
• Ivermectin: 0.2-0.4 mg/kg orally every 7 days for 4-6 weeks (COLLIE/SHELTIE breeds — AVOID, can be toxic).
• Selamectin: Apply spot-on once monthly as per weight (available in 10-20kg, 20-40kg packs).
• Amitraz Dip: Dilute per label, dip every 2 weeks for 4-6 treatments.
• Lime Sulfur: Dilute 1:32, dip weekly for 4-6 weeks.
""",
        administration="""
1. Bathe dog with medicated shampoo first to remove crusts.
2. For dips: wear gloves, saturate coat fully, let air dry (do NOT rinse).
3. For oral ivermectin: give on empty stomach, dose carefully by weight.
4. Treat ALL animals in household simultaneously.
5. Clean environment thoroughly.
""",
        precautions=[
            "IVERMECTIN IS TOXIC to Collies, Shetland Sheepdogs, Australian Shepherds — use Selamectin instead.",
            "Sarcoptic mange is HIGHLY CONTAGIOUS to humans (temporary scabies).",
            "Do not use corticosteroids — they suppress immune response needed to fight mites.",
            "Monitor for side effects: lethargy, vomiting, tremors.",
        ],
        vet_urgency="Visit vet for skin scrape test to confirm mite type. Begin treatment within 1 week.",
        recovery_time="Sarcoptic: 4-6 weeks. Demodectic: 6-12 weeks (immunity-related).",
        home_care="Warm water soaks to soften crusts, omega-3 fatty acid supplements for skin health, soft bedding to prevent secondary infections.",
        prevention="Regular parasite prevention (monthly spot-ons), avoid contact with stray animals, maintain strong immune system with quality diet.",
    ),

    "Parvovirus in Dog": TreatmentInfo(
        disease="Parvovirus in Dog",
        symptoms="Severe vomiting (often bloody), bloody diarrhea, lethargy, fever, loss of appetite, rapid dehydration, foul-smelling stool.",
        medications=[
            {"name": "Intravenous Fluids (Lactated Ringers)", "type": "IV therapy", "purpose": "Rehydration & electrolyte balance"},
            {"name": "Metoclopramide", "type": "Anti-emetic", "purpose": "Controls vomiting"},
            {"name": "Maropitant (Cerenia)", "type": "Anti-emetic", "purpose": "Vomiting control (more potent)"},
            {"name": "Amoxicillin-Clavulanate", "type": "Antibiotic", "purpose": "Prevents secondary bacterial infection"},
            {"name": "Ondansetron", "type": "Anti-emetic", "purpose": "Severe nausea control"},
        ],
        dosage_guide="""
• IV Fluids: 60-90 ml/kg/day depending on dehydration level — VET ADMINISTERED ONLY.
• Metoclopramide: 0.2-0.5 mg/kg IV/IM every 6-8 hours.
• Maropitant: 1 mg/kg SC (subcutaneous) once daily for 5 days.
• Amoxicillin-Clavulanate: 12.5-25 mg/kg orally every 12 hours.
• Ondansetron: 0.1-0.2 mg/kg IV/IM every 8-12 hours.
""",
        administration="""
1. HOSPITALIZATION REQUIRED — parvo is life-threatening.
2. Nothing by mouth (NPO) for 12-24 hours, then gradual reintroduction of bland diet.
3. IV fluids with added dextrose and potassium.
4. Antibiotics given via injection initially, oral once stable.
5. Warm, clean, isolated environment.
""",
        precautions=[
            "PARVO IS EXTREMELY CONTAGIOUS — full isolation required.",
            "Vaccinate all other dogs in household immediately.",
            "Bleach solution (1:30 dilution) is needed to disinfect surfaces.",
            "Puppies under 6 months have highest mortality — urgent care critical.",
        ],
        vet_urgency="EMERGENCY — seek vet IMMEDIATELY (within hours). Parvo kills within 48-72 hours without treatment.",
        recovery_time="5-10 days hospitalization. Full recovery 2-3 weeks. Immunity develops after recovery.",
        home_care="Once home: small frequent meals of boiled chicken + rice, pedialyte for hydration, complete rest, warm bedding.",
        prevention="Vaccination at 6, 10, 14 weeks + annual boosters. Avoid public areas until fully vaccinated. Disinfect with bleach.",
    ),

    "Scabies in Cat": TreatmentInfo(
        disease="Scabies in Cat (Notoedric Mange)",
        symptoms="Intense itching, crusty lesions on ears/face/neck, hair loss, thickened wrinkled skin, scratching until bleeding.",
        medications=[
            {"name": "Selamectin (Revolution)", "type": "Topical spot-on", "purpose": "Safest & most effective for cats"},
            {"name": "Ivermectin", "type": "Injectable/Oral", "purpose": "Alternative treatment"},
            {"name": "Lime Sulfur Dip", "type": "Topical dip", "purpose": "Kills mites & soothes skin"},
            {"name": "Doramectin", "type": "Injectable", "purpose": "Severe cases"},
        ],
        dosage_guide="""
• Selamectin: Apply spot-on every 2 weeks for 3 treatments (dose by weight: 6mg for <2.5kg, 12mg for 2.6-7.5kg, 24mg for >7.5kg).
• Ivermectin: 0.2-0.3 mg/kg SC every 2 weeks for 3 treatments (USE WITH CAUTION in cats).
• Lime Sulfur Dip: 1:32 dilution, dip weekly for 4-6 weeks.
""",
        administration="""
1. Clip hair around affected areas.
2. Clean crusts gently with warm saline.
3. Apply spot-on to back of neck where cat cannot lick.
4. For dips: saturate entire coat, avoid eyes/ears, let air dry.
5. Treat ALL pets in home at same time.
""",
        precautions=[
            "Cats are sensitive to many pesticides — use ONLY cat-safe products.",
            "Can spread to humans (temporary itching).",
            "Do NOT use dog flea products on cats — can be fatal.",
            "Keep cat warm after dipping — wet cat = hypothermia risk.",
        ],
        vet_urgency="Visit vet for skin scrape confirmation. Begin treatment within 2-3 days.",
        recovery_time="2-4 weeks typically. Severe chronic cases may take 6-8 weeks.",
        home_care="Warm environment, soft food (ear lesions make chewing painful), Elizabethan collar to prevent scratching, frequent bedding changes.",
        prevention="Monthly parasite prevention, avoid contact with infected/stray cats, regular grooming.",
    ),

    "Skin Allergy": TreatmentInfo(
        disease="Skin Allergy (Atopic Dermatitis)",
        symptoms="Itchy skin, redness, scratching/biting/licking obsessively, hot spots, ear infections, hair loss, thickened dark skin over time.",
        medications=[
            {"name": "Cetirizine", "type": "Antihistamine", "purpose": "Mild allergy symptoms"},
            {"name": "Prednisolone", "type": "Corticosteroid", "purpose": "Severe inflammation (short-term)"},
            {"name": "Apoquel (Oclacitinib)", "type": "Immunomodulator", "purpose": "Rapid itch relief"},
            {"name": "Cytopoint", "type": "Monoclonal antibody injection", "purpose": "Long-term itch control"},
            {"name": "Medicated Shampoo (Chlorhexidine + Ketoconazole)", "type": "Topical", "purpose": "Secondary infection prevention"},
        ],
        dosage_guide="""
• Cetirizine: 1 mg/kg orally every 12-24 hours (e.g., 5mg for small cat, 10mg for medium dog).
• Prednisolone: 0.5-1 mg/kg orally every 12 hours for 5-7 days, then taper.
• Apoquel: 0.4-0.6 mg/kg orally twice daily for 14 days, then once daily.
• Cytopoint: 10mg for <10kg, 20mg for 10-20kg, 30mg for 20-30kg, 40mg for >30kg — injection every 4-8 weeks.
""",
        administration="""
1. Identify and eliminate allergen (food, pollen, dust mites, flea bites).
2. Bathe with medicated shampoo 2-3 times weekly initially.
3. Give oral meds with food to reduce stomach upset.
4. For steroids: NEVER stop suddenly — taper dose gradually.
5. Keep nails trimmed to reduce skin damage from scratching.
""",
        precautions=[
            "Long-term steroids cause diabetes, liver damage, immune suppression.",
            "Apoquel suppresses immune system — increased infection risk.",
            "Do NOT combine multiple steroids.",
            "Flea control is essential — even one flea bite triggers allergy in sensitized animals.",
        ],
        vet_urgency="Non-urgent for mild cases. Vet visit within 1-2 weeks. Urgent if skin is open/bleeding/hot.",
        recovery_time="Depends on allergen control. Acute flare: 1-2 weeks. Chronic management: lifelong.",
        home_care="Hypoallergenic diet trial, air purifiers, frequent bathing, omega-3/6 fatty acid supplements, keep environment dust-free.",
        prevention="Identify allergens via blood test or elimination diet, regular flea prevention, air filtration, hypoallergenic bedding.",
    ),

    "foot-and-mouth": TreatmentInfo(
        disease="Foot-and-Mouth Disease (FMD)",
        symptoms="High fever, blisters/vesicles on mouth, tongue, teats, and between hooves, drooling, lameness, loss of appetite, weight loss, reduced milk production.",
        medications=[
            {"name": "Broad-spectrum Antibiotics (Penicillin, Oxytetracycline)", "type": "Antibiotic", "purpose": "Prevent secondary bacterial infection"},
            {"name": "NSAIDs (Flunixin Meglumine, Meloxicam)", "type": "Anti-inflammatory/Pain reliever", "purpose": "Fever & pain control"},
            {"name": "Foot Bath (Copper Sulfate, Formalin)", "type": "Topical antiseptic", "purpose": "Disinfect hoof lesions"},
            {"name": "Electrolyte Solutions", "type": "Oral/IV supplement", "purpose": "Prevent dehydration"},
        ],
        dosage_guide="""
• Penicillin: 10,000-20,000 IU/kg IM every 12-24 hours for 3-5 days.
• Oxytetracycline: 5-10 mg/kg IV/IM every 24 hours.
• Flunixin Meglumine: 1.1-2.2 mg/kg IV/IM once daily for 3 days max.
• Meloxicam: 0.5 mg/kg orally once daily.
• Foot bath: 5-10% copper sulfate or 1-5% formalin solution, stand animal for 15-30 min daily.
""",
        administration="""
1. ISOLATE infected animal immediately — FMD is HIGHLY CONTAGIOUS.
2. Provide soft, palatable feed (mash, soaked hay) — mouth ulcers make eating painful.
3. Apply antiseptic foot baths daily for hoof lesions.
4. Administer pain relief to encourage eating/drinking.
5. Report to veterinary authorities — FMD is NOTIFIABLE disease in most countries.
""",
        precautions=[
            "FMD spreads via air, saliva, milk, manure, contaminated equipment.",
            "Humans do NOT get FMD but can carry virus on clothes/shoes.",
            "Quarantine entire farm.",
            "Culling may be mandated by government in endemic regions.",
        ],
        vet_urgency="REPORT IMMEDIATELY to vet and agricultural authorities. FMD is a notifiable disease with serious trade implications.",
        recovery_time="2-3 weeks for mild cases. Permanent hoof/mammary damage possible. Mortality 1-5% in adults, up to 20% in young.",
        home_care="Deep bedding for hoof comfort, shade for mouth lesions, easy access to water, highly palatable feed, separate milking equipment.",
        prevention="Vaccination available for endemic regions. Strict biosecurity: foot baths at farm entrance, quarantine new animals, control wildlife contact.",
    ),

    "healthy": TreatmentInfo(
        disease="Healthy",
        symptoms="Normal appetite, active behavior, shiny coat, clear eyes, normal stool, good body condition.",
        medications=[
            {"name": "No medication needed", "type": "N/A", "purpose": "Animal is healthy"},
        ],
        dosage_guide="No medication required.",
        administration="N/A",
        precautions=[
            "Maintain current health regimen.",
            "Continue regular vaccinations and deworming schedule.",
        ],
        vet_urgency="Routine annual checkup is sufficient.",
        recovery_time="N/A — animal is already healthy.",
        home_care="Continue balanced diet, regular exercise, clean water, proper shelter.",
        prevention="Regular vet checkups, vaccinations, parasite control, balanced nutrition, clean environment.",
    ),

    "lumpy": TreatmentInfo(
        disease="Lumpy Skin Disease (LSD)",
        symptoms="Fever, firm round skin nodules (2-5cm) all over body, especially neck/shoulders/back, swollen lymph nodes, drop in milk production, lameness if nodules on legs.",
        medications=[
            {"name": "Broad-spectrum Antibiotics (Oxytetracycline, Penicillin)", "type": "Antibiotic", "purpose": "Prevent secondary bacterial infection in nodules"},
            {"name": "NSAIDs (Flunixin Meglumine, Ketoprofen)", "type": "Anti-inflammatory", "purpose": "Fever & pain control"},
            {"name": "Iodine/Antiseptic Ointment", "type": "Topical", "purpose": "Treat open nodules"},
            {"name": "Vitamin AD3E injections", "type": "Vitamin supplement", "purpose": "Boost immunity & skin healing"},
        ],
        dosage_guide="""
• Oxytetracycline: 5-10 mg/kg IV/IM every 24 hours for 5-7 days.
• Penicillin: 10,000-20,000 IU/kg IM every 12-24 hours.
• Flunixin Meglumine: 1.1-2.2 mg/kg IV/IM once daily for 3 days.
• Vitamin AD3E: 5-10 ml IM (large animals) once weekly for 2-3 weeks.
• Topical: Apply iodine ointment to open lesions daily.
""",
        administration="""
1. Isolate infected animal — LSD spreads via insects (mosquitoes, flies).
2. Apply topical antiseptic to nodules that have ruptured.
3. Use insect repellents and fly control around animal.
4. Provide soft bedding — nodules are painful.
5. Monitor for secondary infections.
""",
        precautions=[
            "LSD spreads via insect vectors — control flies & mosquitoes.",
            "Nodules may slough off leaving scars.",
            "Secondary infection is main risk.",
            "Quarantine for 4-6 weeks minimum.",
        ],
        vet_urgency="Contact vet within 2-3 days. Report to authorities if LSD is notifiable in your region.",
        recovery_time="4-6 weeks. Nodules heal leaving permanent scars. Some animals remain carriers.",
        home_care="Insect control (fly traps, repellent sprays), soft bedding, nutritious feed, clean water, protect from rain/sun.",
        prevention="Vaccination (live attenuated Neethling strain) available. Vector control, quarantine new animals, breeding for resistance.",
    ),
}


def get_treatment(disease_label: str) -> dict:
    """Get treatment info for a disease label. Returns empty dict if not found."""
    treatment = TREATMENT_DB.get(disease_label)
    if treatment:
        return treatment.to_dict()
    return {}

