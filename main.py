import turtle
import yaml
import os
import random
import time

class IronWillKane:
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
            except: pass

    def calculate_complexity(self, dna):
        """Считает 'вес' рисунка. Чем выше, тем круче."""
        # Вес = количество команд * разнообразие углов
        return len(dna) * len(set([line.split(',')[0] for line in dna]))

    def start_grind(self, target, cycles_to_do):
        self.speak(f"Принято. Я ухожу в глубокое вычисление на {cycles_to_do} циклов.")
        self.speak("Я не остановлюсь на 19-й попытке. Я прогоню ВСЕ.")
        
        best_dna = None
        best_score = 0
        
        # СТРОГИЙ ЦИКЛ БЕЗ ВЫХОДА
        for i in range(1, cycles_to_do + 1):
            self.total_cycles += 1
            
            # Генерируем ДНК
            current_dna = []
            for _ in range(random.randint(30, 60)): # Увеличили сложность
                cmd = random.choice(self.tools)
                current_dna.append(cmd.format(
                    v=random.randint(10, 100), 
                    a=random.randint(0, 360),
                    w=random.randint(1, 5)
                ))

            # Оцениваем сложность
            current_score = self.calculate_complexity(current_dna)
            
            # Если этот вариант сложнее всех предыдущих - запоминаем
            if current_score > best_score:
                best_score = current_score
                best_dna = current_dna
                print(f"📈 Цикл {i}: Найден новый рекорд сложности ({best_score})")

            # Каждые 1000 циклов отчет в консоль, чтобы ты видел, что ноут жив
            if i % 1000 == 0:
                print(f"⚙️ Прогресс: {i}/{cycles_to_do} ({int(i/cycles_to_do*100)}%) | Лучший балл: {best_score}")

        # ТОЛЬКО КОГДА ВСЕ ЦИКЛЫ ПРОЙДЕНЫ - РИСУЕМ
        self.speak(f"Норма {cycles_to_do} выполнена. Отрисовываю самый сложный вариант из найденных.")
        self.execute_render(best_dna)
        
        # Сохранение
        filename = f"{target}_final.eps"
        turtle.getcanvas().postscript(file=filename)
        self.memory.append({"obj": target, "dna": best_dna, "score": best_score})
        
        with open(self.yml_file, "w", encoding="utf-8") as f:
            yaml.dump({"total_cycles": self.total_cycles, "memory": self.memory[-20:]}, f)

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
            t_obj = input("\n[Вы]: Тема: ")
            if t_obj.lower() in ['exit', 'выход']: break
            try:
                demand = int(input("[Вы]: Сколько циклов ОБЯЗАТЕЛЬНО прогнать? "))
                self.start_grind(t_obj, demand)
            except ValueError:
                print("⚠️ Вводи числа!")

if __name__ == "__main__":
    kane = IronWillKane()
    kane.run()
