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

build_window_figure <- function(snapshot, metrics) {
  focal <- snapshot[snapshot$repository %in% high_traffic_repositories, ]
  focal$repository <- factor(focal$repository, levels = high_traffic_repositories)

  seven_day <- metrics[
    metrics$window == "continuation_7_days" &
      metrics$measure == "clones" &
      metrics$repository %in% high_traffic_repositories,
  ]
  full_window <- metrics[
    metrics$window == "current_14_days" &
      metrics$measure == "clones" &
      metrics$repository %in% high_traffic_repositories,
  ]

  annotations <- merge(
    full_window[, c("repository", "range_percent_of_mean", "sample_cv_percent")],
    seven_day[, c("repository", "range_percent_of_mean", "sample_cv_percent")],
    by = "repository",
    suffixes = c("_14", "_7")
  )
  annotations$repository <- factor(
    annotations$repository,
    levels = high_traffic_repositories
  )
  annotations$date_utc <- as.Date("2026-10-06")
  annotations$y <- 18
  annotations$label <- sprintf(
    "14 days: range %.2f%%; CV %.2f%%\n7-day continuation: range %.2f%%; CV %.2f%%",
    annotations$range_percent_of_mean_14,
    annotations$sample_cv_percent_14,
    annotations$range_percent_of_mean_7,
    annotations$sample_cv_percent_7
  )

  ggplot2::ggplot(focal, ggplot2::aes(x = date_utc, y = clones)) +
    ggplot2::annotate(
      "rect",
      xmin = as.Date("2026-10-13") - 0.5,
      xmax = as.Date("2026-10-19") + 0.5,
      ymin = -Inf,
      ymax = Inf,
      fill = "grey92"
    ) +
    ggplot2::annotate(
      "rect",
      xmin = as.Date("2026-10-17") - 0.5,
      xmax = as.Date("2026-10-19") + 0.5,
      ymin = -Inf,
      ymax = Inf,
      fill = "grey82",
      alpha = 0.7
    ) +
    ggplot2::geom_line(linewidth = 0.45, colour = "black") +
    ggplot2::geom_point(size = 1.6, colour = "black") +
    ggplot2::geom_text(
      data = annotations,
      ggplot2::aes(x = date_utc, y = y, label = label),
      inherit.aes = FALSE,
      hjust = 0,
      vjust = 0,
      size = 2.8,
      family = "serif"
    ) +
    ggplot2::facet_wrap(~repository, ncol = 2) +
    ggplot2::scale_x_date(
      limits = as.Date(c("2026-10-06", "2026-10-19")),
      breaks = seq(as.Date("2026-10-06"), as.Date("2026-10-18"), by = "2 days"),
      date_labels = "%b %d"
    ) +
    ggplot2::scale_y_continuous(breaks = c(0, 100, 200, 300), limits = c(0, 300)) +
    ggplot2::labs(
      title = "Daily clone counts and continuation of the recurring plateau",
      subtitle = "Current authenticated window: October 6-19, 2026 (UTC)",
      x = NULL,
      y = "GitHub-counted clone events",
      caption = paste0(
        "Light shading: October 13-19 continuation interval. Darker shading: dates beyond the original October 3-16 window.\n",
        "Range = 100 x (maximum - minimum) / mean. CV uses the sample standard deviation. Shared axes include zero."
      )
    ) +
    theme_manuscript(10) +
    ggplot2::theme(
      axis.text.x = ggplot2::element_text(angle = 30, hjust = 1),
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

  panel_a <- ggplot2::ggplot() +
    ggplot2::geom_hline(yintercept = 4, linetype = "dashed", linewidth = 0.35) +
    ggplot2::geom_vline(xintercept = 25, linetype = "dotted", linewidth = 0.35) +
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
      "text",
      x = 0.18,
      y = 12,
      hjust = 0,
      vjust = 0,
      size = 3,
      family = "serif",
      label = sprintf(
        "%d/%d screened series average <25/day.\nA nonconstant integer series below 25/day\ncannot have range/mean <=4%%.",
        below_25,
        nrow(comparisons)
      )
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
      title = "A. Broad convenience sample",
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
      "Comparison depends on the underlying clone rate\nSame six dates: October 13-18, 2026 (UTC)",
      fontfamily = "serif",
      size = 15,
      lineheight = 1.1
    )
  footer <- cowplot::ggdraw() +
    cowplot::draw_label(
      paste0(
        "Open circles: screened external series (n = ", nrow(comparisons), "). Black squares: four focal repositories.\n",
        "Cumulative and provenance-ambiguous records are excluded; source-host series can be clustered.\n",
        "Only two external series meet the rate stratum."
      ),
      x = 0,
      hjust = 0,
      fontfamily = "serif",
      size = 9
    )

  cowplot::plot_grid(title, panels, footer, ncol = 1, rel_heights = c(0.12, 1, 0.13))
}

