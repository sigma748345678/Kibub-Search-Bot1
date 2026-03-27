import requests
import turtle
import re
import yaml
import os
import random

# Вставь сюда свой токен с Hugging Face
HF_TOKEN = "ТВОЙ_HF_TOKEN_ЗДЕСЬ"
# Используем легкую, но умную модель (например, Zephyr или Mistral)
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

class InternetKane:
    def __init__(self):
        self.yml_file = "kane_memory.yml"
        self.headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        self.total_cycles = 0
        self.memory = {}
        self.load_history()

    def speak(self, text):
        print(f"🐝 [Кейн]: {text}")

    def load_history(self):
        if os.path.exists(self.yml_file):
            with open(self.yml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                self.total_cycles = data.get('total_cycles', 0)
                self.memory = data.get('memory', {})
            print(f"✅ Кейн загружен. Опыт: {self.total_cycles}")

    def query_internet(self, prompt):
        """Тот самый запрос через requests к 'интернет-мозгам'"""
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": 250}}
        response = requests.post(API_URL, headers=self.headers, json=payload)
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        else:
            return f"Ошибка связи: {response.status_code}"

    def get_code_from_web(self, obj):
        self.speak(f"Запрашиваю код для '{obj}' у интернет-друзей...")
        prompt = f"<|system|>\nТы помощник Python Turtle. Выдай только код.</s>\n<|user|>\nНапиши код на Python (turtle) для рисования {obj}. Используй t = turtle.Turtle(). Код оберни в ```python ```.</s>\n<|assistant|>"
        return self.query_internet(prompt)

    def verify_with_internet(self, code, obj):
        """Автоматическая проверка кода через интернет"""
        self.speak("Отправляю код на проверку интернет-учителю...")
        prompt = f"<|system|>\nТы строгий учитель. Если код рисует {obj}, напиши '+1'. Если нет, напиши '-1'.</s>\n<|user|>\nПроверь этот код:\n{code}</s>\n<|assistant|>"
        return self.query_internet(prompt)

    def draw(self, code):
        try:
            turtle.clearscreen()
            t = turtle.Turtle()
            t.speed(0)
            # Выполняем код, который прислал интернет
            exec(code, {"t": t, "turtle": turtle})
            return True
        except Exception as e:
            print(f"⚠️ Ошибка в коде: {e}")
            return False

    def start_cycle(self, obj):
        self.total_cycles += 1
        raw_answer = self.get_code_from_web(obj)
        
        # Вытаскиваем код из ответа
        match = re.search(r'```python\n(.*?)\n```', raw_answer, re.DOTALL)
        if not match:
            self.speak("Интернет прислал что-то странное, попробую еще раз.")
            return

        code = match.group(1)
        
        # Авто-проверка через интернет
        verdict = self.verify_with_internet(code, obj)
        print(f"🎓 [Интернет-Учитель]: {verdict}")

        if "+1" in verdict:
            self.speak(f"Учитель одобрил! Рисую {obj}.")
            if self.draw(code):
                self.memory[obj] = code
                if self.total_cycles >= 100:
                    with open(self.yml_file, "w") as f:
                        yaml.dump({"total_cycles": self.total_cycles, "memory": self.memory}, f)
        else:
            self.speak("Учитель сказал, что код плохой. Попробую позже.")

    def run(self):
        while True:
            target = input("\n[Вы]: Что Кейну нарисовать? (exit): ")
            if target.lower() in ['exit', 'выход']: break
            self.start_cycle(target)

if __name__ == "__main__":
    kane = InternetKane()
    kane.run()
