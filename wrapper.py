import os

from snakemake.shell import shell

if globals().get("snakemake") is None:
    snakemake = None  # prevent linter problems
    raise Exception("This script was run without snakemake")

if len(snakemake.params.keys()) > 0:
    raise Exception("Keyword arguments are not allowed with this wrapper")

script = snakemake.params.pop(0)
if not os.path.exists(script):
    raise Exception("The first parameter is not a valid path to a script file")

params_context = snakemake.__dict__.copy()
args = []
for option in snakemake.params:
    if type(option) is not str:
        raise Exception(f"option {option} is not a string")

    option = option.replace("{hs:", "{")
    exec(f"arg = f'{option}'", {}, params_context)
    args.append(params_context["arg"])
args = " ".join(args)


if snakemake.log:
    log_arg = f"hydra.job_logging.handlers.file.filename={snakemake.log}"
    # args might contain flags at the end that don't like
    # options like log_arg after them
    shell(f"python {script} {log_arg} {args}")
else:
    shell(f"python {script} {args}")
