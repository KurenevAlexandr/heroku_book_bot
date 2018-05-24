"""
Главный модуль, отвественный за логику бота
"""
import time
import subprocess
from open_library.download import load_dict, \
    get_url_by_title, download
from telapi.helpers import get_updates, get_last_update_id, send_message


TITLES = load_dict()


def match_query(query):
    """Проверка корректности запроса пользователя"""
    words = query.split()
    length = words[-1]
    title = " ".join(words[1:-1])

    try:
        length = int(length)
    except ValueError:
        return False, None, None
    return True, title, length


def save_text(text):
    """Сохранение текста для генерации"""
    with open('./markov/input/input.txt', 'w') as input_txt:
        input_txt.write(text)


def train_call(input_dir, model):
    """Обучение модели"""
    _ = subprocess.Popen(
        "python3 ."
        "/markov/train.py "
        "--input-dir {} "
        "--model {}".format(input_dir, model),
        shell=True)


def generate_call(model, length):
    """Вызов генератора"""
    process = subprocess.Popen("python3 ./markov/generate.py "
                               "--model {} --length {}".format(model, length),
                               stdout=subprocess.PIPE, shell=True)
    generated = process.communicate()[0]
    return generated


def process_text(text, length):
    """Генерация предложения"""
    save_text(text)
    model = "./markov/model"

    # train call
    train_call("./markov/input", model)

    # generale call
    generated = generate_call(model, length)
    # return str(text).split()[:length]
    return " ".join(generated.decode().split()[:length])


def handle_updates(updates):
    """Разбирается с апдейтами на стороне телеграма"""
    for update in updates["result"]:
        # print('debug info: ', update)
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
        except KeyError:
            # случается в случае редактирования прошлых сообщений,
            # для бота это нерелевантно -- пропускаем
            continue
        if text == "/done":
            print("Select an item to delete", chat)
        elif text[:4] == '/gen':
            succ, title, length = match_query(text)
            if succ:
                text = "succ"
                if title in TITLES:
                    url = get_url_by_title(title, TITLES)
                    text = download(url)
                    generated = process_text(text, length)
                    send_message(generated, chat)
                    continue
                else:
                    send_message("Такого названия нет", chat)
                    continue
            else:
                send_message("Попробуйте сделать запрос еще раз", chat)
        elif text == "/start":
            send_message("Привет. Этот бот умеет генерить рандомные тексты по"
                         " заголовку книги. Для генерации напиши"
                         " /gen <название книги> <длина запроса>", chat)


def main():
    """Цикл запуска бота"""
    last_update_id = None
    print('running')
    while True:
        updates = get_updates(last_update_id)
        print('running')
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
