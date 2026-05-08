# populate_conditions.py
# Writes all condition content into the conditions/ folder

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONDITIONS_DIR = os.path.join(BASE_DIR, "conditions")

CONDITIONS = {

"diabetes.txt": """
1. WHAT IS DIABETES?
Diabetes mellitus is a chronic metabolic condition characterized by elevated blood glucose resulting from defects in insulin secretion, insulin action, or both.
Insulin is a hormone produced by the beta cells of the pancreas. It allows glucose from food to enter cells and be used for energy.

2. TYPES OF DIABETES
- Type 1 (T1DM): Autoimmune beta-cell destruction; absolute insulin deficiency; lifelong insulin required; 5-10% of cases
- Type 2 (T2DM): Insulin resistance and relative deficiency; obesity-linked; most common form 90-95% of cases
- Gestational (GDM): Develops in pregnancy; resolves post-delivery; raises future T2DM risk
- Pre-Diabetes: FPG 100-125 mg/dL; OGTT 140-199 mg/dL; HbA1c 5.7-6.4%; reversible with intervention

3. DIAGNOSTIC CRITERIA
Diagnosis requires ONE of the following confirmed on repeat testing:
- Fasting Plasma Glucose >= 126 mg/dL (7.0 mmol/L)
- 2-hr OGTT >= 200 mg/dL (11.1 mmol/L)
- HbA1c >= 6.5% (48 mmol/mol)
- Random glucose >= 200 mg/dL with classic symptoms

4. SIGNS AND SYMPTOMS
- Polyuria: frequent urination
- Polydipsia: excessive thirst
- Polyphagia: increased hunger
- Unexplained weight loss especially T1DM
- Fatigue and weakness
- Blurred vision
- Slow-healing wounds or frequent infections
- Numbness or tingling in hands and feet
Note: Type 2 diabetes is often asymptomatic for years; routine screening is essential.

5. RISK FACTORS
- Age >= 45 years; family history; high-risk ethnicity
- Overweight or obesity BMI >= 25
- Physical inactivity; unhealthy diet
- Hypertension; dyslipidemia; smoking

6. GLYCAEMIC TARGETS
- HbA1c < 7.0% for most non-pregnant adults
- Fasting glucose 80-130 mg/dL
- Post-prandial glucose < 180 mg/dL
- Blood pressure < 130/80 mmHg
- LDL cholesterol < 70 mg/dL high CVD risk

7. MANAGEMENT
- Weight loss 5-10% body weight reduction significantly improves glucose control
- Physical activity >= 150 min/week moderate aerobic exercise
- Diet: Mediterranean, DASH, or low-carbohydrate diets
- Metformin: preferred first-line agent; weight neutral; low cost
- GLP-1 RA: semaglutide; cardiovascular benefit; weight loss
- SGLT-2i: empagliflozin; cardiovascular and renal benefit
- DPP-4i: sitagliptin; well tolerated
- Sulfonylurea: glipizide; low cost; risk of hypoglycaemia
- Insulin: glargine; any HbA1c level

8. MONITORING
- HbA1c every 3 months if not at goal or every 6 months if stable
- Blood pressure every visit
- Lipid panel annually
- UACR annually
- eGFR annually
- Dilated eye exam at diagnosis then annually
- Foot exam at every visit

9. COMPLICATIONS
- Diabetic Ketoacidosis DKA: primarily T1DM; life-threatening
- Hyperosmolar Hyperglycaemic State HHS: primarily T2DM; life-threatening
- Hypoglycaemia: glucose < 70 mg/dL; severe if < 54 mg/dL
- Retinopathy: leading cause of blindness in working-age adults
- Nephropathy: leading cause of end-stage renal disease
- Neuropathy: peripheral and autonomic; risk of foot ulcers
- Coronary artery disease; stroke; peripheral artery disease

10. PATIENT EDUCATION
- Know your blood sugar targets and how to measure them
- Take all medications as prescribed; never skip doses
- Follow a balanced consistent meal plan
- Stay physically active daily
- Check your feet every day for sores blisters or redness
- Know the signs of hypoglycaemia and how to treat it
""",

"hypertension.txt": """
1. WHAT IS HYPERTENSION?
Hypertension is a chronic condition where the force of blood against artery walls is persistently elevated.
It is the most common modifiable cardiovascular risk factor known as the silent killer.
Defined as SBP >= 130 mmHg and/or DBP >= 80 mmHg on two or more occasions.

2. CLASSIFICATION
- Normal: SBP < 120 AND DBP < 80
- Elevated: SBP 120-129 AND DBP < 80
- Stage 1 HTN: SBP 130-139 OR DBP 80-89
- Stage 2 HTN: SBP >= 140 OR DBP >= 90
- Hypertensive Crisis: SBP > 180 AND/OR DBP > 120
Important: Hypertensive Emergency is BP > 180/120 with end-organ damage requiring ICU admission.

3. TYPES
- Primary Essential HTN: No identifiable single cause; 90-95% of cases
- Secondary HTN: CKD; primary aldosteronism; renovascular disease; OSA; thyroid disorders; medications

4. RISK FACTORS
- Age; family history; Black race; CKD
- Obesity; physical inactivity; high sodium diet > 2300 mg/day
- Excessive alcohol; smoking; chronic stress; diabetes; dyslipidemia

5. SIGNS AND SYMPTOMS
- Usually asymptomatic until severe
- Occipital headache; dizziness; visual disturbances
- Shortness of breath; chest pain; nosebleeds; fatigue
Note: Absence of symptoms does NOT mean BP is controlled.

6. DIAGNOSIS
- Patient seated quietly >= 5 minutes before measurement
- Feet flat; back supported; arm at heart level
- Take at least 2 readings 1-2 minutes apart
- ABPM is gold standard for 24-hour monitoring

7. BP TARGETS
- General adult population: < 130/80 mmHg
- Adults >= 65 years: < 130/80 mmHg if tolerated
- Diabetes mellitus: < 130/80 mmHg
- Chronic kidney disease: < 130/80 mmHg
- Pregnancy chronic HTN: < 140/90 mmHg

8. MANAGEMENT
- Weight loss: 1 mmHg per kg lost
- DASH diet: 8-14 mmHg reduction
- Sodium reduction < 1500 mg/day: 5-6 mmHg reduction
- Physical activity >= 150 min/week: 4-9 mmHg reduction
- Limit alcohol: 3-4 mmHg reduction
- ACE Inhibitor: lisinopril; preferred in DM+CKD; HF; post-MI
- ARB: losartan; used when ACEi not tolerated
- CCB: amlodipine; preferred in elderly; isolated systolic HTN
- Thiazide Diuretic: chlorthalidone; preferred in elderly; volume overload
- Beta-Blocker: metoprolol; preferred in CAD; HF; AF
- Aldosterone Antagonist: spironolactone; resistant HTN; HFrEF

9. MONITORING
- Recheck BP 1 month after initiating or changing therapy
- Once at goal and stable: follow-up every 3-6 months
- Home BP monitoring target average < 135/85 mmHg
- Annual cardiovascular risk assessment

10. COMPLICATIONS
- Coronary artery disease; myocardial infarction; left ventricular hypertrophy
- Heart failure; atrial fibrillation; aortic dissection
- Ischaemic and haemorrhagic stroke; TIA; vascular dementia
- CKD; end-stage renal disease; hypertensive retinopathy

11. PATIENT EDUCATION
- Take blood pressure medications every day even when you feel well
- Monitor BP at home; keep a log to share at each visit
- Follow a low-sodium diet; aim for < 1500 mg sodium per day
- Exercise at least 30 minutes most days; maintain a healthy weight
- Know warning signs of hypertensive crisis: severe headache; chest pain; sudden vision change
""",

"heart_failure.txt": """
1. DEFINITION
Heart failure is a clinical syndrome where the heart cannot pump sufficient blood to meet the body's metabolic needs or can do so only at elevated filling pressures.

2. CLASSIFICATION
- HFrEF: EF < 40% reduced ejection fraction
- HFmrEF: EF 41-49% mildly reduced
- HFpEF: EF >= 50% preserved ejection fraction
- NYHA Class I: No symptoms with ordinary activity
- NYHA Class II: Mild symptoms; slight limitation
- NYHA Class III: Marked limitation; comfortable only at rest
- NYHA Class IV: Symptoms at rest; unable to carry on any activity

3. CAUSES
- Ischaemic heart disease most common
- Hypertension; valvular disease; cardiomyopathy
- Arrhythmias AF; diabetes; alcohol; chemotherapy

4. SIGNS AND SYMPTOMS
- Dyspnoea on exertion; orthopnoea; paroxysmal nocturnal dyspnoea
- Peripheral oedema; JVD; hepatomegaly
- Fatigue; weight gain; reduced exercise tolerance
- S3 gallop; tachycardia; pulmonary crackles

5. DIAGNOSIS
- BNP >= 100 pg/mL or NT-proBNP >= 300 pg/mL
- Echocardiogram: EF wall motion valve function
- Chest X-ray: cardiomegaly pulmonary vascular congestion
- ECG: LVH prior MI arrhythmia

6. MANAGEMENT HFREF
- ACEi or ARB or ARNI sacubitril/valsartan: mortality benefit
- Beta-blocker: carvedilol; metoprolol succinate; bisoprolol
- Aldosterone antagonist: spironolactone; eplerenone
- SGLT-2 inhibitor: dapagliflozin; empagliflozin
- Loop diuretics: furosemide for congestion symptom relief only
- ICD if EF < 35% and NYHA II-III on optimal therapy
- CRT if EF <= 35% with LBBB and QRS >= 150 ms

7. MANAGEMENT HFPEF
- Treat underlying causes HTN AF obesity diabetes
- SGLT-2 inhibitors reduce HF hospitalisation
- Diuretics for congestion

8. MONITORING
- Daily weights; report gain > 2 lbs/day or > 5 lbs/week
- BMP renal function electrolytes every 1-6 months
- BNP at follow-up visits
- Echo every 1-2 years or after therapy change

9. ACUTE DECOMPENSATION
- IV diuresis furosemide 40-80 mg IV; strict fluid restriction
- Supplemental O2; continuous cardiac monitoring
- Identify precipitants: infection; AF; medication non-adherence
Warning: Sudden severe dyspnoea; chest pain; SpO2 < 90% call 911 immediately.

10. PATIENT EDUCATION
- Weigh daily; limit sodium < 2000 mg/day; fluid < 1.5-2 L/day
- Take all medications daily; never stop without physician advice
- Seek emergency care for sudden weight gain; severe dyspnoea; chest pain
""",

"ckd.txt": """
1. DEFINITION
CKD is defined as abnormalities of kidney structure or function present for > 3 months.
Diagnosed by eGFR < 60 mL/min/1.73m2 for >= 3 months OR markers of kidney damage such as UACR >= 30 mg/g.

2. STAGING
- Stage G1: eGFR >= 90 Normal with damage marker
- Stage G2: eGFR 60-89 Mildly decreased
- Stage G3a: eGFR 45-59 Mildly-moderately decreased
- Stage G3b: eGFR 30-44 Moderately-severely decreased
- Stage G4: eGFR 15-29 Severely decreased
- Stage G5: eGFR < 15 Kidney failure requiring RRT

3. CAUSES
- Diabetic nephropathy most common
- Hypertensive nephropathy; glomerulonephritis
- Polycystic kidney disease; obstructive uropathy
- NSAIDs; contrast; aminoglycosides nephrotoxicity

4. SIGNS AND SYMPTOMS
- Early: usually asymptomatic detected on screening labs
- Late Stage 4-5: fatigue; nausea; vomiting; anorexia; pruritus
- Oedema; dyspnoea; hypertension; anaemia; bone disease

5. MANAGEMENT
- BP control target < 130/80 mmHg; ACEi or ARB preferred
- Glycaemic control in diabetes HbA1c < 7-8%
- SGLT-2 inhibitors dapagliflozin empagliflozin reduce CKD progression
- Protein restriction 0.6-0.8 g/kg/day advanced CKD
- Avoid nephrotoxins: NSAIDs; IV contrast
- Anaemia: iron supplementation; ESA if Hgb < 10 g/dL
- Hyperkalaemia: dietary K+ restriction; patiromer
- Metabolic acidosis: sodium bicarbonate if HCO3 < 22 mEq/L

6. RENAL REPLACEMENT THERAPY
- Haemodialysis HD: 3x/week; AV fistula preferred access
- Peritoneal dialysis PD: home-based; continuous
- Kidney transplantation: preferred long-term option

7. MEDICATION ADJUSTMENTS
- Metformin: hold if eGFR < 30; caution 30-45
- NSAIDs: avoid in CKD worsens progression
- Gabapentin: reduce dose; accumulates in CKD
- DOACs: dose-adjust per product labelling

8. PATIENT EDUCATION
- Know your kidney numbers: eGFR and UACR
- Control blood pressure and blood sugar daily
- Avoid NSAIDs herbal supplements and nephrotoxic agents
- Follow a kidney-friendly diet: low sodium low potassium low phosphorus
""",

"copd.txt": """
1. DEFINITION
COPD is a persistent progressive airflow limitation caused by airway and alveolar abnormalities.
Diagnosed by FEV1/FVC < 0.70 post-bronchodilator spirometry.
Tobacco smoking accounts for 80-90% of cases.

2. GOLD CLASSIFICATION
- GOLD 1 Mild: FEV1 >= 80% predicted
- GOLD 2 Moderate: FEV1 50-79% predicted
- GOLD 3 Severe: FEV1 30-49% predicted
- GOLD 4 Very Severe: FEV1 < 30% predicted

3. RISK FACTORS
- Tobacco smoking most common
- Occupational dust and chemical exposure
- Indoor air pollution biomass fuel
- Alpha-1 antitrypsin deficiency genetic

4. SIGNS AND SYMPTOMS
- Chronic productive cough; increased sputum
- Progressive dyspnoea on exertion hallmark
- Wheeze; prolonged expiration; barrel chest
- Use of accessory muscles; pursed-lip breathing

5. INHALER THERAPY
- Group A: SAMA or SABA as needed
- Group B: LAMA preferred or LABA; add LABA+LAMA if symptomatic
- Group E: LAMA+LABA; add ICS if blood eos >= 300/uL
- Triple: ICS + LABA + LAMA eg Trelegy FF/UMEC/VI
- Roflumilast: severe COPD with chronic bronchitis and exacerbations
- Long-term O2 LTOT if PaO2 <= 55 mmHg or SpO2 <= 88%

6. EXACERBATION MANAGEMENT
- Mild: increase SABA; oral prednisolone 40 mg x 5 days
- Moderate: SABA + SAMA nebs; prednisolone; antibiotics if purulent sputum
- Severe: controlled O2 target SpO2 88-92%; nebs; steroids; antibiotics
- NIV if pH < 7.35 and PaCO2 elevated

7. MONITORING
- Spirometry annually
- SpO2 at each visit; ABG if SpO2 < 92%
- CAT or mMRC score at each visit
- Inhaler technique review at every visit

8. PATIENT EDUCATION
- Stop smoking: single most effective intervention
- Use inhalers correctly; demonstrate technique at every visit
- Recognise early signs of exacerbation: increased dyspnoea sputum changes wheeze
- Keep rescue inhaler SABA accessible at all times
- Stay up to date with all vaccinations
""",

"atrial_fibrillation.txt": """
1. DEFINITION
Atrial fibrillation is the most common sustained cardiac arrhythmia.
Characterised by disorganised atrial electrical activity with irregular often rapid ventricular response.

2. CLASSIFICATION
- Paroxysmal: self-terminating within 7 days usually < 48 hours
- Persistent: lasting > 7 days; requires cardioversion
- Long-standing persistent: continuous > 12 months
- Permanent: rhythm control no longer pursued

3. CAUSES AND RISK FACTORS
- Hypertension most common; HF; valvular disease; CAD
- Hyperthyroidism; obesity; OSA; alcohol
- Post-cardiac surgery; electrolyte disorders

4. SIGNS AND SYMPTOMS
- Palpitations; irregular heartbeat
- Dyspnoea; fatigue; reduced exercise tolerance
- Dizziness; pre-syncope; chest discomfort
- May be asymptomatic detected incidentally

5. STROKE RISK CHA2DS2-VASC
- C Congestive HF: 1 point
- H Hypertension: 1 point
- A Age >= 75: 2 points
- D Diabetes mellitus: 1 point
- S Stroke/TIA history: 2 points
- V Vascular disease MI PAD: 1 point
- A Age 65-74: 1 point
- Sc Sex category Female: 1 point
Score >= 2 male or >= 3 female: anticoagulate

6. ANTICOAGULATION
- Apixaban 5 mg BID preferred DOAC
- Rivaroxaban 20 mg daily with evening meal
- Dabigatran 150 mg BID
- Edoxaban 60 mg daily
- Warfarin if mechanical heart valve or severe mitral stenosis target INR 2-3

7. RATE CONTROL
- Target resting HR < 110 bpm lenient or < 80 bpm strict
- Beta-blockers: metoprolol; bisoprolol preferred
- Non-DHP CCBs: diltiazem; verapamil; avoid in HFrEF
- Digoxin: adjunct; useful in HF

8. RHYTHM CONTROL
- Electrical cardioversion DCCV: synchronised shock
- Flecainide propafenone: structurally normal heart only
- Amiodarone: most effective; significant toxicity
- Catheter ablation PVI: preferred for paroxysmal AF

9. MONITORING
- HR and rhythm at every visit
- Renal function and electrolytes annually
- TFTs annually especially if on amiodarone
- Echo every 1-2 years

10. PATIENT EDUCATION
- Take anticoagulant every day; do not miss doses
- Know signs of stroke: FAST Face drooping Arm weakness Speech difficulty Time to call 911
- Report palpitations; dizziness; worsening breathlessness
- Limit alcohol; treat OSA; manage weight
""",

"hyperlipidaemia.txt": """
1. DEFINITION
Hyperlipidaemia is elevation of lipids in the bloodstream.
A primary modifiable risk factor for atherosclerotic cardiovascular disease ASCVD.

2. LIPID TARGETS
- LDL-C general: < 100 mg/dL; high risk: < 70 mg/dL; very high risk: < 55 mg/dL
- HDL-C men: > 40 mg/dL; women: > 50 mg/dL
- Triglycerides: < 150 mg/dL
- Non-HDL-C: < 130 mg/dL general; < 100 mg/dL high risk

3. RISK CATEGORIES
- Very High Risk: established ASCVD prior MI stroke PAD ACS
- High Risk: LDL >= 190; diabetes age 40-75; 10-yr risk >= 20%
- Intermediate: 10-yr ASCVD risk 7.5-20%
- Low: 10-yr ASCVD risk < 7.5%

4. LIFESTYLE MODIFICATIONS
- Reduce saturated fat < 6% calories; eliminate trans fats
- Increase fibre omega-3s plant sterols
- Weight reduction if overweight
- Physical activity >= 150 min/week aerobic exercise
- Smoking cessation; limit alcohol

5. STATIN THERAPY
- High-intensity: atorvastatin 40-80 mg; rosuvastatin 20-40 mg; LDL reduction >= 50%
- Moderate-intensity: atorvastatin 10-20 mg; rosuvastatin 5-10 mg; LDL reduction 30-49%
- Side effects: myalgia; myopathy rare rhabdomyolysis; elevated LFTs

6. ADD-ON THERAPIES
- Ezetimibe 10 mg daily: inhibits intestinal cholesterol absorption; further LDL reduction 18-25%
- PCSK9 Inhibitors evolocumab alirocumab: injectable q2-4 weeks; LDL reduction 50-60%
- Inclisiran: twice-yearly siRNA injection; similar efficacy to PCSK9i
- Fibrates fenofibrate: hypertriglyceridaemia TG reduction 30-50%
- Omega-3 icosapentaenoic acid Vascepa 4 g/day: CV benefit

7. MONITORING
- Fasting lipid panel at baseline; 4-12 weeks after starting therapy; then every 3-12 months
- LFTs at baseline; recheck only if symptomatic
- CK at baseline; recheck if muscle symptoms develop

8. PATIENT EDUCATION
- Statins are protective; do not stop without physician advice
- Report muscle pain weakness or dark urine immediately
- Dietary changes complement but do not replace medication
- Know your LDL number and personal target
""",

"asthma.txt": """
1. DEFINITION
Asthma is a heterogeneous disease of chronic airway inflammation causing variable airflow limitation.
Diagnosed by FEV1/FVC < 0.70 with >= 12% and 200 mL reversibility after SABA.

2. CLASSIFICATION
- Intermittent: symptoms <= 2 days/week; FEV1 >= 80%
- Mild Persistent: symptoms > 2 days/week; nighttime 3-4/month; FEV1 >= 80%
- Moderate Persistent: daily symptoms; nighttime > 1/week; FEV1 60-79%
- Severe Persistent: continual symptoms; frequent nighttime; FEV1 < 60%

3. TRIGGERS
- Allergens: dust mites; pet dander; cockroach; mould; pollen
- Irritants: smoke; strong odours; air pollution; cold air
- Respiratory infections viral most common exacerbation trigger
- Exercise; aspirin NSAIDs beta-blockers; GERD; stress

4. STEP THERAPY GINA
- Step 1 Intermittent: low-dose ICS-formoterol PRN preferred or SABA PRN
- Step 2 Mild persistent: low-dose ICS daily or low-dose ICS-formoterol PRN
- Step 3 Moderate: low-dose ICS-LABA daily or medium-dose ICS
- Step 4 Severe: medium-dose ICS-LABA; add LAMA
- Step 5 Uncontrolled: high-dose ICS-LABA + LAMA; consider biologic; specialist referral

5. BIOLOGICS
- Omalizumab anti-IgE: allergic asthma elevated total IgE
- Mepolizumab benralizumab anti-IL-5: eosinophilic asthma
- Dupilumab anti-IL-4/13: type 2 inflammation; also treats eczema
- Tezepelumab anti-TSLP: broad type 2 and non-type 2 severe asthma

6. ACUTE EXACERBATION
- Mild-moderate: SABA 4-8 puffs q20 min x 3; prednisolone 40-50 mg x 5-7 days
- Severe: high-flow O2 target SpO2 93-95%; continuous SABA + ipratropium nebs
- IV magnesium sulphate 2 g over 20 min for severe exacerbation

7. MONITORING
- ACT or ACQ for symptom control at each visit
- Spirometry at diagnosis; after stabilisation; annually
- Inhaler technique and adherence at every visit
- Step down if controlled >= 3 months

8. PATIENT EDUCATION
- Use ICS every day even when feeling well; it prevents attacks
- Know difference between preventer ICS and reliever SABA inhalers
- Carry reliever inhaler at all times
- Identify and avoid personal triggers
- Have a written Asthma Action Plan
""",

"obesity.txt": """
1. DEFINITION AND CLASSIFICATION
Obesity is a chronic multifactorial disease of excess adiposity.
- BMI 25.0-29.9: Overweight
- BMI 30.0-34.9: Obesity Class I
- BMI 35.0-39.9: Obesity Class II
- BMI >= 40.0: Obesity Class III morbid/severe
Central adiposity: waist > 40 inches men; > 35 inches women

2. CAUSES
- Energy imbalance excess intake or insufficient expenditure
- Genetic predisposition; epigenetic factors
- Medications: corticosteroids; antipsychotics; insulin; antidepressants
- Hypothyroidism; Cushings syndrome; PCOS; sleep deprivation

3. HEALTH CONSEQUENCES
- T2DM; dyslipidaemia; metabolic syndrome; NAFLD
- Hypertension; CAD; HF; AF; stroke
- OSA; obesity hypoventilation; asthma
- Osteoarthritis; gout; infertility; PCOS
- Increased cancer risk: endometrial; breast; colorectal

4. LIFESTYLE INTERVENTION
- Dietary modification: hypocaloric diet deficit 500-750 kcal/day
- Physical activity >= 150 min/week aerobic; resistance training 2-3x/week
- Behavioural therapy: CBT; goal setting; self-monitoring
- Target >= 5% weight loss for metabolic benefit

5. PHARMACOTHERAPY
- Semaglutide sc Wegovy GLP-1 agonist: expected loss 15-17%
- Tirzepatide sc Zepbound GIP+GLP-1 dual: expected loss 20-22%
- Phentermine/topiramate Qsymia: expected loss 8-10%
- Naltrexone/bupropion Contrave: expected loss 5-8%
- Orlistat: lipase inhibitor; expected loss 3-5%

6. BARIATRIC SURGERY
- Sleeve gastrectomy: most common; 25% EWL; no malabsorption
- Roux-en-Y gastric bypass RYGB: 30-35% EWL; T2DM remission 60-80%
- BPD/DS: greatest weight loss; reserved for BMI > 50

7. MONITORING
- Weight and BMI at every visit
- Reassess comorbidities after >= 5% weight loss
- Post-bariatric: labs every 3-6 months vitamin B12 D iron folate calcium

8. PATIENT EDUCATION
- Obesity is a chronic disease not a personal failure
- Small sustainable changes are more effective than extreme diets
- Set realistic goals: 5-10% weight loss significantly improves health
- Maintain regular follow-up; weight regain is common and manageable
""",

"depression.txt": """
1. DEFINITION
Major Depressive Disorder MDD is a common serious mood disorder.
Characterised by persistent depressed mood or anhedonia that significantly impairs daily functioning.
Leading cause of disability worldwide.

2. DIAGNOSTIC CRITERIA DSM-5
>= 5 symptoms for >= 2 weeks including depressed mood OR anhedonia:
- Depressed mood most of the day nearly every day
- Markedly diminished interest or pleasure anhedonia
- Significant weight or appetite change > 5% in 1 month
- Insomnia or hypersomnia
- Psychomotor agitation or retardation
- Fatigue or loss of energy
- Feelings of worthlessness or excessive guilt
- Diminished concentration or indecisiveness
- Recurrent thoughts of death or suicidal ideation

3. SEVERITY PHQ-9
- Score 0-4: None/minimal; monitor and reassess
- Score 5-9: Mild; watchful waiting; psychotherapy; lifestyle
- Score 10-14: Moderate; psychotherapy and/or pharmacotherapy
- Score 15-19: Moderately severe; pharmacotherapy; consider referral
- Score >= 20: Severe; pharmacotherapy + psychotherapy; consider ECT

4. RISK FACTORS
- Prior depressive episodes; family history
- Chronic medical illness: diabetes; heart disease; cancer; CKD
- Substance use disorder; trauma; PTSD
- Social isolation; significant life stressors
- Female sex 2x higher risk; postpartum period

5. PSYCHOTHERAPY
- Cognitive Behavioural Therapy CBT: gold standard; most evidence
- Interpersonal Therapy IPT: especially for grief and relationship issues
- Behavioural Activation: effective for mild-moderate depression
- Mindfulness-Based CBT MBCT: relapse prevention
Note: Psychotherapy combined with pharmacotherapy is superior to either alone.

6. PHARMACOTHERAPY
- Sertraline SSRI 50-200 mg/day: first-line; fewest drug interactions
- Escitalopram SSRI 10-20 mg/day: clean side-effect profile
- Fluoxetine SSRI 20-60 mg/day: long half-life; useful if adherence concern
- Venlafaxine SNRI 75-225 mg/day: anxiety; chronic pain; depression
- Duloxetine SNRI 60-120 mg/day: diabetic neuropathy + depression
- Bupropion 150-450 mg/day: no sexual dysfunction; avoid if seizure risk
- Mirtazapine 15-45 mg/day: promotes sleep and appetite; useful in elderly
- Esketamine Spravato intranasal: rapid-onset; treatment-resistant depression
- ECT: most effective for severe/refractory depression; immediate suicide risk

7. SAFETY AND SUICIDAL IDEATION
- Always assess suicidality at every visit
- High risk: hospitalise; remove access to lethal means
Warning: SSRIs carry black-box warning for suicidal ideation in patients < 25 years.
- Crisis Line: 988 Suicide and Crisis Lifeline call or text 988

8. MONITORING
- PHQ-9 at each visit to track response
- Reassess 2-4 weeks after starting medication
- Full reassessment at 6-8 weeks
- Monitor weight sleep sexual function SSRI side effects

9. PATIENT EDUCATION
- Depression is a medical illness not a character weakness
- Antidepressants are not addictive; they take time to work 4-8 weeks
- Do not stop medications abruptly; taper under physician guidance
- Therapy and medication together work better than either alone
- Regular exercise reduces depression by 30%; improve sleep; limit alcohol
- Know crisis resources: 988 Suicide and Crisis Lifeline
"""
}


def populate():
    print("=== Populating condition files ===\n")
    for filename, content in CONDITIONS.items():
        filepath = os.path.join(CONDITIONS_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"  Written: {filename}")
    print(f"\nDone! {len(CONDITIONS)} files populated in: {CONDITIONS_DIR}")


if __name__ == "__main__":
    populate()