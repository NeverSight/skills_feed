---
name: cms-react
description: |
  CMS React components (CMS React 元件). Use when building CMS admin interfaces with article management (文章管理), approval workflows (審核流程), permission-based actions, or Mezzanine UI integration. Covers StandardCMSTable, modals, and article stage management. Keywords: CMS, React, 文章管理, 審核, 表格, table, modal, Mezzanine UI, article, workflow
---

# CMS React Components (CMS React 元件)

## Overview

`@rytass/cms-react-components` 提供基於 Mezzanine UI 的 CMS 管理介面元件，支援文章生命週期管理、權限控制和審核流程。

## Quick Start

### 安裝

```bash
npm install @rytass/cms-react-components @mezzanine-ui/react @mezzanine-ui/core
```

### Provider 設定

```tsx
import { DialogProvider, ModalProvider } from '@rytass/cms-react-components';

function App() {
  return (
    <DialogProvider>
      <ModalProvider>
        <YourCMSApp />
      </ModalProvider>
    </DialogProvider>
  );
}
```

## Core Components

### StandardCMSTable

進階資料表格，支援排序、過濾、分頁、批次操作：

```tsx
import {
  StandardCMSTable,
  ArticleStage,
  ArticlesPermissions,
  ArticleTableActions,
} from '@rytass/cms-react-components';

const ArticleList = () => {
  const columns = [
    { title: '標題', dataIndex: 'title' },
    { title: '建立時間', dataIndex: 'createdAt' },
    { title: '狀態', dataIndex: 'stage' },
  ];

  return (
    <StandardCMSTable<Article>
      columns={columns}
      dataSource={articles}
      currentStage={ArticleStage.DRAFT}
      userPermissions={[
        ArticlesPermissions.CreateArticle,
        ArticlesPermissions.UpdateArticleInDraft,
        ArticlesPermissions.DeleteArticleInDraft,
        ArticlesPermissions.SubmitPutBackArticle,
      ]}
      // 可選：自訂各階段可用操作
      actions={{
        [ArticleStage.DRAFT]: [
          ArticleTableActions.Update,
          ArticleTableActions.Submit,
          ArticleTableActions.Delete,
        ],
      }}
      actionsEvents={{
        onView: async (article) => router.push(`/articles/${article.id}`),
        onSubmit: async (article) => await submitArticle(article.id),
        onDelete: async (article) => await deleteArticle(article.id),
        onPutBack: async (article) => await putBackArticle(article.id),
        onRelease: async (article, releasedAt) => await releaseArticle(article.id, releasedAt),
        onWithdraw: async (article) => await withdrawArticle(article.id),
        onApprove: async (article) => await approveArticle(article.id),
        onReject: async (article, reason) => await rejectArticle(article.id, reason),
      }}
    />
  );
};
```

### StandardCMSFormActions

表單操作按鈕，根據權限和階段顯示：

