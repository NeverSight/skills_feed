---
name: file-organizer
description: 透過理解上下文、尋找重複項目、建議更好的結構，以及自動化清理任務，智慧地組織您電腦中的檔案和資料夾。減少認知負擔，保持您的數位工作空間整潔，無需手動費力。
---

# 檔案整理器

此技能作為您的個人整理助手，協助您維護整個電腦中清晰、合理的檔案結構，而無需持續手動整理的心理負擔。

## 何時使用此技能

- 您的「下載」資料夾一團混亂
- 因為檔案散落各處而找不到檔案
- 您有重複的檔案佔用空間
- 您的資料夾結構不再合理
- 您想建立更好的組織習慣
- 您正在開始新專案並需要良好的結構
- 您正在封存舊專案前進行清理

## 此技能的功能

1. **分析現有結構**：檢視您的資料夾和檔案以了解您擁有什麼
2. **尋找重複項目**：識別系統中的重複檔案
3. **建議組織方式**：根據您的內容提出合理的資料夾結構
4. **自動化清理**：經您同意後移動、重新命名和整理檔案
5. **維護上下文**：根據檔案類型、日期和內容做出明智決策
6. **減少雜亂**：識別您可能不再需要的舊檔案

## 如何使用

### 從您的主目錄開始

```
cd ~
```

然後執行 Claude Code 並尋求協助：

```
協助我整理「下載」資料夾
```

```
在我的「文件」資料夾中尋找重複檔案
```

```
檢視我的專案目錄並建議改進方式
```

### 特定整理任務

```
根據這些下載的檔案類型將它們整理到適當的資料夾中
```

```
尋找重複檔案並協助我決定要保留哪些
```

```
清理我 6 個月以上沒有碰過的舊檔案
```

```
為我的 [工作/專案/相片/等] 建立更好的資料夾結構
```

## 指示

當使用者請求檔案整理協助時：

1. **了解範圍**

   詢問澄清問題：
   - 哪個目錄需要整理？（下載、文件、整個主資料夾？）
   - 主要問題是什麼？（找不到東西、重複項目、太混亂、沒有結構？）
   - 是否有要避免的檔案或資料夾？（目前專案、敏感資料？）
   - 要以多積極的方式整理？（保守 vs. 全面清理）

2. **分析現有狀態**

   檢視目標目錄：
   ```bash
   # Get overview of current structure
   ls -la [target_directory]
   
   # Check file types and sizes
   find [target_directory] -type f -exec file {} \; | head -20
   
   # Identify largest files
   du -sh [target_directory]/* | sort -rh | head -20
   
   # Count file types
   find [target_directory] -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
   ```
   
   總結發現：
   - 總檔案和資料夾數
   - 檔案類型分解
   - 大小分佈
   - 日期範圍
   - 明顯的組織問題

3. **識別組織模式**

   根據檔案，確定合理的分組：

   **按類型**：
   - 文件（PDF、DOCX、TXT）
   - 圖片（JPG、PNG、SVG）
   - 影片（MP4、MOV）
   - 壓縮檔（ZIP、TAR、DMG）
   - 程式碼/專案（包含程式碼的目錄）
   - 試算表（XLSX、CSV）
   - 簡報（PPTX、KEY）

   **按目的**：
   - 工作 vs. 個人
   - 活動中 vs. 封存
   - 專案特定
   - 參考資料
   - 臨時/草稿檔案

   **按日期**：
   - 當前年/月
   - 前幾年
   - 非常舊（封存候選）

4. **尋找重複項目**
   
   When requested, search for duplicates:
   ```bash
   # Find exact duplicates by hash
   find [directory] -type f -exec md5 {} \; | sort | uniq -d
   
   # Find files with same name
   find [directory] -type f -printf '%f\n' | sort | uniq -d
   
   # Find similar-sized files
   find [directory] -type f -printf '%s %p\n' | sort -n
   ```
   
   對於每組重複項目：
   - 顯示所有檔案路徑
   - 顯示大小和修改日期
   - 建議保留哪個（通常是最新的或命名最佳的）
   - **重要**：刪除前始終要求確認

5. **提議整理計畫**

   在進行變更前提出清晰的計畫：
   
   ```markdown
   # Organization Plan for [Directory]
   
   ## Current State
   - X files across Y folders
   - [Size] total
   - File types: [breakdown]
   - Issues: [list problems]
   
   ## Proposed Structure
   
   ```
   [Directory]/
   ├── Work/
   │   ├── Projects/
   │   ├── Documents/
   │   └── Archive/
   ├── Personal/
   │   ├── Photos/
   │   ├── Documents/
   │   └── Media/
   └── Downloads/
       ├── To-Sort/
       └── Archive/
   ```
   
   ## Changes I'll Make
   
   1. **Create new folders**: [list]
   2. **Move files**:
      - X PDFs → Work/Documents/
      - Y images → Personal/Photos/
      - Z old files → Archive/
   3. **Rename files**: [any renaming patterns]
   4. **Delete**: [duplicates or trash files]
   
   ## Files Needing Your Decision
   
   - [List any files you're unsure about]
   
   Ready to proceed? (yes/no/modify)
   ```

6. **執行整理**

   獲得批准後，系統化地整理：

   ```bash
   # 建立資料夾結構
   mkdir -p "path/to/new/folders"

   # 移動檔案並清楚記錄
   mv "old/path/file.pdf" "new/path/file.pdf"

   # 使用一致的模式重新命名檔案
   # 範例：「YYYY-MM-DD - Description.ext」
   ```

   **重要規則**：
   - 刪除任何內容前始終確認
   - 記錄所有移動以便可能的復原
   - 保留原始修改日期
   - 優雅地處理檔案名稱衝突
   - 遇到意外情況時停止並詢問

