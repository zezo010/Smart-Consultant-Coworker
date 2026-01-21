# دليل تنظيم ملفات الأنظمة التشريعية (Frameworks)

## 📋 نظرة عامة

هذا الدليل يشرح كيفية تنظيم جميع ملفات الأنظمة التشريعية (Frameworks) في HexaGen GRC.

---

## 📁 الهيكل العام

```
frameworks/
├── NCA/              # الهيئة الوطنية للأمن السيبراني
│   ├── ECC/          # الضوابط الأساسية
│   ├── CCC/          # ضوابط الحوسبة السحابية
│   ├── DCC/          # ضوابط البيانات
│   ├── CSCC/         # ضوابط الأمن السيبراني للأنظمة الحرجة
│   ├── OSMACC/       # ضوابط الأمن السيبراني للتوريد
│   ├── OTCC/         # ضوابط تقنية التشغيل
│   └── TCC/          # ضوابط التكنولوجيا
│
├── ISO/              # المنظمة الدولية للمعايير
│   ├── 27001/        # إدارة أمن المعلومات
│   ├── 27002/        # ضوابط أمن المعلومات
│   ├── 31000/        # إدارة المخاطر
│   └── 22301/        # استمرارية الأعمال
│
├── PDPL/             # نظام حماية البيانات الشخصية
├── NDMO/             # المكتب الوطني لإدارة البيانات
├── SAMA/             # مؤسسة النقد العربي السعودي
├── NIS2/             # توجيه أمن الشبكات والمعلومات (EU)
├── CST/              # إطار تصنيف التهديدات السيبرانية
│
└── mappings/         # المقارنات بين الأنظمة
    ├── NCA_to_ISO.xlsx
    ├── ECC_to_CCC.xlsx
    └── Multi_Framework_Mapping.xlsx
```

---

## 🗂️ التنظيم التفصيلي لكل نظام

### مثال: NCA ECC

```
frameworks/NCA/ECC/
│
├── source_excel/              📊 الملفات الأصلية من Excel
│   ├── NCA_ECC_Controls_AR.xlsx
│   ├── NCA_ECC_Controls_EN.xlsx
│   ├── NCA_ECC_Controls_Bilingual.xlsx
│   └── NCA_ECC_Implementation_Guide.xlsx
│
├── source_pdf/                📄 الملفات الأصلية من PDF
│   ├── NCA_ECC_Official_AR.pdf
│   ├── NCA_ECC_Official_EN.pdf
│   └── NCA_ECC_FAQ.pdf
│
├── controls/                  🎯 الضوابط (بعد المعالجة)
│   ├── controls_master.xlsx        ← الملف الرئيسي
│   ├── controls_ar.csv              ← للاستيراد السريع
│   ├── controls_en.csv
│   ├── controls_by_domain/          ← تصنيف حسب المجال
│   │   ├── governance.xlsx
│   │   ├── risk_management.xlsx
│   │   ├── asset_management.xlsx
│   │   └── ...
│   └── controls_by_level/           ← تصنيف حسب المستوى
│       ├── strategic.xlsx
│       ├── operational.xlsx
│       └── technical.xlsx
│
├── requirements/              📋 المتطلبات التفصيلية
│   ├── all_requirements.xlsx        ← جميع المتطلبات
│   ├── requirements_index.csv       ← فهرس سريع
│   ├── by_control/                  ← متطلبات لكل ضابط
│   │   ├── ECC_5_1_1_requirements.xlsx
│   │   ├── ECC_5_1_2_requirements.xlsx
│   │   └── ...
│   └── by_maturity/                 ← حسب مستوى النضج
│       ├── level1_basic.xlsx
│       ├── level2_intermediate.xlsx
│       └── level3_advanced.xlsx
│
├── evidence_catalog/          📑 كتالوج الأدلة
│   ├── evidence_master.xlsx         ← كتالوج شامل
│   ├── evidence_by_control.xlsx     ← حسب الضابط
│   ├── evidence_by_department.xlsx  ← حسب الإدارة
│   ├── evidence_templates/          ← قوالب الأدلة
│   │   ├── policy_template.docx
│   │   ├── procedure_template.docx
│   │   └── record_template.xlsx
│   └── sample_evidence/             ← أمثلة
│       └── ...
│
├── gap_assessments/           📊 تقييمات الفجوات
│   ├── gap_template.xlsx            ← قالب Gap Assessment
│   ├── gap_methodology.docx         ← منهجية التقييم
│   ├── client_gaps/                 ← تقييمات العملاء
│   │   ├── CLIENT001/
│   │   │   ├── initial_assessment.xlsx
│   │   │   ├── reassessment_Q1.xlsx
│   │   │   └── findings_summary.xlsx
│   │   └── CLIENT002/
│   │       └── ...
│   └── gap_reports/                 ← تقارير الفجوات
│       └── [Generated reports]
│
├── trackers/                  📈 متابعة التنفيذ
│   ├── implementation_tracker.xlsx  ← متابعة التنفيذ
│   ├── compliance_tracker.xlsx      ← متابعة الامتثال
│   ├── remediation_tracker.xlsx     ← خطط المعالجة
│   ├── project_plan.xlsx            ← خطة المشروع
│   └── milestones.xlsx              ← المعالم الرئيسية
│
├── mappings/                  🔗 المقارنات
│   ├── ECC_to_ISO27001.xlsx
│   ├── ECC_to_CCC.xlsx
│   ├── ECC_to_PDPL.xlsx
│   ├── ECC_to_SAMA.xlsx
│   └── cross_reference_matrix.xlsx
│
├── references/                📚 المراجع
│   ├── official_guides/
│   │   ├── implementation_guide.pdf
│   │   └── interpretation_guide.pdf
│   ├── faqs/
│   │   └── NCA_FAQ.pdf
│   ├── case_studies/
│   │   └── ...
│   └── best_practices/
│       └── ...
│
├── processed_json/            🔧 بيانات معالجة (تلقائي)
│   ├── controls.json
│   ├── requirements.json
│   ├── evidence.json
│   └── metadata.json
│
└── README.md                  📖 وثائق خاصة بـ ECC
```

