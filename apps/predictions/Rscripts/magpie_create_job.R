require(magpie)
require("devtools")

# arguments
args <- commandArgs(trailingOnly = TRUE)

magpie.user <- args[1]
magpie.password <- args[2]
magpie.url <- args[3]
magpie.project_id <- args[4]
magpie.model_id <- as.numeric(args[5])
df_pcr <- args[6]
df_treat <- args[7]

# login
set_url(magpie.url)
login(magpie.user, magpie.password)

############### create new job ###########################################
params = get_params(magpie.model_id)
# configure magpie config (part 2)
params["config[default.config_dataFile]"] <- df_pcr
params["config[default.config_dataFile_treat]"] <- df_treat

new_job <- create_job(magpie.project_id, params = params)
magpie.job_id <- new_job[1]
cat(magpie.job_id)