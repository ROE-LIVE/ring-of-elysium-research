# Windows 2022: три оружия, перенос, Appearance и стекло

Состояние 14.10.2026 00:57 UTC. Источник пользователя: `logs/20261013T221638-9edd98`. Клиент: корневой Europa_Client.exe2022 x64 SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`. Адреса VA, image base0x140000000. Оригиналы не изменялись; native-опыты375–378 проводились в runtime/client через Proton, с loopback-сервисами в отдельном net namespace.

## Подтверждённое исправление INV06

Windows-профиль задавал weapon_slots2; сервер запрещал перемещение primary в slot3. Третий автоматический primary вытеснял оружие в занятом слоте. Native377 подтвердил перестановку3→1 через3E80/tag1 (BE `BBHBHHB`), со сохранением instance UID и патронов. Native378 повторил перестановку, после ручного подбора LVOA→3 и Origin12→2.

Перенос ground→equipment3B63 отличается от ПКМ: BE `IIQBHB3iB`, container1/destinationH/automatic0 против container0/destination0/automatic1. Native377 показал отказ старой проверки; native378 принял оба ручных переноса. Прочие ручные ссылки без проверки не разрешены. Разрешены три слота в отдельном profile3; legacy1/2 сохранили прежние ограничения. Автоподбор пистолета предпочитает свободный третий слот.

Native378: Citori после swap в третьем слоте стреляет2→1 и перезаряжается1/6→2/5; завершённая перезарядка и три экземпляра сохранились после реальной потери исходящего UDP20с/33drops, handoff22.434с. Resume_inventory_sync сообщает gun_count3; снимок inventory-three-after-handoff показывает LVOA1/Origin2/Citori3 и2/5. Последующая LVOA1 перезаряжается до30/30 и стреляет30→29. Pendingreload+WorldState из374 этим опытом не исправлен.

В Windows materialize установлен weapon_slots3, добавлены публичные причины отказа move и режим/номер назначения pickup. 549source/507portable unittest пройдены; verify-only и .NET Release:0ошибок/0предупреждений. Windows-повтор нового кода ещё нужен. Источники: server/directory/weapon_probe_2022.py, tools/windows_launch.py переносимого комплекта; исследовательские данные `research/builds/2022/recovery/windows-20261013-9edd98/{377,378}-public-events.json` и native-снимки.

## Appearance остаётся открытым

В native375 первое принятие Saki407 оставило Default-модель, как в пользовательском описании. Native376 проверил первичную73B3 инициализацию profile перед73A2: не исправило изображение. Неуспешная кандидатура сохранена только в исследовании и удалена из рабочего кода; Windows-комплект её не включает. Нужен путь обновления lobby display, вызываемый при Accessories→Appearance; принятый skin ID сам по себе не доказывает обновление модели. Предыдущие адреса/наблюдения322/323: recovery/105-look01/20261012T2058-cold-wardrobe/report.md.

## Стекло: структура найдена, исправление не заявлено

Исходный ENTITYSTATUSINPXSCENE.XML SHA256 `77d9f53107757dc757158978a82c92bc2b3b2e871dbc55ca3fbdad5825805ef1`: в тестовом квартале19однокомпонентных объектов с threshold1/status1 и2двери. Идентификаторы/XYZ в quarter-interactables.json. SC6F55 record decoder140C9E730, SC6F56 batch decoder140C9EA00; record20байт, countU32+records+tailB. Native codec потребил20/25байт без ошибки.

Важное уточнение: wire parts передают абсолютную оставшуюся прочность. Consumer141354631 вычисляет oldHP−wireHP и пишет wireHP; setter1409AD440 вычитает именно вычисленную разницу. Нельзя считать wire поле непосредственно уроном. Setter хранит HP в partRecord+8 (stride12), а resource entry хранит status в partRecord+4 (stride8).

Native378 SC6F56/7691/HP0 изменил resourceHP и componentHP до0; batch19 сделал то же для7690/7682/7686. Адресное чтение ограничено разрешёнными entity ID и их компонентами, не дамп. Однако visual-break branch1409AD511 при r9=1 пропускает140B19B30; packet consumers передают1. На снимках целостность стекла/коллизии не установлена; проход/vault не подтверждён. Прочность0 отдельно не считается исправлением. Следующий опыт: найти C2S запроса разрушения и путь визуального consumer, сопоставить query6F59 (Windows два body85, raw не сохранён). Обновление01:14UTC: гипотеза о списке21ID отвергнута. Native379 vault окна7690 породил6F59/85bytes: ID7690, countU32=1, partDamageU32=1000, extraLengthB=72, native impactContext72. Primary decoder140C9EBE0 иsender141354840: массив значений урона, не индексов частей; в выбранную part записывается r9damage. Тестовый SC6F56/HP0 с тем же context72 применился кresource/componentHP7690→0. Visual иповторное столкновение проверяются отдельно.


## Автоматическое разрушение MAP01, 01:58 UTC

В native379 jump через7690 отправил6F59/85: entity7690,count1,damage1000,len72,impactContext. Прочность без ответа оставалась1. Адреса2022: decode140C9EBE0, sender141354840 (в массив выбранной части пишет r9damage, остальные0). Поле ранее названное списком partID оказалось массивом урона. Ответ6F56 использует абсолютную оставшуюся прочность и context72 из проверенного запроса. После ручного ответа nativeHP0, возвращение через то же окно снаружи внутрь прошло без повторного6F59 (position417280,557163,259419).

Native380 холодный с новым BreakableState: jump7690/1000, distance187.79см →server/nativeHP1→0 автоматически. Реальный C2SUDP20s/32drops/20.995shandoff сохранил состояние, выдан1snapshot; componentHP0. Затем Citorishot7691/1350,distance644.06см →server/nativeHP1→0;7690сохранил0, другие7682/7686остались1. Проход после выстрела через конкретный7691 ещё не привязан к ID, не заявляется. Сервер не восстанавливает оригинальную collision/материалы/авторизацию shots: учебный профиль onepart threshold1/status1, radius750см, проверкаownUID/count/context/finite, отрицательные/чужие/далёкие запросы отклоняются.

Исходный XML содержит7118сущностей с тем же профилем; динамически проверены2окна, остальные ресурсные кандидаты. generate_winter_breakables_2022.py сохраняетID/XYZ/source_line/SHA. Двери и multipart не включены. Состояние раздельное по одиночной сессии, переносится при handoff; совместная комната пока запрещена. Повтор не уменьшаетHP ниже0; impactContext сохраняется для resume.

Windows-команда послеgitpull: `.\run-roe-2022.cmd -WinterDoors -WinterWindows` (при необходимости прежние Kit/Mode/LootCatalog). Зависимости/ресурсы/путь клиента прежние. Проверитьjump/shotglass→уйти/вернуться, затем3guns иdrag. Вжурнале breakable_probe:entity_id/previous/remaining/changed/distance; winter_windows_enabled в launch summary. Windowsнового кода не тестировался.554source/513portabletests,verify-only/.NETRelease0warnings0errors. План3 добавляетMAP01/№115 с partial57.5; это этапы плана, не готовность игры.

## Appearance: адресные проверки381–386

14.10,07:32UTC. Cold382/386 подтверждают: первыйSaki407 принят, equipped/applied и TryOn/displaycache обновлены, изображение остаётсяDefault; после Accessories→Character появляетсяSaki. ACK-only383 оставил equipped0/appliedFalse; начальный AvatarAppliedTrue384 не исправил модель. Собственный native-call385 display3→2/TryOn407 не исправил изображение; отдельно pendant-call действительно изменил state3. Все кандидаты удалены из рабочего кода, helper не включён в Windows launcher. Native381 debuggerSIGTRAP завершил клиент3; это не контроль штатного UI.385 закончен timeout124, хеши выбранных EXE/DLL совпали.

Primary2022: 73A1 registration140EBB610→handler140EBBD60; ACK73A3→140EBC440/73AC→140EBC7A0 не заменяют73A1. Display140F148D0→childstate141191950; TryOn1411ABCC0→apply1411922C0; renderer14114A3D0 выбирает incremental14114A940/rebuild14114C1D0. GetEuAppearanceSystem Lua binding14261AAB0→1418C7B30 читает143040DB0; SetAppearanceState142D384F0→14183B6D0 записываетtype вobject+C8 (14183B8BE), непосредственной перерисовки в успешной ветке нет.

Readonly386: appearance_state−1 до меню,16Character,24Accessories,16при возврате. Skin/displaycache407 иконечныйappearance16 совпадают при разных изображениях. Это локализует следующий опыт: полный UI-переход SwitchToType/EnterCurve/events на UI-потоке и renderer invalidation, а не ещё один каталог или ACK. Промежуточное влияниеstate24 не исключено.11cosmetics regressions прошли после удаления кандидатов. Подробные отрицательные результаты и источники: snapshots/appearance-cold-20261014/appearance-evidence-381-386.md; исходный материал research/builds/2022/recovery/windows-20261013-9edd98. LOOK01 остаётся90по этапам каталога; cold-preview не закрыт. NET06 pendingreload+WorldState374 остаётся отдельным P0 с необходимым новым native-контролем postresume49F→4A0.
