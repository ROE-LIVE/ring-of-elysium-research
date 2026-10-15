# INV02: общий ITEM_DATA, ссылки и смешанный reconnect

09.10.2026,2022 x64 0.2.989.0,map16010,EXE SHA2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18. Независимый runtime/GE-Proton11-7,свои namespace/loopback. Cold92–94 завершены143,selectedhash до/после сохранены.

## Первично подтверждено

Полная таблица `inventory-wire-layout.md` с адресами decoder. `3e80/tag2` содержит BE16slot,а не два независимых page/slot. Decoder140c4ae34–53 собирает оба байта; native принимает1/255/256/4660/65535. `5fb` имеет ref U8container/U8slot(140c28320),`3e82` — BE16slot/U8container(140bd4d60). Отдельная страница и игровой handler дляиндексов>255 не доказаны.

Sparse эмуляция прочитала7 кодовых страниц собственногоcold92(28672байта),не читала globals/секреты/полныйdump. Native140bcf790 принял9ITEMвариантов:gun/ammo/helmet/vest/тримедицины/обвес/gun+part;Python codec совпал по длине,definition,quantity. РазмерыITEM безref:80/58/80/80/78/78/78/80/92. Полный5fb0/9/397 accepted,398 rejected;дельтаslots1/256/65535 accepted;shortitem/ref rejected. `native-results.json`.

## Изменение

`inventory_codec_2022.py` разбирает item union и границыsnapshot/delta/discard,сохраняет неизвестные байты,проверяетNUL-name,count/parts/truncation/trailing. WeaponState использует его дляsnapshot/delta/emptydelta/discard. Payload проверенных fixtures остаётся прежним. Категория5 иtype>2 не угадываются. Шесть регрессий,включая неизвестный highslot при валидной позиции/groundtemplate,не допускают alias низкого байта или изменение ammo.

## Nativecold94

Согласованнаясцена/weaponfixture: nativepickup M4/50x5.56/mag40403/бинты5/аптечка1/medkit1. Установкаmag→M4reload40/10→fire39/10;бинт5→4,HP70→80.

C2Sdrop20с,32пакета: новыйAUTH/idlehandoff20.908с;world.started37653.357206347 сохранён,world_start1. Сервер возвращает21sync,дваguns,medical4/1/1,HP800. Nativeafter-loss показывает Citori2/6,M439/10,mag,броню80/200,HP80,medicine1/1/4. Послеобрываfire→38/10,бинт4→3,HP80→90. Ниparse/decrypt/deliveryerrors,ниповторногоworldstart нет. Snapshot формат проверен nativeэмуляцией; realpickup/restore проверены дельтами.

Cold93 отрицательныйконтрольподготовки: sceneсодержаластарыеentityдлядвухсовпадающихUID приupdatedweaponfixture. BaselineUI заснят,подборы не засчитаны. Cold94 заменяетsceneentries соответствующими ownfixture,оригиналы не меняет. ПервыеRPC позиции давалипереходноеair-state; pickup засчитанытолько после normalground/nativeUI.

243maintests,169kit,verify-only passed. INV02 остаётся50%baseline: ограниченныйknownunion не закрывает полныйкаталог/pages/Windows. СледующийINV03 duplicate drop/reconnect; далееKIT01 поочереди.
