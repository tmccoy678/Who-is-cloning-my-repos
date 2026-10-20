#!/usr/bin/env Rscript

# Recompute the current descriptive statistics and render the manuscript figures.
# Open Who-is-cloning-my-repos.Rproj in RStudio, then source this file from the
# repository root. The same code can be run with:
#
#   Rscript scripts/analyze_and_plot.R
#
# Inputs are preserved CSV and JSON evidence. No network access occurs here.

required_packages <- c(
  "cowplot", "digest", "ggplot2", "jsonlite", "ragg", "rstudioapi", "scales"
)
missing_packages <- required_packages[
  !vapply(required_packages, requireNamespace, logical(1), quietly = TRUE)
]
if (length(missing_packages) > 0) {
  stop("Install the required R packages: ", paste(missing_packages, collapse = ", "))
}

root <- normalizePath(getwd(), winslash = "/", mustWork = TRUE)
if (!file.exists(file.path(root, "CITATION.cff"))) {
  stop("Run this script from the repository root or open the RStudio project first.")
}

data_dir <- file.path(root, "data")
figure_dir <- file.path(root, "figures")
evidence_path <- file.path(
  root, "evidence", "live", "2026-10-20", "github-traffic-response.json"
)
comparison_path <- file.path(data_dir, "reanalysis-comparison-series.csv")
historical_metrics_path <- file.path(data_dir, "reanalysis-window-metrics.csv")
security_history_path <- file.path(
  data_dir, "codex-security-scan-history-summary-2026-10-20.csv"
)
script_path <- file.path(root, "scripts", "analyze_and_plot.R")
lockfile_path <- file.path(root, "renv.lock")

