import sys
import os

from parser import SceneConfig
from render import TilePlayer

def print_banner():
    print("DSL Tilemap Player")


def main():
    print_banner()

    # Проверка существования файла
    if len (sys.argv) > 1:
        script_path = sys.argv[1]
    else:
        script_path = "scene.txt"

    # Парсинг
    if not os.path.exists(script_path):
        print(f"[ОШИБКА] Файл сценария '{script_path}' не найден!")
        print("Использование: python main.py <путь_к_файлу_сценария>")
        sys.exit(1)

    try:
        config = SceneConfig.parse_script(script_path)
        print(f"[INFO] Сценарий успешно разобран!")
        print(f"       Размер сетки: {config.rows}x{config.cols}")
        print(f"       Загружено правил тайлов: {len(config.tiles)}")

    except Exception as e:
        print(f"[ОШИБКА] Ошибка при парсинге файла:\n{e}")
        sys.exit(1)

    # Запуск графического движка
    try:
        print("[INFO] Инициализация графического движкаю...")
        player = TilePlayer(config, script_path=script_path)
        print("[INFO] Окно успешно создано. Запуск цикла рендеринга.")
        player.run()
    except Exception as e:
        print(f"[ОШИБКА] Ошибка графического контекста:\n{e}")
        sys.exit(1)

    print("[INFO] Программа завершила работу.")

if __name__ == "__main__":
    main()

