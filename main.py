import math
import tkinter

from loan import Loan
from file import File


def error_entry_field(entry_field, error_label, error_message="Ошибка ввода"):
    entry_field.config(bg="red")
    error_label.config(text=error_message)


def unerror_entry_field(entry_field, error_label):
    entry_field.config(bg="white")
    error_label.config(text="")


# Контроллер: функция вызывается в момент нажатия на кнопку
def click():
    # метод get() возвращает текущее значение counter
    # метод set() – устанавливает новое значение counter
    unerror_entry_field(
        entry_field_original_loan_amount, error_label_original_loan_amount
    )
    unerror_entry_field(
        entry_field_simple_interest_rate, error_label_simple_interest_rate
    )
    unerror_entry_field(entry_field_loan_term, error_label_loan_term)
    error_label.config(text="")
    total_loan_cost.set("")

    if len(original_loan_amount.get()) == 0:
        error_entry_field(
            entry_field_original_loan_amount,
            error_label_original_loan_amount,
            "Поле не может быть пустым",
        )
    if len(simple_interest_rate.get()) == 0:
        error_entry_field(
            entry_field_simple_interest_rate,
            error_label_simple_interest_rate,
            "Поле не может быть пустым",
        )
    if len(loan_term.get()) == 0:
        error_entry_field(
            entry_field_loan_term, error_label_loan_term, "Поле не может быть пустым"
        )
    if (
        entry_field_original_loan_amount.cget("bg") == "red"
        or entry_field_simple_interest_rate.cget("bg") == "red"
        or entry_field_loan_term.cget("bg") == "red"
    ):
        return
    try:
        result = Loan(
            float(original_loan_amount.get()),
            float(simple_interest_rate.get()),
            float(loan_term.get()),
        ).calculate_total_cost()
        result_text = f"{result:.2f}"
        file = File("result.txt", result_text)
        file.save_total_loan_cost()
        total_loan_cost.set(result_text)
    except ValueError as e:
        error_label.config(text=str(e))
    except OSError:
        error_label.config(text="Не удалось записать результат в файл")


def validate_positive_double(value):
    # Value здесь конкретное значение в текущий момент времени введённое в поле
    # Поэтому допускаем пустую строку и точку
    if value in ("", "."):
        return True
    try:
        number = float(value)
        return math.isfinite(number)
    except ValueError:
        return False


# Создаем главное (корневое) окно,
# в переменную window записываем ссылку на объект класса Tk
window = tkinter.Tk()

task_label = tkinter.Label(
    window, text="Программа для расчета полной стоимости кредита", fg="blue"
)
task_label.pack()

# Модель: создаем объект класса IntVar
original_loan_amount = tkinter.StringVar()
simple_interest_rate = tkinter.StringVar()
loan_term = tkinter.StringVar()
total_loan_cost = tkinter.StringVar()
# Обнуляем созданный объект с помощью метода set()
original_loan_amount.set("")
simple_interest_rate.set("")
loan_term.set("")
total_loan_cost.set("")

# Создаем фрейм в главном окне
input_frame = tkinter.Frame(window, borderwidth=4, relief=tkinter.GROOVE)
input_frame.pack(side="left")

# Создаем виджеты и помещаем их во фрейм
label_original_loan_amount = tkinter.Label(
    input_frame, text="Первоначальная сумма кредита:"
)
# Отображаем виджет с помощью менеджера pack
label_original_loan_amount.pack()
# Пробуем набрать текст в появившемся поле для ввода
entry_field_original_loan_amount = tkinter.Entry(
    input_frame,
    textvariable=original_loan_amount,
    validate="key",
    validatecommand=(
        # tkinter.Entry использует механизм проверки ввода из Tcl/Tk, а не напрямую из Python
        window.register(validate_positive_double),
        # %P это специальный параметр Tkinter, который передает в функцию проверки новое предполагаемое содержимое Entry
        "%P",
    ),
)
entry_field_original_loan_amount.pack()
error_label_original_loan_amount = tkinter.Label(
    input_frame, text="", fg="red", font=("Arial", 9)
)
error_label_original_loan_amount.pack()

label_simple_interest_rate = tkinter.Label(
    input_frame, text="Простая процентная ставка в процентах годовых:"
)
label_simple_interest_rate.pack()
entry_field_simple_interest_rate = tkinter.Entry(
    input_frame,
    highlightthickness=2,
    highlightbackground="gray",
    highlightcolor="gray",
    textvariable=simple_interest_rate,
    validate="key",
    validatecommand=(window.register(validate_positive_double), "%P"),
)
entry_field_simple_interest_rate.pack()
error_label_simple_interest_rate = tkinter.Label(
    input_frame, text="", fg="red", font=("Arial", 9)
)
error_label_simple_interest_rate.pack()

label_loan_term = tkinter.Label(input_frame, text="Срок кредита в месяцах:")
label_loan_term.pack()
entry_field_loan_term = tkinter.Entry(
    input_frame,
    textvariable=loan_term,
    validate="key",
    validatecommand=(window.register(validate_positive_double), "%P"),
)
entry_field_loan_term.pack()
error_label_loan_term = tkinter.Label(input_frame, text="", fg="red", font=("Arial", 9))
error_label_loan_term.pack()

# Создаем кнопку и указываем обработчик при нажатии на нее
button = tkinter.Button(
    input_frame,
    text="Рассчитать",
    command=click,
    font=("Courier", 14, "bold italic"),
    fg="blue",
)
button.pack()

output_frame = tkinter.Frame(window, borderwidth=4, relief=tkinter.GROOVE)
output_frame.pack(side="left")
label_total_loan_cost = tkinter.Label(output_frame, text="Полная стоимость кредита:")
label_total_loan_cost.pack()
entry_field_total_loan_cost = tkinter.Label(output_frame, textvariable=total_loan_cost)
entry_field_total_loan_cost.pack()

error_label = tkinter.Label(input_frame, text="", fg="red", font=("Arial", 9))
error_label.pack()

# Задаем обработчик событий для корневого окна
window.mainloop()
