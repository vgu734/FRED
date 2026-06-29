def get_unemployment_forecast():

    return {
        "last_updated": "2026-06-29T00:00:00Z",
        "model_version": "v1.0",

        "historical": [
            {"date": "2025-10", "value": 4.0},
            {"date": "2025-11", "value": 4.1},
            {"date": "2025-12", "value": 4.2}
        ],

        "forecast": {
            "1_month": {
                "date": "2026-07",
                "prediction": 4.3
            },
            "3_month": {
                "date": "2026-09",
                "prediction": 4.4
            },
            "12_month": {
                "date": "2027-06",
                "prediction": 4.9
            }
        }
    }