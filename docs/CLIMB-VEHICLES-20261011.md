# 11.10: кирки, снегоход и лодка — только2022 x64

Рабочий источник: ROE_SERVER; EXE0.2.989.0/SHA2dca9b1e…6ba18;map16010. Снимок отчётов и коротких публичных наблюдений: [snapshots](../snapshots/recovery-20261011-climb-vehicles/083-kit04/report.md).350 source/307 portable tests,verify-only,.NET8 Release0warnings/errors. Windows-повтор новыхпрофилей отдельно.

KIT04baseline80: RockWall enum3, исходныйTwinBoxTrigger27930, detectorcos20, registered wrappers1418b2450/2360. Cold200/201/202 nativeF→FSM20/21, W/S, F→ground. Available/Active доказаны read-only hardwarebreakpoints; нельзя путать Climb20/21 с ladder22–24. C2S2a продолжает позиции;37 содержит ещё42нерасшифрованныхбайта. Windows: run-roe-2022.cmd -Kit climb -ClimbPractice, камера203°, F/W/S/F.

CAR03external_blocked30:148точек layout001(112/31/5), iCountсуммы66/31/5. Квоты и веса неразличены; iCountкаквес остаётся H1, неоригинал. Layout001–004 дублируют транспорт; корневой pool имеет одну отличающуюся точку. Нужен serverconsumer EuEntityLootControl/Item или authoritative trace выбора/остатковquota/seed.

CAR04baseline62.5: толькоSnowMotor109 из8наземныхтипов; cold203/204 nativeF/W7/F/foot,127м,FSM8→0. Windows -VehicleProfile snowmotor; -OriginalJeeps сохраняетточки ипринудительноменяет102→109. Passenger/damage/upgrades/остальные7cars/RNG отдельно.

CAR05baseline62.5: boat203/79 в исходной135136.205 driveпрошёл, exitXYZ0отклонён;206/207 полныйограниченныйцикл и206 swim→reboard. NativeGetoff producer14131cb30 неинициализируеткрайниебайты14B,40/255 неenum. Exitzero fallback наш: Seat1off215/163/200 изShip203 +initialquat +latestMOVE. Поворотный exit/пассажиры/serverhydrodynamics/Windows открыты. Windows -BoatPractice (walk).

Архитектура остаётся lobby.NET→bridge→PythonTGCP/UDP→клиентскаяфизика; nativehost не найден. Утилиты: readonly/proc selectedfields +capstone, GDBhardwarepoints, normalUI/xdotool, Proton11-7/Xvfb/loopbacknamespace;безGhidra/Docker/дополнительныхмоделей. Клиентскиеоригиналы немодифицированы, SHAEXE/DLLпроверены до/после запусков.

Далее №87/CAR06: native6554 codec/unknownUID подтверждён; HPkey/consumer выясняется. Наличиерасходуемоготоплива длямашин неподтверждено. Карточка: tools/recovery_task.py --task CAR06 --preflight в ROE_SERVER.
