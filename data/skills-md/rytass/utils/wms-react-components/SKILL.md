---
name: wms-react-components
description: |
  WMS map React components (WMS 地圖 React 元件). Use when building warehouse map editors (倉儲地圖編輯器), interactive floor plans, location visualization, or spatial management interfaces. Based on ReactFlow/XYFlow. Keywords: WMS, 倉儲地圖, warehouse map, floor plan, ReactFlow, XYFlow, 地圖編輯, spatial, location
---

# WMS Map React Components (WMS 地圖 React 元件)

## Overview

`@rytass/wms-map-react-components` 提供互動式倉庫空間編輯元件，基於 ReactFlow (XYFlow)，支援背景圖、矩形/路徑繪製、多層編輯和歷史管理。

## Quick Start

### 安裝

```bash
npm install @rytass/wms-map-react-components @xyflow/react @mezzanine-ui/react
```

### 基本使用

```tsx
import { WMSMapModal, ViewMode } from '@rytass/wms-map-react-components';

function App() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button onClick={() => setIsOpen(true)}>開啟地圖編輯器</button>

      <WMSMapModal
        open={isOpen}
        onClose={() => setIsOpen(false)}
        viewMode={ViewMode.EDIT}
        onSave={(mapData) => {
          console.log('Saved:', mapData);
          // 提交到後端
        }}
      />
    </>
  );
}
```

## Core Components

### WMSMapModal

主要的地圖編輯模態框：

```tsx
interface WMSMapModalProps {
  open: boolean;
  onClose: () => void;
  viewMode?: ViewMode;              // EDIT | VIEW（預設 EDIT）
  title?: string;                   // 模態框標題
  colorPalette?: string[];          // 區域顏色選項
  onNodeClick?: (info: WMSNodeClickInfo) => void;
  onSave?: (mapData: Map) => void;
  onBreadcrumbClick?: (warehouseId: string, index: number) => void;
  onNameChange?: (name: string) => Promise<void>;  // 名稱變更回呼
  initialNodes?: FlowNode[];
  initialEdges?: FlowEdge[];
  debugMode?: boolean;
  maxFileSizeKB?: number;           // 背景圖大小限制（預設 30720 = 30MB）
  warehouseIds?: string[];          // 倉儲 ID 列表（用於 breadcrumb）

  // 必要回呼：處理圖片上傳
  onUpload: (files: File[]) => Promise<string[]>;  // 回傳上傳後的 filename 陣列

  // 可選：取得完整圖片 URL
  getFilenameFQDN?: (filename: string) => Promise<string> | string;
}
```

### 子元件

| 元件 | 說明 |
|------|------|
| `WMSMapHeader` | 工具列與標題 |
| `WMSMapContent` | 畫布內容與編輯控制 |
| `Breadcrumb` | 倉儲層級導航 |
| `ContextMenu` | 右鍵菜單 |
| `Toolbar` | 編輯工具列 |

### 節點類型

| 節點 | 說明 |
|------|------|
| `ImageNode` | 背景圖節點 |
| `RectangleNode` | 矩形區域節點 |
| `PathNode` | 路徑/多邊形節點 |

## Enums

### ViewMode

```typescript
enum ViewMode {
  EDIT = 'EDIT',   // 編輯模式
  VIEW = 'VIEW',   // 檢視模式
}
```

### EditMode

```typescript
enum EditMode {
  BACKGROUND = 'BACKGROUND',  // 背景圖編輯
  LAYER = 'LAYER',            // 區域層編輯
}
```

### DrawingMode

```typescript
enum DrawingMode {
  NONE = 'NONE',            // 無繪製
  RECTANGLE = 'RECTANGLE',  // 矩形繪製
  PEN = 'PEN',              // 自由繪製/路徑
}
```

### LayerDrawingTool

```typescript
enum LayerDrawingTool {
  SELECT = 'SELECT',        // 選取工具
  RECTANGLE = 'RECTANGLE',  // 矩形工具
  PEN = 'PEN',              // 鋼筆工具
}
```

