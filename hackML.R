# remove the text columns to build a predictive model
df <- subset(data, select = -c(title,hackathon_url,p_win_count,built_with_tags,unique_skills))
summary(df)
cor(df[2:14])

summary(lm(avg_following~avg_hackathons, data=df))
summary(lm(total_wins~total_projects, data=df))

# split data in train | cv | test
set.seed(740)
inTraining <- createDataPartition(df$did_win, p = 0.8, list = FALSE)
train <- df[ inTraining,]
test <- df[-inTraining,]

fitControl <- trainControl(method = "cv", number=10)

# logistic regression model
glm1 <- glm(did_win~., data = train, family = binomial())
summary(glm1)
varImp(glm1)


glm_model <- train(did_win~., data = train, method = "glm", family = binomial(), trControl = fitControl)
glm_model
summary(glm_model)

## only include statistically significant coefficients
glm_modelp <- train(did_win~number_of_slides+description_word_count+team_member_count+total_wins+total_projects+avg_hackathons+avg_following, data = train, method = "glm", family = binomial(), trControl = fitControl)
glm_modelp
summary(glm_modelp)


glm_pred <- predict(glm_model, newdata = test)
confusionMatrix(data = glm_pred, test$did_win, positive = "1")

glm_pred <- predict(glm_modelp, newdata = test)
confusionMatrix(data = glm_pred, test$did_win, positive = "1")
## models yield nearly identical results, can use model with all data

varImp(glm_model)
varImp(glm_modelp)

# random forest
rf_model <- train(did_win~., data = train, method = "rf", trControl = fitControl)
rf_model

rf_pred <- predict(rf_model, newdata = test)
confusionMatrix(data = rf_pred, test$did_win, positive = "1")
