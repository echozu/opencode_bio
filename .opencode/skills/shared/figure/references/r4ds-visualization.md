# R for Data Science - Data Visualization Reference

> Source: https://r4ds.had.co.nz/data-visualisation.html
> "The simple graph has brought more information to the data analyst's mind than any other device." — John Tukey

## Grammar of Graphics (ggplot2)

Every ggplot2 plot is composed of:

```
ggplot(data = <DATA>) +
  <GEOM_FUNCTION>(mapping = aes(<MAPPINGS>),
                  stat = <STAT>,
                  position = <POSITION>) +
  <COORDINATE_FUNCTION> +
  <FACET_FUNCTION> +
  <SCALE_FUNCTIONS> +
  <THEME>
```

### Aesthetic Mappings (`aes()`)

Map data variables to visual properties:

| Aesthetic | Description | Geoms |
|-----------|-------------|-------|
| `x`, `y` | Position | All |
| `color` / `colour` | Outline color | Points, lines |
| `fill` | Fill color | Bars, areas, boxes |
| `size` | Size/width | Points, lines |
| `shape` | Point shape (0-25) | Points |
| `alpha` | Transparency (0-1) | All |
| `linetype` | Line pattern (1-6) | Lines |
| `group` | Grouping | Lines, polygons |

**Inside `aes()`** = map to variable (legend auto-created)
**Outside `aes()`** = set to constant value

```r
# Map color to variable
ggplot(mpg, aes(x = displ, y = hwy, color = class)) + geom_point()

# Set color to constant
ggplot(mpg, aes(x = displ, y = hwy)) + geom_point(color = "blue")
```

### Faceting

```r
# Wrap by single variable
facet_wrap(~ class, nrow = 2)

# Grid by two variables
facet_grid(drv ~ cyl)

# Free scales
facet_wrap(~ class, scales = "free_y")
```

### Position Adjustments

| Position | Description | Used with |
|----------|-------------|-----------|
| `"identity"` | No adjustment | Default for most |
| `"dodge"` | Side by side | `geom_bar`, `geom_boxplot` |
| `"stack"` | Stacked | `geom_bar`, `geom_area` |
| `"fill"` | Stacked to 100% | `geom_bar` |
| `"jitter"` | Random noise | `geom_point` |

### Statistical Transformations

Every geom has a default stat:
- `geom_bar()` uses `stat_count()` — counts rows per x value
- `geom_histogram()` uses `stat_bin()` — bins continuous data
- `geom_smooth()` uses `stat_smooth()` — regression/loess
- `geom_boxplot()` uses `stat_boxplot()` — five-number summary
- `geom_point()` uses `stat_identity()` — raw values

Override with `stat = "identity"` to use pre-computed values (→ `geom_col()`).

### Coordinate Systems

```r
coord_cartesian(xlim = c(0, 10))  # zoom without dropping data
coord_flip()                       # horizontal bars
coord_polar()                      # pie/radar charts
coord_fixed(ratio = 1)            # equal aspect ratio
coord_map()                        # map projections
```

## Key Patterns

### Scatter + smooth
```r
ggplot(data, aes(x, y)) +
  geom_point(alpha = 0.3) +
  geom_smooth(method = "lm", se = TRUE)
```

### Grouped bar chart
```r
ggplot(data, aes(x = category, y = value, fill = group)) +
  geom_col(position = "dodge") +
  scale_fill_brewer(palette = "Set2")
```

### Distribution comparison
```r
ggplot(data, aes(x = value, fill = group)) +
  geom_density(alpha = 0.5)

ggplot(data, aes(x = group, y = value)) +
  geom_boxplot() +
  geom_jitter(width = 0.2, alpha = 0.3)
```

### Multi-panel
```r
ggplot(data, aes(x, y)) +
  geom_point() +
  facet_wrap(~ group, scales = "free") +
  theme_minimal()
```