### MapRangeType

```typescript
enum MapRangeType {
  RECTANGLE = 'RECTANGLE',  // 矩形區域
  POLYGON = 'POLYGON',      // 多邊形區域
}
```

### MapRangeColor

```typescript
enum MapRangeColor {
  RED = 'RED',
  YELLOW = 'YELLOW',
  GREEN = 'GREEN',
  BLUE = 'BLUE',
  BLACK = 'BLACK',
}
```

## Data Structures

### ID 型別別名

```typescript
export type ID = string;
```

### Map

```typescript
interface Map {
  id: ID;
  backgrounds: MapBackground[];
  ranges: MapRange[];  // MapRectangleRange | MapPolygonRange
}

interface MapBackground {
  id: string;
  filename: string;   // 檔案名稱（非完整 URL）
  width: number;
  height: number;
  x: number;
  y: number;
}

interface MapRectangleRange {
  type: MapRangeType.RECTANGLE;  // 'RECTANGLE'
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  color: string;
}

interface MapPolygonRange {
  type: MapRangeType.POLYGON;  // 'POLYGON'
  id: string;
  points: MapPolygonRangePoint[];
  color: string;
}

interface MapPolygonRangePoint {
  x: number;
  y: number;
}
```

### WMSNodeClickInfo

```typescript
type WMSNodeClickInfo =
  | ImageNodeClickInfo
  | RectangleNodeClickInfo
  | PathNodeClickInfo;

// 基礎介面
interface NodeClickInfo {
  id: string;
  type: string;
  position: { x: number; y: number };
  zIndex?: number;
  selected?: boolean;
}

interface ImageNodeClickInfo extends NodeClickInfo {
  type: 'imageNode';
  imageData: {
    filename: string;
    size: { width: number; height: number };
    originalSize: { width: number; height: number };
    imageUrl: string;
  };
  mapBackground: MapBackground;  // 可直接傳給後端的格式
}

interface RectangleNodeClickInfo extends NodeClickInfo {
  type: 'rectangleNode';
  rectangleData: {
    color: string;
    size: { width: number; height: number };
  };
  mapRectangleRange: MapRectangleRange;  // 可直接傳給後端的格式
}

interface PathNodeClickInfo extends NodeClickInfo {
  type: 'pathNode';
  pathData: {
    color: string;
    strokeWidth: number;
    pointCount: number;
    points: { x: number; y: number }[];
    bounds: {
      minX: number;
      minY: number;
      maxX: number;
      maxY: number;
    } | null;
  };
  mapPolygonRange: MapPolygonRange;  // 可直接傳給後端的格式
}
```

## Utility Functions

### 資料轉換

```typescript
import {
  transformNodeToClickInfo,
  transformNodesToMapData,
  transformApiDataToNodes,
  validateMapData,
  loadMapDataFromApi,
  calculatePolygonBounds,
  calculateNodeZIndex,
  logMapData,
  logNodeData,
} from '@rytass/wms-map-react-components';

// ReactFlow 節點 → 點擊資訊
const clickInfo = transformNodeToClickInfo(node);

// ReactFlow 節點 → 地圖資料 (後端格式)
const mapData = transformNodesToMapData(nodes);

// API 資料 → ReactFlow 節點（支援自訂圖片 URL 產生器）
const nodes = transformApiDataToNodes(apiData);
const nodesWithCustomUrl = transformApiDataToNodes(apiData, (filename) => {
  return `https://cdn.example.com/images/${filename}`;
});

// 驗證地圖資料格式
const isValid = validateMapData(mapData);

// 輔助函數：計算多邊形邊界
const bounds = calculatePolygonBounds(points);
// 回傳: { minX, maxX, minY, maxY, width, height }

// 輔助函數：計算節點 zIndex
const zIndex = calculateNodeZIndex(existingNodes, 'rectangleNode');

