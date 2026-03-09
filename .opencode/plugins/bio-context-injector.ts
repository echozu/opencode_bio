import { readFileSync, existsSync, readdirSync } from "fs"
import { join } from "path"
import type { Plugin } from "@opencode-ai/plugin"

export default function (ctx: any): Plugin {
  return {
    name: "bio-context-injector",
    "experimental.chat.system.transform": async (input, output) => {
      const cwd = process.cwd()
      const anchorPath = join(cwd, "docs", "project-anchor.yaml")
      if (!existsSync(anchorPath)) return

      const anchor = readFileSync(anchorPath, "utf-8")
      const mode =
        anchor.match(/execution_mode:\s*(\S+)/)?.[1] ??
        anchor.match(/mode:\s*(\S+)/)?.[1] ??
        "interactive"
      const hpc =
        anchor.match(/hpc_environment:\s*(\S+)/)?.[1] ??
        anchor.match(/hpc:\s*(\S+)/)?.[1] ??
        "false"

      // Find latest checkpoint across all domains
      let latestCheckpoint = ""
      let currentPhase = "unknown"
      try {
        const docsDir = join(cwd, "docs")
        if (existsSync(docsDir)) {
          const domains = readdirSync(docsDir, { withFileTypes: true }).filter(
            (d) => d.isDirectory()
          )
          for (const domain of domains) {
            const cpDir = join(docsDir, domain.name, "checkpoints")
            if (!existsSync(cpDir)) continue
            const files = readdirSync(cpDir)
              .filter((f) => f.endsWith(".yaml"))
              .sort()
            if (files.length > 0) {
              latestCheckpoint = join(
                "docs",
                domain.name,
                "checkpoints",
                files[files.length - 1]
              )
              const m = files[files.length - 1].match(/phase-(\d+)/)
              if (m) currentPhase = `phase-${m[1]}`
            }
          }
        }
      } catch {}

      const lines = [
        `<bio-analysis-context>`,
        `phase: ${currentPhase}`,
        `mode: ${mode}`,
        `hpc: ${hpc}`,
        latestCheckpoint ? `checkpoint: ${latestCheckpoint}` : null,
        hpc === "true"
          ? `IRON-LAW: ALL code execution (python, R, scripts, bio tools) → sbatch. Login node = file ops + job management ONLY.`
          : null,
        `</bio-analysis-context>`,
      ]
        .filter(Boolean)
        .join("\n")

      output.system.push(lines)
    },
  }
}
