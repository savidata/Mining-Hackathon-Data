rm(list=ls())

library(readr)
library(tidyr)
library(dplyr)
library(ggplot2)
library(caret)
library(Metrics)
library(arm)
library(RColorBrewer)
hackdata = read_csv("hackathon_projects.csv")

display.brewer.all(colorblindFriendly = TRUE)