---

## 📝 هيكل الملفات الموصى به

### 1. Controls File (الضوابط)

**اسم الملف**: `controls_master.xlsx`

**الأعمدة الأساسية**:

| Column | وصف | مثال |
|--------|-----|------|
| control_id | رقم الضابط | ECC-5-1-1 |
| control_title_ar | العنوان (عربي) | إدارة أمن المعلومات |
| control_title_en | العنوان (إنجليزي) | Information Security Management |
| domain | المجال | Governance |
| level | المستوى | Strategic |
| requirements_ar | المتطلبات (عربي) | يجب على المنشأة... |
| requirements_en | المتطلبات (إنجليزي) | Organization must... |
| implementation_guidance_ar | إرشادات التنفيذ | ... |
| expected_evidence | الأدلة المطلوبة | ISMS Policy, Framework Doc |
| maturity_level | مستوى النضج | Basic / Intermediate / Advanced |
| priority | الأولوية | Critical / High / Medium / Low |

---

### 2. Requirements File (المتطلبات التفصيلية)

**اسم الملف**: `all_requirements.xlsx` أو `by_control/ECC_5_1_1_requirements.xlsx`

**الأعمدة**:

| Column | وصف | مثال |
|--------|-----|------|
| requirement_id | رقم المتطلب | ECC-5-1-1-REQ-01 |
| control_id | رقم الضابط | ECC-5-1-1 |
| requirement_ar | المتطلب (عربي) | يجب توثيق نطاق ISMS |
| requirement_en | المتطلب (إنجليزي) | ISMS scope must be documented |
| type | نوع المتطلب | Mandatory / Recommended |
| implementation_steps | خطوات التنفيذ | 1. تحديد الحدود 2. ... |
| evidence_required | الأدلة المطلوبة | ISMS Scope Document |
| verification_method | طريقة التحقق | Document Review |
| responsible_role | الدور المسؤول | CISO |

---

### 3. Gap Assessment File (تقييم الفجوات)

**اسم الملف**: `CLIENT001_ECC_Gap_Assessment.xlsx`

**Sheets**:
1. **Summary** - ملخص التقييم
2. **Detailed Findings** - النتائج التفصيلية
3. **Action Plan** - خطة العمل
4. **Timeline** - الجدول الزمني

**الأعمدة (Detailed Findings)**:

| Column | وصف | مثال |
|--------|-----|------|
| control_id | رقم الضابط | ECC-5-1-1 |
| control_title | عنوان الضابط | ISMS |
| current_status | الوضع الحالي | Not Implemented / Partial / Implemented |
| maturity_level | مستوى النضج الحالي | 0-5 |
| target_maturity | المستوى المستهدف | 0-5 |
| gap_level | مستوى الفجوة | Critical / High / Medium / Low |
| findings_ar | النتائج (عربي) | لا يوجد ISMS موثق |
| findings_en | النتائج (إنجليزي) | No documented ISMS |
| evidence_found | الأدلة الموجودة | None / List of documents |
| evidence_missing | الأدلة المفقودة | ISMS Policy, Scope Document |
| recommendations_ar | التوصيات | إنشاء وثيقة ISMS |
| priority | الأولوية | Critical / High / Medium / Low |
| estimated_effort | الجهد المقدر | Days / Weeks |
| assigned_to | المسؤول | Department / Person |
| due_date | تاريخ الاستحقاق | 2025-03-01 |
| status | حالة المعالجة | Open / In Progress / Completed |

---

### 4. Evidence Catalog (كتالوج الأدلة)

**اسم الملف**: `evidence_by_control.xlsx`

**الأعمدة**:

