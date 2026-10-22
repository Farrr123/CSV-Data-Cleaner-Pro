import csv
import random

# قائمة أسماء عشوائية لاختبار التكرارات والتنسيقات
first_names = ["Ahmed", " Mohamed ", "ALI", "sara", "Fatma", "mahmoud", "Omar", "nour", "Youssef", "Aya"]
last_names = ["Ibrahim", "Hassan", "Ali", "Mohamed", "Khaled", "Samir", "Adel", "Nabil", "Saad", "Fathy"]
departments = ["IT", "it", "It", "iT", "HR", "hr", "Hr", "hR", "Sales", "marketing", "FINANCE"]
cities = ["Cairo", "alexandria", "Giza", "ASWAN", "Luxor", "Mansoura", "Tanta"]

data = []
# إضافة 1200 سطر تجريبي
for i in range(1, 1201):
    f_name = random.choice(first_names)
    l_name = random.choice(last_names)
    
    # إحداث مشاكل متعمدة في الأسماء (مسافات، حروف كلها صغيرة أو كبيرة)
    if i % 5 == 0:
        name = f"  {f_name} {l_name}   " # مسافات زائدة
    elif i % 7 == 0:
        name = f"{f_name.lower()} {l_name.lower()}" # كله سمول
    elif i % 9 == 0:
        name = f"{f_name.upper()} {l_name.upper()}  " # كله كابيتال مع مسافة
    else:
        name = f"{f_name} {l_name}"

    # تكرارات متعمدة لبعض الأسماء لاختبار ميزة حذف الدبلريت
    if i in [50, 150, 300, 500, 750, 1000]:
        name = "Ahmed Ibrahim"

    # إيميلات بمشاكل
    email = f"{f_name.lower()}.{l_name.lower()}{i}@example.com"
    if i % 11 == 0:
        email = f"  UPPER.{email} "

    # هواتف مفقودة لبعض المستخدمين
    phone = f"010{random.randint(10000000, 99999999)}"
    if i % 8 == 0 or i % 13 == 0:
        phone = "" # مفقود

    # أقسام مختلفة
    dept = random.choice(departments)

    # رواتب (بعضها غير صالح كحروف أو فارغ لاختبار Invalid salary)
    if i % 12 == 0:
        salary = "N/A"
    elif i % 19 == 0:
        salary = "Unknown"
    elif i % 25 == 0:
        salary = ""
    else:
        salary = str(random.randint(5000, 25000))

    city = random.choice(cities)
    if i % 6 == 0:
        city = city.lower()

    data.append({
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Department": dept,
        "Salary": salary,
        "City": city
    })

# كتابة البيانات في ملف الـ CSV
file_name = "employees_messy.csv"
with open(file_name, mode="w", encoding="utf-8", newline="") as f:
    fieldnames = ["Name", "Email", "Phone", "Department", "Salary", "City"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"تم إنشاء ملف '{file_name}' بنجاح يحتوي على {len(data)} سطر ومملوء بالمشاكل لاختبار الأداة! 🚀")