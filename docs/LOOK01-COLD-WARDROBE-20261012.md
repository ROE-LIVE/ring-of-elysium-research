# LOOK01 — открытие холодного гардероба, 12 октября 2026

Клиент 2022, корневой Europa_Client.exe 0.2.989.0 x64, SHA-256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`. Только независимая runtime-копия, Proton и loopback. Продолжение девятичасового поручения начато 20:55 UTC; крайний срок 13 октября 05:55 UTC. Это промежуточный этап, а не итог девяти часов.

## Наблюдения

Прогон 322 с новым файлом выбора: прямой Default → Customize снова показывает ItemRenderer вместо одежды. Выбор Saki407 отправляет 73A2/73AB/73AD, отметка выбора меняется, но модель остаётся прежней даже через несколько минут. Возврат Default не открывает гардероб. После перехода в Accessories модель Saki действительно появляется. Затем Character → Default → Customize открывает полноценный гардероб.

В 322 проверены восемь разделов с включённым Owned: Hat, Gloves, Glasses, Mask, Tops, Outer Layer, Bottoms, Shoes. В каждом видны предметы Permanent. Красная Winter Trapper Hat действительно появляется на модели при клике. Это проверка разделов и одного предпросмотра, не подсчёт всех 189 предметов и не сохранение одежды.

Повтор 323 также использует новый пустой файл выбора. Прямой Customize пустой. Более короткий путь **Appearance → Accessories → Character → Customize** открывает гардероб без выбора Saki. Во время этого пути новых cosmetic_request, повторной выдачи каталога и ответов серверной инициализации нет. Каталог 450 оружейных / 361 персонажей / 197 брелков / 189 постоянных моделей одежды выдан один раз.

Начальные ответы upstream: 2EF LOGIN_WORLD_RSP (2288 байт тела), 72D9 (4), 1F5F (24), 32B ENTER_GAME_RSP (29). Позднего 5FB или другого cosmetic sync от upstream в выбранном отрезке нет. LOGIN_WORLD_RSP в 319–322 имеет одинаковый SHA-256 тела `7d12a553a86edbbdb6ee01ab9dd6025c77eeb6831e1ce4b10ad86db3135b6f31`. AUTH не разбирался. Проверены только выбранные блоки собственного захвата; результат содержит код/длину/хеш, без тела и ключа.

## Источники и границы

Первичные Lua: `full-extraction-20261010/extracted/DATA/SCRIPT/LOGIC/GAMEPLAY/UI/CLOTHESCHESTPANEL/CLOTHESCHESTPANELLOGIC.LUA`, строки 32–125: конфигурация от GetEuCharacterEquipTryOnSystem:GetClothesChestConfig, фильтр makeup_level==1 и num>0 при Owned. `APPEARANCE/APPEARANCEMENUPANEL/APPEARANCEMENUPANELLOGIC.LUA`, строки 52–97: смена раздела вызывает SetAppearanceState и SwtichLobbyDisplayState. `APPEARANCECHARACTERPANELLOGIC.LUA`, 311–344: TryOnSkin/EquipSkin. Это первичный код интерфейса; внутренний C++ переход пока не разобран.

Нативные decoder и адресная сверка первичных SFC остаются из предыдущего отчёта: 54E1→140C8CCA0, 73AA→140CA5B20, 73B0→140CA5CD0, 5FB→140C28460. Новая проверка не меняет payload и не доказывает исправления renderer.

Гипотеза: смена display state инициализирует базовую модель и доступную ей конфигурацию одежды. Наблюдение исключает необходимость выбирать Saki или заново выдавать вещи в проверенном пути. Конкретная внутренняя причина, автоматический server-only способ и Windows-повтор остаются открытыми. Обходной путь применять вручную; Lua/клиентские файлы не патчились.

В прокси добавлен журнал cosmetic_upstream_order: только opcode и body_length, без содержимого. Проверка существующего асинхронного теста подтверждает отсутствие raw/fields_hex в этих событиях и прежнюю выдачу один раз на TCP. 479 исходных и 439 portable тестов прошли. Сборка .NET и verify-only проходят; исправлен вывод справки Windows launcher (литеральный процент в argparse).

## Повтор на Windows

Запуск прежний: `.\run-roe-2022.cmd -Mode cycle`. До Training открыть Appearance → Accessories → Character → Default → Customize. Если Default уже выбран, достаточно Character → Customize. Включить Owned и проверить категории. Сохранение и перенос одежды в матч относятся к LOOK04. Следующая задача по порядку — LOOK02: выбор оружейного skin, повторный вход и применение на карте.

Артефакты: `322-upstream-order.json`, `login-world-comparison.json`, `322-selected-events.json`, `322-wardrobe-actions.json`, `322-owned-all-categories.png`, `322-cleanup.json`; PNG обоих прогонов в собственных каталогах 322/323. 322 завершён адресным SIGTERM своего timeout, exit143; выбранные EXE/DLL оригинала и runtime совпали до/после. 323 также остановлен адресно, exit143; выбранные контрольные суммы неизменны, см. 323-cleanup.json.
