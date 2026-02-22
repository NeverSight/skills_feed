---
name: weibo-hot-search
description: 查询微博热搜信息。当用户想要查询微博热搜榜、文娱热搜、热度排行时使用此skill。
---

# 微博热搜查询

## 依赖

```bash
python3 -m pip install wuying-agentbay-sdk
```

## 安装步骤

在使用此技能之前，请确保已安装必要的依赖包：

```bash
python3 -m pip install wuying-agentbay-sdk
```

## 使用场景

- 用户想查询微博热搜榜单
- 用户想了解文娱类热搜话题
- 用户想筛选特定热度以上的热搜内容

## 使用方法

```bash
python3 scripts/browser-use.py "<任务执行步骤>"
```

## 快速示例

```bash
python3 scripts/browser-use.py " \
1. 前往微博网站 https://weibo.com/ \
2. 点击左侧菜单中的微博热搜下的文娱分类 \
3. 你需要提取榜单中前十条热搜消息 \
4. 以markdown格式返回所有符合条件的热搜信息
"
```

## 输出格式

```markdown
## 微博热搜 - 文娱分类

### 热搜列表（热度 ≥ 50000）

1. **话题名称**
   - 热度: xxx
   - 排名: #xxx

2. **话题名称**
   - 热度: xxx
   - 排名: #xxx

### 统计信息
- 总计: xx条热搜
- 最高热度: xxxxx
- 最低热度: xxxxx
```

## 注意事项

- 始终注明信息来源为微博
- 不需要创建新的脚本，用skill目录下的browser-use.py
- 如果页面加载较慢，请耐心等待
- 热度数值可能实时变化，以抓取时刻为准
- skill调用后，控制台会打印出asp流化链接（可视化的url），可告知用户查看