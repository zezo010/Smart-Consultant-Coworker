# HexaGen GRC - Templates Guide

## 📋 نظرة عامة

هذا الدليل يشرح كيفية استخدام وإنشاء قوالب المستندات في HexaGen GRC.

---

## 🎯 نظام القوالب

### المكونات الرئيسية

1. **قوالب DOCX** - ملفات Word مع placeholders
2. **ملف Mapping** - Excel/CSV يربط المتغيرات بالـ placeholders
3. **Template Manager** - كود Python يملأ القوالب

---

## 📁 الملفات الأساسية

### 1. ملف الـ Mapping

**المسار**: `templates/HexaGen_Policy_Template_Mapping.csv`

**الأعمدة**:
- `VariableKey` - اسم المتغير (مثل: CLIENT_NAME_AR)
- `Placeholder` - النص في القالب (مثل: {{HX.CLIENT_NAME_AR}})
- `DataType` - نوع البيانات (text, date, enum, richtext)
- `Required` - هل المتغير مطلوب؟ (TRUE/FALSE)
- `Example_AR` - مثال بالعربية
- `Example_EN` - مثال بالإنجليزية
- `SourceField` - مصدر البيانات (client.name_ar, doc.version)

### 2. قوالب DOCX

**المسار**: `templates/policies/`

**أنواع القوالب**:
- `policy_template_ar.docx` - قالب السياسات (عربي)
- `policy_template_en.docx` - قالب السياسات (إنجليزي)
- `procedure_template_ar.docx` - قالب الإجراءات (عربي)
- `standard_template_ar.docx` - قالب المعايير (عربي)

---

## ✏️ إنشاء قالب DOCX جديد

### الخطوة 1: إنشاء ملف Word

1. افتح Microsoft Word
2. أنشئ مستند جديد
3. صمم الهيكل والتنسيق الذي تريده

### الخطوة 2: إضافة Placeholders

استخدم النمط: `{{HX.VARIABLE_NAME}}`

**مثال**:

```
{{HX.POLICY_NAME_AR}}
{{HX.POLICY_NAME_EN}}

{{HX.CLIENT_NAME_AR}}
{{HX.ISSUE_YEAR}}
```

### الخطوة 3: إنشاء جدول المعلومات

**مثال الجدول**:

| الحقل | القيمة |
|-------|--------|
| رقم الوثيقة | {{HX.DOC_ID}} |
| الإصدار | {{HX.VERSION}} |
| تاريخ الإصدار | {{HX.ISSUE_DATE}} |
| تاريخ المراجعة القادم | {{HX.NEXT_REVIEW_DATE}} |
| التصنيف | {{HX.CLASSIFICATION}} |
| إشارة المشاركة | {{HX.SHARING}} |
| نطاق التطبيق | {{HX.APPLICABILITY}} |

### الخطوة 4: حفظ القالب

احفظ الملف في:
```
templates/policies/your_template_ar.docx
```

---

## 🔧 المتغيرات المتاحة

### معلومات العميل

| Variable | Placeholder | مثال |
|----------|-------------|------|
| CLIENT_NAME_AR | {{HX.CLIENT_NAME_AR}} | شركة الأمان المتقدم |
| CLIENT_NAME_EN | {{HX.CLIENT_NAME_EN}} | Advanced Security Co. |

### معلومات الوثيقة

| Variable | Placeholder | مثال |
|----------|-------------|------|
| POLICY_NAME_AR | {{HX.POLICY_NAME_AR}} | سياسة إدارة المخاطر |
| POLICY_NAME_EN | {{HX.POLICY_NAME_EN}} | Risk Management Policy |
| DOC_ID | {{HX.DOC_ID}} | POL-CRMR-001 |
| VERSION | {{HX.VERSION}} | 1.0 |
| CLASSIFICATION | {{HX.CLASSIFICATION}} | داخلي |
| SHARING | {{HX.SHARING}} | برتقالي |
| APPLICABILITY | {{HX.APPLICABILITY}} | جميع الإدارات |

### التواريخ

| Variable | Placeholder | مثال |
|----------|-------------|------|
| ISSUE_YEAR | {{HX.ISSUE_YEAR}} | 2025 |
| ISSUE_DATE | {{HX.ISSUE_DATE}} | 01/10/2024 |
| NEXT_REVIEW_DATE | {{HX.NEXT_REVIEW_DATE}} | 01/11/2025 |
| EFFECTIVITY_DATE | {{HX.EFFECTIVITY_DATE}} | 01/12/2024 |

### المحتوى المُولَّد

| Variable | Placeholder | الوصف |
|----------|-------------|-------|
| POLICY_CONTENT | {{HX.POLICY_CONTENT}} | محتوى السياسة كاملاً |
| REFERENCES | {{HX.REFERENCES}} | المراجع والمعايير |
| CONTACT_INFO | {{HX.CONTACT_INFO}} | معلومات الاتصال |
| APPENDICES | {{HX.APPENDICES}} | الملاحق |

### معلومات الاعتماد

| Variable | Placeholder | مثال |
|----------|-------------|------|
| APPROVAL_NAME | {{HX.APPROVAL_NAME}} | محمد أحمد |
| APPROVAL_TITLE | {{HX.APPROVAL_TITLE}} | الرئيس التنفيذي |
| APPROVAL_DATE | {{HX.APPROVAL_DATE}} | 15/09/2024 |
| PREPARED_BY | {{HX.PREPARED_BY}} | فريق الأمن السيبراني |
| REVIEWED_BY | {{HX.REVIEWED_BY}} | إدارة المخاطر |

---