```tsx
import {
  StandardCMSFormActions,
  ArticleStage,
  ArticlesPermissions,
} from '@rytass/cms-react-components';
import { useForm } from 'react-hook-form';

interface ArticleFormData {
  title: string;
  content: string;
}

const ArticleForm = () => {
  const methods = useForm<ArticleFormData>();

  return (
    <StandardCMSFormActions<ArticleFormData>
      methods={methods}                          // react-hook-form 的 UseFormReturn
      currentStage={ArticleStage.DRAFT}          // 當前文章階段
      userPermissions={[                         // 使用者權限
        ArticlesPermissions.CreateArticle,
        ArticlesPermissions.UpdateArticleInDraft,
        ArticlesPermissions.SubmitPutBackArticle,
      ]}
      createMode={true}                          // 建立模式 (vs 編輯模式)
      actionsEvents={{
        // 建立模式下的操作
        onCreateToDraft: async (data) => await saveToDraft(data),
        onCreateAndSubmit: async (data) => await createAndSubmit(data),
        onCreateAndRelease: async (data, releasedAt) => {
          await createAndRelease(data, releasedAt);
        },
        onCreateAndApprove: async (data) => await createAndApprove(data),

        // 編輯模式下的操作
        onUpdateToDraft: async (data) => await updateToDraft(data),
        onUpdateAndSubmit: async (data) => await updateAndSubmit(data),
        onUpdateAndRelease: async (data, releasedAt) => {
          await updateAndRelease(data, releasedAt);
        },
        onUpdateAndApprove: async (data) => await updateAndApprove(data),

        // 通用操作
        onSubmit: async (data) => await submitForReview(data),
        onRelease: async (data, releasedAt) => await release(data, releasedAt),
        onApprove: async (data) => await approve(data),
        onReject: async (data, reason) => await reject(data, reason),
        onLeave: async (data) => router.back(),
        onGoToEdit: async (data) => router.push(`/articles/${data.id}/edit`),
      }}
      leaveButtonText="返回列表"                  // 可選：自訂離開按鈕文字
      actionButtonText="儲存草稿"                 // 可選：自訂操作按鈕文字
      submitButtonText="送審"                     // 可選：自訂送出按鈕文字
      disableLeaveButton={(values) => methods.formState.isSubmitting}
      disableActionButton={(values) => !values.title}
      disableSubmitButton={(values) => !values.title || !values.content}
    >
      {/* 表單欄位 */}
      <input {...methods.register('title')} placeholder="標題" />
      <textarea {...methods.register('content')} placeholder="內容" />
    </StandardCMSFormActions>
  );
};
```

**StandardCMSFormActionsProps：**

| 屬性 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `methods` | `UseFormReturn<T>` | 是 | react-hook-form 的表單方法 |
| `currentStage` | `ArticleStage` | 是 | 當前文章階段 |
| `userPermissions` | `ArticlesPermissions[]` | 是 | 使用者權限 |
| `actionsEvents` | `StandardCMSFormActionsEventsProps<T>` | 是 | 各操作回調函式 |
| `createMode` | `boolean` | 否 | 是否為建立模式（影響顯示的按鈕） |
| `children` | `ReactNode` | 是 | 表單內容 |
| `className` | `string` | 否 | 容器 className |
| `actionsClassName` | `string` | 否 | 按鈕區 className |
| `leaveButtonText` | `string` | 否 | 離開按鈕文字 |
| `actionButtonText` | `string` | 否 | 操作按鈕文字 |
| `submitButtonText` | `string` | 否 | 送出按鈕文字 |
| `disableLeaveButton` | `(values: T) => boolean` | 否 | 離開按鈕禁用條件 |
| `disableActionButton` | `(values: T) => boolean` | 否 | 操作按鈕禁用條件 |
| `disableSubmitButton` | `(values: T) => boolean` | 否 | 送出按鈕禁用條件 |
| `onLeave` | `(values: T) => Promise<void>` | 否 | 離開按鈕事件（優先於 actionsEvents.onLeave） |
| `onAction` | `(values: T) => Promise<void>` | 否 | 操作按鈕事件 |
| `onSubmit` | `(values: T) => Promise<void>` | 否 | 送出按鈕事件（優先於 actionsEvents.onSubmit） |

### StandardCMSList

整合 Tabs + Table 的完整文章列表元件：

```tsx
import {
  StandardCMSList,
  ArticleStage,
  ArticlesPermissions,
} from '@rytass/cms-react-components';

const ArticleManagement = () => {
  return (
    <StandardCMSList<Article>
      columns={columns}
      dataSource={articles}
      defaultStage={ArticleStage.DRAFT}
      userPermissions={[
        ArticlesPermissions.CreateArticle,
        ArticlesPermissions.UpdateArticleInDraft,
        ArticlesPermissions.DeleteArticleInDraft,
      ]}
      onTabChange={(stage) => {
        // 切換 Tab 時重新載入資料
        fetchArticles(stage);
      }}
      tabsNaming={{
        [ArticleStage.DRAFT]: '草稿區',
        [ArticleStage.REVIEWING]: '待審核',
        [ArticleStage.VERIFIED]: '可發佈',
        [ArticleStage.SCHEDULED]: '已預約',
        [ArticleStage.RELEASED]: '已發佈',
      }}
      actionsEvents={{
        onView: (article) => router.push(`/articles/${article.id}`),
        onSubmit: async (article) => await submitArticle(article.id),
        onDelete: async (article) => await deleteArticle(article.id),
      }}
    />
  );
};
```

