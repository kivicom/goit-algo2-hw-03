import task1
import task2

def run_task(task_number):
    if task_number == 1:
        report = task1.generate_report()
        with open('report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        print("Звіт для завдання 1 збережений у report.md")
    elif task_number == 2:
        report = task2.generate_report()
        with open('range_query_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        print("Звіт для завдання 2 збережений у range_query_report.md")
    else:
        print("Невірний номер завдання. Використовуйте 1 або 2.")

if __name__ == "__main__":
    task = input("Введіть номер завдання (1 або 2): ")
    try:
        task_number = int(task)
        run_task(task_number)
    except ValueError:
        print("Будь ласка, введіть число 1 або 2.")