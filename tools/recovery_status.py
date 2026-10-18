"""Проверка CSV-плана и сводка достигнутых этапов восстановления, без запуска игры."""

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import os
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATES = {"contract": 10, "wire": 15, "data": 15,
         "server": 20, "client": 20, "scenario": 20}
SCOPES = {"core", "extended", "research"}
STATUSES = {"planned", "research", "partial", "blocked", "verified"}
FIDELITIES = {"unknown", "diagnostic", "partial", "verified"}
HISTORY_FIELDS = ["utc", "plan_version", "build", "scope", "mechanics",
                  "weight", "progress_pct", "verified", "blocked", "csv_sha256", "note"]
UPDATE_FIELDS = ["utc", "plan_version", "build", "id", "change", "old_pct", "new_pct",
                 "old_status", "new_status", "old_gates", "new_gates", "evidence", "limitations", "note"]
EXECUTION_FIELDS = ["utc", "plan_version", "id", "sequence", "work_state", "run_profile", "note"]


def percentage(row):
    # 0 — не подтверждено, 1 — частично, 2 — критерий выполнен.
    return sum(GATES[key] * int(row[key]) / 2 for key in GATES)


def load_plan(path, root=ROOT, recalculate=False, check_references=True):
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source, delimiter=";")
        rows = list(reader)
    if not rows:
        raise ValueError("План пуст")
    required = {"id", "plan_version", "build", "scope", "group", "mechanic", "phase",
                "priority", "weight", "progress_pct", "status", "fidelity", "confidence",
                "evidence", "sources", "depends_on", "acceptance", "next_step", "updated", "basis"} | set(GATES)
    missing = required - set(reader.fieldnames or [])
    if missing:
        raise ValueError(f"Нет колонок: {sorted(missing)}")
    ids = set()
    versions, builds = set(), set()
    for row in rows:
        ident = row["id"]
        if not ident or ident in ids:
            raise ValueError(f"Пустой или повторный id: {ident}")
        ids.add(ident)
        versions.add(row["plan_version"])
        builds.add(row["build"])
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f"{ident}: повреждена CSV-строка")
        if (row["scope"] not in SCOPES or row["status"] not in STATUSES
                or row["fidelity"] not in FIDELITIES
                or row["confidence"] not in {"low", "medium", "high"}):
            raise ValueError(f"{ident}: неверный scope/status/fidelity/confidence")
        if row["basis"] not in {"observed", "requirement", "candidate"}:
            raise ValueError(f"{ident}: неверный basis")
        if row["priority"] not in {"0", "1", "2", "3", "4"} or row["weight"] not in {"1", "2", "3", "5", "8"}:
            raise ValueError(f"{ident}: неверный приоритет/вес")
        if any(row[key] not in {"0", "1", "2"} for key in GATES):
            raise ValueError(f"{ident}: этапы должны быть 0/1/2")
        if recalculate:
            row["progress_pct"] = f"{percentage(row):g}"
        if float(row["progress_pct"]) != percentage(row):
            raise ValueError(f"{ident}: процент не совпадает с этапами; нужен {percentage(row):g}")
        if row["status"] == "verified" and percentage(row) != 100:
            raise ValueError(f"{ident}: verified требует всех этапов=2")
        if not row["acceptance"] or not row["next_step"]:
            raise ValueError(f"{ident}: нужны критерий и следующий шаг")
        if (int(row["client"]) > 0 or int(row["scenario"]) > 0) and not row["evidence"]:
            raise ValueError(f"{ident}: клиентская проверка требует ссылки на опыт")
        for field in ("sources", "evidence", "agent_context", "edit_targets"):
            for reference in filter(None, row.get(field, "").split("|")):
                resolved = (root / reference).resolve()
                if not resolved.is_relative_to(root.resolve()) or (check_references and not resolved.is_file()):
                    raise ValueError(f"{ident}: отсутствует/вне дерева источник {reference}")
        datetime.strptime(row["updated"], "%Y-%m-%d")
    if len(versions) != 1 or len(builds) != 1:
        raise ValueError("Один CSV должен описывать одну версию плана и один билд")
    by_id = {row["id"]: row for row in rows}
    done, active = set(), set()

    def visit(ident):
        if ident in active:
            raise ValueError(f"Цикл зависимостей у {ident}")
        if ident in done:
            return
        active.add(ident)
        for dependency in filter(None, by_id[ident]["depends_on"].split("|")):
            if dependency not in by_id:
                raise ValueError(f"{ident}: нет зависимости {dependency}")
            visit(dependency)
        active.remove(ident)
        done.add(ident)

    for ident in by_id:
        visit(ident)
    validate_execution(rows)
    return rows


