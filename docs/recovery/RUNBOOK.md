18.10.2026, PM: terrain surface LOS opt-in на исходном PXBIN; native014 два genuinekills/UDP20s/StatsKill2Rescued1→новыйTraining10fresh nativeHP100.016 Citori2/6→2/5→2/4. INV02 measured pickup не воспроизвёл задержку картинок; исправления UI не заявлять. WindowsW19 остаётся действующим. План3/115строк/гейты без повышения; native host и originalhurt не восстановлены. См. ../SESSION-RESULT-20261018-PM.md и ../TERRAIN-LOS-20261018.md.

Контроль11.10 15:20UTC: NET09223/224/225 — FSM0 сам по себе не блокирует walk: прежнийUID242C10.4м, новый242Dsolo0м, новый2430(low2bits0)10.4м безпосадки. СемантикаUIDlowbits — гипотеза; следующий контроль2434 и пара2430/2434.

11.10.2026 ~15:00UTC: №87 CAR06 baseline60/partial — native6554 HP10800/16200/21600→HUD0.5/0.75/1.0, accepted Citori-bodyhit17100→0, состояния1/2/3 и6547/6548 пассажир2/водитель1. Учебный500raw/pellet только opt-in; fuel/parts/passexplosion открыты. №88 NET09 ready40/partial — конкурентное лобби, два nativeклиента с разнымиUID и удалённые аватары; C2S2A→SC27→nativeXYZ в обоих направлениях. Общиеloot/HP/clock/vehicle/pose/leave не готовы; uniqueUIDinitialFSM0 требуетFпосадка/Fвыход. Следующая работаNET09: общийroomregistry и одновременныйpickup бездублирования.360source/317portable/.NET0errors;Windowsновыефлагиpending. Источники: research/builds/2022/recovery/087-car06/20261011T1150-native-hp/report.md и088-net09/20261011T1330-lobby-concurrency/report.md.

# Профили опытов для CSV-плана2022

