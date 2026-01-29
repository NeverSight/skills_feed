---
name: jy-aiot-collector-developer
description: 基于矿山鸿雁（jy-aiot）Plugin框架，根据Markdown表格格式的数据采集协议文档，生成混合模式的采集模块代码（配置+代码片段）。使用此技能可快速实现HTTP服务端/客户端、FTP、数据库、MQTT、Kafka等通信协议的采集模块，简化定制协议采集组件的开发复杂度。
---

# JY-AIOT Collector Developer

## Overview

本技能用于为矿山鸿雁（jy-aiot）产品的Plugin框架快速生成数据采集模块代码。根据用户提供的Markdown表格格式的协议定义文档，自动生成符合Plugin框架规范的采集模块，包括：

- **通信层代码**：HTTP服务端/客户端、FTP文件读取、数据库客户端、MQTT订阅、Kafka订阅
- **数据解析器**：将原始数据转换为框架抽象的标准格式
- **配置模板**：符合Plugin框架规范的YAML/JSON配置文件
- **集成入口**：可直接集成到jy-aiot产品的采集框架中

## Protocol Document Format

### Required Fields

协议文档必须包含以下表格结构：

```markdown
## 通信配置

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| protocol | string | 是 | 通信协议：http_server/http_client/ftp/database/mqtt/kafka |
| host | string | 是 | 服务地址 |
| port | int | 是 | 端口号 |
| path | string | 否 | 路径（HTTP/FTP） |
| username | string | 否 | 用户名 |
| password | string | 否 | 密码 |
| interval | int | 否 | 采集间隔（秒），默认60 |

## 数据点定义

| 字段名称 | 字段标识 | 数据类型 | 字节偏移 | 字节长度 | 缩放因子 | 起始位 | 位长度 | 备注 |
|----------|----------|----------|----------|----------|----------|--------|--------|------|
| 温度 | temperature | float | 0 | 4 | 0.1 | - | - | 设备温度值 |
| 压力 | pressure | int | 4 | 2 | 1 | - | - | 管道压力 |

## 数据解析规则

| 规则ID | 目标字段 | 源数据表达式 | 转换公式 | 数据单位 | 备注 |
|--------|----------|--------------|----------|----------|------|
| rule_01 | temperature | raw[0:4] | bytes_to_float_le(value) | ℃ | 小端解析 |
| rule_02 | pressure | raw[4:6] | bytes_to_int_le(value) / 100 | MPa | 缩放转换 |
```

### Supported Communication Protocols

| 协议 | 说明 | 适用场景 |
|------|------|----------|
| http_server | HTTP服务端 | 被动接收设备推送数据 |
| http_client | HTTP客户端 | 主动轮询RESTful API |
| ftp | FTP文件读取 | 定时拉取设备导出文件 |
| database | 数据库客户端 | 直接读取数据库表 |
| mqtt | MQTT订阅 | 订阅MQTT主题接收数据 |
| kafka | Kafka订阅 | 订阅Kafka topic接收数据 |

### Supported Data Types

| 类型标识 | Go类型 | 说明 | 示例 |
|----------|--------|------|------|
| int | int32/int64 | 有符号整数 | 传感器整数值 |
| uint | uint32/uint64 | 无符号整数 | 计数器值 |
| float | float32/float64 | 浮点数 | 温度、压力 |
| string | string | 字符串 | 设备状态文本 |
| bool | bool | 布尔值 | 开关状态 |
| bytes | []byte | 字节数组 | 原始二进制数据 |

## Workflow

### 1. Protocol Analysis

分析用户提供的协议文档，提取：

- 通信方式（protocol字段）
- 连接参数（host、port、credentials）
- 数据点列表（字段名称、标识、类型、位置）
- 解析规则（转换公式、单位）

### 2. Code Generation

根据协议类型生成对应的采集模块代码：

```
collector_{protocol}/
├── config.yaml          # 通信和采集配置
├── collector.go         # 采集器主逻辑
├── parser.go            # 数据解析器
├── metrics.go           # 数据模型定义
└── README.md            # 集成说明
```

