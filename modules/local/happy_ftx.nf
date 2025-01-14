process HAPPY_FTX {
    tag "$meta.id"
    label 'process_medium'

    // WARN: Version information not provided by tool on CLI. Please update version string below when bumping container versions.
    conda "${moduleDir}/environment.yml"
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/hap.py:0.3.14--py27h5c5a3ab_0':
        'biocontainers/hap.py:0.3.14--py27h5c5a3ab_0' }"

    input:
    tuple val(meta), path(input_vcf), path(regions_bed), path(targets_bed)
    tuple val(meta2), path(fasta)
    tuple val(meta3), path(fasta_fai)
    tuple val(meta4), path(bams)

    output:
    tuple val(meta), path('*.csv')       , emit: features
    path "versions.yml"                  , emit: versions

    when:
    task.ext.when == null || task.ext.when

    script:
    def args = task.ext.args ?: ''
    def prefix = task.ext.prefix ?: "${meta.id}"
    def regions = regions_bed ? "-R ${regions_bed}" : ""
    def targets = targets_bed ? "-T ${targets_bed}" : ""
    def bams    = bams ? "--bam ${bams}" : ""
    def features = meta.id.contains("mutect2") ? "generic" :
                    meta.id.contains("strelka") ? "hcc.strelka.${meta.vartype}" :
                    meta.id.contains("varscan") ? "hcc.varsacan2.${meta.vartype}" :
                    meta.id.contains("pisces") ? "hcc.pisces.${meta.vartype}" :
                    "generic"

    def VERSION = '0.3.14' // WARN: Version information not provided by tool on CLI. Please update this string when bumping container versions.
    """
    ftx.py \\
        --feature-table $features \\
        ${args} \\
        --reference ${fasta} \\
        ${regions} \\
        ${targets} \\
        $bams \\
        -o ${prefix}.${meta.vartype} \\
        ${input_vcf}

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        hap.py: $VERSION
    END_VERSIONS
    """

    stub:
    def args = task.ext.args ?: ''
    def VERSION = '0.3.14' // WARN: Version information not provided by tool on CLI. Please update this string when bumping container versions.
    """
    touch ${prefix}.csv

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        hap.py: $VERSION
    END_VERSIONS
    """
}
