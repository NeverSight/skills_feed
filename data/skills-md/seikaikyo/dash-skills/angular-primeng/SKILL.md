---
name: angular-primeng
description: Angular 21 + PrimeNG 企業應用開發最佳實踐。適用於 MES、ERP 等企業級應用開發。涵蓋元件設計、狀態管理、效能優化、PrimeNG 元件使用規範。
source: custom
updated: 2025-01-16
---

# Angular 21 + PrimeNG 開發規範

## 適用場景

- MES 製造執行系統
- ERP 企業資源規劃
- 後台管理系統
- 資料密集型應用

## 核心原則

### 1. 專案結構

```
src/app/
├── core/                    # 核心模組（單例服務）
│   ├── auth/               # 認證相關
│   ├── guards/             # 路由守衛
│   ├── interceptors/       # HTTP 攔截器
│   ├── models/             # 資料模型
│   └── services/           # 共用服務
├── shared/                  # 共用模組
│   ├── components/         # 可復用元件
│   ├── directives/         # 自定義指令
│   ├── pipes/              # 資料管線
│   └── utils/              # 工具函數
├── features/               # 功能模組
│   ├── dashboard/
│   ├── production/
│   └── settings/
└── layout/                 # 版面配置
```

### 2. PrimeNG 設定 (app.config.ts)

```typescript
import { ApplicationConfig } from '@angular/core';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { providePrimeNG } from 'primeng/config';
import Aura from '@primeng/themes/aura';

export const appConfig: ApplicationConfig = {
  providers: [
    provideAnimationsAsync(),
    providePrimeNG({
      theme: {
        preset: Aura,
        options: {
          darkModeSelector: '.dark-mode',
          cssLayer: {
            name: 'primeng',
            order: 'tailwind-base, primeng, tailwind-utilities'
          }
        }
      },
      ripple: true
    })
  ]
};
```

### 3. PrimeNG 元件對照表

| 用途 | 元件 | 範例 |
|------|------|------|
| 表單/詳情側邊欄 | `<p-drawer>` | 編輯工單、新增客戶 |
| 確認對話框 | `<p-dialog>` | 刪除確認、警告訊息 |
| 資料表格 | `<p-table>` | 工單列表、報表 |
| 按鈕 | `<p-button>` | 所有按鈕操作 |
| 文字輸入 | `<input pInputText>` | 搭配 ngModel |
| 下拉選單 | `<p-select>` | 狀態選擇、分類 |
| 日期選擇 | `<p-datepicker>` | 日期範圍篩選 |
| 標籤/徽章 | `<p-tag>` | 狀態標示 |
| Toast 通知 | `<p-toast>` | 操作回饋 |
| 載入遮罩 | `<p-blockui>` | 非同步操作 |

### 4. Signals 狀態管理 (Angular 21)

```typescript
// 推薦：使用 Signals
import { signal, computed, effect } from '@angular/core';

@Component({...})
export class WorkOrderListComponent {
  // 狀態
  workOrders = signal<WorkOrder[]>([]);
  selectedId = signal<string | null>(null);
  isLoading = signal(false);

  // 計算屬性
  selectedOrder = computed(() =>
    this.workOrders().find(o => o.id === this.selectedId())
  );

  pendingCount = computed(() =>
    this.workOrders().filter(o => o.status === 'pending').length
  );

  // 副作用
  constructor() {
    effect(() => {
      console.log('選中的工單:', this.selectedOrder());
    });
  }
}
```

### 5. 服務層設計

```typescript
@Injectable({ providedIn: 'root' })
export class WorkOrderService {
  private apiUrl = environment.apiUrl + '/work-orders';

  constructor(private http: HttpClient) {}

  // 列表查詢（支援篩選）
  getList(params?: WorkOrderQueryParams): Observable<ApiResponse<WorkOrder[]>> {
    return this.http.get<ApiResponse<WorkOrder[]>>(this.apiUrl, { params });
  }

  // 單筆查詢
  getById(id: string): Observable<ApiResponse<WorkOrder>> {
    return this.http.get<ApiResponse<WorkOrder>>(`${this.apiUrl}/${id}`);
  }

  // 新增
  create(data: CreateWorkOrderDto): Observable<ApiResponse<WorkOrder>> {
    return this.http.post<ApiResponse<WorkOrder>>(this.apiUrl, data);
  }

  // 更新
  update(id: string, data: UpdateWorkOrderDto): Observable<ApiResponse<WorkOrder>> {
    return this.http.put<ApiResponse<WorkOrder>>(`${this.apiUrl}/${id}`, data);
  }

  // 刪除
  delete(id: string): Observable<ApiResponse<void>> {
    return this.http.delete<ApiResponse<void>>(`${this.apiUrl}/${id}`);
  }
}
```

### 6. API 回應格式

```typescript
// 統一回應格式
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
}

// 分頁回應
interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    total: number;
    page: number;
    limit: number;
  };
}
```

### 7. 表單處理