def validate_execution(rows):
    """План1 совместим; в плане2 порядок и поручение обязательны у всех строк."""
    fields = {"sequence", "work_state", "agent_context", "agent_goal", "edit_targets",
              "start_command", "run_profile", "verify_command", "deliverables", "result_dir"}
    if all(row["plan_version"] == "1" for row in rows) and not any("sequence" in row for row in rows):
        return
    numbers = set()
    by_id = {row["id"]: row for row in rows}
    for row in rows:
        if not fields <= row.keys() or any(not row[key] for key in fields):
            raise ValueError(f"{row['id']}: неполное поручение агенту")
        if not row["sequence"].isdigit() or int(row["sequence"]) < 1 or int(row["sequence"]) in numbers:
            raise ValueError(f"{row['id']}: неверный/повторный номер задачи")
        numbers.add(int(row["sequence"]))
        if row["work_state"] not in {"baseline", "ready", "queued", "external_blocked", "done"}:
            raise ValueError(f"{row['id']}: неверный work_state")
        if row["work_state"] == "done" and row["status"] != "verified":
            raise ValueError(f"{row['id']}: done требует status=verified")
        if row["run_profile"] not in {"smoke", "loot", "combat", "world", "full", "resources", "windows", "lan", "manual"}:
            raise ValueError(f"{row['id']}: неверный run_profile")
        for dependency in filter(None, row["depends_on"].split("|")):
            if int(by_id[dependency]["sequence"]) >= int(row["sequence"]):
                raise ValueError(f"{row['id']}: зависимость {dependency} должна иметь меньший номер")
    if numbers != set(range(1, len(rows) + 1)):
        raise ValueError("Нумерация должна быть непрерывной1..N")


def aggregate(rows):
    weight = sum(int(row["weight"]) for row in rows)
    return {"mechanics": len(rows), "weight": weight,
            "progress_pct": round(sum(percentage(row) * int(row["weight"]) for row in rows) / weight, 1) if weight else 0,
            "verified": sum(row["status"] == "verified" for row in rows),
            "blocked": sum(row["status"] == "blocked" for row in rows)}


