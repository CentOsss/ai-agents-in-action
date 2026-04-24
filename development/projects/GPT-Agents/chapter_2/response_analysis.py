import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from typing import Dict, Any, Optional

# Загрузка переменных окружения
load_dotenv()

# Инициализация клиента OpenAI
client = OpenAI()

class ResponseAnalyzer:
    def __init__(self):
        self.response_history = []
    
    def extract_response(self, response: Any) -> str:
        """
        Извлекает содержимое ответа из объекта ответа API
        
        Args:
            response: Объект ответа от API OpenAI
            
        Returns:
            str: Текст ответа или сообщение об ошибке
        """
        try:
            content = response.choices[0].message.content
            return content
        except Exception as e:
            return f"Ошибка при извлечении ответа: {str(e)}"
    
    def handle_response(self, response: Any) -> Dict[str, Any]:
        """
        Обрабатывает ответ API и возвращает структурированную информацию
        
        Args:
            response: Объект ответа от API OpenAI
            
        Returns:
            Dict[str, Any]: Словарь с информацией об ответе
        """
        result = {
            "content": self.extract_response(response),
            "finish_reason": response.choices[0].finish_reason,
            "usage": response.usage,
            "model": response.model
        }
        
        self.response_history.append(result)
        return result
    
    def analyze_quality(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Анализирует качество ответа
        
        Args:
            response: Словарь с информацией об ответе
            
        Returns:
            Dict[str, Any]: Результаты анализа
        """
        content = response["content"]
        
        analysis = {
            "length": len(content),
            "tokens_used": response["usage"].total_tokens,
            "completion_reason": response["finish_reason"],
            "has_error": "error" in content.lower(),
            "is_truncated": response["finish_reason"] == "length"
        }
        
        return analysis
    
    def get_response_history(self) -> list:
        """
        Возвращает историю ответов
        
        Returns:
            list: История ответов
        """
        return self.response_history

def main():
    analyzer = ResponseAnalyzer()
    
    # Пример запроса к API
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ]
    )
    
    # Обработка ответа
    processed_response = analyzer.handle_response(response)
    
    # Анализ качества
    quality_analysis = analyzer.analyze_quality(processed_response)
    
    # Вывод результатов
    print("Обработанный ответ:")
    print(json.dumps(processed_response, indent=2, ensure_ascii=False))
    print("\nАнализ качества:")
    print(json.dumps(quality_analysis, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main() 