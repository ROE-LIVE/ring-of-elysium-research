**Актуально08.10, ночь:** [два слота, timed reload и пассивная мишень](RECOVERY-20261008-NIGHT.md). Следующий №22/INV02 — pages/consumables; две пушки уже работают. Новый Windows-повтор и dual-gun reconnect остаются открытыми. Учебная защита50% не является исходной формулой ROE.

# Запуск и проверки

Контекст не содержит клиента, ресурсов, секретов, готовых префиксов и серверных бинарников. Команды рассчитаны на проверенный существующий workspace; это не универсальный установщик. Этот документ сам не запускает сервисы.

## 2022: Linux, Proton, без Docker

```bash
cd /home/jovyan/imported/REsearch/ROE_SERVER
python -B research/builds/2022/iceland-gameplay-20261006/run_winter_demo.py
# Отдельная проверка зон без атак цели:
python -B research/builds/2022/iceland-gameplay-20261006/run_winter_demo.py --no-bot
```

По умолчанию1200 секунд, допускается120..1800; создаётся новый каталог winter-demo-*. Fixtures: scene-winter-separated.json, weapon-ground-gun.json, actor-bot-basic.json или actor-static.json, parcel-separated.json, world-complete-demo.json. До210-й секунды не смешивать ручной ввод с AutoUI. Проверять44-result.png и события, а не только exit. Таймаут124 ожидаем для ограниченного опыта и не доказывает успех действий.

Требуются полная независимая runtime/client; GE-Proton11-7-x86_64 и prefix runtime/proton-2022; NVIDIA/Vulkan ICD; Xvfb, xdotool, x11-utils, iproute2; доступный sudo-n unshare--net; Python /opt/conda/bin/python с cryptography50.0.1 и Pillow; собранный .NET8 LobbyEmulator и tools/vendor/dotnet/dotnet. Для адресного анализа дополнительно Unicorn/Capstone. Региональный ресурс00007edb.dat должен иметь4196002 байта; свободного места не менее15ГиБ.

Новый preset07.10, инструкция в winter-loot-20261007/README.md:

```bash
python -B research/builds/2022/iceland-gameplay-20261006/run_trial.py winter-next-N \
  --scene ../winter-loot-20261007/scene-fast-timers.json \
  --weapon ../winter-loot-20261007/weapon-table-demo.json \
  --world ../winter-loot-20261007/world-fast-timers.json \
  --actor actor-bot-basic.json --parcel parcel-separated.json --loot --live \
  --evacuate 8 --evac-result evac-ui-bridge-no-grace-20261007.json \
  --selection-seconds 47 --duration 900
```

Имя RUN должно быть свободно. Исходные длительности: заменить fast-timers на primary-timers, duration1800. Лестница примерно через4мин или23–24мин от запуска соответственно. После появления F→6–7с подъёма→8с после реальной посадки→кинематографическая задержка→проверка LOCAL в газете→Return to Lobby. Пространственные регионы/точки ручные, Stats архивные, правило восьми секунд одиночное. Climb protection0: её необходимость не доказана.

Для lobby требуется уже подготовленный локальный session-key: путь задан в run.sh, значение в пакет не включено. Сервисы работают на loopback внутри собственного namespace. Полный список требований находится в исторической копии winter README.

Ручной снимок:

```bash
ROE_RUN_DIR="$PWD/research/builds/2022/iceland-gameplay-20261006/RUN" \
 /opt/conda/bin/python -B research/builds/2022/iceland-gameplay-20261006/ui.py snapshot
```

Дополнительные аргументы: `--key Tab`, `--key r`, `--key f`, `--key m`, `--hold w 1`, `--mouse-hold 1 0.4`. Проверять ui.py--help. UI event записывается до действия; при ошибке отсутствие снимка означает, что действие не подтверждено. Для остановки SIGTERM только PID собственного RUN/runner-pid.txt; глобальный pkill wine не использовать.

## 2022: Windows11, запуск из Git

