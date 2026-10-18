# Состояние плана восстановления2022

Версия плана: **3**; данные обновлены до **2026-10-18**.

Проценты показывают взвешенное достижение этапов этого плана. Это не доля исходного серверного кода, не оценка оставшихся часов и не готовность всей игры.

| Объём | Механик | Вес | Этапы, % | Полностью проверено | Заблокировано |
| --- | ---: | ---: | ---: | ---: | ---: |
| Минимальная зимняя сессия | 62 | 216 | 78.0 | 0 | 1 |
| Весь целевой план | 111 | 444 | 70.5 | 0 | 1 |
| Исследовательские ветки отдельно | 4 | 18 | 26.1 | 0 | 1 |

| Направление | Механик | Этапы, % |
| --- | ---: | ---: |
| Вход и транспорт | 9 | 64.8 |
| Персонаж и движение | 6 | 63.5 |
| Зоны и таймеры | 8 | 76.0 |
| Запуск и проверка | 7 | 79.1 |
| Генератор лута | 11 | 70.5 |
| Инвентарь | 8 | 75.8 |
| Зимние наборы | 5 | 86.7 |
| Оружие и попадания | 10 | 68.1 |
| Здоровье и броня | 7 | 62.8 |
| Погода и время | 5 | 66.4 |
| Аирдропы | 6 | 68.0 |
| Эвакуация и завершение | 8 | 84.4 |
| Транспорт | 7 | 65.3 |
| Боты и multiplayer | 8 | 61.0 |
| Аккаунт и внешность | 5 | 86.5 |
| Окружение карты | 1 | 57.5 |

Приоритет0 — сначала устранить блокирующую синхронизацию; приоритет1 — ближайшее восстановление механик. Зависимости в CSV указывают, что нужно для завершения задачи, и сами не означают готовность.

