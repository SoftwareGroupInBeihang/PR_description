# import packages
library(lmerTest)
library(MuMIn)
library(car)

# read data
setwd("H:\\data")
d <- read.csv("stat_data.csv")

# Regression Result for Acceptance
fm.merged <- lmer(merged ~
    edited +
    (1 | repo) +
    log2(repo_age/30 + 0.5) +
    log2(repo_commits + 0.5) +
    log2(experience + 0.5) +
    log2(open_tasks + 0.5) +
    log2(pull_lines + 0.5) +
    log2(pull_desc_len + 0.5),
    data = d)
summary(fm.merged)
r.squaredGLMM(fm.merged)
vif(fm.merged)

# Regression Result for Review Time
fm.close.time <- lmer(log2(close_time/60/60/24 + 0.5) ~
    edited +
    (1 | repo) +
    log2(repo_age/30 + 0.5) +
    log2(repo_commits + 0.5) +
    log2(experience + 0.5) +
    log2(open_tasks + 0.5) +
    log2(pull_lines + 0.5) +
    log2(pull_desc_len + 0.5),
    data = d)
summary(fm.close.time)
r.squaredGLMM(fm.close.time)
vif(fm.close.time)