**StandardCMSListProps：**

繼承 `StandardCMSTableProps`（除了 `currentStage`），額外提供：

| 屬性 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `defaultStage` | `ArticleStage` | 否 | 預設 Tab（預設 `DRAFT`） |
| `onTabChange` | `(stage: ArticleStage) => void` | 否 | Tab 切換回調 |
| `tabsNaming` | `{ [key in ArticleStage]?: string }` | 否 | 自訂 Tab 名稱 |
| `tableClassName` | `string` | 否 | Table 自訂 className |

### StandardCMSTabs

獨立使用的文章狀態 Tabs：

```tsx
import { StandardCMSTabs, ArticleStage } from '@rytass/cms-react-components';

const [activeStage, setActiveStage] = useState(ArticleStage.DRAFT);

<StandardCMSTabs
  activeStage={activeStage}
  onChange={(stage) => setActiveStage(stage)}
  tabsNaming={{
    [ArticleStage.RELEASED]: '已發佈',
    [ArticleStage.SCHEDULED]: '已預約',
    [ArticleStage.VERIFIED]: '可發佈',
    [ArticleStage.REVIEWING]: '待審核',
    [ArticleStage.DRAFT]: '草稿區',
  }}
/>
```

**StandardCMSTabsProps：**

| 屬性 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `activeStage` | `ArticleStage` | 是 | 當前選中的階段 |
| `onChange` | `(stage: ArticleStage) => void` | 是 | Tab 切換回調 |
| `tabsNaming` | `{ [key in ArticleStage]?: string }` | 否 | 自訂 Tab 名稱 |

**預設 Tab 順序：** 已發佈 → 已預約 → 可發佈 → 待審核 → 草稿區

## Modals

### DeleteWithdrawModal

刪除/撤下選擇對話框（讓使用者選擇要刪除還是撤下）：

```tsx
import {
  useModal,
  DeleteWithdrawModal,
  DeleteWithdrawModalRadio,
} from '@rytass/cms-react-components';

const { openModal } = useModal();

openModal({
  children: (
    <DeleteWithdrawModal
      showSeverityIcon={false}
      defaultRadioValue={DeleteWithdrawModalRadio.Withdraw}
      withDelete={true}
      withWithdraw={true}
      onDelete={async () => {
        await deleteArticle(id);
        // closeModal() 由元件內部自動呼叫
      }}
      onWithdraw={async () => {
        await withdrawArticle(id);
        // closeModal() 由元件內部自動呼叫
      }}
    />
  ),
});
```

**DeleteWithdrawModalProps：**

| 屬性 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `showSeverityIcon` | `boolean` | 否 | 顯示警告圖示（預設 `false`） |
| `defaultRadioValue` | `DeleteWithdrawModalRadio` | 是 | 預設選項 |
| `withDelete` | `boolean` | 否 | 顯示「永久刪除」選項 |
| `withWithdraw` | `boolean` | 否 | 顯示「移至可發佈區」選項 |
| `onDelete` | `() => Promise<void>` | 是 | 刪除回調 |
| `onWithdraw` | `() => Promise<void>` | 是 | 撤下回調 |

**DeleteWithdrawModalRadio：**

```typescript
enum DeleteWithdrawModalRadio {
  Delete = 'Delete',     // 永久刪除
  Withdraw = 'Withdraw', // 撤下至可發佈區
}
```