7. **提供摘要和維護提示**

   整理後：
   
   ```markdown
   # Organization Complete! ✨
   
   ## What Changed
   
   - Created [X] new folders
   - Organized [Y] files
   - Freed [Z] GB by removing duplicates
   - Archived [W] old files
   
   ## New Structure
   
   [Show the new folder tree]
   
   ## Maintenance Tips
   
   To keep this organized:
   
   1. **Weekly**: Sort new downloads
   2. **Monthly**: Review and archive completed projects
   3. **Quarterly**: Check for new duplicates
   4. **Yearly**: Archive old files
   
   ## Quick Commands for You
   
   ```bash
   # Find files modified this week
   find . -type f -mtime -7
   
   # Sort downloads by type
   [custom command for their setup]
   
   # Find duplicates
   [custom command]
   ```
   
   Want to organize another folder?
   ```

## Examples

### Example 1: Organizing Downloads (From Justin Dielmann)

**User**: "My Downloads folder is a mess with 500+ files. Help me organize it."

**Process**:
1. Analyzes Downloads folder
2. Finds patterns: work docs, personal photos, installers, random PDFs
3. Proposes structure:
   - Downloads/
     - Work/
     - Personal/
     - Installers/ (DMG, PKG files)
     - Archive/
     - ToSort/ (things needing decisions)
4. Asks for confirmation
5. Moves files intelligently based on content and names
6. Results: 500 files → 5 organized folders

### Example 2: Finding and Removing Duplicates

**User**: "Find duplicate files in my Documents and help me decide which to keep."

**Output**:
```markdown
# Found 23 Sets of Duplicates (156 MB total)

## Duplicate Set 1: "proposal.pdf"
- `/Documents/proposal.pdf` (2.3 MB, modified: 2024-03-15)
- `/Documents/old/proposal.pdf` (2.3 MB, modified: 2024-03-15)
- `/Desktop/proposal.pdf` (2.3 MB, modified: 2024-03-10)

**Recommendation**: Keep `/Documents/proposal.pdf` (most recent in correct location)
Delete the other 2 copies?

[Continue for all duplicates...]
```

### Example 3: Restructuring Projects Folder

**User**: "Review my ~/Projects directory and suggest improvements."

**Output**:
```markdown
# Analysis of ~/Projects

## Current Structure Issues
- Mix of active and archived projects (3+ years old)
- No consistent naming convention
- Some projects at root, others in random subfolders
- Duplicate folders (project-name, project-name-old, project-name-v2)

## Proposed Structure

```
Projects/
├── Active/
│   ├── client-work/
│   ├── side-projects/
│   └── learning/
├── Archive/
│   ├── 2022/
│   ├── 2023/
│   └── 2024/
└── Templates/
```

## Specific Changes
1. Move 12 projects not touched since 2022 → Archive/
2. Consolidate 4 duplicate project folders
3. Rename projects to consistent format: "client-name-project-name"
4. Create Archive for old work

Want me to implement this?
```

### Example 4: Organizing Photos by Date

**User**: "Organize my photo folders by year and month."

**Output**: Creates structure like:
```
Photos/
├── 2023/
│   ├── 01-January/
│   ├── 02-February/
│   └── ...
├── 2024/
│   ├── 01-January/
│   └── ...
└── Unsorted/
```

Then moves photos based on EXIF data or file modification dates.

## Common Organization Tasks

### Downloads Cleanup
```
Organize my Downloads folder - move documents to Documents, 
images to Pictures, keep installers separate, and archive files 
older than 3 months.
```

### Project Organization
```
Review my Projects folder structure and help me separate active 
projects from old ones I should archive.
```

### Duplicate Removal
```
Find all duplicate files in my Documents folder and help me 
decide which ones to keep.
```

### Desktop Cleanup
```
My Desktop is covered in files. Help me organize everything into 
my Documents folder properly.
```

### Photo Organization
```
Organize all photos in this folder by date (year/month) based 
on when they were taken.
```

### Work/Personal Separation
```
Help me separate my work files from personal files across my 
Documents folder.
```

## Pro Tips

1. **Start Small**: Begin with one messy folder (like Downloads) to build trust
2. **Regular Maintenance**: Run weekly cleanup on Downloads
3. **Consistent Naming**: Use "YYYY-MM-DD - Description" format for important files
4. **Archive Aggressively**: Move old projects to Archive instead of deleting
5. **Keep Active Separate**: Maintain clear boundaries between active and archived work
6. **Trust the Process**: Let Claude handle the cognitive load of where things go

## Best Practices

### Folder Naming
- Use clear, descriptive names
- Avoid spaces (use hyphens or underscores)
- Be specific: "client-proposals" not "docs"
- Use prefixes for ordering: "01-current", "02-archive"

### File Naming
- Include dates: "2024-10-17-meeting-notes.md"
- Be descriptive: "q3-financial-report.xlsx"
- Avoid version numbers in names (use version control instead)
- Remove download artifacts: "document-final-v2 (1).pdf" → "document.pdf"

### When to Archive
- Projects not touched in 6+ months
- Completed work that might be referenced later
- Old versions after migration to new systems
- Files you're hesitant to delete (archive first)

## Related Use Cases

- Setting up organization for a new computer
- Preparing files for backup/archiving
- Cleaning up before storage cleanup
- Organizing shared team folders
- Structuring new project directories

