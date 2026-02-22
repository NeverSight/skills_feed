---
name: "idempiere-plugin-development"
description: "Desarrollo de plugins/modulos para iDempiere (OSGi bundles) con Maven/Tycho: crear un nuevo plugin, extender iDempiere sin tocar core (procesos, callouts, model validators, event handlers, formularios ZK, integraciones), empaquetar y entregar (feature/update-site). Usar cuando el trabajo implica agregar o modificar funcionalidad via plugin."
---

# iDempiere Plugin Development (OSGi)

## Objetivo

Implementar cambios en iDempiere con un plugin desacoplado y mantenible:
- bundle OSGi + build Tycho/Maven consistente,
- extension points correctos,
- instalacion reproducible (feature/p2 o mecanismo del proyecto).

## Entorno (si no compila o hay que reproducir)

- Confirmar version iDempiere (branch/tag) y Java target.
- Verificar herramientas: `java -version`, `mvn -v`, `git --version`.
- Confirmar DB dev (ideal: docker compose) y credenciales.
- Hacer build sin IDE primero y capturar el primer error real.

## Antes de tocar codigo

1) Confirmar el tipo de extension
   - Proceso/Report, Callout, ModelValidator, EventHandler, Form/ZUL, REST/OSGi service, etc.
2) Confirmar restriccion clave
   - Evitar cambios en core (salvo necesidad justificada y aprobada).
3) Confirmar alcance de DB
   - Si hay cambios de diccionario/DB, coordinar con `$idempiere-db`.
   - Si hay UI ZK o themes, coordinar con `$idempiere-zk`.

## Puntos de extension (referencia rapida)

- **Proceso / Reporte**: implementar clase (ej: `SvrProcess`) y registrar en `AD_Process` (Classname) + menu/role donde aplique.
- **Callout**: implementar callout y referenciarlo desde la columna/campo correspondiente (evitar logica pesada y efectos colaterales).
- **ModelValidator**: implementar validador y registrarlo como servicio OSGi (preferir patrones ya usados en el repo).
- **Event handler**: suscribirse a eventos OSGi/iDempiere segun el mecanismo del proyecto (copiar un handler existente como base).
- **Form / ZUL**: empaquetar recursos (ZUL/CSS) en el plugin y registrar el acceso (menu/forma) segun convencion del repo.

## Workflow recomendado

1) Ubicar el parent/releng del repo
   - Detectar donde se agregan modulos (parent `pom.xml`, `releng`, `features`, `update-site`).
2) Crear/ajustar el bundle
   - Nombre y paquetes sin colisiones (evitar split packages).
   - Export/Import packages segun necesidad (no exportar por default).
   - Preferir Declarative Services (DS) cuando aplique.
3) Implementar la extension
   - Registrar lo necesario (plugin.xml, DS, o configuracion en AD_* segun el caso).
   - Mantener codigo testeable y sin dependencias innecesarias.
4) Integrar al empaquetado
   - Agregar a feature/update-site si el repo lo usa.
   - Versionar y anotar cambios (semver cuando corresponda).
5) Verificar runtime
   - Confirmar que el bundle queda ACTIVE.
   - Probar el flujo funcional end-to-end en UI.

## Checklist rapido

- [ ] No se toco core (o esta justificado).
- [ ] Bundle compila y resuelve dependencias en OSGi.
- [ ] Extension registrada y ejecuta en runtime.
- [ ] Instrucciones de instalacion/upgrade documentadas.
