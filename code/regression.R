library(lmerTest)
library(lme4)
library(MuMIn)

setwd("C:\\Users\\tkotkch\\Documents\\dataset")
d <- read.csv("regression_ready_data3.csv")

# Model1 for acceptance
model_acceptance <- glmer(merged ~
    edited +
    log(repo_age / 30 + 0.5) +
    log(repo_commits + 0.5) +
    log(author_experience + 0.5) +
    log(open_tasks + 0.5) +
    log(pull_lines + 0.5) +
    log(pull_desc_len + 0.5) +
    log(reviewer_experience + 0.5) +
    author_role_COLLABORATOR +
    author_role_CONTRIBUTOR +
    author_role_MEMBER +
    author_role_NONE +
    reviewer_role_COLLABORATOR +
    reviewer_role_CONTRIBUTOR +
    reviewer_role_MEMBER +
    reviewer_role_NONE +
    category_Motivation +
    category_Implementation +
    category_Quality +
    category_Problem +
    category_Miscellaneous +
    PR_types_Adaptive_Maintenance +
    PR_types_Code_Formatting +
    PR_types_Corrective_Maintenance_._Fix +
    PR_types_Feature_Addition +
    PR_types_Feature_Improvement +
    PR_types_Language_Compatibility +
    PR_types_Library_Compatibility +
    PR_types_Module_Management +
    PR_types_New_Release +
    PR_types_Non.source_Code_Change +
    PR_types_SCS_Management +
    PR_types_Testing +
    PR_types_Usage_Example +
    (1 | repo),
    data = d,
    family = binomial(link = "logit")
)

print(summary(model_acceptance))
print(r.squaredGLMM(model_acceptance))  # Marginal R² and Conditional R²

print("----------------------------------------")


# Model2 for review time
model_review_time <- lmer(log(close_time / 60 / 60 / 24 + 0.5) ~
    edited +
    log(repo_age / 30 + 0.5) +
    log(repo_commits + 0.5) +
    log(author_experience + 0.5) +
    log(open_tasks + 0.5) +
    log(pull_lines + 0.5) +
    log(pull_desc_len + 0.5) +
    log(reviewer_experience + 0.5) +
    author_role_COLLABORATOR +
    author_role_CONTRIBUTOR +
    author_role_MEMBER +
    author_role_NONE +
    reviewer_role_COLLABORATOR +
    reviewer_role_CONTRIBUTOR +
    reviewer_role_MEMBER +
    reviewer_role_NONE +
    category_Motivation +
    category_Implementation +
    category_Quality +
    category_Problem +
    category_Miscellaneous +
    PR_types_Adaptive_Maintenance +
    PR_types_Code_Formatting +
    PR_types_Corrective_Maintenance_._Fix +
    PR_types_Feature_Addition +
    PR_types_Feature_Improvement +
    PR_types_Language_Compatibility +
    PR_types_Library_Compatibility +
    PR_types_Module_Management +
    PR_types_New_Release +
    PR_types_Non.source_Code_Change +
    PR_types_SCS_Management +
    PR_types_Testing +
    PR_types_Usage_Example +
    (1 | repo),
    data = d
)

print("===== 模型2：拉取请求评审时间（线性混合模型）=====")
print(summary(model_review_time))
print(r.squaredGLMM(model_review_time))