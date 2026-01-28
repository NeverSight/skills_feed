---
name: wide-events
description: Conceptual guide to wide events (canonical log lines) for observability. Use when thinking about instrumentation strategy, span annotations, or designing what context to capture.
---

<wide-events>

<philosophy>
traditional := many(log-lines) → grep(services) → hope
wide        := one(event) → query(structured) → answer

optimize(querying) ∧ ¬optimize(writing)
</philosophy>

<current-practice>
implementation := OTel spans + annotations
wide-events    := mental-model for annotation strategy

annotate(span, context) where context = {
  business ∪ user ∪ technical ∪ outcome
}
</current-practice>

<dimensionality>
wide-event.fields := {
  identity:    {traceId, spanId, service, operation}
  user:        {userId, accountTier, accountAge, lifetimeValue}
  business:    {featureFlags, experimentGroup, cartValue}
  performance: {durationMs, dbQueryCount, cacheHitRate, retryCount}
  outcome:     {success, errorCode, httpStatus}
}

high-dimensionality → better-queryability
high-cardinality(userId) → acceptable
</dimensionality>

<anti-patterns>
scattered-logs     := console.log("step1") >> console.log("step2") >> ...
low-dimensionality := span.set("success", true) ∧ |fields| < 5
technical-only     := {http.status, db.queries} ∧ ¬{user, business}
</anti-patterns>

<correct-pattern>
span.setAttributes({
  "request.operation", "user.id", "user.tier",
  "cart.items", "cart.value", "feature.*",
  "db.query_count", "cache.hit_rate",
  "request.success"
})

∀ span → attach(identity ∪ user ∪ business ∪ performance ∪ outcome)
</correct-pattern>

<tail-sampling>
retain(100%) := errors ∨ slow(>p99) ∨ vip
retain(1-5%) := success ∧ fast
</tail-sampling>

<queryability-test>
before(instrument) → verify(answerable({
  "failures where tier=premium ∧ feature.new_flow=true"
  "p99(latency) group by tier"
  "errors group by featureFlags"
  "full context for user X incident"
}))

¬queryable → ¬enough-context
</queryability-test>

<terminology>
cardinality    := |unique values| (userId=high, httpMethod=low)
dimensionality := |fields per event| (more → better)
wide-event     := canonical-log-line := one comprehensive record
</terminology>

<when-to-apply>
deciding(span-annotations)
reviewing(instrumentation-coverage)
debugging(incidents) → "what context was missing?"
planning(new-service-observability)
choosing(fields-to-index)
</when-to-apply>

</wide-events>

Reference: See `Article.md` for full article by Boris Tane (loggingsucks.com)