build_clone_unique_figure <- function(snapshot) {
  selected <- snapshot[
    snapshot$repository %in% high_traffic_repositories &
      snapshot$date_utc >= as.Date("2026-10-13"),
  ]
  aggregate <- stats::aggregate(
    cbind(clones, daily_unique_cloners) ~ date_utc,
    data = selected,
    FUN = sum
  )
  aggregate$excess_clone_events <- aggregate$clones - aggregate$daily_unique_cloners
  lines <- rbind(
    data.frame(
      date_utc = aggregate$date_utc,
      measure = "Clone events",
      value = aggregate$clones
    ),
    data.frame(
      date_utc = aggregate$date_utc,
      measure = "Sum of repository-level daily unique cloners",
      value = aggregate$daily_unique_cloners
    )
  )
  lines$measure <- factor(
    lines$measure,
    levels = c("Clone events", "Sum of repository-level daily unique cloners")
  )

  panel_a <- ggplot2::ggplot(
    lines,
    ggplot2::aes(x = date_utc, y = value, linetype = measure, shape = measure)
  ) +
    ggplot2::geom_line(linewidth = 0.55, colour = "black") +
    ggplot2::geom_point(size = 2, colour = "black") +
    ggplot2::scale_linetype_manual(values = c("solid", "22")) +
    ggplot2::scale_shape_manual(values = c(16, 1)) +
    ggplot2::scale_x_date(date_breaks = "1 day", date_labels = "%b %d") +
    ggplot2::scale_y_continuous(limits = c(520, 590), breaks = seq(520, 590, 10)) +
    ggplot2::labs(
      title = "A. Four-repository daily totals",
      x = NULL,
      y = "Count",
      linetype = NULL,
      shape = NULL
    ) +
    theme_manuscript(10) +
    ggplot2::theme(axis.text.x = ggplot2::element_text(angle = 30, hjust = 1))

  panel_b <- ggplot2::ggplot(
    aggregate,
    ggplot2::aes(x = date_utc, y = excess_clone_events)
  ) +
    ggplot2::geom_col(width = 0.64, fill = "grey35") +
    ggplot2::geom_text(
      ggplot2::aes(label = excess_clone_events),
      vjust = -0.35,
      family = "serif",
      size = 3
    ) +
    ggplot2::scale_x_date(date_breaks = "1 day", date_labels = "%b %d") +
    ggplot2::scale_y_continuous(limits = c(0, 40), breaks = seq(0, 40, 10)) +
    ggplot2::labs(
      title = "B. Clone events beyond the daily unique-cloner sum",
      x = NULL,
      y = "Clone events minus daily unique-cloner sum"
    ) +
    theme_manuscript(10) +
    ggplot2::theme(
      legend.position = "none",
      axis.text.x = ggplot2::element_text(angle = 30, hjust = 1)
    )

  panels <- cowplot::plot_grid(panel_a, panel_b, ncol = 1, rel_heights = c(1.15, 0.85))
  title <- cowplot::ggdraw() +
    cowplot::draw_label(
      "Clone events and daily unique-cloner counts moved together\nOctober 13-19, 2026 (UTC)",
      fontfamily = "serif",
      size = 15,
      lineheight = 1.1
    )
  footer <- cowplot::ggdraw() +
    cowplot::draw_label(
      paste0(
        "Daily unique-cloner values are summed across repositories; cross-repository deduplication is unavailable.\n",
        "October 18 and 19 each sum to 551 daily unique cloners; clone events rose from 568 to 582."
      ),
      x = 0,
      hjust = 0,
      fontfamily = "serif",
      size = 9
    )

  cowplot::plot_grid(title, panels, footer, ncol = 1, rel_heights = c(0.11, 1, 0.12))
}

sha256 <- function(path) {
  digest::digest(file = path, algo = "sha256", serialize = FALSE)
}

snapshot <- read_live_snapshot(evidence_path)
validate_snapshot(snapshot)
metrics <- calculate_metrics(snapshot)
validate_historical_overlap(metrics, historical_metrics_path)

snapshot_path <- file.path(data_dir, "traffic-snapshot-2026-10-20.csv")
metrics_path <- file.path(data_dir, "r-analysis-window-metrics-2026-10-20.csv")
utils::write.csv(snapshot, snapshot_path, row.names = FALSE, na = "")
utils::write.csv(metrics, metrics_path, row.names = FALSE, na = "")

output_paths <- c(
  save_plot(
    build_window_figure(snapshot, metrics),
    "r-window-sensitivity-2026-10-20",
    10.5,
    7.6
  ),
  save_plot(
    build_comparison_figure(metrics),
    "r-rate-comparison-2026-10-20",
    10.8,
    6.2
  ),
  save_plot(
    build_clone_unique_figure(snapshot),
    "r-clones-versus-daily-uniques-2026-10-20",
    9.2,
    7.6
  )
)

input_paths <- c(evidence_path, comparison_path, historical_metrics_path)
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
  derived_tables = lapply(c(snapshot_path, metrics_path), function(path) {
    list(file = sub(paste0("^", root, "/"), "", path), sha256 = sha256(path))
  }),
  outputs = lapply(output_paths, function(path) {
    list(file = sub(paste0("^", root, "/"), "", path), sha256 = sha256(path))
  }),
  notes = c(
    "No network access occurs in this script.",
    "The raw authenticated GitHub traffic response is preserved separately from derived CSV tables.",
    "The script validates complete daily coverage, nonnegative counts, and reconciliation of daily clone counts to each window total.",
    "The shared six-day focal metrics are checked against the independent Python analysis before figures are written.",
    "PNG and vector PDF versions are generated from the same ggplot objects.",
    "The six-day comparison remains October 13-18 because that is the shared interval in the preserved external comparison set."
  )
)

provenance_path <- file.path(figure_dir, "r-figure-provenance-2026-10-20.json")
jsonlite::write_json(provenance, provenance_path, pretty = TRUE, auto_unbox = TRUE)
cat(jsonlite::toJSON(provenance, pretty = TRUE, auto_unbox = TRUE), "\n")
