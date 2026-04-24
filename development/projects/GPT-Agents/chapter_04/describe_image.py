import base64
import os
import requests
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

def describe_image(image_path="animals.png") -> str:
    """
    Uses GPT-4 Vision to inspect and describe the contents of the image.

    :param image_path: str, the name of the PNG file to describe.
    :return: str, description of the image
    :raises: FileNotFoundError if image file not found
    :raises: KeyError if API key not found
    :raises: requests.exceptions.RequestException for API errors
    """
    try:
        api_key = os.environ['OPENAI_API_KEY']
        base_url = os.environ.get('OPENAI_API_BASE', 'https://bothub.chat/api/v2/openai/v1/')
        
        # Function to encode the image
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")

        # Getting the base64 string
        base64_image = encode_image(image_path)

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

        payload = {
            "model": "gpt-4-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What's in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ],
            "max_tokens": 300,
        }

        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()  # Проверка на HTTP ошибки

        return response.json()["choices"][0]["message"]["content"]
        
    except FileNotFoundError:
        return f"Ошибка: Файл изображения не найден: {image_path}"
    except KeyError:
        return "Ошибка: OPENAI_API_KEY не найден в переменных окружения"
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе к API: {str(e)}"
    except Exception as e:
        return f"Непредвиденная ошибка: {str(e)}"


if __name__ == "__main__":
    # Пример использования
    result = describe_image()
    print(result)
