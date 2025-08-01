Перед запуском скрипта необходимо создать вирутальное окружение и активировать его

python3 -m venv env
source env/bin/activate

Далее установить необходимые пакеты

pip3 install tabulate
pip3 install pytest
pip3 install tabulate
pip install pytest pytest-cov

Для запуска скрипта:
python3 script --file путь/до/файла/(ов) --report average (User-Agent) --date YYYY-MM-DD

Для запуска тестов:
pytest tests.py

Для покрытия тестов:
pytest --cov=tests tests.py
