from src.controller.expenses_controller import expensescontroller
from src.controller.incomes_controller import incomescontroller
from src.services.expenses_service import ExpensesService
from src.services.incomes_service import IncomesService

expenses_service = ExpensesService()
expenses_controller = expensescontroller(expenses_service)

incomes_service = IncomesService()
incomes_controller = incomescontroller(incomes_service)
