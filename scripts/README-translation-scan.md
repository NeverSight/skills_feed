# 描述翻译扫描与修复

## 扫描

检查各语言 `description_*.txt` 是否存在「与英文未翻译一致」的问题：

```bash
python scripts/scan_description_translations.py           # 仅输出数量
python scripts/scan_description_translations.py --list 5   # 每语言列出前 5 条路径
```

- **zh-CN**：若 `description_en.txt` 为英文且 `description_cn.txt` 开头与 en 相同 → 视为未译（应为 0）。
- **tw / ar / de / es / fr / it / ja / ko / ru**：若对应 `description_XX.txt` 前 55 字符与 `description_en.txt` 完全一致 → 视为未翻译副本。

## 修复「与 en 相同」的条目

只重译「当前内容与 en 开头相同」的文件，不覆盖已正确翻译的：

```bash
# 按语言分别执行（可加 --dry-run 先看会动哪些文件）
python scripts/translate_descriptions.py --target zh-TW --fix-identical
python scripts/translate_descriptions.py --target ar --fix-identical
python scripts/translate_descriptions.py --target de --fix-identical
python scripts/translate_descriptions.py --target es --fix-identical
python scripts/translate_descriptions.py --target fr --fix-identical
python scripts/translate_descriptions.py --target it --fix-identical
python scripts/translate_descriptions.py --target ja --fix-identical
python scripts/translate_descriptions.py --target ko --fix-identical
python scripts/translate_descriptions.py --target ru --fix-identical
```

修复后再次运行 `scan_description_translations.py` 可确认各语言「identical」数量是否降为 0。

## 批量修复（可选）

```bash
for lang in zh-TW ar de es fr it ja ko ru; do
  python scripts/translate_descriptions.py --target "$lang" --fix-identical
done
```

注意：每种语言约数百到千级文件，整轮耗时较长，建议在 CI 或后台执行。