| Column | وصف | مثال |
|--------|-----|------|
| control_id | رقم الضابط | ECC-5-1-1 |
| evidence_type | نوع الدليل | Policy / Procedure / Record |
| evidence_name_ar | اسم الدليل (عربي) | سياسة ISMS |
| evidence_name_en | اسم الدليل (إنجليزي) | ISMS Policy |
| template_available | توفر قالب | Yes / No |
| template_path | مسار القالب | templates/policies/isms_policy.docx |
| responsible_dept | الإدارة المسؤولة | IT Security |
| creation_frequency | تكرار الإنشاء | Once / Annual / Monthly |
| retention_period | مدة الاحتفاظ | 3 years / Permanent |
| format | الصيغة | DOCX / PDF / XLSX |

---

### 5. Mapping File (المقارنات)

**اسم الملف**: `ECC_to_ISO27001.xlsx`

**الأعمدة**:

| Column | وصف | مثال |
|--------|-----|------|
| source_framework | النظام المصدر | NCA_ECC |
| source_control_id | رقم الضابط المصدر | ECC-5-1-1 |
| source_title | عنوان المصدر | ISMS |
| target_framework | النظام المستهدف | ISO_27001 |
| target_control_id | رقم الضابط المستهدف | 4.1 |
| target_title | عنوان المستهدف | Understanding the organization |
| mapping_type | نوع المقارنة | Direct / Partial / Related / No Match |
| coverage_percentage | نسبة التغطية | 100% / 75% / 50% / 25% |
| notes | ملاحظات | Both require ISMS establishment |

---

## 🚀 سير العمل (Workflow)

### الخطوة 1: استلام الملفات الأصلية

```
1. احصل على ملفات Excel/PDF من الجهة الرسمية
2. ضعها في: source_excel/ أو source_pdf/
3. لا تعدّل الملفات الأصلية
```

### الخطوة 2: المعالجة والتنظيم

```
1. افتح الملف الأصلي
2. نظّم البيانات حسب الهيكل الموصى به
3. احفظ في المجلد المناسب (controls/, requirements/, etc.)
```

### الخطوة 3: Ingestion إلى النظام

```bash
# طريقة 1: CLI
hexagen ingest NCA_ECC frameworks/NCA/ECC/controls/controls_master.xlsx

# طريقة 2: Script
python examples/ingest_framework_files.py --mode all

# طريقة 3: Directory
python examples/ingest_framework_files.py --mode directory \
  --path frameworks/NCA/ECC/source_excel
```

### الخطوة 4: التحقق

```bash
# تحقق من الإحصائيات
hexagen stats

# ابحث لاختبار البيانات
hexagen search "إدارة أمن المعلومات" --framework NCA_ECC
```

---

## 📊 أمثلة عملية

### مثال 1: إضافة ضوابط NCA ECC

```bash
1. ضع الملف في:
   frameworks/NCA/ECC/source_excel/NCA_ECC_Controls.xlsx

2. Ingest:
   hexagen ingest NCA_ECC frameworks/NCA/ECC/source_excel/NCA_ECC_Controls.xlsx

3. التحقق:
   hexagen search "ECC-5-1-1" --framework NCA_ECC
```

### مثال 2: إضافة Gap Assessment لعميل

```bash
1. أنشئ مجلد للعميل:
   frameworks/NCA/ECC/gap_assessments/client_gaps/CLIENT001/

2. ضع ملف Gap:
   frameworks/NCA/ECC/gap_assessments/client_gaps/CLIENT001/initial_gap.xlsx

3. Ingest:
   python examples/ingest_framework_files.py --mode gap \
     --path frameworks/NCA/ECC/gap_assessments/client_gaps/CLIENT001/initial_gap.xlsx \
     --client-id CLIENT001
```

### مثال 3: إضافة متطلبات تفصيلية

```bash
1. ضع ملفات المتطلبات في:
   frameworks/NCA/ECC/requirements/

2. Ingest جميع الملفات:
   python examples/ingest_framework_files.py --mode directory \
     --path frameworks/NCA/ECC/requirements
```

---

## ✅ قائمة التحقق

قبل Ingestion، تأكد من:

- [ ] الملف في المجلد الصحيح
- [ ] الأعمدة تتبع الهيكل الموصى به
- [ ] لا توجد قيم فارغة في الأعمدة الأساسية
- [ ] التواريخ بصيغة صحيحة
- [ ] النصوص العربية بدون مشاكل encoding
- [ ] control_id فريد لا يتكرر

---

## 🔍 استكشاف الأخطاء

### المشكلة: ملف لم يُستورد

**الحل**:
1. تحقق من المسار
2. تحقق من صيغة الملف (.xlsx)
3. تحقق من الأعمدة المطلوبة
4. راجع الـ logs

### المشكلة: نصوص عربية معطوبة

**الحل**:
1. احفظ الملف بـ UTF-8 encoding
2. استخدم Excel بدلاً من CSV
3. تحقق من الخط المستخدم

---

## 📞 للمساعدة

راجع:
- `examples/ingest_framework_files.py`
- `README.md`
- `QUICKSTART.md`

---

**تم إعداده بواسطة فريق HexaGen GRC**