Все команды здесь выполняются из **ROE_SERVER/** после AGENTS.md, поручения задачи и проверки стенда. Ни один профиль не является готовой реализацией всех задач своей группы. Это исходная проверенная база для адресного изменения. Встроенный host не запускается. Docker не используется. Оригинальные клиенты не меняются.

## Подготовка

1. Получить поручение: `python -B tools/recovery_task.py --task ID` и проверить `--preflight`. Прочитать только указанные agent_context и адресные первичные доказательства.
2. Нужны полная независимая `runtime/client`, prefix `runtime/proton-2022`, GE-Proton11-7, Python3.11+/cryptography/lz4/capstone/Pillow, .NET8 lobby build, Xvfb/xdotool/xwininfo, рабочий Vulkan и `sudo unshare --net`. Runner использует `/opt/conda/bin/python`, `/usr/bin/python3`, vendored dotnet, пользователя jovyan и NVIDIA ICD. Для другого сервера адаптировать **наш runner** и сохранить факт адаптации; эти пути не универсальны.
3. Локальный `research/builds/2022/session-06-review/candidate-001.key` должен быть доступен bridge. Значение не выводить. Fixtures, resources и ключ не входят в переносимый agents-context. При нехватке назвать материал и выполнять независимую статическую часть.
4. Проверить свободное место: runner требует16GiB; исключить собственные старые процессы/использование prefix другим опытом. Не останавливать чужие службы. Убедиться, что в runtime не остались экспериментальные EuGameServer.json/GM-маркеры; неизвестные файлы не удалять без выяснения происхождения.
5. Профильные JSON могут содержать абсолютные пути прежнего workspace. При переносе адресно проверить ссылки на ground/parcels/region grid/packet fixtures. Новый конфиг подготовить в каталоге результатов; оригинальные/исторические входы не перезаписывать.

Подробная существующая архитектура запуска и исходные материалы: [host-console README](../../research/builds/2022/host-console-20261007/README.md). Подготовка постоянной среды — репозиторий `git/jupyterROE`; переносимый контекст — `git/agents-context`. Обычный повтор не требует GDB; адресная трасса MOVE02 использует GDB по необходимости и только при разрешении такого опыта.

## smoke: вход, часы, движение, сноуборд

Новое имя содержит ID и UTC; его задаёт агент, не переиспользуя прежний run:

```bash
python -B research/builds/2022/host-console-20261007/run_trial.py recovery-NET01-YYYYMMDDTHHMMSS \
  --scene ../winter-kit-loot-20261007/scene-grounded.json \
  --weapon ../winter-kit-loot-20261007/preset-snowboard.json \
  --environment ../host-console-20261007/environment-winter-hour8-5c.json \
  --selection-seconds 47 --live --duration 300
```

`run_trial.py` сначала проверяет входы; создаёт новый каталог в host-console и запускает `run.sh` через отдельный loopback network namespace. Автоматический UI выполняет путь lobby/Training/выбор стартовой клетки. Не считать exit124 ошибкой само по себе: это ограничение времени процесса; проверять достижение нужного события и cleanup. Прочие ошибки не скрывать.

Результат runner остаётся в `research/builds/2022/host-console-20261007/ИМЯ/`; report/evidence задачи — в её `result_dir`, со ссылкой на реальный run. Не переносить активные run/captures.

## loot: исходные точки и инвентарь

Использовать smoke-команду и добавить:

```text
--loot-catalog ../host-console-20261007/catalog-original-winter-h1.json
```

Это6843позиции поддержанного H1-подмножества, а не исходный RNG. Не включать `--loot` для опыта, где требуется ровно одно контролируемое ручное действие. Настоящий pickup/drop делается через UI; server events сверяются с reserve/clip/ground/quantity. При новом типе предмета сначала decode/state/encode тесты, затем отдельный клиентский контроль; не рассылать весь неподдержанный pool.

## world:180-секундный контроль MOVE02/ZONE02

Подготовить **новый** JSON из `host-console-20261007/world-countdown-control.json`: одна обычная стадия `stage=1`, `at_seconds=0`, `duration=180`, `elapsed_seconds=0`, без последующих стадий и warnings. Сохранить допустимые поля и verified region grid path; HPfloor1000 в контрольном источнике исключает побочный урон. Не править исторический файл. JSON разместить в новой подпапке `result_dir`; runner принимает **абсолютный путь** к нашему конфигу.

Использовать smoke с новым именем и `--duration 600`, добавить:

```text
--world /ABSOLUTE/PATH/TO/NEW/world-180.json --no-auto-weapon
```

Для №5/MOVE02: дождаться первого инвентаря/видимого отсчёта. В первом run отправить **только27**, во втором только2b, в третьем исходную последовательность при необходимости. Сохранить текущую позицию из адресного state/MOVE, чтобы отделить изменение координат от clock/FSM. Тело27 — известный40B-шаблон `position-original-points-b.bin`, own UID и tick+31; поля и clock проверить по native decoder. Не выдавать произвольный enum за исправление.

`queue_actor_position.py` отправляет **2b5→27→2b0**: его нельзя использовать как27-only или2b-only контроль. `--live` читает `live-commands.json`; формат и подстановки — `server/directory/live_scene_probe_2022.py`. Агент готовит отдельные адресные команды и записывает их состав/момент в evidence. Observer `0x141185f5e/0x140e88150`, чтение своего actor+0x1e4 — дополнительная проверка, не замена UI.

Снимки: до сообщения, через10/30с после receipt, пока180с ещё не кончились. Учитывать время доставки, не только записи команды в JSON. Два PNG0:00 вне активной стадии не устанавливают причинность. Для №6/ZONE02 обычный timer уже подтверждён. Финальнуюstage50 проверять отдельно при открытой карте и послеM; Lua finalguard может оставить map header старым при исправном nativeclock. См. research/builds/2022/recovery/005-move02/20261008T0915/report.md. Проверить финальное отображение и warning-матрицу, не менять clock/FSM по прежней корреляции.

## combat: контролируемая цель

Использовать smoke с **согласованной** сценой, которая создаёт actor через565+BE7, и отдельным `--actor actor-bot-basic.json` из iceland-gameplay. Наличие actor-конфига само не создаёт модель: взять проверенную сцену из [первичного отчёта](../../research/builds/2022/iceland-gameplay-20261006/report.md) и подтвердить UID/counter/wire. Не смешивать произвольный fixture с чужим actor UID.

Сначала одна неподвижная цель, один hit и отрицательный контроль. Hit report11dd сам по себе не доказывает raycast/LOS или формулу брони. Для GUN07/HP03 нужен исходный расчёт либо известная hurt/equipment трасса; фиксированная наша формула должна быть явно помечена diagnostic.

## full: общий календарь, контейнеры, эвакуация

Использовать команду существующего [полного профиля](../../research/builds/2022/host-console-20261007/README.md) с новым run name: scene-combined-source-cadence, world-source-ai1-rebased, environment-hour8, loot-catalog, parcels, preset-snowboard, selection47, live, evacuate15, evac-result и duration2400. Она дождётся540с последней стадии; короткая duration300 не подтверждает полный календарь. В новом workspace проверить все ссылки fixtures перед запуском.

Поздний полёт/hover/finish/Stats в этой базе диагностические. Не использовать перенос к вертолёту для доказательства штатного подхода/посадки. Успешный full-source run и no-GM отрицательный повтор уже существуют; следующий full-повтор оправдан после конкретного исправления либо для адресной проверки новой механики.

## resources/manual/windows/lan

- `resources`: статический разбор выбранных таблиц/адресов. Клиент не требуется. Запуск Lua с собственными Generic-заглушками остаётся исследовательским stub execution. Недостающий provider/capture назвать точно.
- `manual`: нужен отдельный обоснованный опыт/новый материал. Универсальной команды для host/AI/общего multiplayer сейчас нет. Составить исполнимый новый рецепт и сохранить его, не подставлять smoke как доказательство этой задачи.
- `windows`: `git/run_roe_2022` с его README/VALIDATION/SIGNALS; native Windows11 в отдельном сеансе. Новый Proton-профиль ещё не переносился автоматически; сначала синхронизировать реализованный объём и зависимости.
- `lan`: отдельно проверяемый2022 Windows↔Linux стенд. Существующий V99 результат не доказывает эту задачу; адресLAN и разрешение наружного bind задаёт пользователь текущего опыта.

## UI, доказательства и окончание

UI helper читает display/xauthority конкретного run, сохраняетPNG. В отдельной оболочке:

```bash
ROE_RUN_DIR=/ABSOLUTE/PATH/TO/ACTUAL/RUN \
python -B research/builds/2022/iceland-gameplay-20261006/ui.py before --key Tab
```

Каждому снимку новое имя. `--hold w 3`, `--key r`, `--key f` — действия UI, не доказательства принятия сервером; сверять выбранные события endpoint, состояние и native response. Не читать полный дамп или сырые авторизационные captures ради одного события.

В конце: остановить собственные процессы, подтвердить cleanup и selected hashes, сохранить report/evidence/checks; обновить CSV по инструкции AGENT-START. Повторять общий137+ suite не требуется для документальной правки; для изменения игровой логики выполнить профильные тесты, затем необходимые интеграционные проверки. Новый negative result сохранять рядом с positive; не переписывать историю.


## Два gun slots и пассивная мишень08.10

Windows: `git pull --ff-only`, затем `.\run-roe-2022.cmd -WeaponProfile m4 -Target armored` вrun_roe_2022. Это перенос текущегоpeer; физическийWindowsповторещёнужен. Plain — отдельныйконтрольбезброни. Не включатьBotsвместесTarget.

ДляProton сначалаmaterialize изактуального `git/run_roe_2022/tools/windows_launch.py` сего `server/directory` вsys.path вновыйresult_dir. ПроверитьWeaponFixture:2/delta/timedTrue; ActorFixture armor300/50%. Затем run_trial.py сgeneratedscene-walk/weapon-snowboard/target-armored/parcel/cosmetics, selection47, --no-auto-weapon, --live, duration1200. [Фактическийcold51 иисточники](../../research/builds/2022/recovery/022-inv02/20261008T2036/evidence.json). Командавыдачикарточкисамаигруне запускает.

NativeUI: pickupM4+5.56 →pickupCitori →1/2fire/R →drop/repick каждого;отдельноcancel switch. Дляarmor — одиночныеM4hit/miss,не очередибезкомпенсацииотдачи. СверятьnativeHP/durable, peerсобытия иUI,не тольконашлог. Исходнаяформулаурона/защиты/LOSнезакрыта. Старыеfixturesпоумолчаниюоставляют1slot/immediate reload — включатьновыеполяявно.
