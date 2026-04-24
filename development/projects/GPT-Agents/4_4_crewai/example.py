from joke_crew import run_joke_crew

def main():
    # Пример 1: Базовая генерация шуток
    print("Пример 1: Генерация шуток про AI инженеров")
    result = run_joke_crew("AI engineer jokes")
    print(result)
    print("\n" + "="*50 + "\n")

    # Пример 2: Генерация шуток с переводом на несколько языков
    print("Пример 2: Генерация шуток с переводом")
    languages = ["Spanish", "French", "German"]
    result = run_joke_crew("AI engineer jokes", languages)
    print(result)
    print("\n" + "="*50 + "\n")

    # Пример 3: Генерация шуток на другую тему
    print("Пример 3: Генерация шуток про программирование")
    result = run_joke_crew("programming jokes")
    print(result)

if __name__ == "__main__":
    main() 