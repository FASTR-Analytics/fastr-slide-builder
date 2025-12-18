---
marp: true
theme: fastr
paginate: true
---

## Adjustment for Outliers

For each value flagged as an outlier, the module calculates what the value "should have been" based on that facility's historical pattern.

**Methods used (in order of preference):**
1. Average of 3 months before and 3 months after
2. Same month from the previous year (for seasonal indicators)
3. Facility-specific historical average

---

### Outlier Adjustment: FASTR Output

![Percent change in volume due to outlier adjustment.](../../resources/default_outputs/Default_1._Percent_change_in_volume_due_to_outlier_adjustment.png)

Heatmap showing percent change in service volumes due to outlier replacement.
