import os
import json
import re

# اسم المجلد الذي يحتوي على الملفات (تأكد أن اسمه مطابق في مستودعك)
header_dir = '8 Ball Pool_header'
result = {}

# البحث عن الكلاسات والأوفستات (أي سطر ينتهي بـ // 0x...)
class_re = re.compile(r'@interface\s+([A-Za-z0-9_]+)')
offset_re = re.compile(r'(.*?)\s*//\s*(0x[0-9a-fA-F]+)')

if not os.path.exists(header_dir):
    print(f"Error: Directory '{header_dir}' not found!")
    exit(1)

for filename in os.listdir(header_dir):
    if filename.endswith('.h'):
        filepath = os.path.join(header_dir, filename)
        current_class = filename.replace('.h', '')
        class_data = {"offsets": []}
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                
                # تحديث اسم الكلاس إذا وجدناه في الكود
                match_class = class_re.search(line)
                if match_class:
                    current_class = match_class.group(1)
                
                # سحب الدالة/المتغير مع الأوفست
                match_offset = offset_re.search(line)
                if match_offset:
                    code_part = match_offset.group(1).strip()
                    offset_part = match_offset.group(2).strip()
                    if code_part:
                        class_data["offsets"].append({
                            "code": code_part,
                            "offset": offset_part
                        })
        
        # حفظ الكلاس فقط إذا كان يحتوي على أوفستات مهمة
        if class_data["offsets"]:
            result[current_class] = class_data

# تصدير النتيجة إلى ملف JSON
with open('extracted_offsets.json', 'w', encoding='utf-8') as out_file:
    json.dump(result, out_file, indent=4, ensure_ascii=False)

print("✅ تم استخراج جميع الأوفستات بنجاح إلى extracted_offsets.json")
