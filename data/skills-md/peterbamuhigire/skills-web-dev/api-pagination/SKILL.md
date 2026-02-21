---
name: api-pagination
description: "Cursor/offset pagination pattern for PHP REST APIs and Android (Jetpack Compose + MVVM). Covers backend response format, Android DTOs, repository, use case, ViewModel state, and infinite-scroll LazyColumn. Use when adding pagination to any list endpoint."
---

# API Pagination Skill

## Overview

Standard offset-based pagination pattern used across the Maduuka platform. Applies to both the PHP backend (REST API) and the Android client (Kotlin + Compose).

**Pattern:** Backend returns `data.items[]` + `data.pagination{}`. Android appends items on scroll, tracks page/totalPages in ViewModel state.

**Deployment:** Backend runs on Windows dev (MySQL 8.4.7), Ubuntu staging (MySQL 8.x), Debian production (MySQL 8.x). Pagination queries must use `utf8mb4_unicode_ci` collation and work identically on all platforms.

## PHP Backend Pattern

### Response Format (MANDATORY)

Every paginated list endpoint MUST return this structure:

```json
{
  "success": true,
  "data": {
    "items": [ ... ],
    "pagination": {
      "page": 1,
      "per_page": 30,
      "total": 142,
      "total_pages": 5
    }
  }
}
```

### PHP Implementation Template

```php
<?php
declare(strict_types=1);
require_once __DIR__ . '/../middleware.php';

require_method('GET');
$auth = require_auth();
$db   = get_db();

$franchiseId = (int)$auth['franchise_id'];
$page        = max(1, (int)($_GET['page'] ?? 1));
$perPage     = min(100, max(1, (int)($_GET['per_page'] ?? 30)));
// Optional filters
$status      = isset($_GET['status']) ? trim((string)$_GET['status']) : '';

try {
    $where  = 't.franchise_id = :fid';
    $params = ['fid' => $franchiseId];

    if ($status !== '') {
        $where .= ' AND t.status = :status';
        $params['status'] = $status;
    }

    // 1. Count total
    $countSql = "SELECT COUNT(*) FROM tbl_example t WHERE {$where}";
    $countStmt = $db->prepare($countSql);
    $countStmt->execute($params);
    $total = (int)$countStmt->fetchColumn();
    $countStmt->closeCursor();   // IMPORTANT for PDO

    $totalPages = $total > 0 ? (int)ceil($total / $perPage) : 1;
    $offset = ($page - 1) * $perPage;

    // 2. Fetch page
    $sql = "SELECT t.* FROM tbl_example t WHERE {$where}
            ORDER BY t.created_at DESC
            LIMIT :lim OFFSET :off";

    $queryParams = $params;
    $queryParams['lim'] = $perPage;
    $queryParams['off'] = $offset;

    $stmt = $db->prepare($sql);
    foreach ($queryParams as $key => $value) {
        if ($key === 'lim' || $key === 'off') {
            $stmt->bindValue($key, $value, PDO::PARAM_INT);
        } else {
            $stmt->bindValue($key, $value);
        }
    }
    $stmt->execute();
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // 3. Return with pagination metadata
    json_response(200, [
        'success' => true,
        'data'    => [
            'items'      => $rows,
            'pagination' => [
                'page'        => $page,
                'per_page'    => $perPage,
                'total'       => $total,
                'total_pages' => $totalPages,
            ],
        ],
    ]);
} catch (Throwable $e) {
    json_response(500, [
        'success' => false,
        'message' => 'Failed to load items',
        'error'   => $e->getMessage(),
    ]);
}
```

### Key PHP Rules

1. **Always `closeCursor()`** after the COUNT query before running the main query (PDO requirement).
2. **Bind LIMIT/OFFSET as `PDO::PARAM_INT`** — string binding causes MySQL errors.
3. **Cap `per_page`** at 100 to prevent abuse: `min(100, max(1, ...))`.
4. **Default `per_page`** is 30 for list screens, 50 for stock-level screens.
5. **Response shape** is `data.items` + `data.pagination` — NEVER return a flat array in `data`.

## Android Client Pattern

### 1. DTO Layer

```kotlin
// Wrapper for paginated list
@JsonClass(generateAdapter = true)
data class ExampleListResponse(
    @Json(name = "success") val success: Boolean,
    @Json(name = "data") val data: ExampleListData? = null,
    @Json(name = "message") val message: String? = null
)

@JsonClass(generateAdapter = true)
data class ExampleListData(
    @Json(name = "items") val items: List<ExampleDto>? = null,
    @Json(name = "pagination") val pagination: PaginationDto? = null
)

// Reuse existing PaginationDto
@JsonClass(generateAdapter = true)
data class PaginationDto(
    @Json(name = "page") val page: Int,
    @Json(name = "per_page") val perPage: Int,
    @Json(name = "total") val total: Int,
    @Json(name = "total_pages") val totalPages: Int
)
```

### 2. Domain Model

```kotlin
data class Pagination(
    val page: Int,
    val perPage: Int,
    val total: Int,
    val totalPages: Int
)
```

### 3. API Service

```kotlin
@GET("example/list")
suspend fun getExamples(
    @Query("status") status: String? = null,
    @Query("page") page: Int = 1,
    @Query("per_page") perPage: Int = 30
): Response<ExampleListResponse>
```

### 4. Repository

