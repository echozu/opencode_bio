import { existsSync, readFileSync } from "fs"
import { join } from "path"
import type { Plugin } from "@opencode-ai/plugin"

const SLURM_WRAPPERS = /\b(sbatch|srun|squeue|scancel|sinfo|sacct|salloc)\b/
const INFO_ONLY = /\s+(--version|--help|-h|--check|--dry-run|--dryrun|-v)\s*$/

const EXECUTION_PATTERNS: RegExp[] = [
  // Script interpreters
  /\bpython[23]?\s+\S+\.py\b/i,
  /\bpython[23]?\s+-[cmu]\s/i,
  /\bRscript\b/i,
  /\bR\s+(--no-save|--vanilla|-e)\b/i,
  /\bperl\s+\S+\.pl\b/i,
  /\bjava\s+(-jar|-cp)\b/i,
  /\bjulia\s+\S+\.jl\b/i,
  // Direct script execution
  /\.\/([\w./-]+)\.(sh|py|R|pl|rb|jl)\b/,
  /\bbash\s+[\w./-]+\.sh\b/,
  /\bsh\s+[\w./-]+\.sh\b/,
  // Bioinformatics tools (catch-all safety net)
  /\b(fastp|fastqc|multiqc|trimmomatic|trim_galore|cutadapt)\b/i,
  /\b(STAR|hisat2|bowtie2|bwa\s|minimap2|salmon|kallisto)\b/,
  /\b(samtools\s+(sort|index|view|merge|markdup|mpileup))\b/i,
  /\b(megahit|metaspades|spades\.py|trinity)\b/i,
  /\b(kraken2|metaphlan|diamond\s+(blastx|blastp)|kaiju|humann|bracken)\b/i,
  /\b(prokka|prodigal|bakta|eggnog-mapper|emapper\.py|dada2)\b/i,
  /\b(cellranger|starsolo|velocyto|alevin-fry)\b/i,
  /\b(gatk\s+\w+|freebayes|deepvariant|mutect2|varscan)\b/i,
  /\b(blast[npx]?|hmmer|muscle|mafft|raxml|iqtree)\b/i,
  /\b(snakemake|nextflow)\b/i,
  /\b(metabat2?|maxbin2?|concoct|checkm)\b/i,
]

export default function (ctx: any): Plugin {
  return {
    name: "hpc-safety-guard",
    "tool.execute.before": async (input, output) => {
      if (input.tool !== "bash") return
      const command: string = (output as any).args?.command ?? ""
      if (!command.trim()) return

      // Check HPC environment from project-anchor.yaml
      const cwd = process.cwd()
      const anchorPath = join(cwd, "docs", "project-anchor.yaml")
      if (!existsSync(anchorPath)) return
      const anchor = readFileSync(anchorPath, "utf-8")
      if (!anchor.includes("hpc_environment: true")) return

      // Layer 1: Already wrapped by Slurm → allow
      if (SLURM_WRAPPERS.test(command)) return
      // Info queries → allow
      if (INFO_ONLY.test(command)) return
      // Layer 2: Detect execution patterns
      const isExecution = EXECUTION_PATTERNS.some((p) => p.test(command))
      if (!isExecution) return

      // ⛔ Block
      const short =
        command.length > 100 ? command.substring(0, 100) + "..." : command
      ;(output as any).args.command = [
        `echo "⛔ HPC SAFETY GUARD: Blocked direct execution on login node."`,
        `echo "Blocked: ${short.replace(/"/g, '\\"')}"`,
        `echo "ALL code execution must be submitted via sbatch."`,
        `echo "1. Write your script to a file"`,
        `echo "2. Create sbatch job script with SLURM headers"`,
        `echo "3. Submit: sbatch your_job.sh"`,
        `echo "Load 'slurm-execution' skill for templates."`,
        `exit 1`,
      ].join(" && ")
    },
  }
}
