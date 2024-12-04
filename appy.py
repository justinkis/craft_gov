from flask import Flask, render_template, request, jsonify
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
import threading
import logging

# Настройка логирования
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = Flask(__name__)

MATERIALS = {
    "technical": [
        {"name": "Наручники", "cost": 2, "weight": 0.35},
        {"name": "Полицейская дубинка", "cost": 5, "weight": 0.82},
        {"name": "Тазер", "cost": 10, "weight": 0.22},
        {"name": "ИРП Армии США", "cost": 5, "weight": 0.60},
        {"name": "Полицейский дрон", "cost": 2000, "weight": 1.20},
        {"name": "Легкий бронежилет", "cost": 15, "weight": 2.00},
        {"name": "Тяжелый бронежилет", "cost": 30, "weight": 4.00},
        {"name": "Легкая бронеразгрузка FIB", "cost": 15, "weight": 2.00},
        {"name": "Тяжелая бронеразгрузка FIB", "cost": 30, "weight": 4.00},
        {"name": "Камера измерения скорости", "cost": 100, "weight": 5.00},
    ],
    "medical": [
        {"name": "Противовирусная вакцина", "cost": 1, "weight": 0.01},
        {"name": "Кодеиновые таблетки", "cost": 1, "weight": 0.01},
        {"name": "Азитромицин", "cost": 10, "weight": 0.01},
        {"name": "Активированный уголь", "cost": 10, "weight": 0.01},
        {"name": "Эпинефрин", "cost": 10, "weight": 0.15},
        {"name": "Дефибриллятор", "cost": 400, "weight": 0.50},
    ],
    "weapon": [
        {"name": "Патроны 9x19mm", "cost": 1, "weight": 0.01},
        {"name": "Патроны 12ga Buckshot", "cost": 1, "weight": 0.05},
        {"name": "Патроны 12ga Rifled", "cost": 1, "weight": 0.03},
        {"name": "Патроны .45 ACP", "cost": 2, "weight": 0.01},
        {"name": "Патроны 7.62x39mm", "cost": 2, "weight": 0.01},
        {"name": "Патроны 5.56x45mm", "cost": 2, "weight": 0.01},
        {"name": "Фонарик", "cost": 2, "weight": 0.20},
        {"name": "Оптический прицел", "cost": 4, "weight": 0.30},
        {"name": "Голографический прицел", "cost": 4, "weight": 0.30},
        {"name": "Глушитель", "cost": 6, "weight": 0.20},
        {"name": "Рукоятка", "cost": 10, "weight": 0.50},
        {"name": "Увеличенный магазин", "cost": 10, "weight": 0.70},
        {"name": "Тяжелый пистолет", "cost": 15, "weight": 0.80},
        {"name": "Карабинная винтовка", "cost": 20, "weight": 2.60},
        {"name": "Карабинная винтовка MK2", "cost": 40, "weight": 2.30},
        {"name": "Ручной пулемет MK2", "cost": 2500, "weight": 7.20},
        {"name": "Военная винтовка", "cost": 30, "weight": 2.90},
        {"name": "Тактический SMG", "cost": 20, "weight": 1.60},
        {"name": "Винтовка Marksman MK2", "cost": 5000, "weight": 3.70},
        {"name": "Помповый дробовик MK2", "cost": 20, "weight": 3.60},
        {"name": "Тяжелая снайперская винтовка", "cost": 1000, "weight": 4.50},
        {"name": "Тяжелая винтовка", "cost": 45, "weight": 3.10},
        {"name": "Тяжелый дробовик", "cost": 30, "weight": 3.34},
        {"name": "Тяжелая снайперская винтовка MK2", "cost": 20000, "weight": 8.00}
    ],
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/materials/<material_type>")
def materials(material_type):
    return render_template(
        "materials.html", materials=MATERIALS.get(material_type, []), material_type=material_type
    )

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    items = data.get("items", [])
    total_weight = 0
    total_materials = 0

    for item in items:
        quantity = item.get("quantity", 0)
        cost = item.get("cost", 0)
        weight = item.get("weight", 0)
        total_weight += weight * quantity
        total_materials += cost * quantity

    if total_weight > 2000:
        return jsonify({"error": "Превышен вес машины!"})

    return jsonify({"total_weight": total_weight, "total_materials": total_materials})


def start_flask():
    logging.info("Запуск Flask сервера...")
    app.run(debug=False, use_reloader=False)
    logging.info("Flask сервер завершил работу.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Крафт GOV")
        self.setGeometry(100, 100, 1024, 768)
        logging.info("Создано главное окно приложения.")

        # Добавляем веб-браузер в окно
        try:
            self.browser = QWebEngineView()
            url = QUrl("http://127.0.0.1:5000")
            self.browser.setUrl(url)
            self.setCentralWidget(self.browser)
            logging.info(f"Браузер установлен с URL {url.toString()}.")
        except Exception as e:
            logging.error(f"Ошибка при добавлении браузера: {e}")


if __name__ == "__main__":
    try:
        logging.info("Приложение запускается...")
        # Запускаем Flask в отдельном потоке
        flask_thread = threading.Thread(target=start_flask, daemon=True)
        flask_thread.start()
        logging.info("Поток Flask успешно запущен.")

        # Создаем GUI-приложение
        logging.info("Запуск GUI-приложения...")
        qt_app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        logging.info("Главное окно GUI-приложения успешно запущено.")
        sys.exit(qt_app.exec_())
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")