| № | ID | Механика | Очередь | Этапы, % | Следующий шаг |
| ---: | --- | --- | --- | ---: | --- |
| 3 | NET07 | Серверное время и первичный epoch | baseline | 90 | Повторить холодный старт вместе с позиционным контролем |
| 6 | ZONE02 | UI отсчёта и предупреждений | baseline | 80 | Проверить видимый warning-баннер после смены стадии на корректной точке спавна; затем START/BEGIN и исходный host→client 481 при late join. |
| 11 | NET06 | Переподключение с сохранением мира | baseline | 70 | WindowsW19; воспроизводимый отрицательный Citori374+prediction before further4A0 changes |
| 12 | NET04 | Потери и переупорядочивание UDP | baseline | 60 | LOOT05 lost821/82b; затем ACKwindow/FIN/expiry иWindows. Combined90+90с passed cold87 |
| 13 | NET05 | Повторы действий и идемпотентность | baseline | 82.5 | Vehicle/medical/rope иWindows; stale application-id native injection отдельно; own5actions/newAUTH подтверждены cold88 |
| 15 | LOOT01 | Спавн предметов по исходным координатам | baseline | 90 | Windows repeat door→оба марша→Origin12/12Gauge/scope199989; затем независимая верхняя точка и reconnect после pickup |
| 16 | LOOT03 | Связь типа точки с loot control | external_blocked | 30 | Нужен совместимый executable GenericStartLoot или authoritative capture известногоInstanceID/TypeId→definition/quantity |
| 17 | LOOT05 | AOI: выдача и удаление видимого лута | baseline | 82.5 | Windows/fullcatalog и исходнаяAOI отдельно; lost821/82b Protoncold90/91 confirmed |
| 18 | INV01 | Полный snapshot и delta удаления | baseline | 90 | INV02: pages/consumables/attachments; два weapon slots и два ammo уже поддержаны |
| 19 | LOOT06 | Подбор боеприпасов | baseline | 90 | LOOT07: другое оружие использует 5.56; затем общие пачки и страницы INV02 |
| 20 | LOOT07 | Подбор оружия с земли | baseline | 90 | INV02: consumable item union; native dual-gun reconnect и Windows повтор |
| 21 | LOOT08 | Подбор/замена брони и шлема | baseline | 90 | HIT03/ITEM02: исходный hit-zone и уменьшение прочности; сейчас INV02 общийinventory |
| 22 | INV02 | Общий инвентарь: страницы/слоты/item union | baseline | 50 | Сравнить native013 успешную цепь с реально задержанным изображением; UI-model/paint consumer не доказан. WindowsW19-06; flag1 сохранить. |
| 23 | INV03 | Выброс/повторный подбор с сохранением состояния | baseline | 90 | Проверить полныйкаталог/Windows; ограниченные M4/parts/armor drop+reconnect подтверждены |
| 25 | KIT05 | Вместимость и вес | baseline | 90 | Полныйcatalog/stackpages/Windows; cold99twoammo fullbag/drop/partial/handoff сохраняютколичество |
| 26 | INV04 | Частичные stack и остаток pickup | baseline | 90 | Полныйcatalog/stackpages/Windows; cold99twoammo fullbag/drop/partial/handoff сохраняютколичество |
| 33 | GUN01 | Стрельба Citori и магазин | baseline | 90 | Проверить пустой магазин и повтор11da |
| 34 | INV06 | Смена оружия и equipment slots | baseline | 82.5 | Windows W16-03/04: drop/repick иswap трёх экземпляров с ихclip/parts; grounddrag и3slots пользователь уже подтвердил |
| 35 | GUN02 | Перезарядка и резерв Citori | baseline | 90 | WindowsW19-01/02: полнаяR безанимации и обычнаяR; прочие семейства отдельно |
| 36 | HP01 | Синхронизация HP/максимума | baseline | 90 | Windows HP0/death; revive/downed отдельная исходная семантика, не выводить из1069. |
| 37 | GUN05 | Уведомление о попадании и HP цели | baseline | 92.5 | WindowsW19:10targets/two genuinekills/independentloot/Stats/secondTraining; originalhurtGUN07 отдельно |
| 38 | GUN07 | Исходный базовый урон и hit-zone | external_blocked | 12.5 | Producer140D09590 (return140D095D6) установлен; нужен original authoritative hurt/provider. Client energy/source geometry не определяют HP/head/armor. |
| 39 | HP02 | Прочность жилета/шлема: передача | baseline | 90 | HP03/HP04: originalhurt consumer или sanitized weapon/zone/armor/range/HP/durable; новыйWindows0/1 drop/repick. |
| 40 | HP03 | Броня: снижение урона | baseline | 77.5 | Windows OwnArmorAbsorbPercent50+Bots+cycle; original hurt/equipment trace для исходной формулы. |
| 41 | HP04 | Расход/разрушение брони от удара | baseline | 77.5 | Windows OwnArmorAbsorbPercent50+Bots+cycle; original hurt/equipment trace для исходной формулы. |
| 43 | GUN06 | Серверная валидация raycast/LOS | baseline | 67.5 | Совместный source terrain+Rock/static objects native контроль; низкие/дальние попадания и Windows. Точныйfloat query и исходная authority/баллистика остаются открыты. |
| 71 | EVAC02 | Трос: взаимодействие/подъём/посадка | baseline | 90 | Ранний native/tutor/time gate дляhover75s; Windows/interrupt отдельный повтор |
| 75 | OPS05 | Воспроизводимый полный одиночный цикл | baseline | 90 | WindowsW19 repeatmatch reset then nextmechanics; no originalhost/RNG claim |
| 115 | MAP01 | Разрушение стекла и частей статических объектов | baseline | 57.5 | Windows repeat WinterWindows; source classification/materials and remote snapshot; retain original physics caveat |

Источники, адреса, ограничения, критерии и этапы каждой механики — в [mechanics-2022.csv](mechanics-2022.csv). Порядок работ — в [README](README.md).

SHA-256 CSV: `27c00689a7edaf855fd0f95afb8995f7fbd72c2a3e37646090999c29d714fd6a`. Сводка создаётся `tools/recovery_status.py`; редактировать нужно CSV.