def render(rows, digest):
    lines = ["# Состояние плана восстановления2022", "",
             f"Версия плана: **{rows[0]['plan_version']}**; данные обновлены до **{max(row['updated'] for row in rows)}**.",
             "", "Проценты показывают взвешенное достижение этапов этого плана. Это не доля исходного серверного кода, не оценка оставшихся часов и не готовность всей игры.",
             "", "| Объём | Механик | Вес | Этапы, % | Полностью проверено | Заблокировано |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for title, selected in [("Минимальная зимняя сессия", [r for r in rows if r["scope"] == "core"]),
                            ("Весь целевой план", [r for r in rows if r["scope"] != "research"]),
                            ("Исследовательские ветки отдельно", [r for r in rows if r["scope"] == "research"])]:
        stats = aggregate(selected)
        lines.append(f"| {title} | {stats['mechanics']} | {stats['weight']} | {stats['progress_pct']} | {stats['verified']} | {stats['blocked']} |")
    lines.extend(["", "| Направление | Механик | Этапы, % |", "| --- | ---: | ---: |"])
    for group in dict.fromkeys(r["group"] for r in rows if r["scope"] != "research"):
        stats = aggregate([r for r in rows if r["group"] == group and r["scope"] != "research"])
        lines.append(f"| {group} | {stats['mechanics']} | {stats['progress_pct']} |")
    lines.extend(["", "Приоритет0 — сначала устранить блокирующую синхронизацию; приоритет1 — ближайшее восстановление механик. Зависимости в CSV указывают, что нужно для завершения задачи, и сами не означают готовность.",
                  "", "| № | ID | Механика | Очередь | Этапы, % | Следующий шаг |", "| ---: | --- | --- | --- | ---: | --- |"])
    for row in rows:
        if row["priority"] in {"0", "1"}:
            lines.append(f"| {row.get('sequence', '')} | {row['id']} | {row['mechanic']} | {row.get('work_state', '')} | {percentage(row):g} | {row['next_step'].replace('|', '/')} |")
    lines.extend(["", "Источники, адреса, ограничения, критерии и этапы каждой механики — в [mechanics-2022.csv](mechanics-2022.csv). Порядок работ — в [README](README.md).",
                  "", f"SHA-256 CSV: `{digest}`. Сводка создаётся `tools/recovery_status.py`; редактировать нужно CSV.", ""])
    return "\n".join(lines)


def update_rows(path, rows, utc, note):
    """Дописывает изменения механик; прежние записи не перезаписываются."""
    previous = {}
    if path.exists() and path.stat().st_size:
        with path.open(encoding="utf-8-sig", newline="") as source:
            reader = csv.DictReader(source, delimiter=";")
            if reader.fieldnames != UPDATE_FIELDS:
                raise ValueError("Несовместимый заголовок updates.csv")
            for entry in reader:
                previous[entry["id"]] = entry
    active_ids = {ident for ident, entry in previous.items() if entry['change'] != 'removed'}
    current_ids = {row['id'] for row in rows}
    if active_ids and active_ids != current_ids:
        old_version = max(int(entry['plan_version']) for entry in previous.values())
        new_version = int(rows[0]['plan_version'])
        if new_version <= old_version:
            raise ValueError('Изменение состава требует увеличения plan_version; возможна неполная запись CSV')
    entries = []
    for row in rows:
        before = previous.get(row["id"], {})
        gates = "".join(row[key] for key in GATES)
        changed = (before.get("new_pct") != row["progress_pct"]
                   or before.get("new_status") != row["status"]
                   or before.get("new_gates") != gates
                   or before.get("evidence") != row["evidence"]
                   or before.get("limitations") != row["limitations"]
                   or before.get("change") == "removed")
        if changed:
            entries.append({"utc": utc, "plan_version": row["plan_version"], "build": row["build"],
                            "id": row["id"], "change": "updated" if before else "baseline",
                            "old_pct": before.get("new_pct", ""), "new_pct": row["progress_pct"],
                            "old_status": before.get("new_status", ""), "new_status": row["status"],
                            "old_gates": before.get("new_gates", ""), "new_gates": gates,
                            "evidence": row["evidence"], "limitations": row["limitations"], "note": note})
    current_ids = {row["id"] for row in rows}
    for ident, before in previous.items():
        if ident not in current_ids and before["change"] != "removed":
            entries.append({"utc": utc, "plan_version": rows[0]["plan_version"], "build": rows[0]["build"],
                            "id": ident, "change": "removed", "old_pct": before["new_pct"], "new_pct": "",
                            "old_status": before["new_status"], "new_status": "", "old_gates": before["new_gates"],
                            "new_gates": "", "evidence": before["evidence"], "limitations": before["limitations"], "note": note})
    return entries


def append_csv(path, fields, entries):
    existed = path.exists() and path.stat().st_size > 0
    with path.open("a", encoding="utf-8" if existed else "utf-8-sig", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=fields, delimiter=";")
        if not existed:
            writer.writeheader()
        writer.writerows(entries)


