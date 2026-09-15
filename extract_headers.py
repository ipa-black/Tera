import os
import json

# اسم المجلد الذي يحتوي على الملفات بعد فك الضغط
header_dir = '8 Ball Pool_header'
result = {}

if not os.path.exists(header_dir):
    print(f"Error: Directory '{header_dir}' not found!")
    exit(1)

for filename in os.listdir(header_dir):
    if filename.endswith('.h'):
        filepath = os.path.join(header_dir, filename)
        class_name = filename.replace('.h', '')
        extracted_lines = []
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                
                # تجاهل الأسطر الفارغة أو الأقواس لوحدها أو استدعاءات المكاتب العادية
                if not line or line.startswith('#import') or line.startswith('#include') or line in ['{', '}', '};']:
                    continue
                
                # استخراج كل شيء مهم:
                # 1. أي سطر فيه 0x (أوفست)
                # 2. الدوال (تحتوي على أقواس)
                # 3. الخصائص المتغيرات
                # 4. أسماء الكلاسات
                if ('0x' in line.lower() or 
                    '(' in line or 
                    '@property' in line or 
                    '@interface' in line or 
                    'class ' in line or 
                    'struct ' in line):
                    
                    extracted_lines.append(line)
        
        # إذا وجدنا أي بيانات مهمة في الملف، نحفظها باسم الكلاس
        if extracted_lines:
            result[class_name] = extracted_lines

# حفظ الناتج في نفس ملف الـ JSON
with open('extracted_offsets.json', 'w', encoding='utf-8') as out_file:
    json.dump(result, out_file, indent=4, ensure_ascii=False)

print(f"✅ تم استخراج كل البيانات بنجاح من {len(result)} ملف!")
