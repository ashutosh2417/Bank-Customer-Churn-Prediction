def risk_level(probability):

    if probability < 0.30:
        return "🟢 Low Risk"

    elif probability < 0.70:
        return "🟡 Medium Risk"

    else:
        return "🔴 High Risk"