import math


class Loan:

    def __init__(
        self, original_loan_amount: float, simple_interest_rate: float, loan_term: float
    ):
        if not all(
            math.isfinite(value)
            for value in (original_loan_amount, simple_interest_rate, loan_term)
        ):
            raise ValueError("Исходные данные должны быть конечными числами.")
        if original_loan_amount < 0:
            raise ValueError("Сумма кредита не может быть отрицательной.")
        if simple_interest_rate < 0:
            raise ValueError("Процентная ставка не может быть отрицательной.")
        if loan_term < 0:
            raise ValueError("Срок кредита не может быть отрицательным.")

        self.original_loan_amount = original_loan_amount
        self.simple_interest_rate = simple_interest_rate
        self.loan_term = loan_term

    def calculate_total_cost(self):
        total_cost = self.original_loan_amount * (
            1 + self.simple_interest_rate / 100 * self.loan_term / 12
        )
        if not math.isfinite(total_cost):
            raise ValueError("Результат расчёта слишком велик.")
        return total_cost
