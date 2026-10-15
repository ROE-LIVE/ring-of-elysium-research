13.10 04:57UTC: HOST02 baseline90 — numeric HUD getters native352/353 подтверждают2+6→fire1+6→reload2+5; cold owned marker/cleanup,354 gate0/nooutput.518source/479portable/verify/PowerShellOK. Windows -DebugConsole подготовлен; реальныйWindows отдельно. GetCurrentMapId1418CCA10 читает143040770=10020, не world; room16010. Provider/SDK ветки безнового материала не повторяются; OPS03 cycle carrier проверяется до05:55UTC. См.docs/DEBUG-SNAPSHOTS-20261013.md.

13.10 04:20UTC: OPS03 baseline80 — portable Linux peer иProton в разных net namespaces; fire/reload,20.00013с buffered pause→resume,secondTraining/reset/fire.512source/473portable/verify-cycle/.NETOK. Windows -RemotePeer jovyan@192.168.1.25 -Profile default подготовлен; реальныйWindows/SSH/LAN ещё не подтверждён. Следующая№112HOST02; продолжаем до05:55UTC. См.docs/LAN-SSH-20261013.md.

13.10 03:11UTC: LOOK05 baseline82.5 — separate Alice/Bob/Alice; durable cosmetics, native UID/equipment/skin; corrected Saki field1, W13.34m/fire.505source/466portable/verify/.NETOK. -Profile alice inWindows; realWindows/sharedUI settings/originalauth отдельно. ДалееOPS03; до05:55UTC продолжаем. См.docs/LOOK05-PROFILES-20261013.md.

13.10 02:35UTC: LOOK04 baseline90 — native341 одежда equip/replace/remove;342 cold и второй Training all8 actor+130, fire/reload.501source/461portable/verifyOK. Opcode3E80,050B это размер decoded структуры. СледующаяLOOK05 изоляция профилей; работа до05:55UTC продолжается. См.docs/LOOK04-CLOTHING-20261013.md.

13.10 01:36UTC: LOOK03 baseline80 — native331–337 Saki cold login→Training; saved Walkie cold lobby/cache; GUI unequip+fresh relogin0.495source/455portable/verifyOK. Match charm visual/same-process reentry/GUI swap/Windows отдельно. СледующаяLOOK04 OnSaveEquip→3E80 (050B — размер структуры); работа до05:55UTC продолжается. См.docs/LOOK03-CHARACTER-ACCESSORIES-20261013.md.

Актуализация11.10.2026: [проверка двух клиентов и общего наземного лута](SHARED-GROUND-20261011.md). NET09 ready40; общего HP/clock/vehicles, leave/epoch и выдачи существующего динамического лута при позднем входе ещё нет. Windows launcher одиночный.

Актуализация10.10,13:25UTC: [nativedeath-parcel/atomicinventory](RECOVERY-20261010-DEATH-PARCEL.md). LOOT10baseline; следующая №51/GUN08. Это текущая очередь; исторические пункты ниже сохраняются какконтекст.

**Актуально08.10, ночь:** [два слота, timed reload и пассивная мишень](RECOVERY-20261008-NIGHT.md). Следующий №22/INV02 — pages/consumables; две пушки уже работают. Новый Windows-повтор и dual-gun reconnect остаются открытыми. Учебная защита50% не является исходной формулой ROE.

Актуализация10.10: [own armor/MOVE03/native fall/death info](RECOVERY-20261010-ARMOR-MOVEMENT-FALL.md); текущая ready №49/LOOT10, оригинальные hurt/fall rules ждут named input. Источники и границы в этой странице и docs/recovery; старые поручения ниже не выбирать как текущую очередь.

**Актуальное состояние08.10, вечер:** [результаты и первичные отчёты](RECOVERY-20261008-EVENING.md). Следующая ready — **№22/INV02**; native slot2 формат принят, серверный registry двух пушек ещё нужен. [CSV](recovery/mechanics-2022.csv) и [AGENT-START](recovery/AGENT-START.md) имеют приоритет над прежними ближайшими шагами ниже.

**Актуальное дополнение08.10:** [ZONE02, NET06 и NET04](RECOVERY-20261008-AFTERNOON.md) (следующийNET05). Ниже сохранён исторический контекст предыдущего этапа.

# Короткое поручение принимающему агенту

Состояние на 08.10.2026. Действующий источник — `ROE_SERVER/docs/recovery/mechanics-2022.csv`, версия плана2. Здесь переносимая копия: [CSV](recovery/mechanics-2022.csv). Другие билды читать отдельно по README/BUILDS; адреса2022 не переносить на V99/Steam2018.

Для отдельной задачи сначала прочитать AGENTS.md и [AGENT-START](recovery/AGENT-START.md), затем выбранную строку и её agent_context. В рабочем ROE_SERVER выполнить `python -B tools/recovery_task.py --task ID`, для диапазона — `--task 5-6`, для текущей задачи — `--next`. Проверка `--preflight` не запускает игру, не читает ключ и называет недостающие материалы. [Снимок инструмента](../snapshots/recovery-plan-20261008-v2/tools/recovery_task.py) требует явных --csv/--workspace при работе из контекста.

Текущая ready-задача — **№6/ZONE02**. [Новый этап](MOVEZONE-20261008.md):15Proton-запусков,38регрессий; ordinary countdown и W после27/2b подтверждены. MOVE02baseline85% с неизвестными wire/data полями. На stage50 M воспроизводит старый map header безRPC, nativeclock исправен; Lua guard найден, финальныйUI не исправлен. Трассировать OnUpdate/SetCountDown/CacheCountdown/режимныефлаги и warning-матрицу. Не внедрять enum3 как исправление. Поручение: `python -B tools/recovery_task.py --next`.

Архитектура2022: независимый Proton runtime → локальное.NET lobby → TCP bridge → TGCP/UDP Python peer; loopback namespace, без Docker. Есть ограниченные движение, лут, наборы, стрельба, HP, зоны, погода, Jeep и эвакуация. Нет исходных host engine/RNG/raycast/бронебаланса/AI/multiplayer. Common1499 уже дал8313точки; Type→Ctrl/квоты остаются неизвестны. Полный положительный geton/LOCAL/lobby и отрицательный no-GM повтор не объединять. Новый совместный профиль проверен под Proton, Windows11 отдельно.

Разрешения и объём брать из текущего поручения пользователя и правил рабочего дерева. Оригиналы не изменять; не читать секреты/полные дампы. Входы и команды профилей — [RUNBOOK](recovery/RUNBOOK.md). Если доступен лишь этот контекст, без полного ROE_SERVER/клиента/ключа/fixtures игровой повтор невозможен; назвать конкретно недостающее и выполнить полезную статическую часть.

Сохранить report/evidence/checks в result_dir: run, адреса/SHA, положительный и отрицательный контроль. Остановить свои процессы. Обновить только затронутые ID/этапы/evidence/work_state, пересчитать сводку, дописать историю и progress/hypotheses, синхронизировать контекст.100%/done требуют выполнения критерия всей задачи; номер и очередь не равны процентам готовности.


Последняя задача: [GUN03](RECOVERY-20261009-ACTIONS.md); далее измерение native eligibility и проверка замены оружия во время reload.


Актуальный GUN03: [native отмена switch/replace](RECOVERY-20261009-CANCEL.md). Пользователь подтвердил базовые действия наWindows; точная анимация/ADS ещё не заявлены.


Последний этап: [AR40403](RECOVERY-20261009-MAGAZINE.md). ДалееGUN06; fixedhit/armorнеявляютсяоригинальнойбаллистикой.
