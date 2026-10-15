# EVAC06: адресные контрольные поля D62

Билд2022 x64 0.2.989.0, map16010, EXE SHA2dca9b1e…6ba18. Cold166/167/168 — отдельные собственные runtime/loopback Proton, оригиналы неизменны.

Контроль A ошибочно менял wire141 как D46: на деле это вложенная NUL-строка nativeCBD. Native140C483C4 вызывает140BD8120 после двух массивов. Кодовый decoder отклонил A: rc−4,used143. Это ошибка подготовки, не отказ UI из-за rank7. Контроль B толькоdistance/time принят rc0,used174 и дал123M/02:03. TailD3E начинается144, D46=152, D4E=160 при исходном XXX.

Контроль C в cold167 доставлен01:15:45.104; повторный вход из Newspaper в Stats показал rank7/43,points71,coins73+29,distance234M,time03:04. Контроль D показалkill101 и большие64-bit поля. Primary140C47D6E/140C47D85 вызываютU64decoder140BCD2C0. Контроль E в cold168 нормализовалU64 damage1234 иpoints9; экран показалkill3,damage123HP,rankpoints11,killpoints7,damagepoints9,victorypoints13,rescued1,time02:00. EXP40 — сумма четырёх видовpoints; bonus42 приC8=19/D8=23 и прочих bonus0. Это наблюдение UI, не восстановленная экономическая формула.

РезультатD имелVictoryоформление, но изолированныйC4=1 (controlF, доставлен01:28:58.748) его не включил. ПоэтомуC4 не назван флагом победы; другой consumer/значение требует адресного разбора. Rescued1 само по себе вE не меняло оформление.

Схема confirmed-fields.json и native-control-checks.json разделяют wire/native/семантику. Нативная проверка использовала только четыре выбранные страницы decoder собственного процесса (16КБ), read-only /proc/PID/mem. Original PEpacked.tp6/vmp не имеет обычной.text, чтение файлового RVAmapping не использовалось. Полный dump/профиль/auth не читались.

Текущий source содержит отдельный учёт сеанса и явный режим reconstructed_session_statistics. Награды0, имя текущее, survival/distance/kills/rawdamage должны совпасть с событиями. Cold169 проверяет интеграцию; до этой проверки функциональный статус не повышен. Причина106E15 остаётся диагностическим мостом. Windows пока требует отдельного повтора.

## Собственный результат cold169

Имя WINTER169 взято из публичного профиля комнаты. M4 и50патронов подобраны черезUI; настоящая перезарядка30, 10 принятых hit reports по пассивной мишениHP1000→0. Серверный учёт:1000rawdamage/1kill/2pickup actions/51quantity/603сек/2680см/1rescued. Отдельные выстрелы безhit не увеличилиdamage. После обычногоW/F и настоящей657A/6541 газета иStats показалиWINTER169,1kill,100damage,26M,10:03,Rescued1. Рейтинг1/1 — политика одного локального игрока; rewards0; dailycap placeholder далlimit reached. Lootcount сохранён в журнале, поляloot наStats не найдены.

Учёт принятых C2S траекторий3D включаетподъём, серверный27reset не увеличиваетdistance; исходная политикадвижения/наград неизвестна. Freeze наdeath/rescue не позволяет поздним событиям менять итог. Native producer проверил результат с более длиннымUTF8/NULname:rc0/used180. Серверныйизнос/урон остаются диагностическим балансом, не original hurt formula.

Cold170 настоящий20секC2Sloss/handoff02:06:38.103 сохранил принятые400rawdamage/2pickup/51quantity; finish02:07:17.905:94сек/2678см/0kills/Rescued1. Stats подтверждён:WINTER170,0kill/40damage/26M/01:34/Rescued1. Раннееkey2/R не применилось; source gun_definition10402, одинCitori fire/4acceptedpellets, неM4. Cold169 приFпринял подъём после конца собственного540секtimer; strict original evac window этой сценой не доказан.

321 тест исходного дерева и270переносимых тестов прошли,verify-only/.NET Release0warnings. Коммит run_roe_2022 7f57f08 pushed. Windows новыйповтор требуется. Следующая задачаEVAC07 — два последовательных матча в одном процессе.
