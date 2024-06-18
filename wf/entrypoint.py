from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], high_conf_small: typing.Optional[LatchFile], truth_small: typing.Optional[LatchFile], high_conf_sv: typing.Optional[LatchFile], truth_sv: typing.Optional[LatchFile], high_conf_cnv: typing.Optional[LatchFile], truth_cnv: typing.Optional[LatchFile], svync_yaml: typing.Optional[str], analysis: typing.Optional[str], preprocess: typing.Optional[str], sv_standardization: typing.Optional[str], similarity: typing.Optional[int], method: typing.Optional[str], min_sv_size: typing.Optional[int], max_sv_size: typing.Optional[int], min_allele_freq: typing.Optional[float], min_num_reads: typing.Optional[int], pctsize: typing.Optional[float], refdist: typing.Optional[int], chunksize: typing.Optional[int], pctseq: typing.Optional[float], pctovl: typing.Optional[float], pick: typing.Optional[str], normshift: typing.Optional[float], normdist: typing.Optional[float], normsizediff: typing.Optional[float], maxdist: typing.Optional[int], variant_filtering: typing.Optional[str], expression: typing.Optional[str], email: typing.Optional[str], multiqc_title: typing.Optional[str], genome: typing.Optional[str], fasta: LatchFile, fai: LatchFile, multiqc_methods_description: typing.Optional[str]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('high_conf_small', high_conf_small),
                *get_flag('truth_small', truth_small),
                *get_flag('high_conf_sv', high_conf_sv),
                *get_flag('truth_sv', truth_sv),
                *get_flag('high_conf_cnv', high_conf_cnv),
                *get_flag('truth_cnv', truth_cnv),
                *get_flag('svync_yaml', svync_yaml),
                *get_flag('analysis', analysis),
                *get_flag('preprocess', preprocess),
                *get_flag('sv_standardization', sv_standardization),
                *get_flag('similarity', similarity),
                *get_flag('method', method),
                *get_flag('min_sv_size', min_sv_size),
                *get_flag('max_sv_size', max_sv_size),
                *get_flag('min_allele_freq', min_allele_freq),
                *get_flag('min_num_reads', min_num_reads),
                *get_flag('pctsize', pctsize),
                *get_flag('refdist', refdist),
                *get_flag('chunksize', chunksize),
                *get_flag('pctseq', pctseq),
                *get_flag('pctovl', pctovl),
                *get_flag('pick', pick),
                *get_flag('normshift', normshift),
                *get_flag('normdist', normdist),
                *get_flag('normsizediff', normsizediff),
                *get_flag('maxdist', maxdist),
                *get_flag('variant_filtering', variant_filtering),
                *get_flag('expression', expression),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('genome', genome),
                *get_flag('fasta', fasta),
                *get_flag('fai', fai),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_variantbenchmarking", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_variantbenchmarking(input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], high_conf_small: typing.Optional[LatchFile], truth_small: typing.Optional[LatchFile], high_conf_sv: typing.Optional[LatchFile], truth_sv: typing.Optional[LatchFile], high_conf_cnv: typing.Optional[LatchFile], truth_cnv: typing.Optional[LatchFile], svync_yaml: typing.Optional[str], analysis: typing.Optional[str], preprocess: typing.Optional[str], sv_standardization: typing.Optional[str], similarity: typing.Optional[int], method: typing.Optional[str], min_sv_size: typing.Optional[int], max_sv_size: typing.Optional[int], min_allele_freq: typing.Optional[float], min_num_reads: typing.Optional[int], pctsize: typing.Optional[float], refdist: typing.Optional[int], chunksize: typing.Optional[int], pctseq: typing.Optional[float], pctovl: typing.Optional[float], pick: typing.Optional[str], normshift: typing.Optional[float], normdist: typing.Optional[float], normsizediff: typing.Optional[float], maxdist: typing.Optional[int], variant_filtering: typing.Optional[str], expression: typing.Optional[str], email: typing.Optional[str], multiqc_title: typing.Optional[str], genome: typing.Optional[str], fasta: LatchFile, fai: LatchFile, multiqc_methods_description: typing.Optional[str]) -> None:
    """
    nf-core/variantbenchmarking

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, outdir=outdir, high_conf_small=high_conf_small, truth_small=truth_small, high_conf_sv=high_conf_sv, truth_sv=truth_sv, high_conf_cnv=high_conf_cnv, truth_cnv=truth_cnv, svync_yaml=svync_yaml, analysis=analysis, preprocess=preprocess, sv_standardization=sv_standardization, similarity=similarity, method=method, min_sv_size=min_sv_size, max_sv_size=max_sv_size, min_allele_freq=min_allele_freq, min_num_reads=min_num_reads, pctsize=pctsize, refdist=refdist, chunksize=chunksize, pctseq=pctseq, pctovl=pctovl, pick=pick, normshift=normshift, normdist=normdist, normsizediff=normsizediff, maxdist=maxdist, variant_filtering=variant_filtering, expression=expression, email=email, multiqc_title=multiqc_title, genome=genome, fasta=fasta, fai=fai, multiqc_methods_description=multiqc_methods_description)