### RejectModal

審核拒絕對話框（含理由輸入）：

```tsx
import { useModal, RejectModal } from '@rytass/cms-react-components';

const { openModal } = useModal();

openModal({
  children: (
    <RejectModal
      onReject={async (reason) => {
        await rejectArticle(id, reason);
        // closeModal() 由元件內部自動呼叫
      }}
    />
  ),
});
```

**RejectModalProps：**

| 屬性 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `onReject` | `(reason: string) => Promise<void>` | 是 | 拒絕回調，帶入使用者輸入的不通過原因 |

> **注意：** RejectModal 會自動顯示「審核不通過」標題和說明文字，使用者必須輸入不通過原因才能送出。Modal 會在 onReject 完成後自動關閉。

### VerifyReleaseModal

發佈/審核多功能對話框：

```tsx
import {
  useModal,
  VerifyReleaseModal,
  VerifyReleaseModalRadio,
} from '@rytass/cms-react-components';

openModal({
  children: (
    <VerifyReleaseModal
      title="發佈文章"
      showSeverityIcon={false}
      defaultRadioValue={VerifyReleaseModalRadio.Now}
      withApprove={true}
      withReject={true}
      onRelease={async (releasedAt: string) => {
        await releaseArticle(id, releasedAt);
      }}
      onApprove={async () => {
        await approveArticle(id);
      }}
      onReject={async (reason: string) => {
        await rejectArticle(id, reason);
      }}
    />
  ),
});
```

**VerifyReleaseModalProps：**

| 屬性 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `title` | `string` | 是 | Modal 標題 |
| `showSeverityIcon` | `boolean` | 否 | 顯示警告圖示 |
| `defaultRadioValue` | `VerifyReleaseModalRadio` | 否 | 預設選項（預設 `Now`） |
| `withApprove` | `boolean` | 否 | 顯示「即刻通過」選項 |
| `withReject` | `boolean` | 否 | 顯示「不通過」選項 |
| `onRelease` | `(releasedAt: string) => Promise<void>` | 是 | 發佈回調（ISO 格式時間） |
| `onApprove` | `() => Promise<void>` | 否 | 通過審核回調 |
| `onReject` | `(reason: string) => Promise<void>` | 否 | 拒絕審核回調 |

### LogsModal

版本歷史與稽核日誌：

```tsx
import { useModal, LogsModal, LogsStageData, ArticleStage } from '@rytass/cms-react-components';

const { openModal } = useModal();

// 定義取得日誌資料的函式
const fetchLogsData = async (): Promise<LogsStageData> => {
  // 從 API 或其他來源取得文章各階段的日誌資料
  return {
    [ArticleStage.DRAFT]: {
      createdAt: '2024-01-01T00:00:00Z',
      createdBy: '王小明',
      updatedAt: '2024-01-02T10:00:00Z',
      updatedBy: '王小明',
      submittedAt: '',
      submittedBy: '',
      verifiedAt: '',
      verifiedBy: '',
      releasedAt: '',
      releasedBy: '',
      version: 1,
    },
    [ArticleStage.REVIEWING]: {
      createdAt: '',
      createdBy: '',
      updatedAt: '',
      updatedBy: '',
      submittedAt: '2024-01-03T09:00:00Z',
      submittedBy: '王小明',
      verifiedAt: '',
      verifiedBy: '',
      releasedAt: '',
      releasedBy: '',
      version: 2,
    },
    // ... 其他階段
  };
};

openModal({
  children: (
    <LogsModal
      onGetData={fetchLogsData}
      stageWording={{
        [ArticleStage.DRAFT]: {
          stageName: '草稿',
          timeTitle: '最後編輯時間',
          memberTitle: '編輯人員',
        },
        [ArticleStage.REVIEWING]: {
          stageName: '待審核',
          timeTitle: '送審時間',
          memberTitle: '送審人員',
        },
        // ... 可自訂各階段的文字
      }}
    />
  ),
});
```