// Debug 工具：格式化輸出資料到 console
logMapData(mapData);   // 輸出完整地圖資料
logNodeData(node);     // 輸出單一節點詳細資訊
```

## Complete Example

```tsx
import { useState, useCallback } from 'react';
import {
  WMSMapModal,
  ViewMode,
  transformNodesToMapData,
  transformApiDataToNodes,
  WMSNodeClickInfo,
  Map,
} from '@rytass/wms-map-react-components';

function WarehouseMapEditor() {
  const [isOpen, setIsOpen] = useState(false);
  const [mapData, setMapData] = useState<Map | null>(null);

  // 從後端載入地圖資料
  const loadMapData = async () => {
    const response = await fetch('/api/warehouse/map');
    const data = await response.json();
    setMapData(data);
  };

  // 上傳圖片到後端（必要回呼）
  const handleUpload = useCallback(async (files: File[]): Promise<string[]> => {
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));

    const response = await fetch('/api/warehouse/upload', {
      method: 'POST',
      body: formData,
    });

    const { filenames } = await response.json();
    return filenames;  // 回傳 filename 陣列
  }, []);

  // 取得圖片完整 URL（可選）
  const getFilenameFQDN = useCallback((filename: string) => {
    return `https://cdn.example.com/warehouse-images/${filename}`;
  }, []);

  // 儲存地圖資料到後端
  const handleSave = useCallback(async (data: Map) => {
    await fetch('/api/warehouse/map', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    setMapData(data);
    setIsOpen(false);
  }, []);

  // 處理區域點擊
  const handleNodeClick = useCallback((info: WMSNodeClickInfo) => {
    if (info.type === 'rectangleNode') {
      // 取得後端格式的資料
      console.log('Clicked zone:', info.mapRectangleRange);
      // 可以導航到該區域的庫存頁面
    }
  }, []);

  return (
    <div>
      <button onClick={() => { loadMapData(); setIsOpen(true); }}>
        編輯倉儲地圖
      </button>

      <WMSMapModal
        open={isOpen}
        onClose={() => setIsOpen(false)}
        viewMode={ViewMode.EDIT}
        title="倉庫 A 地圖"
        colorPalette={[
          '#FF6B6B',  // 紅 - 危險品區
          '#4ECDC4',  // 青 - 冷藏區
          '#45B7D1',  // 藍 - 一般存放區
          '#96CEB4',  // 綠 - 出貨區
          '#FFEAA7',  // 黃 - 暫存區
        ]}
        initialNodes={mapData ? transformApiDataToNodes(mapData, getFilenameFQDN) : undefined}
        onSave={handleSave}
        onNodeClick={handleNodeClick}
        onUpload={handleUpload}
        getFilenameFQDN={getFilenameFQDN}
        maxFileSizeKB={30720}  // 30MB（預設值）
        warehouseIds={['10001', '10001A']}
      />
    </div>
  );
}

