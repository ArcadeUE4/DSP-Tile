import os

class SceneConfig:
    def __init__(self, *args, **kwargs):
        self.rows = 0
        self.cols = 0
        self.grid = []
        self.tiles = {}  # {id: "path/to/img"}

    @staticmethod
    def parse_script(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл '{file_path}' не существует.")

        config = SceneConfig()

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

        if not lines:
            raise ValueError("Файл сценария пуст")

        i = 0
        while i < len(lines):
            line = lines[i]
            tokens = line.split()

            if not tokens:
                i += 1
                continue

            command = tokens[0].lower()

            # Парсинг Screen
            if command == 'screen':
                if len(tokens) < 3:
                    raise ValueError(f"Ошибка в строке {i+1}: Команда Screen требует 2 аргумента (rows, cols)")

                config.rows = int(tokens[1])
                config.cols = int(tokens[2])
                i += 1

                for r in range(config.rows):
                    if i >= len(lines):
                        raise ValueError(f"Недостаточно строк для сетки. Ожидалось {config.rows}, написано {r}")

                    row_tokens = lines[i].split()
                    if len(row_tokens) != config.cols:
                        raise ValueError(
                            f"Ошибка в строке {i+1}: Неверное количество элементов в строке сетки. "
                            f"Ожидалось {config.cols}, получено {len(row_tokens)}."
                        )

                    row_data = [int(val) for val in row_tokens]
                    config.grid.append(row_data)
                    i += 1
                continue

            # Чтение Tiles
            elif command == 'tiles':
                if len(tokens) < 2:
                    raise ValueError(f"Ошибка в строке {i+1}: Команда tiles требует указания количества (count).")

                count = int(tokens[1])
                i += 1

                for t in range(count):
                    if i >= len(lines):
                        raise ValueError(f"Ошибка: Недостаточно строк для тайлов. Ожидалось '{count}', объявлено {t}")

                    tile_tokens = lines[i].split()
                    if len(tile_tokens) < 2:
                        raise ValueError(f"Ошибка в строке {i+1}: Описание тайла должно быть формата '<id> <path>'.")

                    tile_id = int(tile_tokens[0])
                    tile_path = tile_tokens[1]
                    config.tiles[tile_id] = tile_path
                    i += 1
                continue

            i += 1

        if config.rows == 0 or config.cols == 0:
            raise ValueError("Ошибка: Блок 'Screen' не был найден или задан некорректно.")

        if not config.tiles:
            raise ValueError("Ошибка: Блок 'tiles' не содержал ни одного валидного тайла.")

        return config