```kotlin
// Interface
suspend fun getExamples(
    status: String? = null,
    page: Int = 1
): Result<Pair<List<ExampleModel>, Pagination>>

// Implementation
override suspend fun getExamples(
    status: String?,
    page: Int
): Result<Pair<List<ExampleModel>, Pagination>> = safeCall {
    val response = api.getExamples(status = status, page = page)
    if (!response.isSuccessful) throw httpError(response)
    val body = response.body() ?: throw Exception("Empty response")
    if (!body.success) throw Exception(body.message ?: "Failed to load")
    val items = body.data?.items?.map { it.toDomain() } ?: emptyList()
    val pagination = body.data?.pagination?.toDomain() ?: Pagination(1, 30, 0, 1)
    items to pagination
}
```

### 5. Use Case

```kotlin
class GetExamplesUseCase @Inject constructor(
    private val repository: ExampleRepository
) {
    suspend operator fun invoke(
        status: String? = null,
        page: Int = 1
    ): Result<Pair<List<ExampleModel>, Pagination>> {
        return repository.getExamples(status, page)
    }
}
```

### 6. ViewModel State + loadMore()

```kotlin
data class ExampleListState(
    val items: List<ExampleModel> = emptyList(),
    val isLoading: Boolean = false,
    val isLoadingMore: Boolean = false,
    val error: String? = null,
    val currentPage: Int = 1,
    val totalPages: Int = 1
)

@HiltViewModel
class ExampleListViewModel @Inject constructor(
    private val getExamplesUseCase: GetExamplesUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow(ExampleListState())
    val uiState: StateFlow<ExampleListState> = _uiState.asStateFlow()

    init { loadItems() }

    fun loadItems() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null, currentPage = 1) }

            getExamplesUseCase(page = 1).fold(
                onSuccess = { (items, pagination) ->
                    _uiState.update {
                        it.copy(
                            items = items,     // REPLACE on fresh load
                            isLoading = false,
                            currentPage = pagination.page,
                            totalPages = pagination.totalPages
                        )
                    }
                },
                onFailure = { e ->
                    _uiState.update { it.copy(isLoading = false, error = e.message) }
                }
            )
        }
    }

    fun loadMore() {
        val state = _uiState.value
        // Guard: don't load if already loading or on last page
        if (state.isLoadingMore || state.isLoading
            || state.currentPage >= state.totalPages) return

        viewModelScope.launch {
            val nextPage = state.currentPage + 1
            _uiState.update { it.copy(isLoadingMore = true) }

            getExamplesUseCase(page = nextPage).fold(
                onSuccess = { (newItems, pagination) ->
                    _uiState.update {
                        it.copy(
                            items = it.items + newItems,  // APPEND on load more
                            isLoadingMore = false,
                            currentPage = pagination.page,
                            totalPages = pagination.totalPages
                        )
                    }
                },
                onFailure = { e ->
                    _uiState.update { it.copy(isLoadingMore = false, error = e.message) }
                }
            )
        }
    }
}
```

### 7. Compose Screen — Infinite Scroll

```kotlin
@Composable
fun ExampleListScreen(viewModel: ExampleListViewModel = hiltViewModel()) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val listState = rememberLazyListState()

    // Trigger loadMore when within 3 items of the end
    val shouldLoadMore = remember {
        derivedStateOf {
            val lastVisible = listState.layoutInfo.visibleItemsInfo.lastOrNull()?.index ?: 0
            val totalItems = listState.layoutInfo.totalItemsCount
            lastVisible >= totalItems - 3 && !state.isLoading && !state.isLoadingMore
        }
    }
    LaunchedEffect(shouldLoadMore.value) {
        if (shouldLoadMore.value) viewModel.loadMore()
    }

    LazyColumn(state = listState) {
        items(state.items, key = { it.id }) { item ->
            ItemCard(item)
        }

        // Loading more spinner
        if (state.isLoadingMore) {
            item {
                Box(
                    modifier = Modifier.fillMaxWidth().padding(16.dp),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(24.dp),
                        strokeWidth = 2.dp
                    )
                }
            }
        }
    }
}
```

## Key Compose Imports for Pagination

```kotlin
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.remember
```

## Important Rules

1. **`loadItems()` REPLACES** the list (page 1). **`loadMore()` APPENDS** to the list (page 2+).
2. **Guard `loadMore()`** — check `isLoadingMore`, `isLoading`, and `currentPage >= totalPages` before firing.
3. **Threshold = 3** — trigger load-more when user is within 3 items of the end. This gives time for the API call to complete before the user reaches the last item.
4. **Filter changes reset pagination** — when a filter (status, search, warehouse) changes, call `loadItems()` which resets to page 1.
5. **ON_RESUME refresh** calls `loadItems()` (page 1), not `loadMore()`.
6. **`derivedStateOf`** is critical — without it, the LaunchedEffect would re-trigger on every scroll frame instead of only when the condition transitions.
7. **Small spinner** for loading-more (24.dp, 2.dp stroke) vs full-page spinner for initial load.

## Existing Implementations

- **Stock Levels (Phase 1):** `InventoryHomeViewModel.kt` — was the first paginated list
- **Purchase Orders:** `PurchaseOrdersViewModel.kt` + `PurchaseOrdersListScreen.kt`
- **Stock Transfers:** `StockTransfersViewModel.kt` + `StockTransfersListScreen.kt`
- **Stock Adjustments:** `StockAdjustmentsViewModel.kt` + `StockAdjustmentsListScreen.kt`
- **PHP backends:** `purchase-orders/list.php`, `inventory/transfers/list.php`, `inventory/adjustments/list.php`
