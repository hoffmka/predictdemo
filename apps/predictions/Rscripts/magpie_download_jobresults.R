require(magpie)
require("devtools")

# arguments
args <- commandArgs(trailingOnly = TRUE)

magpie.user <- args[1]
magpie.password <- args[2]
magpie.url <- args[3]
magpie.project_id <- args[4]
magpie.model_id <- as.numeric(args[5])
magpie.job_id <- args[6]
media_dir <- args[7]

# login
set_url(magpie.url)
login(magpie.user, magpie.password)

############### download job documents ###################################
results_job(project_id=magpie.project_id, job_id=magpie.job_id, folder=media_dir)
configs_job(project_id=magpie.project_id, job_id=magpie.job_id, folder=media_dir)