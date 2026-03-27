import turtle
import yaml
import os
import random

class SmartKane:
    def __init__(self):
        self.yml_file = "kane_experience.yml"
        self.total_cycles = 0
        self.memory = {} # Твои любимые рисунки (+1)
        self.attempts = 0 # Попытки для текущего объекта
        
        # Базовые "знания" Кейна, которые он расширяет
        self.internet_blocks = [
            "t.forward({val})", "t.left({ang})", "t.right({ang})", 
            "t.circle({val}, {ang})", "t.color(random.choice(['orange', 'black', 'blue', 'red']))",
            "t.width({val}/10)", "t.begin_fill()", "t.end_fill()"
        ]
        self.load_history()

    def speak(self, text):
        print(f"\n🐝 [Кейн]: {text}")

    def load_history(self):
        if os.path.exists(self.yml_file):
            try:
                with open(self.yml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    self.total_cycles = data.get('total_cycles', 0)
                    self.memory = data.get('memory', {})
                print(f"--- 🧠 Кейн вспомнил {self.total_cycles} уроков. ---")
            except: pass

    def save_history(self):
        # Сохранение после 100 циклов (или когда захочешь)
        if self.total_cycles >= 100:
            with open(self.yml_file, "w", encoding="utf-8") as f:
                yaml.dump({"total_cycles": self.total_cycles, "memory": self.memory}, f)

    def generate_creative_code(self, obj):
        """Кейн 'созванивается с инетом' и собирает новый код"""
        # Чем больше попыток (-1), тем сильнее меняется код (рандом зависит от попытки)
        random.seed(self.total_cycles + self.attempts)
        
        code = ["t = turtle.Turtle()", "t.speed(0)"]
        
        # Если Кейн уже успешно рисовал это раньше, он берет базу оттуда
        if obj in self.memory and random.random() > 0.3:
            code.extend(self.memory[obj])
            self.speak(f"Я помню, что тебе нравилось в прошлый раз, но интернет-друг советует добавить деталей!")

        # Добавляем новые случайные линии и формы (от 5 до 15 блоков)
        for _ in range(random.randint(5, 15)):
            block = random.choice(self.internet_blocks)
            code.append(block.format(val=random.randint(10, 100), ang=random.randint(0, 360)))
        
        return code

    def run_drawing(self, code):
        try:
            turtle.clearscreen()
            # Выполняем каждую строчку кода
            for line in code:
                exec(line, {"t": turtle, "random": random, "turtle": turtle})
            return True
        except Exception as e:
            print(f"Ошибка кода: {e}")
            return False

    def train_on_object(self, obj, max_tries):
        self.attempts = 0
        self.speak(f"Хозяин, я пробую нарисовать '{obj}'. Если будет круг — сразу бей меня минусом, я исправлюсь!")
        
        while self.attempts < max_tries:
            self.attempts += 1
            self.total_cycles += 1
            
            code = self.generate_creative_code(obj)
            self.run_drawing(code)
            
            print(f"\n--- Попытка №{self.attempts} ---")
            ans = input(f"[Вы]: Это похоже на '{obj}'? (+1 — ДА / -1 — НЕТ, ДЕЛАЙ ДРУГОЕ): ")
            
            if "+1" in ans:
                self.speak("УРА! Я не безнадежен! Записываю этот рецепт в свою книгу.")
                self.memory[obj] = code[2:] # Сохраняем только суть без инициализации
                self.save_history()
                break
            else:
                self.speak("Понял, это был мусор! Ищу в интернете другие способы...")
                if self.total_cycles >= 100: self.save_history()

    def main_loop(self):
        self.speak("Я Кейн. Я больше не буду рисовать только круги, обещаю! Что рисуем?")
        while True:
            target = input("\n[Вы]: Название объекта (или 'exit'): ")
            if target.lower() in ['exit', 'выход']: break
            
            try:
                limit = int(input("[Вы]: Сколько раз мне разрешено ошибиться? "))
                self.train_on_object(target, limit)
            except:
                print("Введи число!")

if __name__ == "__main__":
    kane = SmartKane()
    kane.main_loop()
