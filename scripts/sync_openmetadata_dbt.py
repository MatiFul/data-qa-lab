"""Sincroniza artefactos dbt del lab con OpenMetadata sin guardar el JWT en Git."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACTS_DIR = PROJECT_ROOT / "reports" / "dbt" / "target"
CONTAINER_WORKDIR = "/tmp/data-qa-dbt-sync"
REQUIRED_ARTIFACTS = ("manifest.json", "catalog.json", "run_results.json")


def run(command: list[str], *, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=False,
        text=True,
        capture_output=capture_output,
    )


def require_success(result: subprocess.CompletedProcess[str], message: str) -> None:
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(f"{message}{': ' + detail if detail else ''}")


def validate_artifacts(artifacts_dir: Path) -> None:
    missing = [name for name in REQUIRED_ARTIFACTS if not (artifacts_dir / name).is_file()]
    if missing:
        raise RuntimeError(
            "Faltan artefactos dbt: "
            + ", ".join(missing)
            + ". Ejecutá primero los comandos documentados en GUIA_OPERATIVA.md."
        )

    for name in REQUIRED_ARTIFACTS:
        with (artifacts_dir / name).open(encoding="utf-8") as artifact:
            json.load(artifact)


def build_config_code(service_name: str) -> str:
    """Código efímero ejecutado dentro del contenedor de ingestión."""
    return f"""
import glob
import json
from pathlib import Path

service_name = {service_name!r}
metadata_pipeline = None
for config_path in glob.glob('/opt/airflow/dag_generated_configs/*.json'):
    with open(config_path, encoding='utf-8') as config_file:
        candidate = json.load(config_file)
    service = candidate.get('service') or {{}}
    if (
        candidate.get('pipelineType') == 'metadata'
        and service.get('fullyQualifiedName') == service_name
    ):
        metadata_pipeline = candidate
        break

if metadata_pipeline is None:
    raise SystemExit(
        f'No existe una ingesta metadata activa para el servicio {{service_name}}. '
        'Creala primero desde OpenMetadata.'
    )

workflow = {{
    'source': {{
        'type': 'dbt',
        'serviceName': service_name,
        'sourceConfig': {{
            'config': {{
                'type': 'DBT',
                'dbtConfigSource': {{
                    'dbtConfigType': 'local',
                    'dbtManifestFilePath': '{CONTAINER_WORKDIR}/manifest.json',
                    'dbtCatalogFilePath': '{CONTAINER_WORKDIR}/catalog.json',
                    'dbtRunResultsFilePath': '{CONTAINER_WORKDIR}/run_results.json',
                }},
                'dbtUpdateDescriptions': True,
                'overrideLineage': False,
            }}
        }},
    }},
    'sink': {{'type': 'metadata-rest', 'config': {{}}}},
    'workflowConfig': {{
        'loggerLevel': 'INFO',
        'openMetadataServerConfig': metadata_pipeline['openMetadataServerConnection'],
    }},
}}

Path('{CONTAINER_WORKDIR}/workflow.json').write_text(
    json.dumps(workflow), encoding='utf-8'
)
print('Configuración efímera creada con la credencial segura ya administrada por OpenMetadata.')
"""


def build_column_lineage_code(service_name: str) -> str:
    """Agrega el linaje de columnas crítico que el parser dbt no siempre infiere."""
    return f"""
import json

from metadata.generated.schema.api.lineage.addLineage import AddLineageRequest
from metadata.generated.schema.entity.data.table import Table
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import OpenMetadataConnection
from metadata.generated.schema.type.entityLineage import ColumnLineage, EntitiesEdge, LineageDetails
from metadata.generated.schema.type.entityReference import EntityReference
from metadata.ingestion.ometa.ometa_api import OpenMetadata

with open('{CONTAINER_WORKDIR}/workflow.json', encoding='utf-8') as workflow_file:
    server_config = json.load(workflow_file)['workflowConfig']['openMetadataServerConfig']

metadata = OpenMetadata(OpenMetadataConnection.model_validate(server_config))
prefix = {service_name!r} + '.qa_lab.'

edges = [
    {{
        'from': prefix + 'dbt_intermediate.int_valid_transactions',
        'to': prefix + 'dbt_marts.fct_transaction_quality',
        'sql': 'fct_transaction_quality: selección de transacciones válidas y cálculo de flags QA.',
        'mappings': [
            (['transaction_id'], 'transaction_id'),
            (['account_id'], 'account_id'),
            (['channel_id'], 'channel_id'),
            (['status_id'], 'status_id'),
            (['branch_id'], 'branch_id'),
            (['transaction_amount'], 'transaction_amount'),
            (['transaction_amount'], 'amount_difference'),
            (['transaction_amount'], 'inconsistent_amount_flag'),
            (['transaction_at'], 'transaction_at'),
            (['transaction_date'], 'transaction_date'),
            (['processed_date'], 'processed_date'),
        ],
    }},
    {{
        'from': prefix + 'dbt_intermediate.int_transaction_item_totals',
        'to': prefix + 'dbt_marts.fct_transaction_quality',
        'sql': 'fct_transaction_quality: unión de totales de ítems y cálculo de diferencias y flags QA.',
        'mappings': [
            (['calculated_item_amount'], 'calculated_item_amount'),
            (['calculated_item_amount'], 'amount_difference'),
            (['calculated_item_amount'], 'inconsistent_amount_flag'),
            (['item_count'], 'item_count'),
            (['item_count'], 'has_no_items_flag'),
        ],
    }},
    {{
        'from': prefix + 'dbt_marts.fct_transaction_quality',
        'to': prefix + 'dbt_marts.mart_daily_quality',
        'sql': 'mart_daily_quality: agregación de métricas y flags por transaction_date.',
        'mappings': [
            (['transaction_date'], 'transaction_date'),
            (['transaction_id'], 'transaction_count'),
            (['transaction_amount'], 'total_transaction_amount'),
            (['calculated_item_amount'], 'total_calculated_item_amount'),
            (['has_no_items_flag'], 'transactions_without_items'),
            (['inconsistent_amount_flag'], 'inconsistent_transactions'),
            (['inconsistent_amount_flag'], 'inconsistency_rate'),
        ],
    }},
]