```typescript
// 推薦：Reactive Forms + PrimeNG
@Component({
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <div class="field">
        <label for="orderNumber">工單編號</label>
        <input pInputText id="orderNumber" formControlName="orderNumber" />
        <small *ngIf="form.get('orderNumber')?.errors?.['required']" class="p-error">
          必填欄位
        </small>
      </div>

      <div class="field">
        <label for="customer">客戶</label>
        <p-select
          id="customer"
          formControlName="customerId"
          [options]="customers()"
          optionLabel="name"
          optionValue="id"
          placeholder="選擇客戶"
        />
      </div>

      <div class="field">
        <label for="dueDate">交期</label>
        <p-datepicker
          id="dueDate"
          formControlName="dueDate"
          dateFormat="yy-mm-dd"
        />
      </div>

      <p-button type="submit" label="儲存" [loading]="isSubmitting()" />
    </form>
  `
})
export class WorkOrderFormComponent {
  form = new FormGroup({
    orderNumber: new FormControl('', Validators.required),
    customerId: new FormControl('', Validators.required),
    dueDate: new FormControl<Date | null>(null)
  });

  customers = signal<Customer[]>([]);
  isSubmitting = signal(false);
}
```

### 8. 表格最佳實踐

```typescript
@Component({
  template: `
    <p-table
      [value]="workOrders()"
      [paginator]="true"
      [rows]="20"
      [rowsPerPageOptions]="[10, 20, 50]"
      [loading]="isLoading()"
      [globalFilterFields]="['orderNumber', 'customerName']"
      styleClass="p-datatable-sm"
    >
      <ng-template pTemplate="header">
        <tr>
          <th pSortableColumn="orderNumber">
            工單編號 <p-sortIcon field="orderNumber" />
          </th>
          <th pSortableColumn="status">狀態</th>
          <th>操作</th>
        </tr>
      </ng-template>

      <ng-template pTemplate="body" let-order>
        <tr>
          <td>{{ order.orderNumber }}</td>
          <td>
            <p-tag [value]="order.status" [severity]="getStatusSeverity(order.status)" />
          </td>
          <td>
            <p-button icon="pi pi-pencil" [text]="true" (click)="edit(order)" />
            <p-button icon="pi pi-trash" [text]="true" severity="danger" (click)="confirmDelete(order)" />
          </td>
        </tr>
      </ng-template>

      <ng-template pTemplate="emptymessage">
        <tr>
          <td colspan="3" class="text-center">無資料</td>
        </tr>
      </ng-template>
    </p-table>
  `
})
export class WorkOrderTableComponent {
  workOrders = signal<WorkOrder[]>([]);
  isLoading = signal(false);

  getStatusSeverity(status: string): 'success' | 'info' | 'warn' | 'danger' {
    const map: Record<string, 'success' | 'info' | 'warn' | 'danger'> = {
      completed: 'success',
      in_progress: 'info',
      pending: 'warn',
      cancelled: 'danger'
    };
    return map[status] || 'info';
  }
}
```

### 9. Drawer 側邊欄模式

```typescript
@Component({
  template: `
    <p-drawer
      [(visible)]="drawerVisible"
      [header]="isEditMode() ? '編輯工單' : '新增工單'"
      position="right"
      [style]="{ width: '500px' }"
      (onHide)="onClose()"
    >
      <app-work-order-form
        [workOrder]="selectedOrder()"
        (save)="onSave($event)"
        (cancel)="drawerVisible = false"
      />
    </p-drawer>
  `
})
export class WorkOrderListComponent {
  drawerVisible = false;
  selectedOrder = signal<WorkOrder | null>(null);

  isEditMode = computed(() => this.selectedOrder() !== null);

  openCreate() {
    this.selectedOrder.set(null);
    this.drawerVisible = true;
  }

  openEdit(order: WorkOrder) {
    this.selectedOrder.set(order);
    this.drawerVisible = true;
  }
}
```

### 10. 錯誤處理

```typescript
// HTTP 攔截器
@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(private messageService: MessageService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req).pipe(
      catchError((error: HttpErrorResponse) => {
        let message = '發生錯誤，請稍後再試';

        if (error.status === 401) {
          message = '請重新登入';
        } else if (error.status === 403) {
          message = '權限不足';
        } else if (error.status === 404) {
          message = '資料不存在';
        } else if (error.status === 503) {
          message = '服務暫時無法使用';
        } else if (error.error?.error?.message) {
          message = error.error.error.message;
        }

        this.messageService.add({
          severity: 'error',
          summary: '錯誤',
          detail: message
        });

        return throwError(() => error);
      })
    );
  }
}
```

## 禁止事項

1. **禁止 Fallback Mock 資料** - API 失敗應顯示錯誤，不得使用假資料
2. **禁止 Emoji** - 程式碼、註解、UI 都不使用 emoji
3. **禁止簡體字** - 全程使用正體中文（台灣用語）
4. **禁止單檔超過 500 行** - 超過需拆分

## 效能優化

1. **OnPush 變更偵測** - 搭配 Signals 使用
2. **trackBy** - 表格列表必須使用
3. **Lazy Loading** - 功能模組延遲載入
4. **虛擬捲動** - 大量資料使用 `<p-scroller>`

## 參考資源

- [Angular Style Guide](https://angular.dev/style-guide)
- [PrimeNG Documentation](https://primeng.org/)
- [Angular Signals](https://angular.dev/guide/signals)