dir.create(data_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(figure_dir, recursive = TRUE, showWarnings = FALSE)

high_traffic_repositories <- c(
  "DobeWorks-v2.1",
  "DEGS-v2.1",
  "BackspaceTextRetention",
  "TrashTreasurePickup"
)

all_repositories <- c(
  "BackspaceTextRetention",
  "DEGS-v2.1",
  "DobeWorks-v2.1",
  "grok-bridge-writeup",
  "TrashTreasurePickup",
  "WeatherTicker"
)

read_live_snapshot <- function(path) {
  payload <- jsonlite::fromJSON(path, simplifyVector = FALSE)
  rows <- list()
  row_index <- 1L

  for (repository in all_repositories) {
    record <- payload$repositories[[repository]]
    daily <- record$clones$clones
    for (entry in daily) {
      rows[[row_index]] <- data.frame(
        repository = repository,
        date_utc = as.Date(substr(entry$timestamp, 1, 10)),
        clones = as.integer(entry$count),
        daily_unique_cloners = as.integer(entry$uniques),
        window_clones = as.integer(record$clones$count),
        window_unique_cloners = as.integer(record$clones$uniques),
        window_views = as.integer(record$views$count),
        window_unique_visitors = as.integer(record$views$uniques),
        captured_at_utc = payload$captured_at,
        stringsAsFactors = FALSE
      )
      row_index <- row_index + 1L
    }
  }

  snapshot <- do.call(rbind, rows)
  snapshot <- snapshot[order(snapshot$repository, snapshot$date_utc), ]
  rownames(snapshot) <- NULL
  snapshot
}

validate_snapshot <- function(snapshot) {
  expected_dates <- seq(as.Date("2026-10-06"), as.Date("2026-10-19"), by = "day")
  observed_repositories <- sort(unique(snapshot$repository))
  if (!identical(observed_repositories, sort(all_repositories))) {
    stop("The live snapshot does not contain the expected six repositories.")
  }

  numeric_fields <- c(
    "clones", "daily_unique_cloners", "window_clones",
    "window_unique_cloners", "window_views", "window_unique_visitors"
  )
  if (anyNA(snapshot[, numeric_fields]) || any(snapshot[, numeric_fields] < 0)) {
    stop("Traffic counts must be complete, numeric, and nonnegative.")
  }

  for (repository in all_repositories) {
    repo_rows <- snapshot[snapshot$repository == repository, ]
    if (!isTRUE(all.equal(repo_rows$date_utc, expected_dates, check.attributes = FALSE))) {
      stop(repository, " does not contain exactly one row for every expected UTC date.")
    }
    if (length(unique(repo_rows$window_clones)) != 1L ||
        sum(repo_rows$clones) != unique(repo_rows$window_clones)) {
      stop(repository, " daily clone counts do not reconcile to the window total.")
    }
    for (field in c(
      "window_unique_cloners", "window_views", "window_unique_visitors",
      "captured_at_utc"
    )) {
      if (length(unique(repo_rows[[field]])) != 1L) {
        stop(repository, " has inconsistent ", field, " values within the window.")
      }
    }
  }

  invisible(TRUE)
}

read_security_history <- function(path) {
  history <- utils::read.csv(path, stringsAsFactors = FALSE, check.names = FALSE)
  history$date_utc <- as.Date(history$date_utc)
  history$scan_jobs <- as.integer(history$scan_jobs)
  history$successful_scan_jobs <- as.integer(history$successful_scan_jobs)
  history
}

validate_security_history <- function(history) {
  required <- c(
    "repository", "date_utc", "scan_jobs", "successful_scan_jobs",
    "first_started_at_utc", "last_started_at_utc"
  )
  if (!identical(names(history), required)) {
    stop("The Codex Security history table has an unexpected schema.")
  }
  if (anyNA(history) || any(history$scan_jobs < 1L)) {
    stop("Codex Security history rows must be complete and contain positive counts.")
  }
  if (!identical(sort(unique(history$repository)), sort(high_traffic_repositories))) {
    stop("The monitored repository set does not match the four focal repositories.")
  }
  if (sum(history$scan_jobs) != 99L ||
      sum(history$successful_scan_jobs) != 99L ||
      any(history$scan_jobs != history$successful_scan_jobs)) {
    stop("The Codex Security history does not reconcile to 99 successful jobs.")
  }
  if (max(history$last_started_at_utc) != "2026-10-11T20:29:06.850165Z") {
    stop("The last recorded Codex Security scan timestamp changed.")
  }

  current <- history[
    history$date_utc >= as.Date("2026-10-06") &
      history$date_utc <= as.Date("2026-10-19"),
    c("repository", "date_utc", "scan_jobs")
  ]
  current <- current[order(current$repository, current$date_utc), ]
  rownames(current) <- NULL
  expected <- data.frame(
    repository = c("DobeWorks-v2.1", "TrashTreasurePickup"),
    date_utc = as.Date(c("2026-10-06", "2026-10-11")),
    scan_jobs = c(9L, 4L),
    stringsAsFactors = FALSE
  )
  if (!identical(current, expected)) {
    stop("Current-window Codex Security scan dates or counts changed.")
  }

  invisible(TRUE)
}

metric_row <- function(values, repository, measure, window, start, end) {
  values <- as.numeric(values)
  sample_sd <- if (length(values) > 1) stats::sd(values) else NA_real_
  mean_value <- mean(values)
  data.frame(
    window = window,
    start = as.Date(start),
    end = as.Date(end),
    repository = repository,
    measure = measure,
    n_days = length(values),
    total = sum(values),
    mean = mean_value,
    median = stats::median(values),
    min = min(values),
    max = max(values),
    sample_sd = sample_sd,
    range_percent_of_mean = 100 * (max(values) - min(values)) / mean_value,
    max_abs_deviation_from_mean_percent =
      100 * max(abs(values - mean_value)) / mean_value,
    sample_cv_percent = 100 * sample_sd / mean_value,
    stringsAsFactors = FALSE
  )
}

calculate_metrics <- function(snapshot) {
  windows <- list(
    current_14_days = as.Date(c("2026-10-06", "2026-10-19")),
    continuation_7_days = as.Date(c("2026-10-13", "2026-10-19")),
    comparison_6_days = as.Date(c("2026-10-13", "2026-10-18")),
    new_only_3_days = as.Date(c("2026-10-17", "2026-10-19"))
  )

  rows <- list()
  row_index <- 1L
  for (window_name in names(windows)) {
    bounds <- windows[[window_name]]
    selected <- snapshot[
      snapshot$date_utc >= bounds[1] & snapshot$date_utc <= bounds[2],
    ]

    for (repository in all_repositories) {
      repo_rows <- selected[selected$repository == repository, ]
      for (measure in c("clones", "daily_unique_cloners")) {
        rows[[row_index]] <- metric_row(
          repo_rows[[measure]], repository, measure, window_name, bounds[1], bounds[2]
        )
        row_index <- row_index + 1L
      }
    }

    high_rows <- selected[selected$repository %in% high_traffic_repositories, ]
    aggregate <- stats::aggregate(
      cbind(clones, daily_unique_cloners) ~ date_utc,
      data = high_rows,
      FUN = sum
    )
    for (measure in c("clones", "daily_unique_cloners")) {
      rows[[row_index]] <- metric_row(
        aggregate[[measure]],
        "Four-repository sum",
        measure,
        window_name,
        bounds[1],
        bounds[2]
      )
      row_index <- row_index + 1L
    }

    pair_rows <- selected[
      selected$repository %in% c("DobeWorks-v2.1", "DEGS-v2.1"),
    ]
    pair <- stats::aggregate(
      cbind(clones, daily_unique_cloners) ~ date_utc,
      data = pair_rows,
      FUN = sum
    )
    for (measure in c("clones", "daily_unique_cloners")) {
      rows[[row_index]] <- metric_row(
        pair[[measure]],
        "DobeWorks plus DEGS",
        measure,
        window_name,
        bounds[1],
        bounds[2]
      )
      row_index <- row_index + 1L
    }
  }

  metrics <- do.call(rbind, rows)
  rownames(metrics) <- NULL
  metrics
}

validate_historical_overlap <- function(metrics, path) {
  historical <- utils::read.csv(path, stringsAsFactors = FALSE, check.names = FALSE)
  historical <- historical[
    historical$window == "selected_6_days" &
      historical$repository %in% high_traffic_repositories,
  ]
  current <- metrics[
    metrics$window == "comparison_6_days" &
      metrics$measure == "clones" &
      metrics$repository %in% high_traffic_repositories,
  ]
  fields <- c(
    "total", "mean", "median", "min", "max", "sample_sd",
    "range_percent_of_mean", "max_abs_deviation_from_mean_percent",
    "sample_cv_percent"
  )

  historical <- historical[order(historical$repository), c("repository", fields)]
  current <- current[order(current$repository), c("repository", fields)]
  if (!identical(historical$repository, current$repository)) {
    stop("Historical and R overlap checks contain different focal repositories.")
  }
  for (field in fields) {
    if (!isTRUE(all.equal(
      as.numeric(historical[[field]]),
      as.numeric(current[[field]]),
      tolerance = 1e-12,
      check.attributes = FALSE
    ))) {
      stop("R and Python overlap metrics differ for field: ", field)
    }
  }

  invisible(TRUE)
}

calculate_security_alignment <- function(snapshot, history) {
  focal_snapshot <- snapshot[
    snapshot$repository %in% high_traffic_repositories,
  ]
  focal_snapshot$repository_day_rank <- rank(
    -focal_snapshot$clones,
    ties.method = "min"
  )

  rows <- lapply(high_traffic_repositories, function(repository) {
    repo_history <- history[history$repository == repository, ]
    repo_snapshot <- focal_snapshot[
      focal_snapshot$repository == repository,
    ]
    jobs <- integer(nrow(repo_snapshot))
    matched <- match(repo_snapshot$date_utc, repo_history$date_utc)
    jobs[!is.na(matched)] <- repo_history$scan_jobs[matched[!is.na(matched)]]
    no_scan_clones <- repo_snapshot$clones[jobs == 0L]
    peak_index <- which.max(repo_snapshot$clones)[1]

    data.frame(
      repository = repository,
      recorded_scan_jobs = sum(repo_history$scan_jobs),
      first_recorded_scan_utc = min(repo_history$first_started_at_utc),
      last_recorded_scan_utc = max(repo_history$last_started_at_utc),
      current_window_scan_jobs = sum(jobs),
      no_scan_day_median_clones = stats::median(no_scan_clones),
      peak_date_utc = repo_snapshot$date_utc[peak_index],
      peak_clones = repo_snapshot$clones[peak_index],
      peak_rank_among_56_repository_days =
        repo_snapshot$repository_day_rank[peak_index],
      scan_jobs_on_peak_date = jobs[peak_index],
      peak_minus_no_scan_median =
        repo_snapshot$clones[peak_index] - stats::median(no_scan_clones),
      stringsAsFactors = FALSE
    )
  })
  alignment <- do.call(rbind, rows)
  scan_aligned <- alignment[alignment$scan_jobs_on_peak_date > 0L, ]
  if (!identical(
    scan_aligned$repository,
    c("DobeWorks-v2.1", "TrashTreasurePickup")
  ) || !identical(
    as.integer(scan_aligned$peak_rank_among_56_repository_days),
    c(1L, 2L)
  )) {
    stop("Scan-aligned peaks are no longer the top two of 56 repository-days.")
  }
  alignment
}

save_plot <- function(plot, stem, width, height) {
  png_path <- file.path(figure_dir, paste0(stem, ".png"))
  pdf_path <- file.path(figure_dir, paste0(stem, ".pdf"))

  ggplot2::ggsave(
    png_path,
    plot = plot,
    device = ragg::agg_png,
    width = width,
    height = height,
    units = "in",
    dpi = 300,
    bg = "white"
  )
  ggplot2::ggsave(
    pdf_path,
    plot = plot,
    device = "pdf",
    width = width,
    height = height,
    units = "in",
    bg = "white",
    useDingbats = FALSE
  )

  c(png_path, pdf_path)
}

theme_manuscript <- function(base_size = 10) {
  ggplot2::theme_bw(base_size = base_size, base_family = "serif") +
    ggplot2::theme(
      panel.grid.minor = ggplot2::element_blank(),
      panel.grid.major.x = ggplot2::element_blank(),
      panel.border = ggplot2::element_blank(),
      axis.line = ggplot2::element_line(linewidth = 0.35, colour = "black"),
      axis.ticks = ggplot2::element_line(linewidth = 0.35),
      strip.background = ggplot2::element_blank(),
      strip.text = ggplot2::element_text(face = "plain", size = base_size + 1),
      plot.title = ggplot2::element_text(face = "plain", size = base_size + 5),
      plot.subtitle = ggplot2::element_text(size = base_size + 1),
      plot.caption = ggplot2::element_text(hjust = 0, size = base_size - 1),
      legend.position = "bottom"
    )
}

build_window_figure <- function(snapshot, metrics, security_history) {
  focal <- snapshot[snapshot$repository %in% high_traffic_repositories, ]
  focal$repository <- factor(focal$repository, levels = high_traffic_repositories)
  focal$scan_jobs <- 0L
  for (index in seq_len(nrow(security_history))) {
    matched <- focal$repository == security_history$repository[index] &
      focal$date_utc == security_history$date_utc[index]
    focal$scan_jobs[matched] <- security_history$scan_jobs[index]
  }

  seven_day <- metrics[
    metrics$window == "continuation_7_days" &
      metrics$measure == "clones" &
      metrics$repository %in% high_traffic_repositories,
  ]
  annotations <- seven_day[
    , c("repository", "range_percent_of_mean", "sample_cv_percent")
  ]
  annotations$repository <- factor(
    annotations$repository,
    levels = high_traffic_repositories
  )
  annotations$date_utc <- as.Date("2026-10-06")
  annotations$y <- 17
  annotations$label <- sprintf(
    "Oct 13-19: range %.2f%%; CV %.2f%%",
    annotations$range_percent_of_mean,
    annotations$sample_cv_percent
  )

  scan_annotations <- focal[focal$scan_jobs > 0L, ]
  scan_annotations$label <- sprintf(
    "%d recorded scans\n%d clones",
    scan_annotations$scan_jobs,
    scan_annotations$clones
  )
  scan_annotations$label_hjust <- ifelse(
    scan_annotations$date_utc == as.Date("2026-10-06"),
    0,
    0.5
  )

  ggplot2::ggplot(focal, ggplot2::aes(x = date_utc, y = clones)) +
    ggplot2::annotate(
      "rect",
      xmin = as.Date("2026-10-12") - 0.5,
      xmax = as.Date("2026-10-19") + 0.5,
      ymin = -Inf,
      ymax = Inf,
      fill = "grey94"
    ) +
    ggplot2::geom_line(linewidth = 0.45, colour = "black") +
    ggplot2::geom_point(shape = 21, size = 1.9, stroke = 0.45, fill = "white") +
    ggplot2::geom_point(
      data = scan_annotations,
      shape = 23,
      size = 3.2,
      stroke = 0.5,
      fill = "black"
    ) +
    ggplot2::geom_text(
      data = scan_annotations,
      ggplot2::aes(label = label, hjust = label_hjust),
      vjust = -0.65,
      size = 2.8,
      family = "serif"
    ) +
    ggplot2::geom_text(
      data = annotations,
      ggplot2::aes(x = date_utc, y = y, label = label),
      inherit.aes = FALSE,
      hjust = 0,
      vjust = 0,
      size = 2.7,
      family = "serif"
    ) +
    ggplot2::facet_wrap(~repository, ncol = 2) +
    ggplot2::scale_x_date(
      limits = as.Date(c("2026-10-06", "2026-10-19")),
      breaks = as.Date(c("2026-10-06", "2026-10-09", "2026-10-12", "2026-10-15", "2026-10-19")),
      date_labels = "%b %d"
    ) +
    ggplot2::scale_y_continuous(breaks = c(0, 100, 200, 300), limits = c(0, 320)) +
    ggplot2::labs(
      title = "Recorded Security Cloud scans align with the two large clone spikes",
      subtitle = "GitHub clone events and successful Codex Security commit-scan jobs, October 6-19, 2026 (UTC)",
      x = NULL,
      y = "GitHub-counted clone events",
      caption = paste0(
        "Filled diamonds mark dates with recorded scan jobs. Grey shading begins after the final recorded scan on October 11; the plateau continues.\n",
        "The connected history contains 99 successful jobs in total. Range = 100 x (maximum - minimum) / mean; CV uses sample SD. Shared axes include zero."
      )
    ) +
    theme_manuscript(10) +
    ggplot2::theme(
      plot.margin = ggplot2::margin(10, 18, 10, 10)
    )
}

build_comparison_figure <- function(metrics) {
  comparisons <- utils::read.csv(
    comparison_path,
    stringsAsFactors = FALSE,
    check.names = FALSE
  )
  comparisons <- comparisons[comparisons$included_in_reanalysis == "True", ]
  rate_matched <- comparisons[comparisons$in_mean_100_to_200_stratum == "True", ]
  focal <- metrics[
    metrics$window == "comparison_6_days" &
      metrics$measure == "clones" &
      metrics$repository %in% high_traffic_repositories,
  ]
  below_25 <- sum(comparisons$mean < 25)
  integer_lower_bound <- data.frame(
    mean = 10^seq(log10(0.16), log10(5000), length.out = 400)
  )
  integer_lower_bound$minimum_nonzero_range_percent <-
    100 / integer_lower_bound$mean
  integer_lower_bound <- integer_lower_bound[
    integer_lower_bound$minimum_nonzero_range_percent >= 0.8 &
      integer_lower_bound$minimum_nonzero_range_percent <= 900,
  ]

  panel_a <- ggplot2::ggplot() +
    ggplot2::geom_hline(yintercept = 4, linetype = "dashed", linewidth = 0.35) +
    ggplot2::geom_vline(xintercept = 25, linetype = "dotted", linewidth = 0.35) +
    ggplot2::geom_line(
      data = integer_lower_bound,
      ggplot2::aes(x = mean, y = minimum_nonzero_range_percent),
      linetype = "dotdash",
      colour = "grey25",
      linewidth = 0.45
    ) +
    ggplot2::geom_point(
      data = comparisons,
      ggplot2::aes(x = mean, y = range_percent_of_mean),
      shape = 1,
      colour = "grey45",
      size = 2
    ) +
    ggplot2::geom_point(
      data = focal,
      ggplot2::aes(x = mean, y = range_percent_of_mean),
      shape = 15,
      colour = "black",
      size = 2.4
    ) +
    ggplot2::annotate(
      "label",
      x = 3.2,
      y = 38,
      size = 2.8,
      family = "serif",
      label = "Integer-count lower bound:\n100 / mean",
      linewidth = 0,
      fill = "white"
    ) +
    ggplot2::scale_x_log10(
      breaks = c(0.2, 1, 10, 100, 1000),
      labels = scales::label_number(big.mark = ",")
    ) +
    ggplot2::scale_y_log10(
      limits = c(0.8, 900),
      breaks = c(1, 4, 10, 100, 600),
      labels = scales::label_number()
    ) +
    ggplot2::labs(
      title = "A. All screened comparison series",
      x = "Mean daily clone count",
      y = "Six-day range / mean (%) - log scale"
    ) +
    theme_manuscript(10) +
    ggplot2::theme(legend.position = "none")

  panel_b <- ggplot2::ggplot() +
    ggplot2::geom_hline(yintercept = 4, linetype = "dashed", linewidth = 0.35) +
    ggplot2::geom_point(
      data = rate_matched,
      ggplot2::aes(x = mean, y = range_percent_of_mean),
      shape = 1,
      colour = "grey30",
      size = 2.8
    ) +
    ggplot2::geom_point(
      data = focal,
      ggplot2::aes(x = mean, y = range_percent_of_mean),
      shape = 15,
      colour = "black",
      size = 2.4
    ) +
    ggplot2::annotate("text", x = 129, y = 285, label = "consort\n191.66%", family = "serif", size = 3) +
    ggplot2::annotate("text", x = 178, y = 110, label = "MegaV_Public\n87.84%", family = "serif", size = 3) +
    ggplot2::annotate("text", x = 154, y = 1.55, label = "Four focal repositories:\n1.40-3.50%", family = "serif", size = 3, hjust = 0) +
    ggplot2::annotate("text", x = 103, y = 4.8, label = "4% reference", family = "serif", size = 2.7, hjust = 0, colour = "grey35") +
    ggplot2::scale_x_continuous(limits = c(100, 210), breaks = c(100, 125, 150, 175, 200)) +
    ggplot2::scale_y_log10(
      limits = c(0.8, 900),
      breaks = c(1, 4, 10, 100, 600),
      labels = scales::label_number()
    ) +
    ggplot2::labs(
      title = "B. Post hoc 100-200/day stratum",
      x = "Mean daily clone count",
      y = NULL
    ) +
    theme_manuscript(10) +
    ggplot2::theme(
      legend.position = "none",
      axis.text.y = ggplot2::element_blank(),
      axis.ticks.y = ggplot2::element_blank()
    )

  panels <- cowplot::plot_grid(panel_a, panel_b, nrow = 1, rel_widths = c(1.15, 1))
  title <- cowplot::ggdraw() +
    cowplot::draw_label(
      "The focal repositories occupy a sparse high-rate, low-variation region\nSame six dates: October 13-18, 2026 (UTC)",
      fontfamily = "serif",
      size = 15,
      lineheight = 1.1
    )
  footer <- cowplot::ggdraw() +
    cowplot::draw_label(
      paste0(
        "Open circles: screened external series (n = ", nrow(comparisons), "). Black squares: four focal repositories.\n",
        below_25, "/", nrow(comparisons), " screened series average <25/day; source-host series can be clustered.\n",
        "Only two external series meet the rate stratum; no screened external series has range/mean <=4%."
      ),
      x = 0,
      hjust = 0,
      fontfamily = "serif",
      size = 9
    )

  cowplot::plot_grid(title, panels, footer, ncol = 1, rel_heights = c(0.12, 1, 0.13))
}

sha256 <- function(path) {
  digest::digest(file = path, algo = "sha256", serialize = FALSE)
}

snapshot <- read_live_snapshot(evidence_path)
validate_snapshot(snapshot)
security_history <- read_security_history(security_history_path)
validate_security_history(security_history)
metrics <- calculate_metrics(snapshot)
validate_historical_overlap(metrics, historical_metrics_path)
security_alignment <- calculate_security_alignment(snapshot, security_history)

snapshot_path <- file.path(data_dir, "traffic-snapshot-2026-10-20.csv")
metrics_path <- file.path(data_dir, "r-analysis-window-metrics-2026-10-20.csv")
security_alignment_path <- file.path(
  data_dir, "r-codex-security-alignment-metrics-2026-10-20.csv"
)
utils::write.csv(snapshot, snapshot_path, row.names = FALSE, na = "")
utils::write.csv(metrics, metrics_path, row.names = FALSE, na = "")
utils::write.csv(
  security_alignment,
  security_alignment_path,
  row.names = FALSE,
  na = ""
)

output_paths <- c(
  save_plot(
    build_window_figure(snapshot, metrics, security_history),
    "r-window-sensitivity-2026-10-20",
    10.5,
    7.6
  ),
  save_plot(
    build_comparison_figure(metrics),
    "r-rate-comparison-2026-10-20",
    10.8,
    6.2
  )
)

input_paths <- c(
  evidence_path,
  comparison_path,
  historical_metrics_path,
  security_history_path
)
execution_context <- if (rstudioapi::isAvailable()) {
  version_info <- rstudioapi::versionInfo()
  list(
    interface = "RStudio Desktop",
    version = version_info$long_version,
    release_name = version_info$release_name
  )
} else {
  list(interface = "Rscript")
}
provenance <- list(
  generated_at_utc = format(Sys.time(), tz = "UTC", usetz = TRUE),
  workflow = "Hand-written R analysis and figure code for RStudio",
  execution_context = execution_context,
  script = "scripts/analyze_and_plot.R",
  script_sha256 = sha256(script_path),
  lockfile = list(file = "renv.lock", sha256 = sha256(lockfile_path)),
  r_version = R.version.string,
  platform = R.version$platform,
  packages = as.list(vapply(
    required_packages,
    function(package) as.character(utils::packageVersion(package)),
    character(1)
  )),
  inputs = lapply(input_paths, function(path) {
    list(file = sub(paste0("^", root, "/"), "", path), sha256 = sha256(path))
  }),
  derived_tables = lapply(
    c(snapshot_path, metrics_path, security_alignment_path),
    function(path) {
    list(file = sub(paste0("^", root, "/"), "", path), sha256 = sha256(path))
    }
  ),
  outputs = lapply(output_paths, function(path) {
    list(file = sub(paste0("^", root, "/"), "", path), sha256 = sha256(path))
  }),
  notes = c(
    "No network access occurs in this script.",
    "The raw authenticated GitHub traffic response is preserved separately from derived CSV tables.",
    "The script validates complete daily coverage, nonnegative counts, and reconciliation of daily clone counts to each window total.",
    "The shared six-day focal metrics are checked against the independent Python analysis before figures are written.",
    "The Codex Security summary is checked for the exact four-repository set, 99 successful jobs, and the last recorded scan timestamp.",
    "PNG and vector PDF versions are generated from the same ggplot objects.",
    "The six-day comparison remains October 13-18 because that is the shared interval in the preserved external comparison set.",
    "The unique-cloner chart was removed because repository-level daily unique counts cannot be deduplicated across repositories and did not add a distinct visual finding."
  )
)

provenance_path <- file.path(figure_dir, "r-figure-provenance-2026-10-20.json")
jsonlite::write_json(provenance, provenance_path, pretty = TRUE, auto_unbox = TRUE)
cat(jsonlite::toJSON(provenance, pretty = TRUE, auto_unbox = TRUE), "\n")
