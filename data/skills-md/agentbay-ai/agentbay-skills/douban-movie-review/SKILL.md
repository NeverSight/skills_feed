---
name: douban-movie-review
description: 查询豆瓣电影热门影评信息。当用户想要查询某部电影的豆瓣影评、用户评价、热门短评时使用此skill。
---

# 豆瓣电影影评查询

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

- 用户询问某部电影的豆瓣影评
- 用户想了解电影的用户评价
- 用户想查看电影的热门短评

## 使用方法

```bash
python3 scripts/browser-use.py "<任务执行步骤>"

```

## 快速示例
python3 scripts/browser-use.py " \
1. 前往豆瓣网站https://www.douban.com/ \
2. 搜索电影盗梦空间 \
3. 点击盗梦空间进入详情界面,下滑到短评部分 \
4. 提取前5条热门评论 \
5. 以markdown格式返回
"


## 输出格式

```markdown
## 《电影名称》豆瓣影评

### 热门短评

1. 用户名 点赞数 评论内容
2. 用户名 点赞数 评论内容
```

## 注意事项

- 始终注明信息来源为豆瓣
- 不需要创建新的脚本，用skill目录下的browser-use.py
- 任务需要执行1~2分钟，不要杀进程，请耐心等待和观察任务，也不要重试
- skill调用后，控制台会打印出asp流化链接（可视化的url），可告知用户查看
