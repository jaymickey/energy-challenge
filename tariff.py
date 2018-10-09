"""Constants for computing bulb bills."""


BULB_TARIFF = {
    "electricity": {
        "unit_rate": 11.949,  # pence per kWh
        "standing_charge": 24.56  # fixed daily charge in pence
    },
    "gas": {
        "unit_rate": 3.8,
        "standing_charge": 24.56
    }
}