// 唯讀檢視元件（VIEW 模式不需要 onUpload）
function WarehouseMapViewer({ mapData }: { mapData: Map }) {
  const [selectedZone, setSelectedZone] = useState<string | null>(null);

  const getFilenameFQDN = (filename: string) =>
    `https://cdn.example.com/warehouse-images/${filename}`;

  return (
    <WMSMapModal
      open={true}
      onClose={() => {}}
      viewMode={ViewMode.VIEW}
      initialNodes={transformApiDataToNodes(mapData, getFilenameFQDN)}
      onUpload={async () => []}  // VIEW 模式下可用空實作
      onNodeClick={(info) => {
        if (info.type === 'rectangleNode') {
          setSelectedZone(info.id);
        }
      }}
    />
  );
}
```

## 多層級導航

```tsx
function WarehouseNavigator() {
  const [breadcrumb, setBreadcrumb] = useState([
    { id: 'warehouse-1', name: '主倉庫' },
  ]);

  const handleBreadcrumbClick = (warehouseId: string, index: number) => {
    // 導航到特定層級
    setBreadcrumb(breadcrumb.slice(0, index + 1));
    loadWarehouseMap(warehouseId);
  };

  const handleZoneClick = (info: WMSNodeClickInfo) => {
    if (info.type === 'rectangleNode') {
      // 進入子區域（需自行維護 zone 名稱對應）
      setBreadcrumb([...breadcrumb, { id: info.id, name: `Zone ${info.id}` }]);
      loadWarehouseMap(info.id);
    }
  };

  return (
    <WMSMapModal
      open={true}
      onClose={() => {}}
      viewMode={ViewMode.VIEW}
      onBreadcrumbClick={handleBreadcrumbClick}
      onNodeClick={handleZoneClick}
    />
  );
}
```

## Constants

> **注意：** Constants 目前未從主入口導出，若需使用請直接從 constants 路徑導入：
> ```typescript
> import { UI_CONFIG, CANVAS_CONFIG } from '@rytass/wms-map-react-components/constants';
> ```

```typescript
// 預設尺寸
DEFAULT_IMAGE_WIDTH         // 300
DEFAULT_IMAGE_HEIGHT        // 200
DEFAULT_RECTANGLE_WIDTH     // 150
DEFAULT_RECTANGLE_HEIGHT    // 100

// 顏色
DEFAULT_RECTANGLE_COLOR     // '#3b82f6'
SELECTION_BORDER_COLOR      // '#3b82f6'
DEFAULT_BACKGROUND_TOOL_COLOR // '#3b82f6'

// 最小尺寸
MIN_RECTANGLE_SIZE          // 10
MIN_RESIZE_WIDTH            // 50
MIN_RESIZE_HEIGHT           // 30

// 文字標籤
DEFAULT_RECTANGLE_LABEL     // '矩形區域'
DEFAULT_PATH_LABEL          // '路徑區域'

// 透明度
ACTIVE_OPACITY              // 1
INACTIVE_OPACITY            // 0.4
RECTANGLE_INACTIVE_OPACITY  // 0.6

// 調整大小控制項尺寸
RESIZE_CONTROL_SIZE         // 16
IMAGE_RESIZE_CONTROL_SIZE   // 20

// UI 配置
UI_CONFIG.HISTORY_SIZE       // 50 (Undo/Redo 歷史大小)
UI_CONFIG.COLOR_CHANGE_DELAY // 800ms
UI_CONFIG.STAGGER_DELAY      // 100ms (圖片上傳間隔)
UI_CONFIG.NODE_SAVE_DELAY    // 50ms

// Canvas 配置
CANVAS_CONFIG.MIN_ZOOM        // 0.1
CANVAS_CONFIG.MAX_ZOOM        // 4
CANVAS_CONFIG.DEFAULT_VIEWPORT // { x: 0, y: 0, zoom: 1 }
CANVAS_CONFIG.BACKGROUND_COLOR // '#F5F5F5'

// 檔案上傳配置
UPLOAD_CONFIG.DEFAULT_MAX_FILE_SIZE_KB  // 30720 (30MB)
UPLOAD_CONFIG.SUPPORTED_MIME_TYPES      // ['image/png', 'image/jpeg', ...]

// 支援的圖片類型
SUPPORTED_IMAGE_TYPES.ACCEPT      // 'image/png,image/jpeg,image/jpg'
SUPPORTED_IMAGE_TYPES.PATTERN     // /^image\/(png|jpeg|jpg)$/
SUPPORTED_IMAGE_TYPES.EXTENSIONS  // ['png', 'jpg', 'jpeg']

