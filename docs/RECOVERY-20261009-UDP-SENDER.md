# NET04: повторная доставка серверного ответа,2022

Клиент x64 0.2.989.0, зимняя карта16010; EXE SHA2562dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18. Опыт09.10.2026,14:08–14:12UTC; независимый runtime, Proton GE11-7, loopback namespace. Оригиналы не изменены.

## Реализация

`server/directory/reliable_udp_2022.py` хранит исходные датаграммы до cumulative ACK, проверяет serial32/wrap и отвергает ACK за границей отправленного. Повторяет те же байты без повторного AES/frame counter/игрового обработчика. SYN занимает один байт sequence. В endpoint повтор SYN с тем же clientISN сохраняет текущую сессию. Новый режим включается только `--reliable-udp`; обычный Windows launcher его не включает.

Параметры нашего стенда: первый повтор250мс, exponential backoff до2с,8повторов, максимум2048датаграмм/1MiB на sender. Это собственная политика, не найденные константы игры. Исчерпание повторов/переполнение отмечается udp_delivery_failed и прекращает выдачу sender. Входная сборка/reorder пока отсутствует; нет утверждения о восстановлении полного reliableUDP.

## Первичные результаты

Прогон: `research/builds/2022/host-console-20261007/recovery-net04-sender-20261009-77/`. Начальный handshake и вход в сцену прошли без udp_retry/frame_error. В14:10:35.915 fire: Citori clip1,reserve6.

В14:11:03.410 установлено правило OUTPUT в собственной namespace: UDP sport18001, IPv4 length80:65535, statistic nth first. В14:11:07.028 удалено через finally. Счётчик ровно1пакет/109IPбайт; opcode правилом не фильтровался. В14:11:03.518 отправлен81-байтный UDP-пакет seq268454634 (57байт L1data) при reload_started. В14:11:03.781 зарегистрирован единственный udp_retry этого sequence. В14:11:03.782 штатный клиент прислал ACK268454691, точно конец сегмента. Через0.264с повтор получил подтверждение. Сохранённые источники: single-loss.json, loss-headers.json, selected-events.json. L1 sequence — смещение+4, ACK+8, длина заголовка — старшая половина байта+12.

В14:11:05.236 ровно один reload amount1,clip2,reserve5. PNG24-sender-after-loss показывает2/5; затем W0.6с, PNG25-sender-movement. Нет handoff/reconnect и udp_delivery_failed. Без расшифровки исходящего пакета не приписываем ему доказанный wire opcode; временная связь с reload_started и источник encoder49d согласуются с ответом начала перезарядки.

Шесть новых тестов: потерянный reload response повторяется побайтно, повтор запроса не списывает патроны; cumulative/partial/future/stale ACK и wrap; ACK без флага; repeated SYN; backoff/исчерпание; предел памяти. Основное дерево208tests, Windows-комплект136tests, verify-only прошёл. Это тесты и Proton, не новый nativeWindows-повтор.

## Границы и следующий шаг

NET04 остаётся ready60%, NET05 baseline82.5%, NET06 baseline70%; этапы не повышены. Cold75 client→server20с отрицательный результат не исправлен данным опытом. Следующий шаг — ограниченная входная сборка потока, детерминированная перестановка двух сегментов и повтор ACK; затем отдельно20с client→server/SYN/AUTH. Не включать sender по умолчанию до этих контролей.

Свой timeout22461 остановлен, runner exit143; active_clients пуст. SHA256 EXE/двухDLL до/после совпадают с оригиналами, файлы независимы. Сырой трафик, ключи и бинарники в Git не передаются.
