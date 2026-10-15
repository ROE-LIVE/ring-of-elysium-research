# Гранаты2022 — 10.10.2026

№52/GUN09 baseline75%, stages1/2/2/1/2/1, fidelitypartial. Следующаяready №53/GUN10. Проценты относятся к этапам задачи.

Штатные frag50001/smoke50002/flash50003 подбираются, выводятся в slot5/6, бросаются1004, завершаются1007. Peer расходует один предмет, отвечает1005/1008/1009 и сохраняет registry/остатки после20с handoff. Cold143: frag HP1000→900→800, smoke visible/native callback, flash native callback. Fuse5/5/2.5. Cold144: послеобрыва оставшаяся граната бросается и HP900→800.

Source: ROE_SERVER/research/builds/2022/recovery/052-gun09/20261010T1414-throw/report.md; копия snapshots/recovery-grenades-20261010. QSWeaponConfigTable SFC6142585; native callbacks1410EF820/930/AC0/B90, effect1411E1320. Адреса только2022 x64 SHA2dca9b1e…6ba18.

Windows kit: run_roe_2022, команда `run-roe-2022.cmd -Mode cycle -Target plain -FragDamage 100 -ReliableUDP -IdleHandoff`. Default fixedloot содержит2 каждого типа. Right-click bag→grenade slot, Tab,5,left mouse. Damage0..1000 — наша flat политика, original formula/LOS/flash blind/multiplayer/in-flightlostfinish неизвестны. Windows11 отдельно. Нет исходного native host.

302 source/235 portable tests и verify-only проходят. Прогон142/143/144 остановлен, SHA оригиналов/runtime совпадают. Секреты/AUTH/полные memory dumps не включены.