// 預設倉庫 ID
DEFAULT_WAREHOUSE_IDS  // ['10001', '10001A', '10002', '100002B', '100003', '100003B']
```

## Dependencies

**Required:**
- `@xyflow/react` ^12.10.0

**Peer Dependencies:**
- `@mezzanine-ui/react`
- `@mezzanine-ui/react-hook-form-v2`
- `react`, `react-dom`
- `react-hook-form`

## Troubleshooting

### 地圖無法顯示

確保 ReactFlow Provider 正確包裝：
```tsx
// WMSMapModal 內部已包含 ReactFlowProvider
// 不需要額外包裝
```

### 背景圖上傳失敗

檢查 `maxFileSizeKB` 設定，預設為 30720KB (30MB)。

### 節點無法拖曳

確認 `viewMode` 設為 `ViewMode.EDIT`。

## React Hooks

`@rytass/wms-map-react-components` 提供以下內部 Hooks，用於地圖編輯器的核心功能。

> **注意：** 這些 Hooks 目前為內部使用，未在主入口匯出。若需使用，請直接從相應檔案導入：
> ```typescript
> import { useContextMenu } from '@rytass/wms-map-react-components/hooks/use-context-menu';
> ```

### useContextMenu

管理節點的右鍵菜單與圖層排列操作。

```typescript
interface UseContextMenuProps {
  id: string;                                    // 節點 ID
  editMode: EditMode;                            // 當前編輯模式
  isEditable: boolean;                           // 是否可編輯
  nodeType?: 'rectangleNode' | 'pathNode' | 'imageNode';
}

interface UseContextMenuReturn {
  contextMenu: { visible: boolean; x: number; y: number };
  handleContextMenu: (event: React.MouseEvent) => void;
  handleCloseContextMenu: () => void;
  handleDelete: () => void;
  arrangeActions: {
    onBringToFront: () => void;   // 移至最上層
    onBringForward: () => void;   // 上移一層
    onSendBackward: () => void;   // 下移一層
    onSendToBack: () => void;     // 移至最下層
  };
  arrangeStates: {
    canBringToFront: boolean;
    canBringForward: boolean;
    canSendBackward: boolean;
    canSendToBack: boolean;
  };
  getNodes: () => Node[];
  setNodes: (nodes: Node[] | ((nodes: Node[]) => Node[])) => void;
}

const { contextMenu, handleContextMenu, arrangeActions } = useContextMenu({
  id: nodeId,
  editMode: EditMode.LAYER,
  isEditable: true,
  nodeType: 'rectangleNode',
});
```

### useDirectStateHistory

直接狀態歷史系統，支援 Undo/Redo 功能。

```typescript
interface UseDirectStateHistoryOptions {
  maxHistorySize?: number;  // 預設 50
  debugMode?: boolean;      // 預設 false
}

interface UseDirectStateHistoryReturn {
  saveState: (nodes: FlowNode[], edges: FlowEdge[], operation: string, editMode: EditMode) => void;
  undo: () => { nodes: FlowNode[]; edges: FlowEdge[]; editMode: EditMode } | null;
  redo: () => { nodes: FlowNode[]; edges: FlowEdge[]; editMode: EditMode } | null;
  canUndo: boolean;
  canRedo: boolean;
  initializeHistory: (initialNodes: FlowNode[], initialEdges: FlowEdge[], editMode: EditMode) => void;
  clearHistory: () => void;
  getHistorySummary: () => HistorySummary;
  history?: HistoryState[];       // debugMode 啟用時可用
  currentIndex?: number;          // debugMode 啟用時可用
}

const {
  saveState,
  undo,
  redo,
  canUndo,
  canRedo,
  initializeHistory,
} = useDirectStateHistory({ maxHistorySize: 100, debugMode: false });

// 初始化
initializeHistory(nodes, edges, EditMode.LAYER);

// 保存操作後狀態
saveState(nodes, edges, 'add-rectangle', EditMode.LAYER);

// 執行 Undo
const prevState = undo();
if (prevState) {
  setNodes(prevState.nodes);
  setEdges(prevState.edges);
}
```

### usePenDrawing

鋼筆工具繪製多邊形/路徑區域。

```typescript
interface UsePenDrawingProps {
  editMode: EditMode;
  drawingMode: DrawingMode;
  onCreatePath: (points: { x: number; y: number }[]) => void;
}

