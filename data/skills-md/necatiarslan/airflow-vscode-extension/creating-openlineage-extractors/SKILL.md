---
name: creating-openlineage-extractors
description: Create custom OpenLineage extractors for Airflow operators. Use when the user needs lineage from unsupported or third-party operators, wants column-level lineage, or needs complex extraction logic beyond what inlets/outlets provide.
---

# Creating OpenLineage Extractors

This skill guides you through creating custom OpenLineage extractors to capture lineage from Airflow operators that do not have built-in support.

## When to Use Each Approach

| Scenario | Approach |
| --- | --- |
| Operator you own or maintain | OpenLineage Methods (recommended) |
| Third-party operator you cannot modify | Custom Extractor |
| Need column-level lineage | OpenLineage Methods or Custom Extractor |
| Complex extraction logic | OpenLineage Methods or Custom Extractor |
| Simple table-level lineage | Inlets/Outlets (simplest, lowest priority) |

## Approach 1: OpenLineage Methods (recommended)

```python
from airflow.models import BaseOperator

class MyCustomOperator(BaseOperator):
    def __init__(self, source_table: str, target_table: str, **kwargs):
        super().__init__(**kwargs)
        self.source_table = source_table
        self.target_table = target_table
        self._rows_processed = 0

    def execute(self, context):
        self._rows_processed = self._process_data()
        return self._rows_processed

    def get_openlineage_facets_on_start(self):
        from openlineage.client.event_v2 import Dataset
        from airflow.providers.openlineage.extractors import OperatorLineage

        return OperatorLineage(
            inputs=[Dataset(namespace="postgres://db", name=self.source_table)],
            outputs=[Dataset(namespace="postgres://db", name=self.target_table)],
        )

    def get_openlineage_facets_on_complete(self, task_instance):
        from openlineage.client.event_v2 import Dataset
        from openlineage.client.facet_v2 import output_statistics_output_dataset
        from airflow.providers.openlineage.extractors import OperatorLineage

        return OperatorLineage(
            inputs=[Dataset(namespace="postgres://db", name=self.source_table)],
            outputs=[
                Dataset(
                    namespace="postgres://db",
                    name=self.target_table,
                    facets={
                        "outputStatistics": output_statistics_output_dataset.OutputStatisticsOutputDatasetFacet(
                            rowCount=self._rows_processed
                        )
                    },
                )
            ],
        )
```

## Approach 2: Custom Extractors

```python
from airflow.providers.openlineage.extractors.base import BaseExtractor, OperatorLineage
from openlineage.client.event_v2 import Dataset

class MyOperatorExtractor(BaseExtractor):
    @classmethod
    def get_operator_classnames(cls) -> list[str]:
        return ["MyCustomOperator"]

    def _execute_extraction(self) -> OperatorLineage | None:
        source_table = self.operator.source_table
        target_table = self.operator.target_table

        return OperatorLineage(
            inputs=[Dataset(namespace="postgres://mydb:5432", name=f"public.{source_table}")],
            outputs=[Dataset(namespace="postgres://mydb:5432", name=f"public.{target_table}")],
        )

    def extract_on_complete(self, task_instance) -> OperatorLineage | None:
        return None
```

## Registering Extractors

Configuration file:

```ini
[openlineage]
extractors = mypackage.extractors.MyOperatorExtractor;mypackage.extractors.AnotherExtractor
```

Environment variable:

```bash
AIRFLOW__OPENLINEAGE__EXTRACTORS='mypackage.extractors.MyOperatorExtractor;mypackage.extractors.AnotherExtractor'
```
