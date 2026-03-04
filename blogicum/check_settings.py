import sys
sys.path.insert(0, '.')
try:
    from blogicum import settings
    print("✅ settings.py импортируется успешно")
    print(f"BASE_DIR: {settings.BASE_DIR}")
    print(f"TEMPLATES_DIR: {settings.TEMPLATES_DIR}")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