def execution_changes(path, rows, utc, note):
    if not all("sequence" in row for row in rows):
        return []
    before = {}
    if path.exists() and path.stat().st_size:
        with path.open(encoding="utf-8-sig", newline="") as source:
            reader = csv.DictReader(source, delimiter=";")
            if reader.fieldnames != EXECUTION_FIELDS:
                raise ValueError("Несовместимый заголовок execution-history.csv")
            for entry in reader:
                before[entry["id"]] = entry
    return [{"utc": utc, **{key: row[key] for key in ("plan_version", "id", "sequence", "work_state", "run_profile")}, "note": note}
            for row in rows if any(before.get(row["id"], {}).get(key) != row[key]
                                   for key in ("plan_version", "sequence", "work_state", "run_profile"))]


def write_plan_atomically(path, rows):
    """Ошибка записи не оставляет половину плана вместо исходного CSV."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8-sig',newline='',
                                         dir=path.parent,prefix='.'+path.name+'-',delete=False) as destination:
            temporary = Path(destination.name)
            writer=csv.DictWriter(destination,fieldnames=list(rows[0]),delimiter=';')
            writer.writeheader()
            writer.writerows(rows)
        if path.exists():os.chmod(temporary,path.stat().st_mode & 0o777)
        os.replace(temporary,path)
    finally:
        if temporary is not None:temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=ROOT / "docs/recovery/mechanics-2022.csv")
    parser.add_argument("--write", action="store_true", help="Обновить status.md рядом с CSV")
    parser.add_argument("--recalculate", action="store_true", help="Пересчитать progress_pct в CSV после изменения этапов")
    parser.add_argument("--snapshot", action="store_true", help="Добавить датированную сводку в history.csv")
    parser.add_argument("--note", default="", help="Объяснение изменения для snapshot")
    args = parser.parse_args()
    if args.snapshot and not args.note.strip():
        parser.error("--snapshot требует --note с объяснением изменения")
    try:
        rows = load_plan(args.csv, recalculate=args.recalculate)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Ошибка плана: {error}\n")
    history = args.csv.with_name('history.csv')
    updates = args.csv.with_name('updates.csv')
    execution = args.csv.with_name('execution-history.csv')
    utc = datetime.now(timezone.utc).isoformat()
    if args.snapshot:
        try:
            changes = update_rows(updates, rows, utc, args.note)
            queue_changes = execution_changes(execution, rows, utc, args.note)
            if history.exists() and history.stat().st_size:
                with history.open(encoding='utf-8-sig',newline='') as source:
                    if next(csv.reader(source,delimiter=';'),[]) != HISTORY_FIELDS:
                        raise ValueError('Несовместимый заголовок history.csv')
        except (ValueError,OSError) as error:
            parser.exit(1,f'Ошибка журнала: {error}\n')
    if args.recalculate:
        write_plan_atomically(args.csv,rows)
    digest=hashlib.sha256(args.csv.read_bytes()).hexdigest()
    report=render(rows,digest)
    if args.write:
        args.csv.with_name('status.md').write_text(report,encoding='utf-8')
    if args.snapshot:
        entries = []
        for scope in ("core", "target", "research"):
            selected = [r for r in rows if r["scope"] != "research"] if scope == "target" else [r for r in rows if r["scope"] == scope]
            entries.append({"utc": utc, "plan_version": rows[0]["plan_version"], "build": rows[0]["build"],
                            "scope": scope, **aggregate(selected), "csv_sha256": digest, "note": args.note})
        append_csv(updates, UPDATE_FIELDS, changes)
        append_csv(history, HISTORY_FIELDS, entries)
        if queue_changes:
            append_csv(execution, EXECUTION_FIELDS, queue_changes)
    print(report)


if __name__ == "__main__":
    main()
