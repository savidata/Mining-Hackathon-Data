summary(hackdata)

proj <- subset(hackdata, total_projects == 0)
teamnum <- subset(hackdata, team_member_count == 0)
hack <- subset(hackdata, avg_hackathons == 0)
summary(hack)
data <- subset(hackdata, total_projects != 0 & team_member_count != 0)


data$submit_to_registered <- NULL # DO NOT INCLUDE IN PAPER
data$total_wins <- data$total_wins - data$did_win
num <- 1
data$total_projects <- data$total_projects - num


summary(data)
length(unique(data$hackathon_url))
sum(!complete.cases(data))
colSums(is.na(data))
# Only missing values in the text tag columns, so no need to remove rows

length(unique(data$built_with_tags))
length(unique(data$unique_skills))
# There are too many unique features in the text variables for one-hot encoding

data$did_win <- as.factor(data$did_win)

table(data$did_win)

ggplot(data = data,aes(did_win)) +
  geom_bar(mapping = aes(y = (..count..)/sum(..count..)), fill = "lightsteelblue3") +
  scale_y_continuous(labels=scales::percent) +
  ylab("Percent") +
  xlab("Project Outcome (win = 1)") +
  ggtitle("Project Outcomes as a Percent")
# Data is unbalanced

data$team <- ifelse(data$team_member_count == 1, 0, 1)
data$team <- as.factor(data$team)
table(data$did_win,data$team)

ggplot(data = data,aes(did_win, fill = team)) +
  geom_bar(mapping = aes(y = (..count..)/sum(..count..)), position = "dodge") +
  scale_y_continuous(labels=scales::percent) +
  ylab("Percent") +
  xlab("Project Outcome (win = 1)") +
  ggtitle("Team Status on Project Outcomes") +
  scale_fill_brewer(palette = "Paired")
# Being on a team appears to be an advantage for competing