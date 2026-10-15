# Состав для передачи

Это новая история без private и полных старых snapshots. Включены выбранные Markdown, два CSV, индекс путей исходного workspace и обезличенная выборка Windows-событий. Клиента, извлечённых архивов/Lua целиком, ключей, raw AUTH, полных дампов и видео нет. Для исследования конкретного отсутствующего источника используйте SOURCE-INDEX.json.

После git add: `python -B tools/share_audit.py`. Проверка состава/хешей не заменяет просмотр diff и оценку происхождения новых файлов. Точный список — SOURCE-MANIFEST.json.

Обновление уже настроенного репозитория:

```bash
git push -u origin main
```

Основной репозиторий: https://github.com/ROE-LIVE/ring-of-elysium-research . Код запуска: https://github.com/ROE-LIVE/ring-of-elysium-local .
