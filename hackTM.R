library(tidytext)
library(wordcloud)

textdf <- subset(data, select = c(did_win,built_with_tags,unique_skills))

tidytags <- textdf %>%
  unnest_tokens(tags, built_with_tags, token = "regex", pattern = ",")

tidyskills <- textdf %>%
  unnest_tokens(skills, unique_skills, token = "regex", pattern = ",")

tagscount <- count(tidytags, tags, sort = TRUE)
skillscount <- count(tidyskills, skills, sort = TRUE)
tagscount
skillscount

wordcloud(tagscount$tags,tagscount$n,max.words = 10)
wordcloud(skillscount$skills,skillscount$n,max.words = 10)

# just for winning projects
windf <- subset(textdf, did_win == 1)

tidytagsw <- windf %>%
  unnest_tokens(tags, built_with_tags, token = "regex", pattern = ",")

tidyskillsw <- windf %>%
  unnest_tokens(skills, unique_skills, token = "regex", pattern = ",")

tagscountw <- count(tidytagsw, tags, sort = TRUE)
skillscountw <- count(tidyskillsw, skills, sort = TRUE)
tagscountw
skillscountw

wordcloud(tagscountw$tags,tagscountw$n,max.words = 10, colors = "plum4")
wordcloud(skillscountw$skills,skillscountw$n,max.words = 10, colors = "plum4")

# just for losing projects
losedf <- subset(textdf, did_win == 0)

tidytagsl <- losedf %>%
  unnest_tokens(tags, built_with_tags, token = "regex", pattern = ",")

tidyskillsl <- losedf %>%
  unnest_tokens(skills, unique_skills, token = "regex", pattern = ",")

tagscountl <- count(tidytagsl, tags, sort = TRUE)
skillscountl <- count(tidyskillsl, skills, sort = TRUE)
tagscountl
skillscountl

wordcloud(tagscountl$tags,tagscountl$n,max.words = 10, colors = "tomato4")
wordcloud(skillscountl$skills,skillscountl$n,max.words = 10, colors = "tomato4")
