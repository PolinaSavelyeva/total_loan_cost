class File:

    def __init__(self, file_name: str, value: str):
        self.file_name = file_name
        self.value = value

    def save_total_loan_cost(self):
        with open(self.file_name, "w") as file:
            file.write(self.value + "\n")
