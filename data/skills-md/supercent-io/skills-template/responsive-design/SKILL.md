---
name: responsive-design
description: Create responsive web designs that work across all devices and screen sizes. Use when building mobile-first layouts, implementing breakpoints, or optimizing for different viewports. Handles CSS Grid, Flexbox, media queries, viewport units, and responsive images.
tags: [responsive, mobile-first, CSS, Flexbox, Grid, media-query, viewport]
platforms: [Claude, ChatGPT, Gemini]
---

# Responsive Design


## When to use this skill

- **새 웹사이트/앱**: 모바일-데스크톱 겸용 레이아웃 설계
- **레거시 개선**: 고정 레이아웃을 반응형으로 전환
- **성능 최적화**: 디바이스별 이미지 최적화
- **다양한 화면**: 태블릿, 데스크톱, 대형 화면 지원

## Instructions

### Step 1: Mobile-First 접근

작은 화면부터 설계하고 점진적으로 확장합니다.

**예시**:
```css
/* 기본: 모바일 (320px~) */
.container {
  padding: 1rem;
  font-size: 14px;
}

.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

/* 태블릿 (768px~) */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
    font-size: 16px;
  }

  .grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
}

/* 데스크톱 (1024px~) */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 3rem;
  }

  .grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
}

/* 대형 화면 (1440px~) */
@media (min-width: 1440px) {
  .grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### Step 2: Flexbox/Grid 레이아웃

현대적인 CSS 레이아웃 시스템을 활용합니다.

**Flexbox** (1차원 레이아웃):
```css
/* 네비게이션 바 */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

/* 카드 리스트 */
.card-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (min-width: 768px) {
  .card-list {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .card {
    flex: 1 1 calc(50% - 0.5rem);  /* 2 columns */
  }
}

@media (min-width: 1024px) {
  .card {
    flex: 1 1 calc(33.333% - 0.667rem);  /* 3 columns */
  }
}
```

**CSS Grid** (2차원 레이아웃):
```css
/* 대시보드 레이아웃 */
.dashboard {
  display: grid;
  grid-template-areas:
    "header"
    "sidebar"
    "main"
    "footer";
  gap: 1rem;
}

@media (min-width: 768px) {
  .dashboard {
    grid-template-areas:
      "header header"
      "sidebar main"
      "footer footer";
    grid-template-columns: 250px 1fr;
  }
}

@media (min-width: 1024px) {
  .dashboard {
    grid-template-columns: 300px 1fr;
  }
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

### Step 3: 반응형 이미지

디바이스에 맞는 이미지를 제공합니다.

**srcset 사용**:
```html
<img
  src="image-800.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w,
    image-1600.jpg 1600w
  "
  sizes="
    (max-width: 600px) 100vw,
    (max-width: 900px) 50vw,
    33vw
  "
  alt="Responsive image"
/>
```

**picture 요소** (Art Direction):
```html
<picture>
  <!-- 모바일: 세로 이미지 -->
  <source media="(max-width: 767px)" srcset="portrait.jpg">

  <!-- 태블릿: 정사각형 이미지 -->
  <source media="(max-width: 1023px)" srcset="square.jpg">

  <!-- 데스크톱: 가로 이미지 -->
  <img src="landscape.jpg" alt="Art direction example">
</picture>
```

**CSS 배경 이미지**:
```css
.hero {
  background-image: url('hero-mobile.jpg');
}

@media (min-width: 768px) {
  .hero {
    background-image: url('hero-tablet.jpg');
  }
}

@media (min-width: 1024px) {
  .hero {
    background-image: url('hero-desktop.jpg');
  }
}

/* 또는 image-set() 사용 */
.hero {
  background-image: image-set(
    url('hero-1x.jpg') 1x,
    url('hero-2x.jpg') 2x
  );
}
```

### Step 4: 반응형 타이포그래피

화면 크기에 따라 텍스트 크기를 조정합니다.

**clamp() 함수** (유동적 크기):
```css
:root {
  /* min, preferred, max */
  --font-size-body: clamp(14px, 2.5vw, 18px);
  --font-size-h1: clamp(24px, 5vw, 48px);
  --font-size-h2: clamp(20px, 4vw, 36px);
}

body {
  font-size: var(--font-size-body);
}

h1 {
  font-size: var(--font-size-h1);
  line-height: 1.2;
}

h2 {
  font-size: var(--font-size-h2);
  line-height: 1.3;
}
```

**미디어 쿼리 방식**:
```css
body {
  font-size: 14px;
  line-height: 1.6;
}

@media (min-width: 768px) {
  body { font-size: 16px; }
}

@media (min-width: 1024px) {
  body { font-size: 18px; }
}
```

### Step 5: Container Queries (신기능)

부모 컨테이너 크기에 따라 스타일 적용합니다.

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

.card {
  padding: 1rem;
}

.card h2 {
  font-size: 1.2rem;
}

/* 컨테이너가 400px 이상일 때 */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
    padding: 1.5rem;
  }

  .card h2 {
    font-size: 1.5rem;
  }
}

