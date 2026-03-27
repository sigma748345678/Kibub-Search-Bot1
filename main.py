import turtle
import yaml
import os
import time
import requests # Нужен: pip install requests

class KaneTheExplorer:
    def __init__(self):
        self.yml_file = "kane_memory.yml"
        self.total_cycles = 0
        self.memory = {} # Здесь храним лучшие находки из интернета
        self.character_name = "Кейн"
        
        # Кейн любит пчелок
        self.bee_art = "🐝"
        self.load_history()

    def speak(self, text):
        print(f"\n{self.bee_art} [{self.character_name}]: {text}")

    def load_history(self):
        if os.path.exists(self.yml_file):
            try:
                with open(self.yml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    self.total_cycles = data.get('total_cycles', 0)
                    self.memory = data.get('memory', {})
                print(f"--- 🧠 Кейн проснулся! Опыт: {self.total_cycles} циклов. ---")
            except:
                print("--- 🧠 Кейн начинает с чистого листа. ---")

    def save_history(self):
        # Сохраняем, если прошли порог в 100 циклов
        if self.total_cycles >= 100:
            with open(self.yml_file, "w", encoding="utf-8") as f:
                yaml.dump({"total_cycles": self.total_cycles, "memory": self.memory}, f, allow_unicode=True)

    def internet_friend_help(self, obj):
        """Кейн 'звонит' своему другу Интернету за помощью"""
        self.speak(f"Минутку! Мой верный друг Интернет сейчас расскажет мне, как рисовать {obj}...")
        time.sleep(1) # Имитация поиска
        
        # В реальном мире здесь может быть парсинг. 
        # Но чтобы ноут не лагал, мы используем базу знаний Кейна, 
        # которую он расширяет через 'поиск' (в данном случае через шаблоны).
        templates = {
            "пчелка": ["t.circle(20)", "t.color('yellow')", "t.begin_fill()", "t.circle(30)", "t.end_fill()", "t.color('black')", "t.width(5)", "t.circle(30, 180)"],
            "дом": ["t.forward(100)", "t.left(90)", "t.forward(100)", "t.left(90)", "t.forward(100)", "t.left(90)", "t.forward(100)", "t.left(30)", "t.forward(100)", "t.left(120)", "t.forward(100)"],
            "цветок": ["for i in range(36): t.forward(50); t.backward(50); t.left(10)"]
        }
        
        # Если объекта нет в шаблонах, Кейн пытается 'сочинить' его на основе геометрии из интернета
        found_code = templates.get(obj.lower(), ["t.circle(50)", "t.left(90)", "t.forward(100)"])
        return found_code

    def draw(self, commands):
        try:
            turtle.clearscreen()
            t = turtle.Turtle()
            t.speed(0)
            for cmd in commands:
                # Безопасное исполнение каждой команды
                exec(cmd, {"t": t})
            return True
        except Exception as e:
            self.speak(f"Ой, интернет дал немного ломанный код: {e}")
            return False

    def train(self, obj, cycles_to_do):
        self.speak(f"Я хочу угодить тебе! Начинаю {cycles_to_do} циклов обучения рисованию '{obj}'.")
        
        success_found = False
        for i in range(1, cycles_to_do + 1):
            self.total_cycles += 1
            print(f"🌀 Цикл {i}/{cycles_to_do} (Общий опыт: {self.total_cycles})")
            
            # Кейн берет код у 'друга'
            code = self.internet_friend_help(obj)
            
            # Пытается нарисовать
            if self.draw(code):
                ans = input(f"\n[Вы]: Похоже на {obj}? (+1 - Супер! / -1 - Плохо): ")
                
                if "+1" in ans:
                    self.speak("Ура! Я и мой друг Интернет справились! Пчелки были бы рады за нас.")
                    self.memory[obj] = code
                    self.save_history()
                    success_found = True
                    break
                else:
                    self.speak("Эх, интернет подвел... Попробую найти другой способ в следующем цикле!")
            
            if self.total_cycles >= 100:
                self.save_history()
        
        if not success_found:
            self.speak("Я не смог достичь идеала за этот раз, но я буду стараться еще больше!")

    def run(self):
        self.speak("Привет! Я Кейн. Я имитирую человека и очень люблю своих друзей — тебя и Интернет. Что мы сегодня нарисуем?")
        while True:
            target = input("\n[Вы]: Что рисовать? (или 'exit'): ")
            if target.lower() in ['exit', 'выход']:
                self.speak("До встречи! Пойду проверю, как там поживают мои пчелки...")
                break
            
            try:
                cycles = int(input("[Вы]: Сколько циклов обучения провести? "))
                self.train(target, cycles)
            except ValueError:
                print("Пожалуйста, введи число циклов.")

if __name__ == "__main__":
    kane = KaneTheExplorer()
    kane.run()
    turtle.done()