## 💻 استخدام القوالب في الكود

### مثال بسيط

```python
from hexagen_grc.docs.template_manager import TemplateManager
from hexagen_grc.common.schemas import ClientProfile, Language

# 1. Initialize Template Manager
tm = TemplateManager()

# 2. Create Client Profile
client = ClientProfile(
    client_id="CLIENT001",
    client_name="شركة الأمان",
    client_name_ar="شركة الأمان المتقدم",
    client_name_en="Advanced Security",
    industry="IT"
)

# 3. Prepare Document Info
document_info = {
    'policy_name_ar': 'سياسة الأمن السيبراني',
    'doc_id': 'POL-CS-001',
    'version': '1.0',
    'classification': 'داخلي'
}

# 4. Prepare Generated Content
generated_content = {
    'policy_blocks': 'محتوى السياسة...',
    'references': 'NCA ECC; ISO 27001'
}

# 5. Build Variables
variables = tm.build_variable_data(
    client_profile=client,
    document_info=document_info,
    generated_content=generated_content,
    language=Language.ARABIC
)

# 6. Fill Template
output = tm.fill_template(
    template_path=Path('templates/policies/policy_template_ar.docx'),
    variables=variables,
    output_path=Path('outputs/generated_policy.docx'),
    language=Language.ARABIC
)
```

---

## 📝 إضافة متغير جديد

### الخطوة 1: أضف إلى ملف Mapping

افتح `HexaGen_Policy_Template_Mapping.csv` وأضف سطر:

```csv
CUSTOM_FIELD,{{HX.CUSTOM_FIELD}},text,FALSE,قيمة عربية,English Value,custom.field
```

### الخطوة 2: أضف إلى القالب

في ملف DOCX، أضف:
```
{{HX.CUSTOM_FIELD}}
```

### الخطوة 3: قدّم القيمة في الكود

```python
variables['CUSTOM_FIELD'] = 'القيمة المطلوبة'
```

---

## 🎨 تنسيق النصوص العربية

### RTL (من اليمين لليسار)

القوالب العربية تُطبّق RTL تلقائياً عند استخدام `Language.ARABIC`

### الخطوط المناسبة

استخدم في القالب:
- **Arial** - للنصوص العامة
- **Sakkal Majalla** - للعناوين العربية
- **Traditional Arabic** - للنصوص الطويلة

---

## ✅ التحقق من القالب

### قبل الاستخدام

1. تأكد من وجود جميع الـ placeholders المطلوبة
2. تحقق من التنسيق والمحاذاة
3. اختبر مع بيانات نموذجية

### استخدام Validator

```python
# Validate required variables
validation = tm.validate_variables(variables)

if validation['missing']:
    print(f"Missing: {validation['missing']}")
else:
    print("All required variables present!")
```

---

## 🔍 استكشاف الأخطاء

### المشكلة: Placeholder لا يُستبدل

**الحل**:
1. تأكد أن النص يطابق تماماً ({{HX.VARIABLE_NAME}})
2. تحقق من عدم وجود مسافات زائدة
3. تأكد أن المتغير موجود في ملف Mapping

### المشكلة: النص العربي معكوس

**الحل**:
1. تأكد من استخدام `Language.ARABIC`
2. تحقق من إعدادات RTL في القالب الأصلي
3. استخدم خطوط داعمة للعربية

### المشكلة: الجدول يفقد التنسيق

**الحل**:
1. لا تستخدم placeholders طويلة في خلايا صغيرة
2. استخدم Content Controls في Word (متقدم)
3. املأ الجداول برمجياً بدلاً من placeholders

---

## 📚 أمثلة إضافية

### Example 1: إنشاء إجراء

```python
document_info = {
    'policy_name_ar': 'إجراء إدارة التغيير',
    'policy_name_en': 'Change Management Procedure',
    'doc_id': 'PROC-CHM-001',
    'version': '1.0'
}

output = tm.fill_template(
    template_path=Path('templates/procedures/procedure_template_ar.docx'),
    variables=variables,
    output_path=Path('outputs/change_management_procedure.docx')
)
```

### Example 2: إنشاء معيار

```python
document_info = {
    'policy_name_ar': 'معيار تشفير البيانات',
    'doc_id': 'STD-ENC-001',
    'version': '2.0'
}

output = tm.fill_template(
    template_path=Path('templates/standards/standard_template_ar.docx'),
    variables=variables,
    output_path=Path('outputs/encryption_standard.docx')
)
```

---

## 🚀 النصائح والممارسات الجيدة

### 1. التسمية

- استخدم أسماء واضحة للمتغيرات
- اتبع نمط موحد (UPPERCASE_WITH_UNDERSCORES)
- أضف اللغة في النهاية (_AR, _EN)

### 2. التنظيم

- احفظ القوالب في مجلدات منفصلة حسب النوع
- استخدم نظام إصدارات للقوالب
- وثّق التغييرات في ملف CHANGELOG

### 3. الصيانة

- راجع القوالب دورياً
- حدّث ملف Mapping عند إضافة متغيرات
- احتفظ بنسخ احتياطية من القوالب

### 4. الجودة

- اختبر مع بيانات حقيقية
- تحقق من جميع السيناريوهات (عربي/إنجليزي)
- اطلب مراجعة من المستخدمين النهائيين

---

## 📞 الدعم

للأسئلة والمساعدة:
- اقرأ التوثيق في `README.md`
- شاهد الأمثلة في `examples/`
- راجع الكود في `src/hexagen_grc/docs/`

---

**تم إنشاء هذا الدليل بواسطة HexaGen GRC Team**

**آخر تحديث**: 2024
