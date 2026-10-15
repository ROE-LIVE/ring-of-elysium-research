# LOOK01 — сверка каталогов2022,12.10.2026

EXE0.2.989.0 x64, SHA2562dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18; независимые runtime/Proton319–321, loopback. Задача остаётся ready80: холодный гардероб ещё не подтверждён устойчиво.

## Подтверждено

Четыре выбранных члена оригинального TableBin.sfc v3 прочитаны адресно и побайтно совпали с прежней и новой распаковкой. 2CF:offset10305941/SHA33898dd6… —451строка/450ID, единственный одинаковый дубль7200001.989:26107466/SHA484a9236… —361ID;5FB:20050313/SHAfd1cc2a7… —197брелков;A89:27966169/SHA1be17206… —1340itemстрок. Полные SHA/размеры/offset в primary-archive-verification.json.

Одежда:1151строка восьми позиций;795 имеют положительный срок,356 постоянных строк объединены в189 сочетаний position/male/female model. Выдаётся минимальный постоянныйID на сочетание; это наша offline-policy, не доказательство исторической доступности. Все189 выбранных pickableTRUE, временныхID нет. Распределение:27hat/14glove/12glasses/23mask/35shirt/31coat/29pant/18shoe. Ни отсутствующихID, ни лишних, ни дубликатов в выдаче450/361/197/189 нет; character_groups совпадает с989.

Новый audit_cosmetics_catalog_2022.py воспроизводит сравнение, сохраняет SHA/дубли/алиасы, отвергает конфликт одногоID, отрицательный срок, отсутствие моделей, DTD и неверныеID. Старый каталог менять не понадобилось. Native320:54E1→140C8CCA0/v117,73AA→140CA5B20/v118,73B0→140CA5CD0/v118,5FB→140C28460/v136; rc0, used=length1808/1484/1588/15511. Читались только требуемые code-страницы своего процесса; эмуляция decoder не доказывает cardinality всегоUI.

Native319 показывает персонажей/Saki407, M4RagingSea с доступнымEquip, брелки отWalkieTalkie доLittleBear в конце списка, одеждуPermanent/Owned после выбораSaki и возвратаDefault. Новые proxy-проверки: повторныйENTER_GAME в том жеTCP не выдаёт второйкаталог; новыйTCP получает одинполныйкаталог; чужойUID не меняетвыбор. Записи выдачи поодномунаconnection в selected-cosmetic-events.json.

## Отрицательный результат

Холодный320: Defaultженский→Customize показываетItemRenderer/пустойгардероб, включаяOwned. Восемь снимков зафиксированы до окончания процесса, но отсутствие остальных значков делает переключение категорий неуспешным: не выдавать их за восемь успешных проверок. Клики17:03 послеtimeout недействительны и исключены из доказательств.321: opt-in initialize_default_avatar=True отправляет пустой73A1, однако в17:10 гардероб также пуст. Опция экспериментальная, поумолчаниюFalse; конфигурацияWindows её не включает. ВыборMr.DMM17:11 открывает charactercustomize, а не wardrobe; исправления одежды не доказал.

Гипотеза: требуется дополнительная инициализация default/gender/customization. Не установлено, связан ли дефект с порядком сообщений, USERINFO или UIstate. Нужен следующий адресный опыт: сравнить wardrobe после Saki→Default наfreshfemale, сохранить только публичные cosmeticrequests и проверить собственные поля default/gender. Перенос внешности в матч/сохранение одежды/полныйcatalogappearance — отдельныеLOOK02–04. Windows нового опыта ещё не проверен.

## Проверки и повтор

479source/439portable tests прошли; verify-only cycle/Bots/LiveControl и.NET8Release0errors/0warnings. Один тест переноса сначала обнаружил отсутствие captures/ в свежейрепе; исправлено созданиемкаталога в тесте. КодLocalCosmetics также нормализует iterableконтейнеры и раньше проверяет типID, не меняя штатных payload.

Команда аудита из ROE_SERVER: python -B tools/audit_cosmetics_catalog_2022.py --tables research/extracted/all-sfc/SFC/TableBin --compare research/builds/2022/winter-inventory-20261007/account-all-local.json --output NEW-REPORT.json. Файлoutput должен бытьновым. В portableрепе можно сравнить config/cosmetics.json с доступной копией четырёх XML; игровые ресурсы не коммитятся.

Windows запуск прежний: .\run-roe-2022.cmd -Mode cycle. Каталоги включены поумолчанию;Appearance доступен доTraining. ПроверитьweaponEquip/charactergroups/accessorytail, аDefault→Customize отдельно сообщить сrunлогом. Прогоны319–321 завершены поtimeout; контрольные суммы выбранных оригинальных иruntimeEXE/DLL сверены вcleanup-checks.json.
