import base64
import requests

# Данные из вашего _prompt для API OpenAI
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjIzYmE2ZjUyLTJjMDMtNGIwZC1hODU5LTUwYWJmYjM5M2VhZCIsImlzRGV2ZWxvcGVyIjp0cnVlLCJpYXQiOjE3NDI1NDIwNDgsImV4cCI6MjA1ODExODA0OH0.2-iGay6r98RWNLRZZ3iAZU-l8FRbg7KQkvtLXAdqYpE"
BASE_URL = "https://bothub.chat/api/v2/openai/v1/"
COMPLETIONS_ENDPOINT = BASE_URL.rstrip('/') + "/chat/completions"

def describe_image(image_path: str) -> str:
    """
    Использует GPT-4 Vision для осмотра и описания содержимого изображения.
    Принимает путь к файлу изображения (image_path) и возвращает его описание.
    В контексте AutoGen Studio, image_path может быть относительным путем к файлу 
    в рабочей директории агента или абсолютным путем.
    """
    api_key_to_use = API_KEY

    try:
        # Функция для кодирования изображения в формат Base64
        def encode_image(current_image_path):
            with open(current_image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        base64_image = encode_image(image_path)
    except FileNotFoundError:
        return f"Ошибка: Файл изображения не найден по пути: {image_path}"
    except Exception as e:
        return f"Ошибка при кодировании изображения: {str(e)}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key_to_use}"
    }

    payload = {
        "model": "gpt-4-turbo", # Модель для Vision, как в примере из книги
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}" # Предполагаем JPEG
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    
    try:
        response = requests.post(COMPLETIONS_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status() # Проверка на HTTP ошибки (4xx, 5xx)
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Ошибка сети или API при запросе к {COMPLETIONS_ENDPOINT}: {str(e)}"
    except (KeyError, IndexError) as e:
        # Попытка получить больше информации из ответа, если он есть
        error_details = response.text if 'response' in locals() and hasattr(response, 'text') else 'Нет деталей ответа'
        return f"Ошибка при обработке ответа от API: {str(e)}. Ответ: {error_details}"
    except Exception as e:
        return f"Непредвиденная ошибка при вызове API: {str(e)}"

if __name__ == '__main__':
    # Этот блок для локального тестирования скрипта.
    # Он не будет выполняться, когда функция вызывается как навык в AutoGen Studio.
    print("Скрипт describe_image.py запущен для локального теста.")
    print(f"API Key (первые 5 символов): {API_KEY[:5]}...")
    print(f"Endpoint: {COMPLETIONS_ENDPOINT}")
    
    # Замените 'path_to_your_test_image.png' на реальный путь к изображению для теста.
    # Убедитесь, что изображение существует по этому пути.
    test_image_path = input("Введите путь к тестовому изображению (например, test.png): ")
    
    if test_image_path:
        print(f"\nОписание для изображения '{test_image_path}':")
        description = describe_image(test_image_path)
        print(description)
    else:
        print("Путь к изображению не указан. Тест не выполнен.")

    # Пример создания простого пустого файла для теста, если нужно:
    # with open("empty_test_image.png", "w") as f:
    #     f.write("")
    # print(describe_image("empty_test_image.png")) 