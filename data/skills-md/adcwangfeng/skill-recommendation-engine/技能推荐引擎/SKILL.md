---
name: 技能推荐引擎
description: 智能技能推荐系统，根据用户场景自动推荐最合适的3个技能方案，并支持自动打包和GitHub托管
dependencies:
  - node.js
  - npm
  - git
---

# 技能推荐引擎

## Description
智能技能推荐系统，根据用户场景自动推荐最合适的3个技能方案，并支持自动打包和GitHub托管。

## Capabilities
- 分析用户需求场景
- 智能推荐匹配的技能
- 自动生成标准化技能包
- 安全配置管理
- 自动创建GitHub仓库
- 自动上传技能包
- 支持npx安装

## Usage
- 描述您的使用场景
- 系统将自动追问3个关键问题
- 推荐3个最合适的技能方案
- 选择方案后自动打包并上传至GitHub
- 生成的技能包支持通过npx命令安装

## Example Usage Scenarios
- **Automation**: 自动化重复任务的技能创建
- **Integration**: 系统集成类技能生成
- **Monitoring**: 监控类技能创建
- **Communication**: 通信交互类技能生成

## Example Commands
- "我需要一个自动化任务管理工具"
- "帮我创建一个数据分析系统"
- "我想要一个聊天机器人"
- "创建一个文件处理技能"

## Files
- `index.js`: 主入口文件
- `engine.js`: 核心推荐引擎
- `config.js`: 安全配置管理器
- `config_wizard.js`: 配置向导
- `skill_matcher.js`: 技能匹配算法
- `github_handler.js`: GitHub自动托管功能
- `question_generator.js`: 智能提问模块
- `skill_template.js`: 标准化技能模板
- `packager.js`: 技能打包工具
- `setup_config.js`: 配置向导启动脚本

## Dependencies
- Node.js >= 14.0.0
- Git client
- GitHub account with appropriate permissions

## Configuration
The skill requires GitHub authentication for repository creation and file uploads.
Run `node setup_config.js` to initialize the configuration.