
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'high_conf_small': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='SMALL: Path to the high confidence BED files.',
    ),
    'truth_small': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='SMALL: Path to the golden set VCF files.',
    ),
    'high_conf_sv': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='SV: Path to the high confidence BED files.',
    ),
    'truth_sv': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description=' SV: Path to the golden set VCF files.',
    ),
    'high_conf_cnv': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='CNV: Path to the high confidence BED files.',
    ),
    'truth_cnv': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='CNV: Path to the golden set VCF files.',
    ),
    'svync_yaml': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Custom configuration files for Svync standardization',
    ),
    'analysis': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='',
    ),
    'preprocess': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='',
    ),
    'sv_standardization': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='',
    ),
    'similarity': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='',
    ),
    'method': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='',
    ),
    'min_sv_size': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Maximum SV size of variants to benchmark, 0 to disable , Default:50',
    ),
    'max_sv_size': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Maximum SV size of variants to benchmark, -1 to disable , Default:-1',
    ),
    'min_allele_freq': NextflowParameter(
        type=typing.Optional[float],
        default=None,
        section_title=None,
        description='Minimum Alele Frequency of variants to benchmark, Use -1 to disable , Default:-1',
    ),
    'min_num_reads': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Minimum number of read supporting variants to benchmark, Use, -1 to disable , Default:-1',
    ),
    'pctsize': NextflowParameter(
        type=typing.Optional[float],
        default=None,
        section_title=None,
        description='TRUVARI PARAMETER. Ratio of min(base_size, comp_size)/max(base_size, comp_size)',
    ),
    'refdist': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description="TRUVARI PARAMETER. Maximum distance comparison calls must be within from base call's start/end",
    ),
    'chunksize': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='TRUVARI PARAMETER.',
    ),
    'pctseq': NextflowParameter(
        type=typing.Optional[float],
        default=None,
        section_title=None,
        description='TRUVARI PARAMETER. Edit distance ratio between the REF/ALT haplotype sequences of base and comparison call.',
    ),
    'pctovl': NextflowParameter(
        type=typing.Optional[float],
        default=None,
        section_title=None,
        description="TRUVARI PARAMETER. Ratio of two calls' (overlapping bases)/(longest span).",
    ),
    'pick': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='TRUVARI PARAMETER.How many matches a variant is allowed to participate in is controlled: single,ac,multi',
    ),
    'normshift': NextflowParameter(
        type=typing.Optional[float],
        default=None,
        section_title=None,
        description='SVANALYZER PARAMETER. Disallow matches if alignments between alternate alleles have normalized shift greater than normshift (default 0.2) ',
    ),
    'normdist': NextflowParameter(
        type=typing.Optional[float],
        default=None,
        section_title=None,
        description='SVANALYZER PARAMETER. Disallow matches if alternate alleles have normalized edit distance greater than normdist (default 0.2)',
    ),
    'normsizediff': NextflowParameter(
        type=typing.Optional[float],
        default=None,
        section_title=None,
        description='SVANALYZER PARAMETER. Disallow matches if alternate alleles have normalized size difference greater than normsizediff (default 0.2) ',
    ),
    'maxdist': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='SVANALYZER PARAMETER. Disallow matches if positions of two variants are more than maxdist bases from each other (default 100,000).',
    ),
    'variant_filtering': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Use either exclude or include to enable variant filtering using bcftools expressions, Default:null',
    ),
    'expression': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Use bcftools expressions here https://samtools.github.io/bcftools/bcftools.html#expressions. This must be coupled with variant_expression, Default:null',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'genome': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Reference genome options',
        description='Name of iGenomes reference.',
    ),
    'fasta': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title=None,
        description='Path to FASTA genome file.',
    ),
    'fai': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title=None,
        description='Path to FAI genome file.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

