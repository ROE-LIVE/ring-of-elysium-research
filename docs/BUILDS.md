# Билды и идентификация

Рабочая база: `/home/jovyan/imported/REsearch`. Исследовательское дерево: `ROE_SERVER/`. Отдельный Git с переносимым V99 сервером: `/home/jovyan/roe-server`, origin `ROE-LIVE/roe-server`; зафиксированное состояние HEAD `1efd5f1`.

| Метка | Исходный каталог относительно REsearch | EXE | SHA-256 основного исследованного EXE |
| --- | --- | --- | --- |
| 2022 | Ring of Elysium-2022 | Europa_Client.exe, x64, 0.2.989.0 | `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18` |
| V99 | Ring of Elysium-V99 | x64/Europa_Client.exe, x64, 0.2.368.0 | `5e1d3d3cde06bdfb5c5104d247f9f75cb22e6bf5db752cd632f97175a1721fb5` |
| 2018 ранний | Ring of Elysium-2018 | Europa_Client.exe, x86, 0.2.82.0 | `ff980bec18fe325d2cfb0b624f0a3b3c9911ccbb4cdbc16c5d40b3a47852619a` |
| Steam2018-19sep | Ring of Elysium-2018-steam-19-sep/1.8729165155683311171 | Europa_Client.exe, x86, 0.2.173.0 | `f1fc78404071dd79b8c7f550106e7b2816ec00936d5b8e01159471bac9d2e1f5` |

Источники: `ROE_SERVER/docs/builds.md`; ранний `research/builds/2018/initial-analysis.md`; Steam `steam-19sep-20261006/build-identity.json`; V99 `hosting-route-20261006/report.md`; 2022 `iceland-gameplay-20261006/final-continuation-hashes.json`. Контрольные хеши подтверждают выбранные EXE/DLL, а не всю комплектацию каждого билда.

V99 имеет также корневой x86 EXE; адреса x64 опыта к нему неприменимы. PE timestamp V99 — апрель 2019: имя V99 не означает 1999 или самый первый Steam-клиент. Ранний 2018: timestamp 2018-05-23; launcher metadata th_live/0.2.15.5 отличается от EXE. Его точный канал и комплектность не доказаны. Steam2018: depot 755791, manifest 8729165155683311171; дата совпадает с релизом, но первенство манифеста не доказано.

Отдельные исторические дампы 0.2.36.0 (апрель 2018) и 0.2.412.0 (2019) не равны этим клиентам. Названия файлов `roe_*_2023.py` обозначают происхождение инструментов; применимость конкретного кодека к 2022 подтверждается отдельно.

Map ID тоже зависит от билда: V99 опыт 16007 нельзя автоматически объявлять зимним Iceland. Steam таблица: 16007 KillZone, 16010 Iceland, 16005 TestMap. 2022 зимний опыт — 16010 EU_IceLand_4096/IceLand_001, старый оружейный — 16014 KillZone_004.