#### LogsModalProps

| 屬性            | 型別                                                                | 必填 | 說明                     |
| --------------- | ------------------------------------------------------------------- | ---- | ------------------------ |
| `onGetData`     | `() => Promise<LogsStageData>`                                      | 是   | 取得日誌資料的非同步函式 |
| `stageWording`  | `{ [keys in ArticleStage]?: { stageName?, timeTitle?, memberTitle? } }` | 否   | 自訂各階段的顯示文字     |

#### LogsStageData 與 LogsData

```typescript
// 各階段的日誌資料
type LogsStageData = {
  [keys in ArticleStage]?: LogsData | null;
};

// 單一階段的詳細資料
interface LogsData {
  createdAt: string;
  createdBy: string;
  updatedAt: string;
  updatedBy: string;
  submittedAt: string;
  submittedBy: string;
  verifiedAt: string;
  verifiedBy: string;
  releasedAt: string;
  releasedBy: string;
  version?: number;   // 版本號
  reason?: string;    // 退回原因（僅 DRAFT 階段顯示）
}
```

## TypeScript Interfaces

### Events Props

```typescript
// Table 操作事件
interface StandardCMSTableEventsProps<T extends TableDataSourceWithID> {
  onView?: (source: T) => Promise<void>;
  onSubmit?: (source: T) => Promise<void>;
  onPutBack?: (source: T) => Promise<void>;
  onRelease?: (source: T, releasedAt: string) => Promise<void>;
  onWithdraw?: (source: T) => Promise<void>;
  onApprove?: (source: T) => Promise<void>;
  onReject?: (source: T, reason: string) => Promise<void>;
  onDelete?: (source: T) => Promise<void>;
}

// FormActions 操作事件
interface StandardCMSFormActionsEventsProps<T extends FieldValues> {
  onLeave?: (values: T) => Promise<void>;
  onGoToEdit?: (values: T) => Promise<void>;
  onCreateToDraft?: (values: T) => Promise<void>;
  onCreateAndRelease?: (values: T, releasedAt: string) => Promise<void>;
  onCreateAndApprove?: (values: T) => Promise<void>;
  onCreateAndSubmit?: (values: T) => Promise<void>;
  onUpdateToDraft?: (values: T) => Promise<void>;
  onUpdateAndRelease?: (values: T, releasedAt: string) => Promise<void>;
  onUpdateAndApprove?: (values: T) => Promise<void>;
  onUpdateAndSubmit?: (values: T) => Promise<void>;
  onRelease?: (values: T, releasedAt: string) => Promise<void>;
  onApprove?: (values: T) => Promise<void>;
  onReject?: (values: T, reason: string) => Promise<void>;
  onSubmit?: (values: T) => Promise<void>;
}
```

### ArticleTableActionsType

定義各階段可用的 Table 操作：

```typescript
interface ArticleTableActionsType {
  [ArticleStage.DRAFT]?: (
    | ArticleTableActions.Update
    | ArticleTableActions.Submit
    | ArticleTableActions.Release
    | ArticleTableActions.Delete
  )[];
  [ArticleStage.REVIEWING]?: (
    | ArticleTableActions.Update
    | ArticleTableActions.Review
    | ArticleTableActions.Delete
    | ArticleTableActions.PutBack
  )[];
  [ArticleStage.VERIFIED]?: (
    | ArticleTableActions.View
    | ArticleTableActions.Update
    | ArticleTableActions.Release
    | ArticleTableActions.Delete
  )[];
  [ArticleStage.SCHEDULED]?: (
    | ArticleTableActions.View
    | ArticleTableActions.Update
    | ArticleTableActions.Withdraw
  )[];
  [ArticleStage.RELEASED]?: (
    | ArticleTableActions.Update
    | ArticleTableActions.Delete
  )[];
  [ArticleStage.UNKNOWN]?: [];
}
```

## Enums

### ArticleStage

