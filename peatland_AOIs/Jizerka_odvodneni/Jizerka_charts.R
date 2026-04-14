library(tidyverse)
library(lubridate)
library(ggplot2)

# Setup
folder_name <- basename(getwd())
files <- c("Forest_merged.csv", "Peat_merged.csv", "Bogpine_merged.csv")
colors <- c(Forest = "green", Peat = "brown", Bogpine = "orange")
lst_columns <- c("LST_C_L5", "LST_C_L7", "LST_C_L8")

trend_results <- list()

# Load and prepare data
all_data <- map_df(files, function(file) {
  class_name <- str_remove(file, "_merged.csv")
  
  read_csv(file, show_col_types = FALSE) %>%
    mutate(system_time_start = dmy(system_time_start)) %>%
    filter(month %in% c(5, 6, 7, 8, 9, 10)) %>%
    mutate(LST_mean = rowMeans(across(all_of(lst_columns)), na.rm = TRUE)) %>%
    filter(LST_mean >= 2 & LST_mean <= 42) %>%
    drop_na(LST_mean, system_time_start) %>%
    mutate(date_num = as.numeric(system_time_start), class = class_name)
})

# Calculate long-term trend for each class
for (class_name in unique(all_data$class)) {
  df_class <- all_data %>% filter(class == class_name)
  model <- lm(LST_mean ~ date_num, data = df_class)
  slope_per_year <- coef(model)[2] * 365
  trend_results[[class_name]] <- slope_per_year
  cat(sprintf("%s: %.3f °C/year\n", class_name, slope_per_year))
}

# Format trend text for plot
trend_text <- paste(
  names(trend_results),
  sprintf(": %.3f °C/year", unlist(trend_results)),
  collapse = "\n"
)

# Chart 1: Daily LST values with long-term trend lines
p1 <- all_data %>%
  ggplot(aes(x = system_time_start, y = LST_mean, color = class)) +
  geom_point(alpha = 0.4, size = 2) +
  geom_smooth(method = "lm", se = FALSE, linewidth = 1) +
  scale_color_manual(values = colors) +
  labs(
    title = paste("LST Trend —", folder_name),
    x = "Date", y = "Mean LST (°C)", color = "Class"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  geom_label(
    aes(x = min(system_time_start), y = max(LST_mean)),
    label = trend_text, inherit.aes = FALSE,
    hjust = 0, vjust = 1, size = 3.5, fill = "white", alpha = 0.8
  )

# Chart 2: Yearly variability with boxplots and mean lines
p2 <- all_data %>%
  mutate(year = year(system_time_start)) %>%
  ggplot(aes(x = factor(year), y = LST_mean, fill = class)) +
  geom_boxplot(alpha = 0.7) +
  stat_summary(fun = mean, geom = "line", aes(group = class, color = class), linewidth = 1.2) +
  stat_summary(fun = mean, geom = "point", aes(color = class), size = 3, shape = 4) +
  scale_fill_manual(values = colors) +
  scale_color_manual(values = colors) +
  labs(
    title = paste("LST Yearly Variability —", folder_name),
    x = "Year", y = "Mean LST (°C)", fill = "Class", color = "Class"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Chart 3: Mean vs Variability relationship
yearly_stats <- all_data %>%
  mutate(year = year(system_time_start)) %>%
  group_by(year, class) %>%
  summarise(yearly_mean = mean(LST_mean), yearly_sd = sd(LST_mean), .groups = "drop")

p3 <- yearly_stats %>%
  ggplot(aes(x = yearly_mean, y = yearly_sd, color = class, size = year)) +
  geom_point(alpha = 0.6) +
  geom_text(aes(label = year), size = 3, vjust = -0.5, show.legend = FALSE) +
  scale_color_manual(values = colors) +
  scale_size_continuous(name = "Year", range = c(2, 8)) +
  labs(
    title = paste("LST: Mean vs Variability —", folder_name),
    x = "Yearly Mean LST (°C)",
    y = "Yearly Variability (Std Dev)",
    color = "Class"
  ) +
  theme_minimal()

# Display all three charts
print(p1)
print(p2)
print(p3)


