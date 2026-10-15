# Управление состоянием одиночного стенда2022

Запустите из Windows-репозитория:

```powershell
.\run-roe-2022.cmd -Mode cycle -Bots -BotGroundRoute -BotBehavior -ReliableUDP -IdleHandoff -LiveControl
```

После входа на карту откройте второй PowerShell в этом же репозитории. Подставьте **каталог текущего запуска**, напечатанный launcher как журнал. VerifyOnly и старые runs не являются активной сессией.

```powershell
$roeRun = '.\runs\ИМЯ_ТЕКУЩЕГО_ЗАПУСКА'
& .\.tools\python\python.exe -B .\tools\scene_action_2022.py --run $roeRun --id heal-1 --action set_own_health --hp 850
& .\.tools\python\python.exe -B .\tools\scene_action_2022.py --run $roeRun --id ammo-1 --action give_ammo --definition 30004 --quantity 6
& .\.tools\python\python.exe -B .\tools\scene_action_2022.py --run $roeRun --id npc-hit-1 --action damage_npc --damage 100
```

| Действие | Результат и предел |
| --- | --- |
| set_own_health | RawHP1..начальныйHPпрофиля;850≈85/100HUD; dead не оживляет |
| give_ammo | Текущий ownbag,1..100шт;30004=12ga,30001=5.56,30002=7.62,30005=.45; вся пачка должна помещаться |
| damage_npc | Учебный100rawурон существующему NPC; его броня учитывается; смерть переносит текущие вещи, если есть inventory |

Добавление в очередь ещё не подтверждает применение. В `game-endpoint/events.jsonl` ищите `live_state_action`, вашID иaccepted/reason. ID выполняется один раз в текущей сессии; одинаковый повтор не повторяет выдачу/урон. Для нового действия/повторной попытки послеотказа — новыйID. По желанию--recipient задаёт ownAccountUID из лога, не UIDNPC. Очередь записывайте одним оператором. Endpoint читает её через heartbeat; редактирование не требует рестарта.

Это наш административный controller, не оригинальная консоль и не общий multiplayerAPI. Протоколные HP/смерть/инвентарь подтверждены Proton318; нативныйWindows нового режима ещё нужно проверить. Произвольный raw1069 может быть только картинкой; typedaction действительно меняет WorldState. Другие события требуют соответствующего серверного обработчика, а не одного opcode.

Подробные факты/отказы: [OPS04](OPS04-STATE-ACTIONS-20261012.md). Сценарийбота: [BOT05](BOT-BEHAVIOR-20261012.md).
