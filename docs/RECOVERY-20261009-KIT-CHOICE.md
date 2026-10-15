# KIT01: смена набора с непустым инвентарём

09.10.2026,2022 x64 0.2.989.0,map16010. Независимыйruntime, GE-Proton11-7/Xvfb,свойloopback namespace. ВыбранныеEXE/DLL до/после совпали,exit143,своипроцессы остановлены.

## Первичные источники

TableBin/A89 rows1079/1087/1095:200904climb300,200906snowboard225,200907glider150; ресурссверен с исходнымSFC в winter-kit-loot-20261007/loot-primary-sfc-verification.json. Выбранныеполя primary-selected-weights-kits.json. RAW descriptors142d94e88/eb8/ee8 задают2/3/4;10d0decoder140c27d10,handler140eaee10 пересчитывает ownactor+354 mask1/2/4. Capacity516decoder140c2b200,handler140d6a440,cacheattr5; backpackvisual+378 другойпараметр.

## Native cold98

Normalground безпозиционногоRPC. Nativepickup M4/50x556/mag40403,установкамагазина, reload40/10. Citori2/6,helmet80,vest200. Затемнастоящийpickup:

- Исходныйсноуборд:mask2, RAW2/3/4=0/1/0,capacity225.
- Glider91000:mask1,1/0/0,150; прежнийнабор выпадает70001.
- Native repick70001:mask2,0/1/0,225.
- Climb91001:mask4,0/0/1,300,компоненткирк+11a0/+20=1.
- C2S20с→AUTHidlehandoff19:10:39UTC,world.started41689.643845282 сохранён;world_start1. Native mask4/0/0/1/300,кирки1;инвентарь40/10,2/6,обвес/броня сохранены.
- Возвратнаglider:mask1/1/0/0/150,кирки0. Ровнооднаспособность вкаждомвыборочномзамере.

Полямemory читалисьтолькоread-only sample_kit.py: маска/cache/capacity/FSM/позиция/компонент. Ключи/сессия/full dump нечитались. Собственныйpeer выключает две остальныеRAW передcapacity. Ниодинзамер не показал смешанноймаски. Actual climbing/обычныйполет отдельно;этоткритерий касаетсявыбора.

## Отрицательные контроли и проверки

Cold97 ownpreset поошибкеубрал начальный5fb: Ground появился,ноWeaponState/world/environment неинициализировались. Это отрицательныйконтрольпресета,неработоспособностьнабора. Cold98 вернул delayed3s5fb; самыйраннийзамер18:57:30UTC был доэтого5fb иmask0/cap100, не засчитанкакготовыйнабор. Положительныйзамер18:58:30 сохранёнотдельно.

Регрессия сохраняетgunUID/clip,патроны иброню при сменетрёхнаборов; меньшаяcapacity неуничтожаетвыданныестэки,новыйpickup приперевесе получает0. Это собственнаяполитикаpeer,не установленноеоригинальноеправило.246maintests/2новыерегрессии прошли. KIT01baseline90: Windowsновыйповтор/перевесnative отдельно. СледующийKIT05 затемINV04: двастэка/fullbag/drop/частичныйpickup.

Снимок: snapshots/recovery-kit01-nonempty-20261009. PNG/runостаютсявROE_SERVER; неготовыйстенд.