Отдельный [run_roe_2022](https://github.com/ROE-LIVE/run_roe_2022), актуальный коммит d2db3a6. В уже скачанном репозитории:

```powershell
cd G:\REsearch\run_roe_2022
git pull --ff-only
.\run-roe-2022.cmd
```

Полный клиент2022 должен лежать в `G:\REsearch\Ring of Elysium-2022`, EXE SHA2dca9b1e…6ba18. Существующий16-байтный `private/candidate-001.key` включён в приватный репозиторий по прямому указанию владельца; в agents-context его нет. Архив не требуется. Bootstrap скачивает Python3.12.10, зависимости и .NET8 SDK в `.tools`; launcher собирает lobby, копирует полный клиент независимо в `runtime/client` и настраивает только свои правила брандмауэра через UAC. Следующие запуски используют инструменты и runtime повторно. Backend работает на этом же ПК, только loopback; Jupyter/Docker для него не нужны.

В игре: Play → Training → Start Matchmaking, выбрать клетку и дождаться47с. Варианты: `-Kit glider`, `-Kit climb`, `-Mode cycle -Duration 900`; climb traversal не подтверждён, cycle/Stats диагностические. Ключ и конфиги проверяет `-VerifyOnly`, без игры/сервисов; это не проверка клиента, .NET или брандмауэра.

Чистый Git-checkout с core.autocrlf=true сохранил ключ побайтно и прошёл25 SHA SOURCE-MANIFEST,49 Linux-тестов, проверку трёх наборов и сборку lobby без предупреждений/ошибок. Разбор PowerShell выполнен. Нативный Windows11, UAC/NetSecurity и автоматическая загрузка зависимостей на физическом ПК в этом опыте не проверены. Источник: [README](https://github.com/ROE-LIVE/run_roe_2022/blob/main/README.md), [VALIDATION](https://github.com/ROE-LIVE/run_roe_2022/blob/main/VALIDATION.md). Игровое подтверждение предыдущих этапов остаётся Proton/Wine.

## V99: Windows11 → Linux LAN

Код находится в git@github.com:ROE-LIVE/roe-server.git. Linux запуск через Docker, без Compose и .env:

```bash
cd /home/jovyan/roe-server/server/v99_remote
docker build -t roe-v99:local .
docker run -d --name roe-v99 --init --stop-timeout 15 \
 --cap-drop ALL --security-opt no-new-privileges:true \
 -p 192.168.1.25:9002:9002/udp \
 -e V99_HOST=0.0.0.0 -e V99_PEER_IP=192.168.1.121 -e V99_DURATION=7200 \
 --mount type=volume,source=roe-v99-data,target=/data roe-v99:local
```

При переносе заменить IP и разрешить UDP9002 от ПК. Сервер поддерживает один сеанс. check_connection.py занимает его; после проверки перед игрой нужен restart. Test-NetConnection-Port9002 проверяет TCP, поэтому здесь не подходит.

Windows:

```powershell
cd G:\REsearch\roe-server
.\run-v99-windows.cmd
```

Клиент по умолчанию G:\REsearch\Ring of Elysium-V99; сервер192.168.1.25. Требуется Python3.11+ x64 через py или python; fallback исправлен. Дождаться105 секунд и queue_enabled, пройти регион/персонажа, использовать Training. Launcher создаёт полную копию около13.6ГиБ. В этой ветке .NET, candidate-001.key и windows-character-kit2022 не требуются. Реальных исторических ключей нет; peer выдаёт собственный тестовый ключ.

Инструкция: [Windows V99](../snapshots/roe-server/docs/WINDOWS_V99_START.md). Этот запуск диагностический: штатный вход без bootstrap ещё не восстановлен.

## Steam2018

Готовой команды игрового сервера нет. Комплекты deploy/steam2018-windows11-* диагностируют старт и не запускают доказанный host. Последний физический Windows опыт не подтвердил сцену, пользователь сообщал о крашах ОС. Сначала существующие события/адресный отчёт, новый запуск — по отдельному разрешению.

## Регрессии

```bash
cd /home/jovyan/imported/REsearch/ROE_SERVER
python -B -m unittest discover -s tests -v
```

Последняя проверка:109 тестов после локального каталога/генератора/equipment. У roe-server собственные тесты/fixtures; предыдущий Windows перенос прошёл15 тестов. Перед повтором проверять билд/SHA, порты, место и собственные процессы. Хеши контекстного пакета не заменяют регрессии или проверку целостности клиента.

Постоянная установка зависимостей в образ Jupyter и сохранение workspace на PVC описаны в [JUPYTER-ENVIRONMENT.md](JUPYTER-ENVIRONMENT.md). Рецепт и инструменты подготовки среды находятся в отдельном [jupyterROE](https://github.com/ROE-LIVE/jupyterROE).


Для нового зимнего опыта с открытой внешностью по умолчанию см. [WINTER-INVENTORY-2022](WINTER-INVENTORY-2022.md). Команда tools/run_winter_2022.py доступна в исходном ROE_SERVER, не в этом контекстном репозитории.

Таблица реализованных сигналов и самостоятельные опыты: [run_roe_2022/SIGNALS.md](https://github.com/ROE-LIVE/run_roe_2022/blob/main/SIGNALS.md), коммит9c397b0. Там указаны opcode по направлениям, файлы настроек/обработчиков, проверка событий в scene/events.jsonl и пример изменения урона/времени аирдропа. Ручной reader --live-commands есть в низкоуровневом peer, но Windows CMD пока не подключает его; интерактивная панель управления отсутствует.
