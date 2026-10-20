"""Адресное чтение81публичного XML из установленного клиента2022.

Читает только manifest-диапазоны, не распаковывает VFS целиком, не запускает
игру/внешний extractor. SHA каждого результата обязателен. Кеш вне клиента.
"""
import hashlib
import json
from pathlib import Path
import struct
import zlib

from audit_prefab_loot_nodes_2022 import xml, xyz, world_point
from export_loot_tables_2022 import export


def _relative(value):
    if not isinstance(value,str) or not value or ':' in value or '\\' in value:
        raise ValueError('Нужен относительный нормализованный путь')
    path=Path(value)
    if path.is_absolute() or any(part in ('.','..') for part in path.parts):
        raise ValueError('Путь вне manifest-каталога')
    return path


def read_resource(client, record):
    """Ограниченное чтение одного проверенного SFC/VFS блока без ключей."""
    path=Path(client)/_relative(record['source'])
    size,offset=record['size'],record['offset']
    if (type(size)is not int or not 1<=size<=16*1024*1024
            or type(offset)is not int or not 16<=offset<path.stat().st_size):
        raise ValueError('Размер/offset выбранного ресурса вне границ')
    with path.open('rb')as source:
        header=source.read(12)
        if record['storage']=='sfc_lz4':
            if header[:4]!=b'SFC\x1a' or struct.unpack_from('<I',header,4)[0]not in(2,3):
                raise ValueError('Неизвестный SFC')
            source.seek(offset-4);packed_size=struct.unpack('<I',source.read(4))[0]
            if not 1<=packed_size<=16*1024*1024 or offset+packed_size+4>path.stat().st_size:
                raise ValueError('Выбранный LZ4 блок вне границ')
            packed=source.read(packed_size)
            if struct.unpack('<I',source.read(4))[0]!=size:
                raise ValueError('USize не совпал с manifest')
            from lz4.block import decompress
            data=decompress(packed,uncompressed_size=size)
        elif record['storage']=='vfs_zlib':
            if header[:4]!=b'vfs ':
                raise ValueError('Неизвестный VFS')
            block_size=struct.unpack_from('<I',header,8)[0]
            source.seek(offset);block=source.read(16)
            if len(block)!=16:raise ValueError('Укороченный VFS data header')
            magic,count,next_offset=struct.unpack('<4sIq',block)
            length=count*block_size-16
            if (magic!=b'data' or not 16<=block_size<=65536 or next_offset!=0
                    or not 1<=length<=16*1024*1024 or offset+16+length>path.stat().st_size):
                raise ValueError('Неподдержанный/составной VFS data блок')
            packed=source.read(length)
            try:
                decoder=zlib.decompressobj()
                data=decoder.decompress(packed,size+1)
                if not decoder.eof or len(data)!=size:
                    raise ValueError('Неверный размер/конец Zlib потока')
            except zlib.error:
                # Некоторые XML хранятся без сжатия. SHA всё равно обязателен.
                data=packed[:size]
        else:
            raise ValueError('Неизвестное хранение выбранного XML')
    if len(data)!=size or hashlib.sha256(data).hexdigest()!=record['sha256']:
        raise ValueError('Выбранный ресурс не совпал с SHA manifest: '+record['path'])
    return data


def enumerate_nodes(cache, manifest):
    """Все подходящие prefab-узлы; чужой список координат не требуется."""
    layout,_=xml(Path(cache)/_relative(manifest['layout']))
    allowed=set(manifest['prefabs']);prefabs={};nodes=[];seen=set()
    for ordinal,instance in enumerate(layout.iter('LayoutInstance')):
        resource=instance.get('mParentName','')
        path=resource.replace('.','/').upper()+'.XML'
        if path not in allowed:continue
        if path not in prefabs:prefabs[path]=xml(Path(cache)/_relative(path))[0]
        for node in prefabs[path].iter('mSpawnerNodes'):
            if node.get('mSpawnerID')is None:continue
            controller=int(node.get('mSpawnerID'))
            if controller not in(1,3,5):continue
            name=node.get('mName');key=(ordinal,name)
            if not name or key in seen:raise ValueError('Повтор/пустое имя prefab-узла')
            seen.add(key)
            x,y,z=world_point(instance,xyz(node.find('mRelativePos')))
            nodes.append(dict(Index=len(nodes),Instance=ordinal,Node=name,Prefab=resource,
                              Controller=controller,X=x,Y=y,Z=z,position_verified=True))
    if len(nodes)!=manifest['expected_nodes']:
        raise ValueError('Число исходных узлов не совпало с manifest')
    return nodes


def load_source(client, manifest_path, cache):
    manifest_path,cache=Path(manifest_path),Path(cache)
    if manifest_path.stat().st_size>128*1024:raise ValueError('Manifest превышает128КиБ')
    raw=manifest_path.read_bytes();manifest=json.loads(raw)
    resources=manifest['resources']
    if (manifest.get('version')!=1 or manifest.get('map_id')!=16010
            or not 1<=len(resources)<=128 or sum(r['size']for r in resources)>32*1024*1024):
        raise ValueError('Нужен небольшой проверенный manifest2022/16010')
    seen=set()
    for record in resources:
        path=cache/_relative(record['path'])
        if record['path']in seen:raise ValueError('Повтор пути manifest')
        seen.add(record['path'])
        verified=(path.is_file()and path.stat().st_size==record['size']
                  and hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256'])
        if not verified:
            data=read_resource(client,record);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
        if 'table_alias'in record:
            alias=cache/'tables'/_relative(record['table_alias'])
            alias.parent.mkdir(parents=True,exist_ok=True);alias.write_bytes(path.read_bytes())
    nodes=enumerate_nodes(cache,manifest)
    tables=export(cache/'tables',16010)
    summary=dict(map_id=16010,nodes=len(nodes),resources=len(resources),
                 manifest_sha256=hashlib.sha256(raw).hexdigest(),
                 enumeration='LayoutInstance ordinal / source mSpawnerNodes order',
                 original_algorithm_verified=False)
    (cache/'source-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return nodes,tables,summary
