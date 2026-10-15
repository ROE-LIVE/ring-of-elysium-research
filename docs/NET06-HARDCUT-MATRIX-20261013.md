# NET06: жёсткий TCP-разрыв во время перезарядки

13.10.2026, 12:51–13:25UTC. Корневой EXE2022 x64 0.2.989.0, SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`, map16010, база0x140000000. Настоящий portable peer f38b29d и Proton-клиент в разных loopback network namespaces. Согласование одного дополнительного final4A0 взято из NET06-PREDICTION-20261013.md без изменения политики.

| Опыт | Перед R: магазин/резерв | После разрыва: peer/HUD | Расход резерва |
|---|---|---|---|
|363 Citori slot1|1/6|2/5|1|
|363 Citori пустой, автоматическая R|0/3|2/1|2|
|364 M4 slot2|29/20|30/19|1|
|364 M4 пустой, резерв меньше магазина|0/19|19/0|19|

Fault bridge действительно закрывает активное TCP-соединение и отклоняет новые20с. Backend жив; authenticated_idle_relay наблюдался спустя23–26с после последнего трафика. В каждой настоящей pendingreload одно согласование `repeats=1`; новая application, не transport duplicate. Числа подтверждены собственными числовыми getters, reload events с ammunition_definition30001 для M4. После последнего случая выстрел и короткая очередь дали18/0→16/0, сервер и getter совпали.

## Первичные данные и ограничения

363/364/native-magazine.json: четыре аппаратные точки140E7E04B,141323390,1413235F1,140E7E051; code_patched=false/registers_written=false. Handler140E7DEC0→virtual140D032D0→prediction141323390→publisher140D032C0/gun+90. 363-empty аппаратный захват начат поздно, rows0: этот случай подтверждён getters/events, свежая handler-трасса для него отсутствует.

В364 у M4 остаётся prediction node counter0/kind1/predicted clip2. Authoritative становится19, HUD19, последующие выстрелы корректны. Причина остаточной записи пока неизвестна; нельзя заявлять полное согласование очереди всех видов оружия. Возможная связь с исходным ITEM_DATA fixture — гипотеза, не вывод.

Первый кандидат363-empty-request.json **недействителен как pendingreload**: автоматическая R завершилась, пока вводились getters. Сохранены invalid-note и отрицательное ограничение. Исправленный empty_cut.py реагирует на собственный server reload_started/clip0 и сразу закрывает соединение; правильные запросы *empty-actual-request.json.

Этот portable walk-профиль не создаёт WorldState: world_position/HP/stage в handoff null. Опыт доказывает ammo/inventory handoff, не сохранение полного календаря/HP/мира. Реальный Windows/SSH/LAN отдельно. NET06 остаётсяbaseline70.

363/364-public-events.json, *public-getters.tsv, *request.json, native-magazine.json — выбранные первичные данные. Raw auth, ключи, игровые бинарники и полные дампы не включены. Собственные процессы остановлены, cleanup JSON; выбранные EXE/DLL original/runtime SHA до/после совпадают, файлы независимы.

Дополнительно исправлена только телеметрия: fire/handoff теперь имеют ammunition_definition/ammunition_quantity. Старое reserve всегда относится к12ga и сохраняется для совместимости; для M4 оно6, а не19/0. Новая регрессия проверяет именно это отличие. Новая телеметрия не была частью native364; игровые wire-пакеты не изменены.

Следующий опыт: обычным движением пройти квартал исходных loot points; затем отдельная M4 prediction fixture/reload queue и Windows-повтор.