### 3. Core Components

#### Collector Interface

所有采集模块必须实现Plugin框架的核心接口：

```go
type Collector interface {
    // Init 初始化采集器
    Init(config Config) error
    
    // Start 启动采集
    Start(ctx context.Context) error
    
    // Stop 停止采集
    Stop() error
    
    // GetMetrics 获取采集到的数据
    GetMetrics() []Metric
    
    // Health 健康检查
    Health() HealthStatus
}
```

#### Metric Data Model

```go
type Metric struct {
    DeviceID    string            `json:"device_id"`    // 设备标识
    MetricID    string            `json:"metric_id"`    // 指标标识
    Timestamp   time.Time         `json:"timestamp"`    // 采集时间
    Value       interface{}       `json:"value"`        // 值
    Quality     DataQuality       `json:"quality"`      // 数据质量
    Tags        map[string]string `json:"tags"`         // 标签
    Fields      map[string]string `json:"fields"`       // 扩展字段
}

type DataQuality int

const (
    QualityGood     DataQuality = 0  // 好
    QualityBad      DataQuality = 1  // 坏数据
    QualityUncertain DataQuality = 2  // 不确定
)
```

### 4. Protocol-Specific Implementations

#### HTTP Server Collector

用于被动接收设备推送的数据：

```go
type HTTPServerCollector struct {
    config     HTTPServerConfig
    handler    *http.Server
    parser     DataParser
    buffer     sync.Map
}

func (c *HTTPServerCollector) Start(ctx context.Context) error {
    c.handler = &http.Server{
        Addr:    fmt.Sprintf(":%d", c.config.Port),
        Handler: c.createRouter(),
    }
    go c.handler.ListenAndServe()
    return nil
}
```

#### MQTT Collector

用于订阅MQTT主题接收实时数据：

```go
type MQTTCollector struct {
    config     MQTTConfig
    client     mqtt.Client
    parser     DataParser
    buffer     sync.Map
}

func (c *MQTTCollector) Start(ctx context.Context) error {
    opts := mqtt.NewClientOptions().
        AddBroker(fmt.Sprintf("tcp://%s:%d", c.config.Host, c.config.Port)).
        SetClientID(c.config.ClientID)
    
    c.client = mqtt.NewClient(opts)
    if token := c.client.Connect(); token.Wait() && token.Error() != nil {
        return token.Error()
    }
    
    c.client.Subscribe(c.config.Topic, 0, c.messageHandler)
    return nil
}
```

#### Database Collector

用于直接查询数据库：

```go
type DatabaseCollector struct {
    config     DatabaseConfig
    db         *sql.DB
    parser     DataParser
    interval   time.Duration
}

func (c *DatabaseCollector) Start(ctx context.Context) error {
    connStr := fmt.Sprintf("user=%s password=%s host=%s port=%d dbname=%s",
        c.config.Username, c.config.Password, 
        c.config.Host, c.config.Port, c.config.Database)
    
    var err error
    c.db, err = sql.Open("postgres", connStr)
    if err != nil {
        return err
    }
    
    ticker := time.NewTicker(c.interval)
    go c.pollLoop(ctx, ticker)
    return nil
}
```

## Generated Code Structure

### Directory Layout

```
jy-aiot-collector-{protocol}/
├── config/
│   ├── collector.yaml          # 主配置
│   └── metrics.yaml            # 指标定义
├── internal/
│   ├── collector.go            # 采集器实现
│   ├── parser.go               # 数据解析器
│   ├── client.go               # 协议客户端
│   └── model.go                # 数据模型
├── scripts/
│   ├── test_connection.sh      # 连接测试脚本
│   └── mock_server.py          # 模拟服务器（测试用）
├── deploy/
│   ├── docker-compose.yml      # 部署配置
│   └── k8s-deployment.yaml     # K8s部署
├── go.mod
├── main.go
└── README.md
```

### Configuration Template

