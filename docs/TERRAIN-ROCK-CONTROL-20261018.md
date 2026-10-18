# GUN06: совместный fixture terrain+Rock, native017

18.10.2026, корневой2022 x64 SHA256
`2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`,
Iceland16010. Тот же опубликованный код terrain LOS; изменений кода в опыте нет.

В проверенный actor fixture одного source Rock305 добавлен только
`collision_heightfield_file` с известным LinuxPXBIN. Сцена сохраняет прежний
диагностический spawn около камня; это не обычный путь игрока из DEFAULT.
Настоящие drag подобрали M4/AK/боезапас/RedDot, M4reload30/30.

Шесть одиночных выстрелов. Два настоящих запроса11DD (counter3/4) приняты:
terrain_checked=true, validation=diagnostic_ray_material,
collision_record_count=0, penetration={}, peerHP1000→900→800.
Они проходят **выше края**, а не через материал. Нового native-сэмпла HP после
них нет. Для остальных четырёх выстрелов11DD не получен; по этому отсутствию
не различаем промах и остановку камнем.

**Совместный положительный контроль открытого луча получен. Пробитие в
совместной конфигурации не подтверждено.** Проекция луча при X371500 сама по
себе не является измеренным impact. Последовательное воспроизведение мыши
старого009 не повторило его точный луч: recoil/input/spread не изолированы.
Следующее: адресный контроль фактического projectile query у тонкого края,
затем genuine count2 черезRock с terrain guard. Этапы GUN06 не повышены.

Материалы:
`research/builds/2022/recovery/043-gun06/20261018T1730-terrain-rock-joint/`:
launch017-args.json, actor-terrain-rock.json, drive017.py/log,
native017-shots.json, native017-open-hits.json, cleanup.json.
Все записи ресурсов/полные raw-пакеты остаются вне Git. Выбранные EXE/DLL
хеши до/после совпали, собственный запуск остановлен.
