# Energy Company Technical Challenge

This repo stores code that was written as part of a coding challenge for an energy company.

## Assumptions

In addition to the assumptions provided in the challenge description, I have made some additional assumptions:

- Exceptions raised in `calculate_bill()` will be handled further up the call stack in a final solution.
- If electricity and gas where both present, the file would look like this:

  ```json
  {
    "account-abc" : [
      {
        "electricity": [
            ...
        ]
      },
      {
        "gas": [
            ...
        ]
      }
    ]
  }
  ```

- Gas usage is measured in cubic meters and needs to be converted to kWh.
  - Conversion calcuation here: https://community.bulb.co.uk/discussion/730/gas-unit-conversion-calculation
- kWh values are rounded to the nearest whole value (https://community.bulb.co.uk/discussion/1600/help-with-bill-calculations)
- Given usage is linear and the readings aren't always taken on the last day of the month, the monthly bill is calculated via:
  - `((reading_current_month - reading_last_month) / days_between_readings) * days_in_month`

## Solution

The solution I have created adds a number of elements:

- Custom exceptions for when a member or account is not found, or when an invalid energy source is specified.
- `m3_to_kwh()` - converts gas readings, in cubic meters, to kWh.
- `process_sources()` - loops through energy sources and calculates the total £ amount and kWh for both electricity and gas for the calendar month.
- Additional tests in order to check account looping and source logic is correct.

## Usage

The only requirement is Python 3

### Testing

To run the tests: `python3 -m unittest`