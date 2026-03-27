import turtle
import yaml
import os
import random
import time

class TurboKane:
    def __init__(self):
        self.yml_file = "kane_memory.yml"
        self.total_cycles = 0 # Общий счетчик за все время
        self.memory = []
        self.load_history()
        
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
                print(f"--- 🧠 Память загружена. Опыт: {self.total_cycles} циклов ---")
            except: pass

    def evaluate_art(self, commands):
        """Внутренний судья: фильтрует скучные рисунки"""
        moves = sum(1 for c in commands if "forward" in c or "circle" in c)
        turns = sum(1 for c in commands if "left" in c or "right" in c)
        return moves > 15 and turns > 10 

    def start_production(self, target_obj, need_arts, max_energy):
        self.speak(f"Понял! Ищу {need_arts} шедевров для '{target_obj}'.")
        self.speak(f"У меня есть запас в {max_energy} попыток. Поехали!")
        
        found = 0
        spent_energy = 0
        
        while found < need_arts and spent_energy < max_energy:
            spent_energy += 1
            self.total_cycles += 1
            
            # Генерация ДНК рисунка
            current_dna = []
            for _ in range(random.randint(25, 50)):
                cmd = random.choice(self.tools)
                current_dna.append(cmd.format(
                    v=random.randint(20, 100), 
                    a=random.randint(0, 360),
                    w=random.randint(1, 5)
                ))

            # Авто-проверка качества
            if self.evaluate_art(current_dna):
                found += 1
                print(f"✨ [Успех {found}/{need_arts}] на попытке {spent_energy}!")
                
                self.execute_render(current_dna)
                
                # Сохраняем файл чертежа
                filename = f"{target_obj}_{found}.eps"
                turtle.getcanvas().postscript(file=filename)
                
                self.memory.append({"object": target_obj, "dna": current_dna})
                
                # Сохраняем прогресс в YAML
                if self.total_cycles >= 100:
                    with open(self.yml_file, "w", encoding="utf-8") as f:
                        yaml.dump({"total_cycles": self.total_cycles, "memory": self.memory[-50:]}, f)
                
                time.sleep(1.5) # Пауза, чтобы поглазеть
            
            if spent_energy % 50 == 0:
                print(f"💤 Потрачено {spent_energy} попыток из {max_energy}...")

        if found >= need_arts:
            self.speak(f"Задание выполнено! Найдено {found} рисунков.")
        else:
            self.speak(f"Энергия кончилась! Нашел только {found}. Нужно больше попыток в следующий раз.")

    def execute_render(self, dna):
        try:
            turtle.clearscreen()
            t = turtle.Turtle()
            t.speed(0)
            for cmd in dna:
                exec(cmd, {"t": t, "random": random})
        except: pass

    def run(self):
        while True:
            target = input("\n[Вы]: Тема (пчела/дом/хаос): ")
            if target.lower() in ['exit', 'выход']: break
            
            try:
                max_e = int(input("[Вы]: Сколько циклов (попыток) разрешить? "))
                count = int(input("[Вы]: Сколько шедевров нужно найти? "))
                self.start_production(target, count, max_e)
            except ValueError:
                print("⚠️ Вводи числа, пожалуйста!")

if __name__ == "__main__":
    kane = TurboKane()
    kane.run()