```typescript
enum ArticleStage {
  DRAFT = 'DRAFT',           // 草稿
  REVIEWING = 'REVIEWING',   // 審核中
  VERIFIED = 'VERIFIED',     // 已核准
  SCHEDULED = 'SCHEDULED',   // 預約發布
  RELEASED = 'RELEASED',     // 已發布
  UNKNOWN = 'UNKNOWN',       // 未知狀態
}
```

### ArticlesPermissions

**細顆粒度權限（按文章狀態細分）：**

```typescript
enum ArticlesPermissions {
  // 通用權限
  CreateArticle = 'CreateArticle',               // 建立文章
  SubmitPutBackArticle = 'SubmitPutBackArticle', // 送審/退回
  ApproveRejectArticle = 'ApproveRejectArticle', // 審核通過/拒絕

  // Draft 草稿階段
  UpdateArticleInDraft = 'UpdateArticleInDraft',
  DeleteArticleInDraft = 'DeleteArticleInDraft',

  // Reviewing 審核中階段
  UpdateArticleInReviewing = 'UpdateArticleInReviewing',
  DeleteArticleInReviewing = 'DeleteArticleInReviewing',

  // Verified 已核准階段
  UpdateArticleInVerified = 'UpdateArticleInVerified',
  ReleaseArticleInVerified = 'ReleaseArticleInVerified',
  DeleteArticleInVerified = 'DeleteArticleInVerified',

  // Scheduled 預約發布階段
  UpdateArticleInScheduled = 'UpdateArticleInScheduled',
  ReleaseArticleInScheduled = 'ReleaseArticleInScheduled',
  WithdrawArticleInScheduled = 'WithdrawArticleInScheduled',

  // Released 已發布階段
  UpdateArticleInReleased = 'UpdateArticleInReleased',
  ReleaseArticleInReleased = 'ReleaseArticleInReleased',
  WithdrawArticleInReleased = 'WithdrawArticleInReleased',
  DeleteArticleInReleased = 'DeleteArticleInReleased',
}
```

### ArticleTableActions

**注意：使用 PascalCase（非 SCREAMING_SNAKE_CASE）**

```typescript
enum ArticleTableActions {
  View = 'View',         // 檢視
  Update = 'Update',     // 編輯
  Delete = 'Delete',     // 刪除
  Submit = 'Submit',     // 送審
  PutBack = 'PutBack',   // 退回
  Review = 'Review',     // 審核
  Release = 'Release',   // 發布
  Withdraw = 'Withdraw', // 撤下
}
```

### VerifyReleaseModalRadio

```typescript
enum VerifyReleaseModalRadio {
  Now = 'Now',           // 立即發佈
  Schedule = 'Schedule', // 預約發佈
  Approve = 'Approve',   // 即刻通過
  Reject = 'Reject',     // 不通過
}
```

## Default Permission Presets

```typescript
import {
  defaultAdminRolePermissions,
  defaultGeneralRolePermissions,
  defaultTableActions,
} from '@rytass/cms-react-components';

// Admin 角色預設權限（完整權限）
// 包含所有階段的 Update/Delete/Release/Withdraw 權限

// 一般角色預設權限（有限權限）
// 主要包含 Create、Draft 編輯、送審、部分發布權限

// 預設表格操作（按階段）
// DRAFT: [Update, Submit, Release, Delete]
// REVIEWING: [Update, Review, Delete, PutBack]
// VERIFIED: [View, Update, Release, Delete]
// SCHEDULED: [View, Update, Withdraw]
// RELEASED: [Update, Delete]
```

## Utilities

### havePermission

權限檢查工具函式：

```tsx
import { havePermission, ArticlesPermissions } from '@rytass/cms-react-components';

const canDelete = havePermission({
  userPermissions: userPermissions,
  targetPermission: ArticlesPermissions.DeleteArticleInDraft,
});

if (canDelete) {
  // 顯示刪除按鈕
}
```