interface UsePenDrawingReturn {
  containerRef: React.RefObject<HTMLDivElement | null>;  // 綁定到容器
  isDrawing: boolean;                                     // 是否正在繪製
  previewPath: { x: number; y: number }[] | null;        // 預覽路徑
  currentPoints: { x: number; y: number }[];             // 已繪製的點
  firstPoint: { x: number; y: number } | null;           // 第一個點（閉合提示用）
  canClose: boolean;                                      // 是否可閉合（>=3 點）
  forceComplete: () => void;                             // 強制完成繪製
}

const {
  containerRef,
  isDrawing,
  previewPath,
  canClose,
} = usePenDrawing({
  editMode: EditMode.LAYER,
  drawingMode: DrawingMode.PEN,
  onCreatePath: (points) => {
    // 建立路徑節點
    createPathNode(points);
  },
});

// 操作方式：
// - 單擊：添加點
// - 雙擊：完成並閉合路徑
// - 點擊第一個點：閉合路徑
// - Enter：完成並閉合路徑
// - Escape：取消繪製
// - Shift + 點擊：約束至 45 度角
```

### useRectangleDrawing

矩形區域繪製工具。

```typescript
interface UseRectangleDrawingProps {
  editMode: EditMode;
  drawingMode: DrawingMode;
  onCreateRectangle: (startX: number, startY: number, endX: number, endY: number) => void;
}

interface UseRectangleDrawingReturn {
  containerRef: React.RefObject<HTMLDivElement | null>;
  isDrawing: boolean;
  previewRect: {
    x: number;
    y: number;
    width: number;
    height: number;
  } | null;
}

const {
  containerRef,
  isDrawing,
  previewRect,
} = useRectangleDrawing({
  editMode: EditMode.LAYER,
  drawingMode: DrawingMode.RECTANGLE,
  onCreateRectangle: (x1, y1, x2, y2) => {
    createRectangleNode(x1, y1, x2, y2);
  },
});

// 操作方式：
// - 按住滑鼠拖曳建立矩形
// - 放開滑鼠完成建立
// - 最小尺寸限制：MIN_RECTANGLE_SIZE
```

### useTextEditing

節點文字標籤編輯功能。

```typescript
interface UseTextEditingProps {
  id: string;                     // 節點 ID
  label: string;                  // 當前標籤文字
  isEditable: boolean;            // 是否可編輯
  onTextEditComplete?: (id: string, oldText: string, newText: string) => void;
}

interface UseTextEditingReturn {
  isEditing: boolean;
  editingText: string;
  inputRef: React.RefObject<HTMLInputElement | null>;
  setEditingText: React.Dispatch<React.SetStateAction<string>>;
  handleDoubleClick: (event: React.MouseEvent) => void;  // 雙擊開始編輯
  handleKeyDown: (event: React.KeyboardEvent) => void;   // 鍵盤事件處理
  handleBlur: () => void;                                 // 失焦保存
  updateNodeData: (updates: Record<string, unknown>) => void;
}

const {
  isEditing,
  editingText,
  inputRef,
  setEditingText,
  handleDoubleClick,
  handleKeyDown,
  handleBlur,
} = useTextEditing({
  id: nodeId,
  label: 'Zone A',
  isEditable: true,
  onTextEditComplete: (id, oldText, newText) => {
    console.log(`節點 ${id} 標籤從 "${oldText}" 改為 "${newText}"`);
    saveState(nodes, edges, 'edit-label', editMode);
  },
});

// 操作方式：
// - 雙擊節點：開始編輯
// - Enter：確認保存
// - Escape：取消編輯
// - 點擊外部：自動保存
```

### Hooks 使用注意事項

1. **必須在 ReactFlowProvider 內使用**：所有 hooks 依賴 `useReactFlow`
2. **內部使用為主**：這些 hooks 主要供 WMS 元件內部使用
3. **歷史記錄整合**：繪製與編輯操作應搭配 `useDirectStateHistory` 記錄
4. **模式檢查**：各 hooks 會檢查 `editMode` 和 `drawingMode` 狀態