```yaml
# collector.yaml
collector:
  name: "temperature_sensor"
  protocol: "mqtt"
  enabled: true
  interval: 10  # 秒

mqtt:
  broker: "tcp://192.168.1.100:1883"
  topic: "sensors/+/temperature"
  client_id: "jy-aiot-collector-001"
  username: "collector"
  password: "${MQTT_PASSWORD}"
  qos: 1
  clean_session: true

metrics:
  - id: "temperature"
    name: "设备温度"
    source: "payload.temperature"
    datatype: "float"
    unit: "℃"
    tags:
      device_type: "sensor"

parser:
  format: "json"
  timestamp_field: "timestamp"
  timestamp_format: "2006-01-02T15:04:05Z07:00"

output:
  buffer_size: 1000
  batch_size: 100
  flush_interval: 5
```

### Parser Implementation

```go
// internal/parser.go
type DataParser interface {
    Parse(raw []byte) ([]Metric, error)
    Validate(data interface{}) bool
    Transform(value interface{}, rule string) interface{}
}

type JSONParser struct {
    timestampField string
    timestampFormat string
}

func (p *JSONParser) Parse(raw []byte) ([]Metric, error) {
    var data map[string]interface{}
    if err := json.Unmarshal(raw, &data); err != nil {
        return nil, err
    }
    
    metrics := make([]Metric, 0)
    // 解析逻辑
    return metrics, nil
}
```

## Integration Guide

### 1. Module Registration

在Plugin框架中注册采集模块：

```go
// plugin.go
func init() {
    collector.Register("mqtt", NewMQTTCollector)
    collector.Register("http_server", NewHTTPServerCollector)
    collector.Register("database", NewDatabaseCollector)
}
```

### 2. Configuration Loading

加载并验证配置：

```go
// config/config.go
type Config struct {
    Collector CollectorConfig `yaml:"collector"`
    MQTT      MQTTConfig      `yaml:"mqtt"`
    Metrics   []MetricConfig  `yaml:"metrics"`
    Parser    ParserConfig    `yaml:"parser"`
    Output    OutputConfig    `yaml:"output"`
}

func LoadConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, err
    }
    
    var config Config
    if err := yaml.Unmarshal(data, &config); err != nil {
        return nil, err
    }
    
    // 验证配置
    if err := config.Validate(); err != nil {
        return nil, err
    }
    
    return &config, nil
}
```

### 3. Health Check

实现健康检查接口：

```go
func (c *MQTTCollector) Health() HealthStatus {
    status := HealthStatus{
        Status: "healthy",
        Checks: make(map[string]string),
    }
    
    if !c.client.IsConnected() {
        status.Status = "unhealthy"
        status.Checks["connection"] = "disconnected"
    }
    
    return status
}
```

## Example Usage

### User Request Example

用户请求：
```
请基于以下协议文档生成MQTT温度传感器采集模块：

## 通信配置
| 字段 | 值 |
|------|-----|
| protocol | mqtt |
| host | 192.168.1.100 |
| port | 1883 |
| topic | sensors/+/temperature |

## 数据点定义
| 字段名称 | 字段标识 | 数据类型 |
|----------|----------|----------|
| 温度值 | temperature | float |
| 设备ID | device_id | string |
```

### Generated Response

根据协议文档生成完整的采集模块代码，包括：
- `collector.yaml` 配置文件
- `internal/collector.go` 采集器实现
- `internal/parser.go` JSON解析器
- `main.go` 程序入口
- `README.md` 集成说明

## Resources

### scripts/

- `generate_collector.py` - 采集模块代码生成脚本
- `test_protocol.py` - 协议解析测试工具
- `mock_device.py` - 模拟设备数据源

### references/

- [COMMUNICATION.md](references/COMMUNICATION.md) - 各通信协议详细配置
- [PARSING.md](references/PARSING.md) - 数据解析规则和转换函数
- [MODELS.md](references/MODELS.md) - 数据模型和接口定义
- [EXAMPLES.md](references/EXAMPLES.md) - 完整采集模块示例

### assets/

- `templates/collector_template.go` - 采集器代码模板
- `templates/config_template.yaml` - 配置文件模板
- `schemas/metric.schema.json` - 指标定义JSON Schema