column_mapping_count = 0
for edge in edges:
    source = metadata.get_by_name(entity=Table, fqn=edge['from'])
    target = metadata.get_by_name(entity=Table, fqn=edge['to'])
    if source is None or target is None:
        raise SystemExit(f"No se encontró el par de tablas {{edge['from']}} -> {{edge['to']}}")

    columns_lineage = []
    for source_columns, target_column in edge['mappings']:
        columns_lineage.append(
            ColumnLineage(
                fromColumns=[edge['from'] + '.' + name for name in source_columns],
                toColumn=edge['to'] + '.' + target_column,
            )
        )
    metadata.add_lineage(
        data=AddLineageRequest(
            edge=EntitiesEdge(
                fromEntity=EntityReference(id=source.id, type='table'),
                toEntity=EntityReference(id=target.id, type='table'),
                description='Linaje crítico de columnas del Data QA Lab.',
                lineageDetails=LineageDetails(
                    sqlQuery=edge['sql'], columnsLineage=columns_lineage
                ),
            )
        )
    )
    column_mapping_count += len(columns_lineage)

lineage = metadata.get_lineage_by_name(
    entity=Table,
    fqn=prefix + 'dbt_marts.fct_transaction_quality',
    up_depth=1,
    down_depth=1,
)
lineage_edges = lineage.get('upstreamEdges', []) + lineage.get('downstreamEdges', [])
visible_mappings = sum(
    len((edge.get('lineageDetails') or {{}}).get('columnsLineage') or [])
    for edge in lineage_edges
)
if len(lineage_edges) != len(edges) or visible_mappings != column_mapping_count:
    raise SystemExit(
        f'Validación de linaje incompleta: {{len(lineage_edges)}} aristas y '
        f'{{visible_mappings}} mapeos visibles.'
    )

print(f'Linaje crítico validado: {{len(edges)}} aristas y {{column_mapping_count}} mapeos de columnas.')
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Publica descripciones, tests y lineage dbt en OpenMetadata."
    )
    parser.add_argument("--service-name", default="postgres_lab")
    parser.add_argument("--container", default="openmetadata_ingestion")
    parser.add_argument(
        "--artifacts-dir", type=Path, default=DEFAULT_ARTIFACTS_DIR
    )
    args = parser.parse_args()

    artifacts_dir = args.artifacts_dir.resolve()

    try:
        validate_artifacts(artifacts_dir)

        inspect = run(
            [
                "docker",
                "inspect",
                "--format",
                "{{.State.Running}}",
                args.container,
            ],
            capture_output=True,
        )
        require_success(inspect, f"No se pudo inspeccionar {args.container}")
        if inspect.stdout.strip().lower() != "true":
            raise RuntimeError(f"El contenedor {args.container} no está en ejecución.")

        require_success(
            run(["docker", "exec", args.container, "mkdir", "-p", CONTAINER_WORKDIR]),
            "No se pudo preparar el directorio efímero",
        )

        for name in REQUIRED_ARTIFACTS:
            require_success(
                run(
                    [
                        "docker",
                        "cp",
                        str(artifacts_dir / name),
                        f"{args.container}:{CONTAINER_WORKDIR}/{name}",
                    ]
                ),
                f"No se pudo copiar {name}",
            )

        require_success(
            run(
                [
                    "docker",
                    "exec",
                    args.container,
                    "python",
                    "-c",
                    build_config_code(args.service_name),
                ]
            ),
            "No se pudo construir el workflow dbt",
        )

        result = run(
            [
                "docker",
                "exec",
                args.container,
                "metadata",
                "ingest",
                "-c",
                f"{CONTAINER_WORKDIR}/workflow.json",
            ]
        )
        require_success(result, "La ingesta dbt de OpenMetadata falló")

        require_success(
            run(
                [
                    "docker",
                    "exec",
                    args.container,
                    "python",
                    "-c",
                    build_column_lineage_code(args.service_name),
                ]
            ),
            "No se pudo completar el linaje crítico por columnas",
        )
        print("Sincronización dbt -> OpenMetadata completada.")
        return 0
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    finally:
        run(
            [
                "docker",
                "exec",
                args.container,
                "rm",
                "-rf",
                CONTAINER_WORKDIR,
            ],
            capture_output=True,
        )


if __name__ == "__main__":
    raise SystemExit(main())
