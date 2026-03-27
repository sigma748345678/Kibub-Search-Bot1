import turtle
import yaml
import os
import random
import time

class ControlledKane:
    def __init__(self):
        self.yml_file = "kane_memory.yml"
        self.total_cycles = 0 
        self.memory = []
        self.load_history()
        
        # Инструменты для рисования
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
                print(f"--- 🧠 Система: Загружено {self.total_cycles} циклов опыта ---")
            except: pass

    def evaluate(self, dna):
        """Проверка: достаточно ли сложный рисунок?"""
        moves = sum(1 for c in dna if "forward" in c or "circle" in c)
        turns = sum(1 for c in dna if "left" in c or "right" in c)
        # Если больше 15 движений и 10 поворотов - это не просто круг
        return moves > 15 and turns > 10

    def work(self, target, target_count, max_limit):
        self.speak(f"Начинаю охоту за шедеврами на тему '{target}'!")
        self.speak(f"Мой лимит на сегодня: {max_limit} попыток. Погнали!")
        
        found = 0
        attempts = 0
        
        while attempts < max_limit and found < target_count:
            attempts += 1
            self.total_cycles += 1
            
            # Генерируем случайный код
            current_dna = []
            for _ in range(random.randint(20, 50)):
                cmd = random.choice(self.tools)
                current_dna.append(cmd.format(
                    v=random.randint(10, 100), 
                    a=random.randint(0, 360),
                    w=random.randint(1, 5)
                ))

            # Проверяем качество
            if self.evaluate(current_dna):
                found += 1
                print(f"✨ Нашел! ({found}/{target_count}) Попытка: {attempts}")
                
                # Рисуем
                self.render(current_dna)
                
                # Сохраняем "фото"
                filename = f"{target}_{found}.eps"
                turtle.getcanvas().postscript(file=filename)
                
                # Записываем в память
                self.memory.append({"obj": target, "dna": current_dna})
                
                # Сохраняем YAML каждые 50 общих циклов
                if self.total_cycles % 50 == 0:
                    with open(self.yml_file, "w", encoding="utf-8") as f:
                        yaml.dump({"total_cycles": self.total_cycles, "memory": self.memory[-30:]}, f)
                
                time.sleep(1) # Даем время посмотреть
            
            if attempts % 100 == 0:
                print(f"📈 Пройдено {attempts} из {max_limit} попыток...")

        self.speak(f"Работа окончена! Найдено шедевров: {found}. Потрачено попыток: {attempts}.")

    def render(self, dna):
        try:
            turtle.clearscreen()
            t = turtle.Turtle()
            t.speed(0)
            for cmd in dna:
                exec(cmd, {"t": t, "random": random})
        except: pass

    def run(self):
        self.speak("Я готов. Лимиты устанавливаешь ты!")
        while True:
            t_obj = input("\n[Вы]: Тема (например, Пчела): ")
            if t_obj.lower() in ['exit', 'выход']: break
            
            try:
                # ВОТ ТВОИ ЛИМИТЫ
                user_limit = int(input("[Вы]: Максимальный лимит попыток (циклов): "))
                user_count = int(input("[Вы]: Сколько шедевров нужно найти: "))
                
                self.work(t_obj, user_count, user_limit)
            except ValueError:
                print("⚠️ Ошибка: вводи только целые числа!")

if __name__ == "__main__":
    kane = ControlledKane()
    kane.run()
