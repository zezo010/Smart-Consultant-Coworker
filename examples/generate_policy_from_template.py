"""
Example: Generate Policy Document from Template

This example demonstrates how to:
1. Load a DOCX template with placeholders
2. Use the mapping file to map variables
3. Fill the template with client data
4. Generate a professional policy document
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hexagen_grc.common.schemas import ClientProfile, Language
from hexagen_grc.docs.template_manager import TemplateManager


def main():
    """Generate a policy document from template."""

    print("=" * 60)
    print("HexaGen GRC - Policy Generation from Template")
    print("=" * 60)
    print()

    # 1. Initialize Template Manager
    print("📋 Step 1: Initializing Template Manager...")
    template_manager = TemplateManager()

    # Display loaded variables
    variables = template_manager.list_all_variables()
    print(f"   ✓ Loaded {len(variables)} variables from mapping")
    print()

    # 2. Create Client Profile
    print("👤 Step 2: Creating Client Profile...")
    client = ClientProfile(
        client_id="CLIENT001",
        client_name="شركة الأمان المتقدم",
        client_name_ar="شركة الأمان المتقدم للاستشارات",
        client_name_en="Advanced Security Consulting Company",
        industry="Information Technology",
        sector="Cybersecurity Consulting",
        classification="Internal"
    )
    print(f"   ✓ Client: {client.client_name}")
    print()

    # 3. Prepare Document Information
    print("📄 Step 3: Preparing Document Information...")
    today = datetime.now()
    next_review = today + timedelta(days=365)

    document_info = {
        'policy_name_ar': 'سياسة إدارة المخاطر السيبرانية',
        'policy_name_en': 'Cybersecurity Risk Management Policy',
        'title': 'سياسة إدارة المخاطر السيبرانية',
        'doc_id': 'POL-CRMR-001',
        'version': '1.0',
        'classification': 'داخلي',
        'sharing_label': 'برتقالي',
        'applicability': 'جميع الإدارات والموظفين',
        'department_owner': 'إدارة الأمن السيبراني',
        'issue_year': today.year,
        'issue_date': today,
        'next_review_date': next_review,
        'prepared_by': 'فريق الأمن السيبراني - HexaGen',
        'reviewed_by': 'إدارة المخاطر المؤسسية',
        'approvals': {
            'name': 'أحمد محمد السالم',
            'title': 'الرئيس التنفيذي',
            'date': today
        }
    }
    print(f"   ✓ Policy: {document_info['policy_name_ar']}")
    print(f"   ✓ Doc ID: {document_info['doc_id']}")
    print()

    # 4. Prepare Generated Content
    print("✍️ Step 4: Preparing Generated Content...")
    generated_content = {
        'policy_blocks': """
1. الغرض
تهدف هذه السياسة إلى تحديد إطار عمل شامل لإدارة المخاطر السيبرانية في المنشأة، بما يتوافق مع متطلبات الهيئة الوطنية للأمن السيبراني [NCA-ECC-5-4-1].

2. النطاق
تطبق هذه السياسة على جميع الموظفين والمقاولين والشركاء الذين يستخدمون أنظمة المعلومات الخاصة بالمنشأة.

3. متطلبات السياسة
3.1 يجب على المنشأة تنفيذ عملية منهجية لإدارة المخاطر [NCA-ECC-5-4-1]
3.2 يجب إجراء تقييم دوري للمخاطر [NCA-ECC-5-4-2]
3.3 يجب توثيق جميع المخاطر المحددة في سجل المخاطر [ISO27001:6.1.2]
        """,
        'references': 'NCA ECC (الضوابط الأساسية للأمن السيبراني); ISO 27001:2022 (إدارة أمن المعلومات)',
        'contact': 'للاستفسارات: البريد الإلكتروني: grc@advancedsec.sa | الهاتف: +966-11-XXXXXXX',
        'appendices': ''
    }
    print(f"   ✓ Content prepared ({len(generated_content['policy_blocks'])} characters)")
    print()

    # 5. Build Variable Data
    print("🔧 Step 5: Building Variable Data...")
    variables_data = template_manager.build_variable_data(
        client_profile=client,
        document_info=document_info,
        generated_content=generated_content,
        language=Language.ARABIC
    )
    print(f"   ✓ Built {len(variables_data)} variables")
    print()

    # 6. Validate Variables
    print("✅ Step 6: Validating Variables...")
    validation = template_manager.validate_variables(variables_data)
    print(f"   ✓ Required: {validation['required_count']}")
    print(f"   ✓ Present: {validation['present_count']}")
    if validation['missing']:
        print(f"   ⚠️  Missing: {', '.join(validation['missing'])}")
    print()

    # 7. Fill Template (if exists)
    print("📝 Step 7: Filling Template...")

    # Note: You need to create the actual DOCX template first
    # For now, we'll show what would happen
    template_path = Path("templates/policies/policy_template_ar.docx")
    output_path = Path("data/outputs/generated_policy.docx")

    if template_path.exists():
        try:
            filled_doc = template_manager.fill_template(
                template_path=template_path,
                variables=variables_data,
                output_path=output_path,
                language=Language.ARABIC
            )
            print(f"   ✓ Document generated: {filled_doc}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
    else:
        print(f"   ℹ️  Template not found: {template_path}")
        print(f"   ℹ️  Create a DOCX template with placeholders like:")
        print()
        print("      {{HX.POLICY_NAME_AR}}")
        print("      {{HX.CLIENT_NAME_AR}}")
        print("      {{HX.DOC_ID}}")
        print("      etc.")
        print()
        print(f"   ℹ️  See templates/HexaGen_Policy_Template_Mapping.csv for all placeholders")

    print()
    print("=" * 60)
    print("✅ Example Complete!")
    print("=" * 60)
    print()

    # Display some sample mappings
    print("📊 Sample Variable Mappings:")
    print("-" * 60)
    sample_vars = [
        'CLIENT_NAME_AR',
        'POLICY_NAME_AR',
        'DOC_ID',
        'VERSION',
        'ISSUE_DATE',
        'CLASSIFICATION'
    ]

    for var_key in sample_vars:
        if var_key in variables_data:
            placeholder = template_manager.get_placeholder_map().get(var_key, '')
            value = variables_data[var_key]
            print(f"{placeholder:35} → {value}")

    print("-" * 60)
    print()


if __name__ == "__main__":
    main()
