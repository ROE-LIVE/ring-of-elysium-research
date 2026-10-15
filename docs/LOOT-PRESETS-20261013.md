# Лут зимней карты2022: источники и тестовый участок

13.10.2026, native360 под GE-Proton11-7. EXE из корня клиента2022,
x64 0.2.989.0, SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`,
map16010. Оригиналы не изменены; loopback peer, независимая runtime-копия.

## Что есть в первичных ресурсах

Именованные файлы находятся в
`research/builds/2022/full-extraction-20261010/extracted/`:

* `DATA/SERVER/EU_ICELAND_4096/ICELAND_001/ENTITYPOINTCONFIG.XML`:
  8313 точек, включая217/6023/1675 обычных точек TypeId1/3/5. Сохранены
  InstanceID, XYZ, Direction, имя архетипа и номер строки. SHA256
  `2187235d2dfa8adaee356428725bcb8087c6dd03a38a2e5af4de8298a0107f3c`.
  ICELAND_002/003/004 побайтово совпадают с001. Корневой файл другой,
  содержит741 точку: его нельзя автоматически складывать с001.
* `DATA/TABLE/EULOOT/EUENTITYLOOTCONTROLCFGTABLE_1.XML`:21 группа map16010.
  Строки40/46/52 — группы1/3/5, radius200, extraMax7, параметры40;50,
  20;23 и40;40. Строки28/34 — приоритетные51/52: scalar17;25,
  array17;29. Они расходятся; пулов iCtrlID51/52 в обычной item-таблице нет.
* `DATA/TABLE/EULOOT/EUENTITYLOOTITEMCFGTABLE_1.XML`:258 строк map16010;
  по60 строк в группах1/3/5, остальные — книги/коллекционные/сюжетные предметы.
  Есть iCount и дополнительные наборы. Например строка208: M4A1, definition10201,
  iCount27, варианты дополнительных5.56:2×30 с параметром60 либо3×30 с40.
  Название предмета не заменяет числовые поля: например строка202 содержит
  текстX30, но фактический ExtraItemStackCount15.
* Обе обычные именованные таблицы побайтово совпадают с уже проверенными
  TableBin000001bb/00000a71. Это уточнение путей, а не новая серверная версия.
* `DATA/TABLE/ENTITYTABLE/ENTITYTABLE_LOOT.XML`, строки4/6/8 связывают
  EntityID1/3/5 с EU_LootBox, но не содержат явного LootControl binding.
  `DATA/SERVER/SCRIPTS/10064/ICELAND_S.LUA:115` вызывает GenericStartLoot(sc_mid),
  без реализации выбора. `DATA/CONFIG/EUICELANDGAMEMODECFG.XML` содержит настройки
  границы замерзания, а не генератор лута.

## Что восстановлено практически

`tools/recover_winter_loot_presets_2022.py` создаёт `audit.json`, `presets.csv`,
`items.csv`, `points.csv` и интерактивную схему `map.html`. Щелчок показывает
InstanceID/TypeId/XYZ/исходную строку; колесо приближает участок. Это схема XY,
без изображения ландшафта; содержимое конкретной исходной точки неизвестно.

`generate_winter_loot_catalog_2022.py --bounds-cm XMIN YMIN XMAX YMAX` теперь
выбирает отдельный участок. `--authored-xyz` сохраняет высоту мебели/этажей;
дополнительные модели могут совпадать. Наш H1 выбирает предметы с возвращением,
использует iCount как вес, перенормирует поддерживаемый пул. Исходные RNG,
seed, применение квот, priority51/52 и TypeId→Ctrl этим не восстановлены.

Участок XY413000..419000/554000..560000, seed20261013:15 исходных точек,
24 предмета на10 занятых точках. Native360 получил каталог двумя пачками16+8.
В доме у точки199985, строка3498, XYZ416721,557410,259021 показаны LVOA-C
и патроны. Обычный right-click подобрал index100000×1 и100001×30; remaining0.
При диагностическом переносе за пределы AOI удалены22 оставшихся предмета;
при возврате выданы22, подобранные100000/100001 не появились снова.
Перенос — наш контроль, не обычное передвижение по всему кварталу.

## Повторение и границы

Из ROE_SERVER:

```bash
python -B tools/recover_winter_loot_presets_2022.py --extracted research/builds/2022/full-extraction-20261010/extracted --output research/builds/2022/recovery/loot-presets-20261013
python -B tools/generate_winter_loot_catalog_2022.py --points research/builds/2022/host-console-20261007/iceland-original-points.json --seed 20261013 --pool peer-supported --authored-xyz --bounds-cm 413000 554000 419000 560000 --output research/builds/2022/recovery/loot-presets-20261013/catalog-test-quarter.json
```

В Windows-комплекте каталог подключается опционально:
`run-roe-2022.cmd -LootCatalog config\loot-test-quarter.json -ReliableUDP -IdleHandoff`.
Он добавляет лут именно указанного участка; выбор клетки не переносится
автоматически туда, стартовые диагностические fixtures остаются. Windows-повтор
этого каталога ещё нужен. Индексы Windows-каталога180000..180023 и UID
переназначены, чтобы не пересекаться с фиксированными fixtures; координаты
и содержимое совпадают с native360. Основной запуск по умолчанию не изменён.

Результаты: `research/builds/2022/recovery/loot-presets-20261013/`;
игровой прогон: `research/builds/2022/host-console-20261007/recovery-loot-presets-20261013-360/`.
522 Python-теста прошли, включая41 по луту; suite выдаёт ResourceWarning
незакрытых сокетов в существующих сетевых тестах. EXE/DLL до/после совпали,
собственный runner завершён143 и очищен. Portable481тест, проверка
каталога через verify-only и .NET8 Release также пройдены.

Следующий эксперимент: проверить обычным движением несколько зданий и этажей
этого каталога, сбор комплектов/возврат/AOI, затем расширять участок. Для точного
оригинального генератора нужен исполняемый server-provider GenericStartLoot
или обезличенная исходная запись match layout с известными InstanceID,
выбранными definition/quantity и несколькими последовательными матчами.
Одни XML-параметры неоднозначность алгоритма не устраняют.
