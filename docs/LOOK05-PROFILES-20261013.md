# LOOK05 — отдельные локальные профили2022

13.10.2026,03:11UTC. Именованные профили сохраняют собственный выбор персонажа, одежды, оружейных скинов и брелков. Добавлен Windows-параметр `-Profile alice`; обычная команда сохраняет прежний профиль `default`. Это локальные учётки нашего peer, не восстановленная оригинальная авторизация.

Клиент: корневой Europa_Client.exe0.2.989.0 x64, SHA2562dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18, base140000000,map16010. GE-Proton11-7, независимая runtime-копия, собственный loopback namespace. Оригиналы не изменялись, Docker/Ghidra/дополнительные модели не использовались. Поручение9часов продолжается до05:55UTC.

## Реализация

`tools/local_account_2022.py` нормализует имя:1..32 ASCII, регистр не различается, пути/пробелы/имена устройств Windows запрещены. Профильdefault читает прежний `runtime/local-account/cosmetics.json`. Остальные — `runtime/local-accounts/NAME/cosmetics.json`. Helper не создаёт файлы. Лобби атомарно сохраняет собственный выбор; endpoint читает свежий файл при создании нового матча.

Логический profile ID `local-2022:NAME` постоянен. Synthetic actor UID устойчиво выводится из имени, low2bits0 основаны на прежнем native223–226. Новый run имеет отдельный session ID в launch-summary; это ID журнала, а не оригинальный сетевой ticket. UID передаётся уже проверенному LobbyActorUIDStream: строго ENTER_GAME_RSP32B, decoded+22, исходные размер/шифрование сохраняются. Полноценная идентификация через LOGIN/USERINFO не заявлена.

## Нативные проверки

343 Alice/UID515BB152327080: cold Training с восемью вещами, Default персонажем, RainbowCitori10402210. Real UI Owned→HAT→Empty→Back снимает1000023; сохранённые equipment остаются13–19. ФайлBob не изменился побайтно.345 новыйAlice послеBob восстанавливает семь вещей, безшапки и сRainbow; native own actor+130 подтверждает definitions, gun+6C —skin. Сам файлAlice остался прежним.

344/346/348 Bob: неправильно составленный мной пресет `[0,0,0,0,407]` создаёт инвентарь, но камера/персонаж не появляются штатно на земле.347 сDefault тем жеUID даёт нормальную сцену.348 с прежним диапазономUID2434 и ошибочным пресетом тоже не исправляет сцену. Это отрицательные контроли; они не доказывают дефект новогоUID.

Первичный GUI-выбор337 хранит **`[407,0,0,0,0]`**. После исправления349 Bob/UID515BB17776DF68 появляется какSaki на зимней карте, одежда13–19/22 пустая, Citori skin0. W3с меняет нативную XY позицию на13.34м; реальный выстрел принят peer. Alice по-прежнему сохраняет семь вещей и свойskin. Не угадывать назначение остальных четырёх полей по owned ID.

Адресные чтения: world encoded1430958C0/143094D90→own actor; UIDactor+28; inventoryactor+130; equipment map+60; gun map+B0/skin+6C. Controlleractor+B0→+30→movement, XYZdouble+C0/C8/D0. По каждой проверке читаются только выбранные публичные поля, безAUTH/общего дампа. Первичные материалы:343/345/349-native-game-equipment.json,343/345/349-owned-gun-skins.json,343/344/345-isolation-check.json,349-movement.json,349-public-fire.json и negative-preset-control.json.

## Проверки и запуск

505source/466portable тестов, verify-only Alice/BobOK; .NET8 Release0warnings/0errors. Все собственные343–349 остановлены; selected EXE/DLL SHA до/после совпадают.

Windows: `git pull --ff-only`, затем `.\run-roe-2022.cmd -Profile alice -Mode cycle -WeaponProfile m4 -ReliableUDP -IdleHandoff`. ДляBob заменить толькоProfile. Закрыть предыдущий клиент перед следующим. Новый профиль получает доступный каталог, но не копирует выборdefault. Для Default одежды обходной путь Accessories→Character→Customize всё ещё нужен.

Граница: изоляция долговременной внешности и её игровых equipment; добытый в матче лут сбрасывается по правилам нового матча. Графика/UserData/клавиши общей runtime-копии, одновременные аккаунты, Windows/LAN и оригинальная авторизация не закрыты. LOOK05baseline82.5; далееOPS03 разделение клиента и peer.

Примечание к историческому snapshot: первый текст оценил LOOK05 как77.5 вручную; recovery_status по записанным этапам вычисляет82.5. Актуальны CSV и эта страница. В LOOK04 имя200906 уточнено поA89: snowboard; историческое planer неверно.
