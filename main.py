name=input("Введите имя:")
surname = input("Введите фамилию:")
birth_year = input("Введите год рождения:")
CURRENT_YEAR = 2025
age = current_year - int(birth_year)
print(f"Здравствуйте{name} {surname} - вам {age} лет")