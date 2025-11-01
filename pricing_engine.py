from datetime import datetime

# -----------------------------
# Dynamic Pricing Engine
# -----------------------------

def get_season_multiplier(month: int):
    """Return a multiplier based on the season."""
    if month in [6, 7, 8, 9]:  # Monsoon
        return {"season": "Monsoon", "multiplier": 1.10}
    elif month in [10, 11]:  # Festival season
        return {"season": "Festival", "multiplier": 1.03}
    elif month in [12, 1, 2]:  # Winter
        return {"season": "Winter", "multiplier": 1.08}
    elif month in [4, 5]:  # Summer
        return {"season": "Summer", "multiplier": 0.98}
    else:
        return {"season": "Normal", "multiplier": 1.00}


def get_region_multiplier(region: str, vehicle_type: str):
    """Return region-based multiplier depending on geography and car type."""
    region = region.lower()
    vehicle_type = vehicle_type.lower()

    # Hill or rugged terrain
    if any(x in region for x in ["himachal", "uttarakhand", "sikkim", "manali", "leh", "mountain"]):
        if vehicle_type in ["suv", "offroad", "4x4"]:
            return 1.10

    # Metro regions (high fuel prices, traffic)
    if any(x in region for x in ["mumbai", "delhi", "bangalore", "chennai", "kolkata"]):
        if vehicle_type in ["hatchback", "compact", "sedan"]:
            return 0.95

    # Rural or small-town demand for utility vehicles
    if any(x in region for x in ["village", "rural", "town", "agra", "kanpur"]):
        if vehicle_type in ["pickup", "utility", "suv"]:
            return 1.05

    return 1.00


def get_trend_multiplier(fuel_price_rising: bool = False):
    """Adjust prices based on market trends such as fuel price spikes."""
    if fuel_price_rising:
        return 0.97  # small penalty on fuel-inefficient vehicles
    return 1.00


def calculate_recommended_price(base_price: float, region: str, vehicle_type: str, fuel_price_rising: bool = False):
    """Compute recommended price using all factors."""
    month = datetime.now().month

    season_data = get_season_multiplier(month)
    region_multiplier = get_region_multiplier(region, vehicle_type)
    trend_multiplier = get_trend_multiplier(fuel_price_rising)

    recommended_price = base_price * season_data["multiplier"] * region_multiplier * trend_multiplier

    return {
        "base_price": base_price,
        "recommended_price": round(recommended_price, 2),
        "factors": {
            "region_multiplier": region_multiplier,
            "season_multiplier": season_data["multiplier"],
            "trend_multiplier": trend_multiplier,
            "season": season_data["season"]
        },
        "message": f"Recommended price adjusted for {season_data['season']} season and regional demand."
    }


# Example test
if __name__ == "__main__":
    result = calculate_recommended_price(
        base_price=800000,
        region="Mumbai",
        vehicle_type="Hatchback",
        fuel_price_rising=True
    )
    print(result)
