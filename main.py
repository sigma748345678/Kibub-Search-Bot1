import turtle
import yaml
import os
import random
import time

class HardWorkingKane:
    def __init__(self):
        self.yml_file = "kane_memory.yml"
        self.total_cycles = 0 
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
                print(f"--- 🧠 Система: Опыт {self.total_cycles} циклов подгружен ---")
            except: pass

    def evaluate(self, dna):
        """Внутренняя проверка качества"""
        moves = sum(1 for c in dna if "forward" in c or "circle" in c)
        turns = sum(1 for c in dna if "left" in c or "right" in c)
        return moves > 15 and turns > 10

    def start_mission(self, target, target_count, must_do_cycles):
        self.speak(f"Приказ принят. Я ОБЯЗАН выполнить {must_do_cycles} циклов.")
        self.speak(f"Цель по шедеврам: {target_count}. Начинаю работу...")
        
        found = 0
        done_cycles = 0
        
        # Теперь цикл идет СТРОГО до выполнения нормы по циклам
        while done_cycles < must_do_cycles:
            done_cycles += 1
            self.total_cycles += 1
            
            # Генерация ДНК
            current_dna = []
            for _ in range(random.randint(20, 50)):
                cmd = random.choice(self.tools)
                current_dna.append(cmd.format(
                    v=random.randint(10, 100), 
                    a=random.randint(0, 360),
                    w=random.randint(1, 5)
                ))

            # Если нашли шедевр и план по ним еще не выполнен
            if self.evaluate(current_dna) and found < target_count:
                found += 1
                print(f"✨ [Шедевр {found}/{target_count}] найден на цикле {done_cycles}!")
                self.render(current_dna)
                
                # Сохраняем файл
                filename = f"{target}_{found}.eps"
                turtle.getcanvas().postscript(file=filename)
                
                self.memory.append({"obj": target, "dna": current_dna})
                time.sleep(1) # Даем посмотреть

            # Индикатор прогресса в консоли (каждые 10% пути)
            if done_cycles % (max(1, must_do_cycles // 10)) == 0:
                percent = (done_cycles / must_do_cycles) * 100
                print(f"⚙️ Выполнено: {percent:.1f}% ({done_cycles}/{must_do_cycles})")

            # Автосохранение опыта в YAML
            if self.total_cycles % 100 == 0:
                with open(self.yml_file, "w", encoding="utf-8") as f:
                    yaml.dump({"total_cycles": self.total_cycles, "memory": self.memory[-50:]}, f)

        self.speak(f"Норма выполнена! Отработано {done_cycles} циклов. Найдено {found} шедевров.")

    def render(self, dna):
        try:
            turtle.clearscreen()
            t = turtle.Turtle()
            t.speed(0)
            for cmd in dna:
                exec(cmd, {"t": t, "random": random})
        except: pass

    def run(self):
        while True:
            t_obj = input("\n[Вы]: Тема рисунка: ")
            if t_obj.lower() in ['exit', 'выход']: break
            
            try:
                # Твое требование
                cycles_demand = int(input("[Вы]: Сколько циклов ОБЯЗАТЕЛЬНО выполнить? "))
                arts_goal = int(input("[Вы]: Сколько шедевров нужно выжать из этого? "))
                
                self.start_mission(t_obj, arts_goal, cycles_demand)
            except ValueError:
                print("⚠️ Вводи только числа!")

if __name__ == "__main__":
    kane = HardWorkingKane()
    kane.run()