### VersionLog Icon

版本日誌圖示元件：

```tsx
import { VersionLog } from '@rytass/cms-react-components';

<VersionLog width={24} height={24} />
```

## Hooks

### useDialog

```tsx
import { useDialog } from '@rytass/cms-react-components';

const { openDialog, closeDialog } = useDialog();

openDialog({
  title: '提示',
  content: '操作成功！',
  onConfirm: closeDialog,
});
```

### useModal

```tsx
import { useModal } from '@rytass/cms-react-components';

const { openModal, closeModal } = useModal();

openModal({
  children: <YourModalComponent prop1="value" />,
  // 可選配置（繼承 Mezzanine UI ModalProps）
  size: 'medium',                    // 'small' | 'medium' | 'large' | 'extraLarge'
  width: 600,                        // 自訂寬度 (px)
  severity: 'warning',               // 'success' | 'warning' | 'error'
  hideCloseIcon: true,               // 是否隱藏關閉按鈕（預設 true）
  disableCloseOnBackdropClick: false, // 是否禁止點擊背景關閉（預設 false）
  className: 'my-modal',             // 自訂 className
  onClose: () => {},                 // 關閉時回調
});
```

**ModalConfigType：**

| 屬性 | 型別 | 預設值 | 說明 |
|------|------|--------|------|
| `children` | `React.JSX.Element` | - | Modal 內容（傳入 JSX） |
| `size` | `ModalSize` | `'medium'` | Modal 尺寸 |
| `width` | `number` | - | 自訂寬度 (px) |
| `severity` | `string` | - | 嚴重程度圖示 |
| `hideCloseIcon` | `boolean` | `true` | 隱藏關閉按鈕 |
| `disableCloseOnBackdropClick` | `boolean` | `false` | 禁止點擊背景關閉 |
| `className` | `string` | - | 自訂 className |
| `onClose` | `() => void` | - | 關閉時回調 |

## Complete Example

