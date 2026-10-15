# Обновление Windows-комплекта после исследований 9 октября2026

Репозиторий `ROE-LIVE/run_roe_2022`, commit **4a77946**. Все34 файла SOURCE-MANIFEST теперь совпадают с исходниками ROE_SERVER; Windows launcher/bootstrap и компактный журнал имеют отдельную реализацию.

Перенесён `LobbyClockStream` и параметр `--local-server-clock` в запуск Windows proxy. Первый lobby1f5f получает текущее UNIX-время вместо архивного. Проверки покрывают фрагментацию/объединение TCP, сохранение соседних кадров, неправильную длину и незавершённый поток. Это тот же механизм, который ранее проверялся в Proton.

На Windows после pull:

```powershell
cd G:\REsearch\run_roe_2022
git pull --ff-only
.\run-roe-2022.cmd -Mode cycle -WeaponProfile m4 -Target armored
```

Для проверки ACK/retry и idle handoff:

```powershell
.\run-roe-2022.cmd -Mode cycle -WeaponProfile m4 -Target armored -ReliableUDP -IdleHandoff
```

Клиент по умолчанию `G:\REsearch\Ring of Elysium-2022`; готовая независимая runtime-копия переиспользуется. Сервисы локальные на Windows, Jupyter не нужен. Ключ уже находится в приватном Windows-репозитории по прежнему указанию владельца; его содержимое не читалось/не выводилось при обновлении. Журналы в `runs\ДАТА-НОМЕР\`.

176 тестов Windows-комплекта, verify-only и.NET8 Release build прошли;0 ошибок/предупреждений. Игра в этом обновлении не запускалась; новые изменения требуют native Windows-повтора. Сноуборд и инвентарь проверены под Proton; штатный планер и лазание остаются незакрытыми. Текущая очередь [KIT03 №28](recovery/AGENT-START.md), [отчёт планера](RECOVERY-20261009-GLIDER-CHECK.md).
