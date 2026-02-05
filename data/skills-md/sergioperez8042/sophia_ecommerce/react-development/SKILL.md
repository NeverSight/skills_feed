---
name: react-development
description: Habilidad para desarrollar aplicaciones web modernas usando React, aplicando buenas prácticas, patrones de diseño, testing, TypeScript y frameworks del ecosistema.
capabilities:
  - Crear interfaces de usuario dinámicas con componentes reutilizables usando JSX.
  - Gestionar estado y ciclo de vida con Hooks (`useState`, `useEffect`, Hooks personalizados).
  - Implementar enrutamiento con React Router y gestión de estado con Context API o Redux.
  - Desarrollar aplicaciones con frameworks basados en React como Next.js (SSR/SSG).
  - Escribir pruebas unitarias y de integración con Jest y React Testing Library.
  - Aplicar linters y formateadores (ESLint, Prettier) para mantener calidad de código.
  - Usar TypeScript para tipado estático y mayor mantenibilidad.
  - Integrar CI/CD (GitHub Actions) para ejecutar tests y linters automáticamente.
examples:
  - |
    ```jsx
    import { useState } from 'react';

    function UserInfo({ userName }) {
      const [count, setCount] = useState(0);

      return (
        <div>
          <h2>Nombre: {userName}</h2>
          <p>Has hecho clic {count} veces.</p>
          <button onClick={() => setCount(count + 1)}>
            Haz clic
          </button>
        </div>
      );
    }

    export default function App() {
      return (
        <>
          <UserInfo userName="María" />
          <UserInfo userName="Jorge" />
        </>
      );
    }
    ```
references:
  - https://react.dev
  - https://react.dev/reference/react
  - https://reactrouter.com
  - https://redux.js.org
  - https://nextjs.org
  - https://jestjs.io
  - https://testing-library.com/docs/react-testing-library/intro
  - https://www.typescriptlang.org
  - https://tailwindcss.com
  - https://chakra-ui.com
---

## Descripción técnica

React es una biblioteca de JavaScript basada en componentes para construir interfaces de usuario. El enfoque moderno prioriza **componentes funcionales** y **Hooks**, evitando clases.

### Buenas prácticas clave

- **Estructura de carpetas**
src/
components/
hooks/
pages/
services/
tests/

- **Convenciones**
- Componentes: `PascalCase`
- Hooks personalizados: `useSomething`
- **Gestión de estado**
- Context API para estado global simple
- Redux / Zustand para lógica compleja
- **Rendimiento**
- Code splitting con `React.lazy` y `Suspense`
- **Estilos**
- Tailwind CSS, Emotion o Styled Components
- **Testing**
- Tests de componentes con React Testing Library
- **SSR / SEO**
- Next.js para aplicaciones productivas

React se integra comúnmente con pipelines de CI/CD para asegurar calidad continua antes del despliegue.
