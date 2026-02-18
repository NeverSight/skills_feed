---
name: oh-graphic-pixel-tests-generator
description: 用于OH-图形-像素级比对用例编写。本技能为AI助手生成OpenHarmony图形测试代码提供完整的框架参考、API文档和代码模板。
---
# 目录

1. [框架概述](#框架概述)
2. [测试流程详解](#测试流程详解)
3. [测试宏系统](#测试宏系统)
4. [完整API参考](#完整api参考)
5. [参数配置说明](#参数配置说明)
6. [测试模板库](#测试模板库)
7. [Drawing API 参考](#drawing-api-参考)
8. [最佳实践](#最佳实践)

---

## 框架概述

### 核心原理

OH-图形测试框架基于 **像素级比对** 验证图形渲染正确性。测试运行在真实的 Rosen 渲染环境中，通过创建场景图节点、执行渲染、截图保存来实现验证。

### 架构流程

```
┌─────────────────────────────────────────────────────────────────┐
│  测试用例 (RSGraphicTest)                                        │
│    - 创建测试节点                                                │
│    - 设置节点属性                                                │
│    - 录制绘制命令                                                │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  RS客户端 (render_service_client)                                │
│    - RSCanvasNode / RSSurfaceNode / RSDisplayNode               │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  RSTransactionProxy::FlushImplicitTransaction()                 │
│    - 事务提交，触发IPC通信                                       │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  RS服务端 (render_service)                                       │
│    - 接收事务，更新服务端节点树                                  │
│    - 渲染管线处理                                               │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  2D Graphics (Drawing引擎)                                       │
│    - Canvas 绘制命令执行                                         │
│    - GPU/Backend 渲染                                           │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  DisplayManager::GetScreenshot()                                │
│    - 获取渲染结果截图                                           │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  PNG 保存                                                        │
│    /data/local/graphic_test/<分类>/<测试类>_<测试名>.png         │
└─────────────────────────────────────────────────────────────────┘
```

### 测试模式


| 模式      | 宏               | 截图方式 | 用途                           |
| --------- | ---------------- | -------- | ------------------------------ |
| AUTOMATIC | `GRAPHIC_TEST`   | 自动截图 | 标准功能测试，测试结束自动截图 |
| MANUAL    | `GRAPHIC_N_TEST` | 手动截图 | 需要手动控制截图时机           |
| DYNAMIC   | `GRAPHIC_D_TEST` | 动态截图 | 支持录制回放的动态测试         |

### 目录结构

```
graphic_test/
├── graphic_test_framework/      # 测试框架
│   ├── include/
│   │   ├── rs_graphic_test.h          # 测试基类
│   │   ├── rs_graphic_test_ext.h      # 测试宏定义
│   │   ├── rs_graphic_test_img.h      # 图片辅助函数
│   │   ├── rs_graphic_test_utils.h    # 工具函数
│   │   └── rs_graphic_test_director.h # 测试控制器
│   └── src/
│       └── rs_graphic_test.cpp        # 框架实现
│
├── test/                          # 测试用例
│   ├── open_capability/            # 开放能力测试
│   ├── rs_perform_feature/         # 性能特性测试
│   ├── drawing_engine/             # 绘制引擎测试
│   └── test_template/              # 测试模板
│
└── BUILD.gn                       # 构建配置
```

---

## 测试流程详解

### 完整生命周期

```
┌─────────────────────────────────────────────────────────────────┐
│  SetUpTestCase() [静态，测试套件开始时执行一次]                  │
│                                                                  │
│  • imageWriteId_ = 0  // 重置截图ID计数器                        │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  SetUp() [每个测试用例执行前]                                    │
│                                                                  │
│  1. ShouldRunCurrentTest()                                      │
│     - 根据 --testType 和 --testMode 参数过滤测试                │
│     - 不满足条件则跳过 (GTEST_SKIP)                              │
│                                                                  │
│  2. 创建测试 Surface                                             │
│     RSSurfaceNode::Create(config, APP_WINDOW_NODE)              │
│     → SetBounds({0, 0, width, height})                          │
│     → SetFrame({0, 0, width, height})                           │
│     → SetBackgroundColor(0xffffffff)                            │
│                                                                  │
│  3. BeforeEach() [用户重写]                                      │
│     - SetScreenSize(width, height)                              │
│     - SetSurfaceBounds(bounds)                                  │
│     - 加载测试资源等                                             │
│                                                                  │
│  4. 多测试模式处理 (isMultiple=true)                             │
│     - 计算网格布局: GetScreenCapacity()                         │
│     - 设置虚拟屏幕尺寸: capacity.x * size.x                     │
│     - 计算当前测试位置: GetPos(testId)                          │
│     - 设置 Surface 位置到对应网格                                │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  测试用例函数体                                                  │
│                                                                  │
│  1. 创建节点                                                     │
│     auto node = RSCanvasNode::Create();                         │
│                                                                  │
│  2. 设置节点属性                                                 │
│     node->SetBounds({x, y, w, h});                              │
│     node->SetFrame({x, y, w, h});                               │
│     node->SetBackgroundColor(color);                            │
│                                                                  │
│  3. 添加到场景图                                                 │
│     GetRootNode()->AddChild(node);                              │
│                                                                  │
│  4. 注册节点 [必须调用]                                          │
│     RegisterNode(node);  // 保持节点引用，防止被释放             │
│                                                                  │
│  5. 录制绘制命令                                                 │
│     auto drawing = node->BeginRecording(w, h);                  │
│     drawing->DrawXXX(...);                                      │
│     node->FinishRecording();                                    │
│                                                                  │
│  6. 刷新事务                                                     │
│     RSTransactionProxy::GetInstance()->FlushImplicitTransaction();│
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  TearDown() [每个测试用例执行后]                                 │
│                                                                  │
│  1. WaitOtherTest()                                             │
│     - 多测试模式: 延迟截图直到所有测试完成                        │
│     - 单测试模式: 直接继续                                       │
│                                                                  │
│  2. StartUIAnimation()                                          │
│     - 启动并执行所有动画                                         │
│                                                                  │
│  3. FlushMessageAndWait(testCaseWaitTime)                       │
│     - 等待渲染完成 (默认 1000ms)                                 │
│                                                                  │
│  4. WaitTimeout(normalWaitTime)                                 │
│     - 额外等待 (默认 10ms)                                       │
│                                                                  │
│  5. 根据测试模式处理                                             │
│     - MANUAL: WaitTimeout(manualTestWaitTime) [手动模式等待]    │
│     - AUTOMATIC/DYNAMIC: TestCaseCapture() [自动截图]           │
│                                                                  │
│  6. AfterEach() [用户重写]                                       │
│     - 用户自定义清理                                             │
│                                                                  │
│  7. 资源清理                                                     │
│     - ResetTestSurface()                                        │
│     - nodes_.clear()                                            │
│     - SendProfilerCommand("rssubtree_clear")                    │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  TearDownTestCase() [静态，测试套件结束时执行一次]               │
│  • 无操作                                                        │
└─────────────────────────────────────────────────────────────────┘
```

### 关键步骤说明

#### 1. RegisterNode() 的重要性

```cpp
// RegisterNode() 做了两件事：
// 1. 将节点添加到 nodes_ 向量，保持 shared_ptr 引用
// 2. 调用 GetRootNode()->RegisterNode(node) 注册到根节点

void RegisterNode(std::shared_ptr<RSNode> node) {
    nodes_.push_back(node);                              // 保持引用
    GetRootNode()->RegisterNode(node);                   // 注册到树
}
```

**不调用 RegisterNode() 的后果**：节点可能被提前释放，导致渲染错误或崩溃。

#### 2. 多测试网格布局

当使用 `GRAPHIC_TESTS` 宏（isMultiple=true）时：

```cpp
// 计算网格容量（尽量接近正方形）
// 例如：12个测试 → 4x3 网格
UIPoint GetScreenCapacity(int testCnt) {
    int cl = 1;  // 列数
    int num = 1;
    while (num < testCnt) {
        cl++;
        num = cl * cl;  // cl² >= testCnt
    }
    int rl = ceil(testCnt / cl);  // 行数
    return {cl, rl};
}

// 计算测试位置
UIPoint GetPos(int id, int cl) {
    int x = id % cl;  // 列索引
    int y = id / cl;  // 行索引
    return {x, y};
}
```

每个测试的 Surface 会被放置到虚拟屏幕的对应网格位置。

#### 3. 截图路径规则

```cpp
// 路径生成规则
std::string GetImageSavePath(const std::string filePath) {
    // filePath: /path/to/graphic_test/test/xxx/my_test.cpp
    // 提取: /test/xxx/
    // 结果: /data/local/graphic_test/test/xxx/

    // 最终文件名格式：
    // /data/local/graphic_test/test/xxx/<测试类>_<测试名>.png
}
```

#### 4. 事务刷新时机

```cpp
// FlushImplicitTransaction() 触发：
// 1. 客户端命令打包
// 2. IPC 发送到服务端
// 3. 服务端更新节点树
// 4. 触发渲染管线

// 必须在以下操作后调用：
// - 节点属性修改后
// - 绘制命令录制完成后
// - 动画启动后
```

---

## 测试宏系统

### 宏定义展开

```cpp
// GRAPHIC_TEST 宏展开后的实际代码
#define GRAPHIC_TEST(test_case_name, test_type, test_name) \
    bool GTEST_TEST_UNIQUE_ID_##test_case_name##test_name##__LINE__ = \
        OHOS::Rosen::TestDefManager::Instance().Regist( \
        #test_case_name, #test_name, test_type, \
        RSGraphicTestMode::AUTOMATIC, __FILE__, false); \
    TEST_F(test_case_name, test_name)
```

### 测试宏类型


| 宏                                     | 测试模式  | isMultiple | 用途                 |
| -------------------------------------- | --------- | ---------- | -------------------- |
| `GRAPHIC_TEST(TestCase, Type, Name)`   | AUTOMATIC | false      | 标准测试，自动截图   |
| `GRAPHIC_N_TEST(TestCase, Type, Name)` | MANUAL    | false      | 手动模式，需手动截图 |
| `GRAPHIC_D_TEST(TestCase, Type, Name)` | DYNAMIC   | false      | 动态回放测试         |
| `GRAPHIC_TESTS(TestCase, Type, Name)`  | AUTOMATIC | true       | 多测试网格布局       |

### 参数说明

```cpp
GRAPHIC_TEST(测试类名, 测试类型, 测试函数名)

// 测试类名: 继承 RSGraphicTest 的类名
// 测试类型: RSGraphicTestType 枚举值
// 测试函数名: 测试用例的函数名
```

### 测试类型 (RSGraphicTestType)

```cpp
enum RSGraphicTestType {
    FRAMEWORK_TEST,           // 框架测试
    ANIMATION_TEST,           // 动画测试
    CONTENT_DISPLAY_TEST,     // 内容显示测试
    SCREEN_MANAGER_TEST,      // 屏幕管理测试
    HARDWARE_PRESENT_TEST,    // 硬件呈现测试
    DRAWING_TEST,             // 绘制测试
    LTPO_TEST,                // LTPO测试
    TEXT_TEST,                // 文本测试
    PIXMAP_TEST,              // PixelMap测试
    SYMBOL_TEST,              // 符号测试
    EFFECT_TEST,              // 效果测试
    HYBRID_RENDER_TEST,       // 混合渲染测试
    GPU_COMPOSER_TEST,        // GPU合成测试
};
```

### TestDefInfo 结构

```cpp
struct TestDefInfo {
    std::string testCaseName;    // 测试类名
    std::string testName;        // 测试函数名
    RSGraphicTestType testType;  // 测试类型
    RSGraphicTestMode testMode;  // 测试模式
    std::string filePath;        // 源文件路径
    bool isMultiple;             // 是否多测试模式
    uint8_t testId;              // 测试ID (多测试模式)
};
```

### 测试注册流程

```cpp
// 1. 宏调用时注册测试信息
TestDefManager::Instance().Regist(name, type, mode, file, isMultiple)

// 2. SetUp() 中检查是否运行当前测试
ShouldRunCurrentTest() {
    auto extInfo = TestDefManager::GetTestInfo(caseName, testName);
    if (filterTestTypes.count(extInfo->testType) == 0) return false;
    if (runTestMode != ALL && extInfo->testMode != runTestMode) return false;
    return true;
}
```

---

## 参数配置说明

### 命令行参数

```bash
# 运行特定类型的测试
./RSGraphicTest --testType=CONTENT_DISPLAY_TEST

# 运行多种类型
./RSGraphicTest --testType=CONTENT_DISPLAY_TEST --testType=ANIMATION_TEST

# 运行特定模式
./RSGraphicTest --testMode=AUTOMATIC    # 自动测试
./RSGraphicTest --testMode=MANUAL       # 手动测试
./RSGraphicTest --testMode=DYNAMIC      # 动态测试

# 设置等待时间
./RSGraphicTest --testCaseWaitTime=2000      # 测试用例等待时间(ms)
./RSGraphicTest --normalWaitTime=100         # 正常等待时间(ms)
./RSGraphicTest --surfaceCaptureWaitTime=1500 # 截图等待时间(ms)
./RSGraphicTest --manualTestWaitTime=3000    # 手动测试等待时间(ms)

# 设置VSync速率
./RSGraphicTest --vsyncRate=2

# 跳过截图
./RSGraphicTest --skipCapture

# 使用gtest过滤器
./RSGraphicTest --gtest_filter=MyTest.*
./RSGraphicTest --gtest_filter=MyTest.MySpecificTest
```

### RSParameterParse 配置项

```cpp
class RSParameterParse {
    std::string imageSavePath = "/data/local/graphic_test/";
    int testCaseWaitTime = 1000;        // 测试用例等待时间(ms)
    int normalWaitTime = 10;             // 正常等待时间(ms)
    int surfaceCaptureWaitTime = 1000;  // 截图等待时间(ms)
    int manualTestWaitTime = 1500;      // 手动测试等待时间(ms)
    std::unordered_set<RSGraphicTestType> filterTestTypes = {};
    RSGraphicTestMode runTestMode = RSGraphicTestMode::ALL;
    int32_t vsyncRate = 1;
    bool skipCapture_ = false;
};
```

### 测试过滤逻辑

```cpp
// ShouldRunCurrentTest() 中的过滤逻辑
bool ShouldRunCurrentTest() {
    auto extInfo = TestDefManager::GetTestInfo(caseName, testName);

    // 类型过滤
    if (!filterTestTypes.empty() &&
        filterTestTypes.count(extInfo->testType) == 0) {
        return false;
    }

    // 模式过滤
    if (runTestMode != ALL && extInfo->testMode != runTestMode) {
        return false;
    }

    return true;
}
```

---

## 测试模板库

### 基础测试模板

```cpp
#include "rs_graphic_test.h"

using namespace testing;
using namespace testing::ext;

namespace OHOS::Rosen {

class MyFeatureTest : public RSGraphicTest {
public:
    void BeforeEach() override
    {
        // 设置屏幕尺寸
        SetScreenSize(1200, 2000);
        // 设置Surface边界
        SetSurfaceBounds({0, 0, 1200, 2000});
    }
};

/*
 * @tc.name: BasicFeatureTest
 * @tc.desc: 测试基本功能
 * @tc.type: FUNC
 * @tc.require: issue12345
 */
GRAPHIC_TEST(MyFeatureTest, CONTENT_DISPLAY_TEST, BasicFeatureTest)
{
    // 1. 创建节点
    auto canvasNode = RSCanvasNode::Create();

    // 2. 设置属性
    canvasNode->SetBounds({100, 100, 500, 500});
    canvasNode->SetFrame({100, 100, 500, 500});
    canvasNode->SetBackgroundColor(0xFFFFFFFF);

    // 3. 添加到场景
    GetRootNode()->AddChild(canvasNode);

    // 4. 注册节点 (必须!)
    RegisterNode(canvasNode);

    // 5. 录制绘制
    auto drawing = canvasNode->BeginRecording(500, 500);
    drawing->DrawRect({50, 50, 450, 450}, Drawing::Paint());
    canvasNode->FinishRecording();

    // 6. 刷新事务
    RSTransactionProxy::GetInstance()->FlushImplicitTransaction();
}

} // namespace OHOS::Rosen
```

### 网格布局模板

```cpp
/*
 * @tc.name: GridLayoutTest
 * @tc.desc: 多项测试网格布局
 * @tc.type: FUNC
 */
GRAPHIC_TEST(MyFeatureTest, CONTENT_DISPLAY_TEST, GridLayoutTest)
{
    // 测试项配置
    int32_t itemCount = 12;
    int32_t nodeWidth = 200;
    int32_t nodeHeight = 200;
    int32_t gap = 50;
    int32_t column = 4;

    // 生成测试颜色数组
    uint32_t colors[] = {
        0xFFFF0000, 0xFF00FF00, 0xFF0000FF, 0xFFFFFF00,
        0xFFFF00FF, 0xFF00FFFF, 0xFFFF8000, 0xFF808080,
        0xFF800000, 0xFF008000, 0xFF000080, 0xFF808000
    };

    for (int32_t i = 0; i < itemCount; i++) {
        auto node = RSCanvasNode::Create();

        // 计算位置
        int32_t row = i / column;
        int32_t col = i % column;
        int32_t x = gap + (nodeWidth + gap) * col;
        int32_t y = gap + (nodeHeight + gap) * row;

        // 设置属性
        node->SetBounds({x, y, nodeWidth, nodeHeight});
        node->SetFrame({x, y, nodeWidth, nodeHeight});
        node->SetBackgroundColor(colors[i]);

        GetRootNode()->AddChild(node);
        RegisterNode(node);
    }

    RSTransactionProxy::GetInstance()->FlushImplicitTransaction();
}
```

### 动画测试模板

#### 方式1: RSNode::Animate (推荐 - 单次动画)

```cpp
/*
 * @tc.name: AnimationClosureTest
 * @tc.desc: 测试动画闭包效果
 * @tc.type: FUNC
 */
GRAPHIC_TEST(MyFeatureTest, ANIMATION_TEST, AnimationClosureTest)
{
    auto node = RSCanvasNode::Create();
    node->SetBounds({100, 100, 400, 400});
    node->SetFrame({100, 100, 400, 400});
    node->SetBackgroundColor(0xFF0000FF);

    GetRootNode()->AddChild(node);
    RegisterNode(node);

    // 使用RSNode::Animate创建动画闭包
    RSAnimationTimingProtocol protocol;
    protocol.SetDuration(300);  // 300ms - 测试用建议值，避免过长
    protocol.SetRepeat(1);      // 执行1次

    auto timingCurve = RSAnimationTimingCurve::EASE_IN_OUT;

    RSNode::Animate(protocol, timingCurve,
        [&]() {
            // 动画闭包: 所有属性修改会被动画化
            node->SetTranslate({50, 50});      // 小幅度平移
            node->SetScale(1.2f);              // 适度缩放
            node->SetAlpha(0.8f);              // 透明度
            node->SetRotation(45.0f);          // 旋转角度
        },
        []() {
            // 动画完成回调 (可选)
            std::cout << "Animation finished" << std::endl;
        }
    );

    RSTransactionProxy::GetInstance()->FlushImplicitTransaction();
}
```

#### 方式2: OpenImplicitAnimation/CloseImplicitAnimation

```cpp
/*
 * @tc.name: ImplicitAnimationTest
 * @tc.desc: 测试显式动画闭包
 * @tc.type: FUNC
 */
GRAPHIC_TEST(MyFeatureTest, ANIMATION_TEST, ImplicitAnimationTest)
{
    auto node = RSCanvasNode::Create();
    node->SetBounds({100, 100, 400, 400});
    node->SetFrame({100, 100, 400, 400});
    node->SetBackgroundColor(0xFF00FF00);

    GetRootNode()->AddChild(node);
    RegisterNode(node);

    // 打开动画闭包
    RSAnimationTimingProtocol protocol;
    protocol.SetDuration(250);  // 250ms
    protocol.SetRepeat(1);

    RSNode::OpenImplicitAnimation(protocol, RSAnimationTimingCurve::EASE_IN);

    // 闭包内的所有属性修改都会被动画化
    node->SetTranslate({30, 30});
    node->SetRotation(90.0f);

    // 关闭动画闭包，返回创建的动画列表
    auto animations = RSNode::CloseImplicitAnimation();

    RSTransactionProxy::GetInstance()->FlushImplicitTransaction();
}
```

#### 多个动画节点测试模板

```cpp
/*
 * @tc.name: MultipleAnimationTest
 * @tc.desc: 测试多个节点动画
 * @tc.type: FUNC
 */
GRAPHIC_TEST(MyFeatureTest, ANIMATION_TEST, MultipleAnimationTest)
{
    const int nodeCount = 4;
    const int nodeSize = 150;
    const int gap = 50;

    for (int i = 0; i < nodeCount; i++) {
        auto node = RSCanvasNode::Create();
        int x = 100 + (nodeSize + gap) * i;
        int y = 200;

        node->SetBounds({x, y, nodeSize, nodeSize});
        node->SetFrame({x, y, nodeSize, nodeSize});
        node->SetBackgroundColor(0xFF0000FF + (i * 0x00110000));

        GetRootNode()->AddChild(node);
        RegisterNode(node);

        // 每个节点独立的动画
        RSAnimationTimingProtocol protocol;
        protocol.SetDuration(200 + i * 50);  // 200ms, 250ms, 300ms, 350ms
        protocol.SetRepeat(1);

        RSNode::Animate(protocol, RSAnimationTimingCurve::EASE_OUT,
            [node, i]() {
                node->SetTranslate({0.0f, -50.0f - i * 10.0f});  // 不同偏移量
                node->SetScale(1.1f + i * 0.05f);
            }
        );
    }

    RSTransactionProxy::GetInstance()->FlushImplicitTransaction();
}
```

### PixelMap 测试模板

```cpp
/*
 * @tc.name: PixelMapDisplayTest
 * @tc.desc: 测试PixelMap显示
 * @tc.type: FUNC
 */
GRAPHIC_TEST(MyFeatureTest, PIXMAP_TEST, PixelMapDisplayTest)
{
    // 加载图片
    auto pixelMap = DecodePixelMap(
        "/data/local/tmp/test.jpg",
        Media::AllocatorType::SHARE_MEM_ALLOC
    );

    if (!pixelMap) {
        std::cout << "Failed to load pixelmap" << std::endl;
        return;
    }

    // 使用图片节点
    auto node = SetUpNodeBgImage("/data/local/tmp/test.jpg", {100, 100, 500, 500});
    GetRootNode()->AddChild(node);
    RegisterNode(node);

    // 或在Canvas中绘制
    auto canvasNode = RSCanvasNode::Create();
    canvasNode->SetBounds({100, 100, 500, 500});
    canvasNode->SetFrame({100, 100, 500, 500});
    GetRootNode()->AddChild(canvasNode);
    RegisterNode(canvasNode);

    auto drawing = canvasNode->BeginRecording(500, 500);
    auto extendDrawing = static_cast<ExtendRecordingCanvas*>(drawing);

    Drawing::SamplingOptions sampling;
    extendDrawing->DrawPixelMapWithParm(pixelMap, {}, sampling);

    canvasNode->FinishRecording();
    RSTransactionProxy::GetInstance()->FlushImplicitTransaction();
}
```

### 变换测试模板

```cpp
/*
 * @tc.name: TransformTest
 * @tc.desc: 测试变换操作
 * @tc.type: FUNC
 */
GRAPHIC_TEST(MyFeatureTest, DRAWING_TEST, TransformTest)
{
    float scales[] = {0.5f, 1.0f, 1.5f, 2.0f};
    float angles[] = {0.0f, 45.0f, 90.0f, 135.0f};
    int32_t scaleCount = sizeof(scales) / sizeof(scales[0]);
    int32_t angleCount = sizeof(angles) / sizeof(angles[0]);
    int32_t nodeSize = 200;
    int32_t gap = 50;

    for (int32_t i = 0; i < scaleCount; i++) {
        for (int32_t j = 0; j < angleCount; j++) {
            auto node = RSCanvasNode::Create();
            int32_t x = gap + (nodeSize + gap) * j;
            int32_t y = gap + (nodeSize + gap) * i;

            node->SetBounds({x, y, nodeSize, nodeSize});
            node->SetFrame({x, y, nodeSize, nodeSize});
            node->SetBackgroundColor(0xFFFFFFFF);
            GetRootNode()->AddChild(node);
            RegisterNode(node);

            auto drawing = node->BeginRecording(nodeSize, nodeSize);

            // 应用变换
            drawing->Translate(nodeSize / 2, nodeSize / 2);
            drawing->Rotate(angles[j]);
            drawing->Scale(scales[i], scales[i]);
            drawing->Translate(-nodeSize / 2, -nodeSize / 2);

            // 绘制矩形
            Drawing::Paint paint;
            paintSetColor(paint, 0xFFFF0000);
            drawing->DrawRect({50, 50, 150, 150}, paint);

            node->FinishRecording();
        }
    }

    RSTransactionProxy::GetInstance()->FlushImplicitTransaction();
}
```

### 边界值测试模板

```cpp
/*
 * @tc.name: BoundaryValueTest
 * @tc.desc: 测试边界值
 * @tc.type: FUNC
 */
GRAPHIC_TEST(MyFeatureTest, CONTENT_DISPLAY_TEST, BoundaryValueTest)
{
    // 测试边界值：负数、零、大数值
    float values[] = {
        -100.0f, -10.0f, -1.0f, 0.0f,  // 负数和零
        0.1f, 1.0f, 10.0f, 100.0f,     // 正常值
        1000.0f, 10000.0f              // 大数值
    };
    int32_t count = sizeof(values) / sizeof(values[0]);
    int32_t nodeWidth = 300;
    int32_t nodeHeight = 100;
    int32_t gap = 30;

    for (int32_t i = 0; i < count; i++) {
        auto node = RSCanvasNode::Create();
        int32_t y = gap + (nodeHeight + gap) * i;

        node->SetBounds({50, y, nodeWidth, nodeHeight});
        node->SetFrame({50, y, nodeWidth, nodeHeight});
        node->SetBackgroundColor(0xFFFFFFFF);
        GetRootNode()->AddChild(node);
        RegisterNode(node);

        auto drawing = node->BeginRecording(nodeWidth, nodeHeight);

        // 使用边界值进行测试
        char text[64];
        snprintf(text, sizeof(text), "Value: %.1f", values[i]);

        drawing->DrawTextBlob(..., text); // 绘制文本
        // 或绘制其他图形表示

        node->FinishRecording();
    }

    RSTransactionProxy::GetInstance()->FlushImplicitTransaction();
}
```

### 手动截图测试模板

```cpp
class MyManualTest : public RSGraphicTest {
public:
    void BeforeEach() override
    {
        SetScreenSize(1200, 2000);
        SetSurfaceBounds({0, 0, 1200, 2000});
    }

    void TestCaseCapture()
    {
        auto pixelMap = DisplayManager::GetInstance().GetScreenshot(
            DisplayManager::GetInstance().GetDefaultDisplayId()
        );
        if (pixelMap) {
            const auto* testInfo = ::testing::UnitTest::GetInstance()->current_test_info();
            std::string fileName = "/data/local/graphic_test/my_test/";
            fileName += std::string(testInfo->test_case_name()) + "_" +
                       std::string(testInfo->name()) + ".png";

            // 创建目录
            namespace fs = std::filesystem;
            fs::create_directories(fileName.substr(0, fileName.find_last_of('/')));

            if (!WriteToPngWithPixelMap(fileName, *pixelMap)) {
                std::cout << "[FAILED] " << fileName << std::endl;
            } else {
                std::cout << "png write to " << fileName << std::endl;
            }
        }
    }
};

/*
 * @tc.name: ManualCaptureTest
 * @tc.desc: 手动控制截图时机
 * @tc.type: FUNC
 */
GRAPHIC_N_TEST(MyManualTest, CONTENT_DISPLAY_TEST, ManualCaptureTest)
{
    auto node = RSCanvasNode::Create();
    node->SetBounds({100, 100, 500, 500});
    node->SetFrame({100, 100, 500, 500});
    node->SetBackgroundColor(0xFF0000FF);
    GetRootNode()->AddChild(node);
    RegisterNode(node);

    auto drawing = node->BeginRecording(500, 500);
    drawing->DrawRect({100, 100, 400, 400}, Drawing::Paint());
    node->FinishRecording();

    RSTransactionProxy::GetInstance()->FlushImplicitTransaction();

    // 等待渲染完成
    usleep(1000000); // 1秒

    // 手动截图
    TestCaseCapture();
}
```

---
---

## 最佳实践

### 必须遵守的规则

1. **始终调用 RegisterNode()**

   ```cpp
   GetRootNode()->AddChild(node);
   RegisterNode(node);  // 必须！
   ```
2. **刷新事务**

   ```cpp
   RSTransactionProxy::GetInstance()->FlushImplicitTransaction();
   ```
3. **使用 BeforeEach 设置环境**

   ```cpp
   void BeforeEach() override {
       SetScreenSize(1200, 2000);
       SetSurfaceBounds({0, 0, 1200, 2000});
   }
   ```

### 节点属性设置顺序

```cpp
// 推荐顺序
auto node = RSCanvasNode::Create();
node->SetBounds({x, y, w, h});          // 1. 先设置边界
node->SetFrame({x, y, w, h});           // 2. 再设置帧
node->SetBackgroundColor(color);        // 3. 设置背景
GetRootNode()->AddChild(node);          // 4. 添加到场景
RegisterNode(node);                     // 5. 注册节点
```

### 颜色格式

```cpp
// ARGB 格式: 0xAARRGGBB
uint32_t color = 0xFFFF0000;  // 不透明红色

// 常用颜色
0xFF000000  // 黑色
0xFFFFFFFF  // 白色
0xFFFF0000  // 红色
0xFF00FF00  // 绿色
0xFF0000FF  // 蓝色
```

### 网格布局计算

```cpp
// 计算网格位置
int32_t row = i / column;
int32_t col = i % column;
int32_t x = gap + (nodeWidth + gap) * col;
int32_t y = gap + (nodeHeight + gap) * row;
```

### 资源路径

```cpp
// 图片路径
std::string imagePath = "/data/local/tmp/test.jpg";

// 截图保存路径
std::string savePath = "/data/local/graphic_test/<分类>/<测试类>_<测试名>.png";
```

### 常见错误


| 错误         | 原因                    | 解决方案                           |
| ------------ | ----------------------- | ---------------------------------- |
| 节点不显示   | 未调用 RegisterNode()   | 添加 RegisterNode(node)            |
| 截图空白     | 未刷新事务              | 添加 FlushImplicitTransaction()    |
| 节点位置错误 | Bounds/Frame 设置不一致 | 确保 Bounds 和 Frame 一致          |
| 内存泄漏     | nodes_ 未清理           | 框架自动清理，检查是否有额外引用   |
| 动画未执行   | 未调用StartUIAnimation  | 框架在TearDown自动调用，或手动调用 |
| 动画测试超时 | duration/repeat设置过大 | 使用200-500ms，repeat=1            |

### 动画测试最佳实践

```cpp
// 1. 使用合理的动画时长 (200-500ms)
RSAnimationTimingProtocol protocol;
protocol.SetDuration(300);  // ✅ 推荐: 300ms
protocol.SetDuration(5000); // ❌ 避免: 过长导致测试超时

// 2. 避免无限循环
protocol.SetRepeat(1);  // ✅ 推荐: 执行1次
protocol.SetRepeat(0);  // ❌ 避免: 无限循环

// 3. 使用小幅度变化
node->SetTranslate({50, 50});    // ✅ 推荐: 小幅度
node->SetTranslate({1000, 1000}); // ❌ 避免: 过大偏移

// 4. 首选RSNode::Animate闭包
RSNode::Animate(protocol, curve, [&]() {
    node->SetTranslate({30, 30});
});  // ✅ 推荐: 简洁清晰

// vs 显式闭包 (需要手动匹配Open/Close)
RSNode::OpenImplicitAnimation(protocol, curve);
node->SetTranslate({30, 30});
RSNode::CloseImplicitAnimation();  // ⚠️ 可选: 更灵活但容易遗漏
```

### 调试技巧

```cpp
// 1. 查看节点树
GetRootNode()->DumpTree();

// 2. 输出日志
LOGI("Test message: %s", "debug info");
std::cout << "Debug: " << value << std::endl;

// 3. 单独运行测试
./RSGraphicTest --gtest_filter=MyTest.MySpecificTest

// 4. 跳过截图快速调试
./RSGraphicTest --skipCapture
```

### 性能建议

1. **复用 PixelMap**：避免重复解码同一图片
2. **控制节点数量**：单测试建议不超过 100 个节点
3. **合理设置等待时间**：根据渲染复杂度调整 waitTime
4. **使用网格布局**：多个测试项时使用 GRAPHIC_TESTS

---

## 参考示例

### 现有测试用例位置

- `graphic_test/test/open_capability/pixmap/pixelmap_display_test.cpp` - PixelMap 测试
- `graphic_test/test/rs_perform_feature/dirty_region/boundary_test.cpp` - 边界测试
- `graphic_test/test/rs_perform_feature/dirty_region/merge_dirty_rect_test.cpp` - 脏区域合并测试
- `graphic_test/test/rs_perform_feature/gpu_composer/gpu_composer_test.cpp` - GPU 合成测试
- `graphic_test/test/drawing_engine/drawing/demo.cpp` - 绘制引擎示例

### 测试框架API参考

#### RSGraphicTest 基类

##### 屏幕和Surface管理

```cpp
// 获取屏幕尺寸
Vector2f GetScreenSize() const;
// 返回: {width, height}

// 设置屏幕尺寸
void SetScreenSize(float width, float height);

// 设置测试Surface边界
void SetSurfaceBounds(const Vector4f& bounds);
// bounds: {left, top, right, bottom} 或 {x, y, width, height}

// 设置屏幕Surface边界 (多测试模式)
void SetScreenSurfaceBounds(const Vector4f& bounds);

// 设置Surface背景色
void SetSurfaceColor(const RSColor& color);
// color: 0xAARRGGBB 格式
```

##### 节点管理

```cpp
// 获取根节点
std::shared_ptr<RSGraphicRootNode> GetRootNode() const;

// 注册节点 (必须调用)
void RegisterNode(std::shared_ptr<RSNode> node);
// 作用: 保持节点引用，防止被提前释放

// 从文件加载渲染节点树
void AddFileRenderNodeTreeToNode(std::shared_ptr<RSNode> node,
                                 const std::string& filePath);
```

##### 动画和同步

```cpp
// 开始执行UI动画 (在TearDown中自动调用)
void StartUIAnimation();

// 等待指定毫秒数
void WaitTimeout(int ms);
```

**动画闭包API (RSNode静态方法):**

```cpp
// 方式1: RSNode::Animate - 单次动画闭包
static std::vector<std::shared_ptr<RSAnimation>> Animate(
    const RSAnimationTimingProtocol& timingProtocol,  // 时序协议
    const RSAnimationTimingCurve& timingCurve,         // 缓动曲线
    const PropertyCallback& callback,                  // 属性修改闭包
    const std::function<void()>& finishCallback = nullptr,   // 完成回调
    const std::function<void()>& repeatCallback = nullptr    // 重复回调
);

// 方式2: OpenImplicitAnimation/CloseImplicitAnimation - 显式动画闭包
static void OpenImplicitAnimation(
    const RSAnimationTimingProtocol& timingProtocol,
    const RSAnimationTimingCurve& timingCurve,
    const std::function<void()>& finishCallback = nullptr
);

static std::vector<std::shared_ptr<RSAnimation>> CloseImplicitAnimation();
```

**动画参数建议 (避免执行时间过长):**


| 参数            | 建议值     | 说明               |
| --------------- | ---------- | ------------------ |
| duration        | 200-500ms  | 测试动画不宜过长   |
| repeat          | 1次或0次   | 避免无限循环       |
| delay           | 0-100ms    | 减少等待时间       |
| translate/scale | 小幅度变化 | 避免过大的坐标偏移 |

**RSAnimationTimingProtocol:**

```cpp
RSAnimationTimingProtocol protocol;
protocol.SetDuration(500);          // 持续时间(毫秒)
protocol.SetRepeat(1);              // 重复次数(0=无限, 1=一次)
protocol.SetDelay(0);               // 延迟时间
protocol.SetSpeed(1.0f);            // 播放速度
protocol.SetDirection(Direction::NORMAL);  // 播放方向
```

**RSAnimationTimingCurve 预设:**

```cpp
RSAnimationTimingCurve::EASE        // 缓动
RSAnimationTimingCurve::EASE_IN     // 缓入
RSAnimationTimingCurve::EASE_OUT    // 缓出
RSAnimationTimingCurve::EASE_IN_OUT // 缓入缓出
RSAnimationTimingCurve::LINEAR      // 线性
RSAnimationTimingCurve::SPRING      // 弹簧
```

##### 生命周期钩子

```cpp
// 用户重写: 每个测试用例执行前
virtual void BeforeEach() {}

// 用户重写: 每个测试用例执行后
virtual void AfterEach() {}
```

##### 回放功能

```cpp
// 准备回放
void PlaybackRecover(const std::string& filePath, float pauseTimeStamp);
// filePath: 录制文件路径
// pauseTimeStamp: 暂停时间戳(秒)

// 停止回放
void PlaybackStop();
```

#### RSGraphicTestDirector 单例

```cpp
// 获取单例
static RSGraphicTestDirector& Instance();

// 获取根节点
std::shared_ptr<RSGraphicRootNode> GetRootNode() const;

// 获取屏幕尺寸
Vector2f GetScreenSize() const;

// 设置屏幕尺寸
void SetScreenSize(float width, float height);

// 设置Surface边界
void SetSurfaceBounds(const Vector4f& bounds);

// 设置屏幕Surface边界
void SetScreenSurfaceBounds(const Vector4f& bounds);

// 设置Surface颜色
void SetSurfaceColor(const RSColor& color);

// 刷新消息
void FlushMessage();

// 刷新并等待
bool FlushMessageAndWait(int timeoutMs);

// 截图
std::shared_ptr<Media::PixelMap> TakeScreenCaptureAndWait(int ms, bool isScreenShot = false);

// 设置/获取单测试模式
void SetSingleTest(bool isSingleTest);
bool IsSingleTest();

// 设置/获取动态测试模式
void SetDynamicTest(bool isDynamicTest);
bool IsDynamicTest();

// 启动动画
void StartRunUIAnimation();

// 检查是否有运行中的动画
bool HasUIRunningAnimation();

// 发送Profiler命令
void SendProfilerCommand(const std::string command, int outTime = 0);
```

#### 图片辅助函数 (rs_graphic_test_img.h)

```cpp
// 解码PixelMap
std::shared_ptr<Media::PixelMap> DecodePixelMap(
    const std::string& pathName,
    const Media::AllocatorType& allocatorType,
    const Media::PixelFormat& dstFormat = Media::PixelFormat::RGBA_8888
);
// pathName: 图片文件路径
// allocatorType: 通常使用 Media::AllocatorType::SHARE_MEM_ALLOC
// dstFormat: 目标像素格式

// 设置节点背景图片 (路径)
std::shared_ptr<RSCanvasNode> SetUpNodeBgImage(
    const std::string& pathName,
    const Vector4f bounds
);

// 设置节点背景图片 (数据)
std::shared_ptr<RSCanvasNode> SetUpNodeBgImage(
    const uint8_t* data,
    uint32_t size,
    const Vector4f bounds
);
```

#### 工具函数 (rs_graphic_test_utils.h)

```cpp
// 保存PixelMap为PNG
bool WriteToPngWithPixelMap(const std::string& fileName,
                            Media::PixelMap& pixelMap);

// 等待指定毫秒
void WaitTimeout(int ms);
```

---

### Drawing API 参考

#### 获取Recording Canvas

```cpp
auto drawing = canvasNode->BeginRecording(width, height);
// ... 执行绘制操作 ...
canvasNode->FinishRecording();
```

#### 几何图形绘制

```cpp
// 点
drawing->DrawPoint(point);
drawing->DrawPoints(PointMode::POINTS, count, pts);
// PointMode: POINTS, LINES, POLYGON

// 线
drawing->DrawLine(startPt, endPt);

// 矩形
drawing->DrawRect(rect);

// 圆角矩形
drawing->DrawRoundRect(roundRect);
drawing->DrawNestedRoundRect(outer, inner);

// 弧形
drawing->DrawArc(oval, startAngle, sweepAngle);

// 饼图
drawing->DrawPie(oval, startAngle, sweepAngle);

// 椭圆
drawing->DrawOval(oval);

// 圆形
drawing->DrawCircle(center, radius);

// 路径
drawing->DrawPath(path);

// 区域
drawing->DrawRegion(region);

// 网格面片
drawing->DrawPatch(cubics[12], colors[4], texCoords[4], mode);

// 顶点网格
drawing->DrawVertices(vertices, mode);
```

#### 图片绘制

```cpp
// 位图
drawing->DrawBitmap(bitmap, x, y);

// 图片 (简单位置)
drawing->DrawImage(image, x, y, sampling);

// 图片 (源-目标矩形)
drawing->DrawImageRect(image, src, dst, sampling, constraint);
drawing->DrawImageRect(image, dst, sampling);

// 九宫格
drawing->DrawImageNine(image, center, dst, filterMode, brush);
drawing->DrawImageLattice(image, lattice, dst, filterMode);

// 图集
drawing->DrawAtlas(atlas, xform[], tex[], colors[], count, mode, sampling);
```

#### PixelMap 绘制 (ExtendRecordingCanvas)

```cpp
auto extendDrawing = static_cast<ExtendRecordingCanvas*>(drawing);

// 带参数绘制
extendDrawing->DrawPixelMapWithParm(pixelMap, rsImageInfo, sampling);

// 矩形区域
extendDrawing->DrawPixelMapRect(pixelMap, src, dst, sampling, constraint);

// 九宫格
extendDrawing->DrawPixelMapNine(pixelMap, center, dst, filterMode);
extendDrawing->DrawPixelMapLattice(pixelMap, lattice, dst, filterMode);

// 带Brush的九宫格
extendDrawing->DrawImageNineWithPixelMap(pixelMap, center, dst, filter, brush);

// SurfaceBuffer
#ifdef ROSEN_OHOS
extendDrawing->DrawSurfaceBuffer(surfaceBufferInfo);
#endif
```

#### 颜色和文本

```cpp
// 纯色 (带混合模式)
drawing->DrawColor(color, BlendMode::SRC_OVER);

// 背景
drawing->DrawBackground(brush);

// 文本块
drawing->DrawTextBlob(blob, x, y);

// 符号
drawing->DrawSymbol(symbolData, locate);

// Picture
drawing->DrawPicture(picture);
```

#### 裁剪操作

```cpp
// 矩形裁剪
drawing->ClipRect(rect, ClipOp::INTERSECT, doAntiAlias);
// ClipOp: DIFFERENCE, INTERSECT

// 圆角矩形裁剪
drawing->ClipRoundRect(roundRect, ClipOp::INTERSECT, doAntiAlias);

// 路径裁剪
drawing->ClipPath(path, ClipOp::INTERSECT, doAntiAlias);

// 区域裁剪
drawing->ClipRegion(region, ClipOp::INTERSECT);

// 自适应圆角裁剪
drawing->ClipAdaptiveRoundRect(radius[4]);
```

#### 变换操作

```cpp
// 设置矩阵
drawing->SetMatrix(matrix);

// 重置矩阵
drawing->ResetMatrix();

// 连接矩阵
drawing->ConcatMatrix(matrix);

// 平移
drawing->Translate(dx, dy);

// 缩放
drawing->Scale(sx, sy);

// 旋转 (绕指定中心)
drawing->Rotate(degrees, cx, cy);

// 错切
drawing->Shear(sx, sy);
```

#### 状态管理

```cpp
// 保存状态
uint32_t saveCount = drawing->Save();

// 保存图层 (离屏渲染)
drawing->SaveLayer(saveLayerOps);

// 恢复状态
drawing->Restore();

// 获取保存层数
uint32_t count = drawing->GetSaveCount();

// 丢弃所有未恢复的保存
drawing->Discard();
```

#### 其他操作

```cpp
// 清空
drawing->Clear();
drawing->Clear(color);

// 刷新
drawing->Flush();

// 自定义文本类型
drawing->SetIsCustomTextType(true);
bool isCustom = drawing->IsCustomTextType();

// 自定义字体
drawing->SetIsCustomTypeface(true);
bool isCustomTypeface = drawing->IsCustomTypeface();

// 录制命令模式
drawing->SetIsRecordCmd(true);
bool isRecordCmd = drawing->IsRecordCmd();

// 重置混合渲染尺寸
drawing->ResetHybridRenderSize(width, height);
```

#### 自定义绘制函数

```cpp
using DrawFunc = std::function<void(Drawing::Canvas* canvas, const Drawing::Rect* rect)>;

extendDrawing->DrawDrawFunc([](Drawing::Canvas* canvas, const Drawing::Rect* rect) {
    // 延迟绘制
    canvas->DrawRect(/* ... */);
});
```
---

### BUILD.gn 配置模板

```python
import("//build/ohos.gni")
import("//foundation/graphic/graphic_2d/graphic_config.gni")

ohos_unittest("my_feature_test") {
  module_out_name = "my_feature_test"

  sources = [
    "my_test.cpp",
  ]

  include_dirs = [
    "//foundation/graphic/graphic_2d/rosen/test",
    "//foundation/graphic/graphic_2d/rosen/include",
    "//foundation/graphic/graphic_2d/graphic_test/graphic_test_framework/include",
  ]

  deps = [
    "//foundation/graphic/graphic_2d/rosen:librosen",
    "//foundation/graphic/graphic_2d/graphic_test/graphic_test_framework:libgraphic_test_framework",
  ]

  external_deps = [
    "hilog_native:libhilog",
    "image_framework:image_native",
  ]

  part_name = "graphic_2d"
  subsystem_name = "graphic"
}
```

---

## 附录

### 常用头文件

```cpp
#include "rs_graphic_test.h"           // 测试基类
#include "rs_graphic_test_img.h"       // 图片辅助
#include "rs_graphic_test_utils.h"     // 工具函数
#include "ui/rs_canvas_node.h"         // Canvas节点
#include "ui/rs_surface_node.h"        // Surface节点
#include "transaction/rs_interfaces.h" // 事务接口
#include "display_manager.h"           // 显示管理器
#include "pixel_map.h"                 // PixelMap
#include "image_source.h"              // 图片源
```

### 常用类型

```cpp
using Vector2f = OHOS::Rosen::Vector2f;      // {x, y}
using Vector4f = OHOS::Rosen::Vector4f;      // {left, top, right, bottom}
using RSColor = OHOS::Rosen::RSColor;        // uint32_t 颜色
```

### 测试注释格式

```cpp
/*
 * @tc.name: TestName
 * @tc.desc: 测试描述
 * @tc.type: FUNC | PERF | RELI
 * @tc.require: issue编号 或 AR编号
 */
```