```tsx
import {
  DialogProvider,
  ModalProvider,
  StandardCMSList,           // 整合版（Tabs + Table）
  StandardCMSTable,
  StandardCMSTabs,
  useModal,
  DeleteWithdrawModal,
  DeleteWithdrawModalRadio,  // 刪除/撤下選項
  RejectModal,
  VerifyReleaseModal,
  VerifyReleaseModalRadio,
  ArticleStage,
  ArticlesPermissions,
  ArticleTableActions,
  defaultAdminRolePermissions,  // 預設權限集
  defaultGeneralRolePermissions,
  defaultTableActions,
} from '@rytass/cms-react-components';

// App wrapper
function App() {
  return (
    <DialogProvider>
      <ModalProvider>
        <ArticleManagement />
      </ModalProvider>
    </DialogProvider>
  );
}

// 方法一：使用 StandardCMSList（推薦）
function ArticleManagementSimple() {
  const { openModal, closeModal } = useModal();

  return (
    <StandardCMSList<Article>
      columns={columns}
      dataSource={articles}
      defaultStage={ArticleStage.DRAFT}
      userPermissions={defaultAdminRolePermissions}
      onTabChange={(stage) => fetchArticles(stage)}
      actionsEvents={{
        onView: async (article) => router.push(`/articles/${article.id}`),
        onSubmit: async (article) => await submitArticle(article.id),
        onDelete: async (article) => await deleteArticle(article.id),
        onRelease: async (article, releasedAt) => {
          await releaseArticle(article.id, releasedAt);
        },
        onApprove: async (article) => await approveArticle(article.id),
        onReject: async (article, reason) => await rejectArticle(article.id, reason),
      }}
    />
  );
}

// 方法二：分開使用 Tabs + Table（更靈活）
function ArticleManagement() {
  const { openModal, closeModal } = useModal();
  const [articles, setArticles] = useState<Article[]>([]);
  const [currentStage, setCurrentStage] = useState(ArticleStage.DRAFT);

  // 使用細顆粒度權限
  const userPermissions = [
    ArticlesPermissions.CreateArticle,
    ArticlesPermissions.SubmitPutBackArticle,
    ArticlesPermissions.ApproveRejectArticle,
    // Draft
    ArticlesPermissions.UpdateArticleInDraft,
    ArticlesPermissions.DeleteArticleInDraft,
    // Reviewing
    ArticlesPermissions.UpdateArticleInReviewing,
    // Released
    ArticlesPermissions.UpdateArticleInReleased,
    ArticlesPermissions.ReleaseArticleInReleased,
  ];

  const handleDelete = (article: Article) => {
    openModal({
      children: (
        <DeleteWithdrawModal
          defaultRadioValue={DeleteWithdrawModalRadio.Delete}
          withDelete={true}
          withWithdraw={currentStage === ArticleStage.RELEASED}
          onDelete={async () => {
            await deleteArticle(article.id);
            refreshArticles();
          }}
          onWithdraw={async () => {
            await withdrawArticle(article.id);
            refreshArticles();
          }}
        />
      ),
    });
  };

  const handleRelease = (article: Article) => {
    openModal({
      children: (
        <VerifyReleaseModal
          title="發佈文章"
          withApprove={currentStage === ArticleStage.REVIEWING}
          withReject={currentStage === ArticleStage.REVIEWING}
          onRelease={async (releasedAt) => {
            await releaseArticle(article.id, releasedAt);
            refreshArticles();
            closeModal();
          }}
          onApprove={async () => {
            await approveArticle(article.id);
            refreshArticles();
            closeModal();
          }}
          onReject={async (reason) => {
            await rejectArticle(article.id, reason);
            refreshArticles();
            closeModal();
          }}
        />
      ),
    });
  };

  return (
    <div>
      <StandardCMSTabs
        activeStage={currentStage}
        onChange={(stage) => {
          setCurrentStage(stage);
          fetchArticles(stage);
        }}
      />

      <StandardCMSTable<Article>
        columns={columns}
        dataSource={articles}
        currentStage={currentStage}
        userPermissions={userPermissions}
        actions={defaultTableActions}
        actionsEvents={{
          onView: async (article) => router.push(`/articles/${article.id}`),
          onDelete: handleDelete,
          onSubmit: async (article) => {
            await submitArticle(article.id);
            refreshArticles();
          },
          onPutBack: async (article) => {
            await putBackArticle(article.id);
            refreshArticles();
          },
          onRelease: handleRelease,
          onWithdraw: async (article) => {
            await withdrawArticle(article.id);
            refreshArticles();
          },
          onApprove: async (article) => {
            await approveArticle(article.id);
            refreshArticles();
          },
          onReject: async (article, reason) => {
            await rejectArticle(article.id, reason);
            refreshArticles();
          },
        }}
      />
    </div>
  );
}
```

## Dependencies

**Peer Dependencies:**
- `@mezzanine-ui/core`
- `@mezzanine-ui/react`
- `@mezzanine-ui/icons`
- `react`, `react-dom`
- `react-hook-form`
- `dayjs`
- `lodash`

## Troubleshooting

### Modal 不顯示

確保在應用根層級包裝 `ModalProvider`：

```tsx
<ModalProvider>
  <App />
</ModalProvider>
```

### 權限按鈕不顯示

確認 `userPermissions` 陣列包含對應的**細顆粒度權限**：

```tsx
// 錯誤：使用簡化權限（不存在）
userPermissions={[ArticlesPermissions.DELETE]}  // ❌ 不存在

// 正確：使用按階段細分的權限
userPermissions={[
  ArticlesPermissions.DeleteArticleInDraft,     // ✓ Draft 階段刪除
  ArticlesPermissions.DeleteArticleInReleased,  // ✓ Released 階段刪除
]}

// 或使用預設權限集
userPermissions={defaultAdminRolePermissions}  // ✓ 完整權限
```
