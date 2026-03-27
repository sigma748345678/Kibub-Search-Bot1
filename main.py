import turtle
import yaml
import os
import random
import time

class AutonomousKane:
    def __init__(self):
        self.yml_file = "kane_memory.yml"
        self.total_cycles = 0
        self.memory = []
        self.load_history()
        
        # Инструменты Кейна
        self.tools = [
            "t.forward({v})", "t.left({a})", "t.right({a})", 
            "t.circle({v}, {a})", "t.width({w})",
            "t.pencolor(random.random(), random.random(), random.random())"
        ]

    def speak(self, text):
        print(f"🐝 [Кейн]: {text}")

    def load_history(self):
        if os.path.exists(self.yml_file):
            try:
                with open(self.yml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    self.total_cycles = data.get('total_cycles', 0)
                    self.memory = data.get('memory', [])
                print(f"--- 🧠 Система: Кейн загружен. Опыт: {self.total_cycles} ---")
            except: pass

    def save_history(self):
        # Автоматическое сохранение в YAML после 100 циклов
        if self.total_cycles >= 100:
            with open(self.yml_file, "w", encoding="utf-8") as f:
                yaml.dump({"total_cycles": self.total_cycles, "memory": self.memory[-30:]}, f)

    def evaluate_art(self, commands):
        """Внутренний судья: проверяет сложность рисунка без участия человека"""
        score = 0
        dist = 0
        angles = 0
        
        for cmd in commands:
            if "forward" in cmd or "circle" in cmd:
                score += 1 # За каждое движение
            if "left" in cmd or "right" in cmd:
                angles += 1 # За каждый поворот
        
        # Критерий успеха: минимум 10 движений и 5 поворотов
        # Если рисунок слишком простой (круг или линия), он не пройдет
        if score > 10 and angles > 5:
            return True
        return False

    def self_learn(self, target_obj):
        self.speak(f"Начинаю автономное исследование объекта '{target_obj}'...")
        
        attempts_in_session = 0
        while attempts_in_session < 50: # Кейн сделает 50 попыток сам
            attempts_in_session += 1
            self.total_cycles += 1
            
            # Генерация случайного набора команд (ДНК рисунка)
            current_dna = []
            complexity = random.randint(15, 30)
            for _ in range(complexity):
                cmd = random.choice(self.tools)
                current_dna.append(cmd.format(
                    v=random.randint(10, 80), 
                    a=random.randint(0, 360),
                    w=random.randint(1, 5)
                ))

            # Внутренняя проверка
            if self.evaluate_art(current_dna):
                print(f"✅ Попытка {attempts_in_session}: Рисунок признан годным. Отрисовка...")
                self.execute_render(current_dna)
                self.memory.append({"object": target_obj, "dna": current_dna})
                self.save_history()
                time.sleep(1) # Даем тебе посмотреть на результат
                break # Нашел один хороший вариант и закончил
            else:
                if attempts_in_session % 10 == 0:
                    print(f"❌ Попытка {attempts_in_session}: Слишком просто, ищу дальше...")

    def execute_render(self, dna):
        try:
            turtle.clearscreen()
            t = turtle.Turtle()
            t.speed(0)
            for cmd in dna:
                exec(cmd, {"t": t, "random": random})
        except: pass

    def run(self):
        self.speak("Я запущен в режиме полной автономии. Я сам решаю, что красиво.")
        while True:
            target = input("\n[Вы]: Что мне изучить сегодня? (exit): ")
            if target.lower() in ['exit', 'выход']: break
            self.self_learn(target)

if __name__ == "__main__":
    kane = AutonomousKane()
    kane.run()
