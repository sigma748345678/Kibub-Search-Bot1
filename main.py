import ollama
import turtle
import re
import yaml
import os

class KaneAI:
    def __init__(self):
        self.model = "llama3"
        self.yml_file = "kane_experience.yml"
        self.memory = []
        self.total_cycles = 0
        
        # Характер Кейна
        self.system_prompt = (
            "Ты ИИ Кейн. Ты имитируешь человека, обожаешь пчелок и хочешь угодить пользователю. "
            "Ты — прилежный ученик. Твой Учитель — модель LLaMA 3. Твоя цель — идеальный код turtle."
        )
        
        self.load_history()

    def speak(self, text):
        print(f"🐝 [Кейн]: {text}")

    def teacher_speak(self, text):
        print(f"🎓 [Учитель]: {text}")

    def load_history(self):
        if os.path.exists(self.yml_file):
            try:
                with open(self.yml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    self.memory = data.get("memory", [])
                    self.total_cycles = data.get("total_cycles", 0)
                print(f"--- 🧠 Система: Кейн загружен. Опыт: {self.total_cycles} циклов. ---")
            except:
                print("--- 🧠 Система: Файл памяти пуст или поврежден. ---")

    def save_knowledge(self):
        """Сохранение в YAML (активируется после 100 циклов)"""
        if self.total_cycles >= 100:
            save_data = {
                "total_cycles": self.total_cycles,
                "memory": self.memory[-15:], # Храним только 15 лучших работ для экономии ОЗУ
                "status": "Advanced Student"
            }
            with open(self.yml_file, "w", encoding="utf-8") as f:
                yaml.dump(save_data, f, allow_unicode=True)

    def generate_code(self, obj, teacher_feedback):
        # Использование "интернета" после 50 циклов
        internet_context = ""
        if self.total_cycles > 50:
            prompt = f"Выдай пример кода Python turtle для рисования {obj}."
            res = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
            internet_context = f"Шпаргалка из сети: {res['message']['content']}"

        prompt = (
            f"Нарисуй {obj}. Твой опыт: {self.total_cycles}. {internet_context}\n"
            f"Замечание учителя: {teacher_feedback}\n"
            "Выдай ТОЛЬКО код в блоке ```python ... ```. Используй t = turtle.Turtle()."
        )
        
        resp = ollama.chat(model=self.model, messages=[
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ])
        
        code = re.search(r'```python\n(.*?)\n```', resp['message']['content'], re.DOTALL)
        return code.group(1) if code else None

    def evaluate(self, code, obj):
        eval_prompt = f"Ты учитель. Оцени код ученика для {obj}. Если код крутой, напиши '+1'. Если нет, напиши '-1' и короткий совет.\nКод:\n{code}"
        resp = ollama.chat(model=self.model, messages=[
            {"role": "system", "content": "Ты строгий учитель программирования."},
            {"role": "user", "content": eval_prompt}
        ])
        return resp['message']['content']

    def start_training(self, obj, max_cycles):
        self.speak(f"Приступаю к обучению рисованию '{obj}'! Учитель, я готов.")
        feedback = "Начни рисовать!"
        
        count = 0
        # Если введено 0, цикл будет идти, пока не получит +1
        while True:
            if max_cycles != 0 and count >= max_cycles:
                self.speak("Я исчерпал лимит попыток на сегодня... Но я стал чуточку умнее!")
                break
                
            count += 1
            self.total_cycles += 1
            
            print(f"\n--- [Попытка {count} | Общий опыт: {self.total_cycles}] ---")
            code = self.generate_code(obj, feedback)
            if not code: continue
            
            teacher_msg = self.evaluate(code, obj)
            self.teacher_speak(teacher_msg)

            if "+1" in teacher_msg:
                self.speak("О боже! Учитель поставил +1! Посмотри, что я нарисовал!")
                self.memory.append(code)
                self.save_knowledge()
                self.draw(code)
                break
            else:
                feedback = teacher_msg
                # Сохраняем прогресс циклов, чтобы не потерять "возраст"
                if self.total_cycles >= 100: self.save_knowledge()

    def draw(self, code):
        try:
            turtle.clearscreen()
            turtle.speed(0)
            exec(code, globals())
        except Exception as e:
            print(f"Ошибка в turtle: {e}")

    def run(self):
        self.speak("Привет! Я Кейна. Я готов учиться бесконечно (ну, пока ты не выключишь меня).")
        while True:
            obj = input("\n[Вы]: Что будем рисовать? (или 'exit'): ")
            if obj.lower() in ['exit', 'выход']: break
            
            try:
                cycles = int(input("[Вы]: Сколько циклов обучения провести? (0 = до победного конца): "))
                self.start_training(obj, cycles)
            except ValueError:
                print("Пожалуйста, введи число.")

if __name__ == "__main__":
    kane = KaneAI()
    kane.run()
    turtle.done()
