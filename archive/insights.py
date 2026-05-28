def generate_insights(prod, log, inv):

    top_state = (
        prod.groupby("State")["Production_MT"]
        .sum()
        .idxmax()
    )

    top_crop = (
        prod.groupby("Crop")["Production_MT"]
        .sum()
        .idxmax()
    )

    risky_state = (
        log.groupby("State")["LogisticsRisk"]
        .mean()
        .idxmax()
    )

    highest_delay_vehicle = (
        log.groupby("VehicleType")["DelayHours"]
        .mean()
        .idxmax()
    )

    vulnerable_crop = (
        inv.groupby("Crop")["StorageLoss"]
        .mean()
        .idxmax()
    )

    best_storage = (
        inv.groupby("StorageType")["StorageLoss"]
        .mean()
        .idxmin()
    )

    insight = f"""
### 🌾 AI Supply Chain Insights

- **{top_state}** has the highest agricultural production.

- **{top_crop}** is the dominant crop by production volume.

- **{risky_state}** shows the highest logistics risk.

- **{highest_delay_vehicle}** experiences the highest transportation delays.

- **{vulnerable_crop}** suffers the greatest spoilage losses.

- **{best_storage}** storage demonstrates the lowest spoilage impact.

### 📈 Operational Recommendations

- Improve cold-chain infrastructure in high-risk states.
- Optimize logistics routes for delay-prone transportation modes.
- Prioritize spoilage reduction strategies for highly perishable crops.
"""

    return insight