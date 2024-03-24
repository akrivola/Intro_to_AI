from deeppavlov import build_model, configs

# Загрузка модели для поиска решений
model = build_model(configs.squad.squad_ru_bert, download=True)

# Функция для поиска решений проблем Windows
def search_windows_solution(query):
    results = model([query], ["Какие решения есть для проблем с Windows?"])
    solutions = results[0][0]

    return solutions

# Пример использования
query = "Мой компьютер не включается, что делать?"
solutions = search_windows_solution(query)
print(solutions)