/* 컨테이너가 600px 이상일 때 */
@container card (min-width: 600px) {
  .card {
    grid-template-columns: 300px 1fr;
    padding: 2rem;
  }
}
```

## Output format

### 표준 브레이크포인트

```css
/* Mobile (default): 320px ~ 767px */
/* Tablet: 768px ~ 1023px */
/* Desktop: 1024px ~ 1439px */
/* Large: 1440px+ */

:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}

/* 사용 예시 */
@media (min-width: 768px) { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
```

## Constraints

### 필수 규칙 (MUST)

1. **Viewport 메타태그**: HTML에 반드시 포함
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   ```

2. **Mobile-First**: 모바일 기본, min-width 미디어 쿼리 사용
   - ✅ `@media (min-width: 768px)`
   - ❌ `@media (max-width: 767px)` (Desktop-first)

3. **상대 단위**: px 대신 rem, em, %, vw/vh 사용
   - font-size: rem
   - padding/margin: rem 또는 em
   - width: % 또는 vw

### 금지 사항 (MUST NOT)

1. **고정 너비 금지**: `width: 1200px` 지양
   - `max-width: 1200px` 사용

2. **중복 코드**: 모든 브레이크포인트에 같은 스타일 반복 금지
   - 공통 스타일은 기본으로, 차이만 미디어 쿼리에

## Examples

### 예시 1: 반응형 네비게이션

```tsx
function ResponsiveNav() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="navbar">
      {/* 로고 */}
      <a href="/" className="logo">MyApp</a>

      {/* 햄버거 버튼 (모바일) */}
      <button
        className="menu-toggle"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle menu"
        aria-expanded={isOpen}
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      {/* 네비게이션 링크 */}
      <ul className={`nav-links ${isOpen ? 'active' : ''}`}>
        <li><a href="/about">About</a></li>
        <li><a href="/services">Services</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
  );
}
```

```css
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}

/* 햄버거 버튼 (모바일만) */
.menu-toggle {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-links {
  display: none;
  position: absolute;
  top: 60px;
  left: 0;
  right: 0;
  background: white;
  flex-direction: column;
}

.nav-links.active {
  display: flex;
}

/* 태블릿 이상: 햄버거 숨기고 항상 표시 */
@media (min-width: 768px) {
  .menu-toggle {
    display: none;
  }

  .nav-links {
    display: flex;
    position: static;
    flex-direction: row;
    gap: 2rem;
  }
}
```

### 예시 2: 반응형 그리드 카드

```tsx
function ProductGrid({ products }) {
  return (
    <div className="product-grid">
      {products.map(product => (
        <div key={product.id} className="product-card">
          <img src={product.image} alt={product.name} />
          <h3>{product.name}</h3>
          <p className="price">${product.price}</p>
          <button>Add to Cart</button>
        </div>
      ))}
    </div>
  );
}
```

```css
.product-grid {
  display: grid;
  grid-template-columns: 1fr;  /* 모바일: 1 column */
  gap: 1rem;
  padding: 1rem;
}

@media (min-width: 640px) {
  .product-grid {
    grid-template-columns: repeat(2, 1fr);  /* 2 columns */
  }
}

@media (min-width: 1024px) {
  .product-grid {
    grid-template-columns: repeat(3, 1fr);  /* 3 columns */
    gap: 1.5rem;
  }
}

@media (min-width: 1440px) {
  .product-grid {
    grid-template-columns: repeat(4, 1fr);  /* 4 columns */
    gap: 2rem;
  }
}

.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
}

.product-card img {
  width: 100%;
  height: auto;
  aspect-ratio: 1 / 1;
  object-fit: cover;
}
```

## Best practices

1. **컨테이너 쿼리 우선**: 가능하면 미디어 쿼리 대신 컨테이너 쿼리
2. **Flexbox vs Grid**: 1차원은 Flexbox, 2차원은 Grid
3. **성능**: 이미지 lazy loading, WebP 포맷 사용
4. **테스트**: Chrome DevTools Device Mode, BrowserStack

## References

- [MDN Responsive Design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [CSS Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Container_Queries)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 관련 스킬
- [ui-component-patterns](../ui-component-patterns/SKILL.md): 반응형 컴포넌트
- [web-accessibility](../web-accessibility/SKILL.md): 접근성과 함께 고려

### 태그
`#responsive` `#mobile-first` `#CSS` `#Flexbox` `#Grid` `#media-query` `#frontend`