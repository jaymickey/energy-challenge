import load_readings
from tariff import BULB_TARIFF
from datetime import datetime, date
from calendar import monthrange
from exceptions import NotFoundError, InvalidSource


def m3_to_kwh(m3_reading):
    """
    Calculate the number of kWh from the provided m3 (cubic meters) amount.
    The formula used has been taken from this page:
        https://community.bulb.co.uk/discussion/730/gas-unit-conversion-calculation
    """
    return ((m3_reading * 1.02264) * 39) / 3.6


def process_sources(energy_sources, bill_month, bill_year):
    """
    Loop through energy sources and calculates the total £ amount and kWh
    for both electricity and gas for the calendar month. The average
    consumption is calculated by taking the reading date for the specified
    month/year, subtracting the previous months reading, and dividing the
    resulting number by the number of days between those two readings.
    That average is then multiplied by the number of days in the billing
    calendar month.
    """
    amount = 0
    total_est_consumption = 0
    for energy_source in energy_sources:
        source, items = energy_source.popitem()
        if source not in ['electricity', 'gas']:
            raise InvalidSource(f'${source} is not a valid energy source.')
        # Retreive the index of the reading where the month matches
        # that of the bill_date. There is probably a better way to
        # do this that doesn't require creating 2 datetime objects.
        index = next(
            (i for i, d in enumerate(items)
                if datetime.fromisoformat(
                    d['readingDate'][:-1]).year == bill_year
                and datetime.fromisoformat(
                    d['readingDate'][:-1]).month == bill_month),
            None)

        if index is None:
            # Refactor later to allow for a predictive bill based
            # on past readings.
            raise NotFoundError('Invalid billing date')

        # Given the assumption that the energy usage is linear, and the
        # readings aren't always taken on the last day of the month - to
        # calculate the the bill for the full billing period the average
        # consumption is calculated based on the number of days between
        # the reading for the current billing month, and the previous
        # billing month. This avergae is then multiplied by the number of
        # days in the calendar month.
        reading = items[index]
        past_reading = items[index-1]
        reading_date = datetime.fromisoformat(reading['readingDate'][:-1])
        past_reading_date = datetime.fromisoformat(
            past_reading['readingDate'][:-1])
        reading_interval = (reading_date - past_reading_date).days
        avg_consumption = (
            (reading.get('cumulative') - past_reading.get('cumulative'))
            / reading_interval)
        days_in_month = monthrange(reading_date.year, reading_date.month)[1]
        est_consumption = avg_consumption * days_in_month

        # Gas is generally measured in cubic meters, so need to convert to kWh
        if source == 'gas' and reading['unit'] == 'm3':
            est_consumption = m3_to_kwh(est_consumption)
        # Round the estimated consumption to the nearest whole number as Bulb
        # doesn't bill to the decimal. Source:
        # https://community.bulb.co.uk/discussion/1600/help-with-bill-calculations
        est_consumption = int(round(est_consumption, 0))
        tariff = BULB_TARIFF[source]
        amount += (
            (tariff['standing_charge'] * days_in_month)
            + (tariff['unit_rate'] * est_consumption)) / 100
        total_est_consumption += est_consumption

    return amount, total_est_consumption


def calculate_bill(member_id=None, account_id=None, bill_date=None):
    """
    Calculate the bill for the provided member and account ID.
    If account_id is 'ALL' then the bill will be calculated as a total
    of all accounts for that specific member.
    """
    # If account_id is None, then assume all accounts are included
    account_id = account_id or 'ALL'
    readings = load_readings.get_readings()
    member = readings.get(member_id)
    if member is None:
        raise NotFoundError(f'Member ID (${member_id}) not found')

    amount, kwh = 0, 0
    bill_date = date.fromisoformat(bill_date)
    if account_id.lower() == 'all':
        for account in member:
            for acc_id, energy_sources in account.items():
                amt, consumption = process_sources(
                    energy_sources, bill_date.month, bill_date.year)
                amount += amt
                kwh += consumption
    else:
        account = next(
            (d for d in member if account_id in d), (None, None))
        if account is None:
            raise NotFoundError(f'Account ID (${account_id}) not found')
        amount, kwh = process_sources(
            account[account_id], bill_date.month, bill_date.year)

    return round(amount, 2), int(kwh)


def calculate_and_print_bill(member_id, account, bill_date):
    """Calculate the bill and then print it to screen.
    Account is an optional argument - I could bill for one account or many.
    There's no need to refactor this function."""
    member_id = member_id or 'member-123'
    bill_date = bill_date or '2017-08-31'
    account = account or 'ALL'
    amount, kwh = calculate_bill(member_id, account, bill_date)
    print('Hello {member}!'.format(member=member_id))
    print('Your bill for {account} on {date} is £{amount}'.format(
        account=account,
        date=bill_date,
        amount=amount))
    print('based on {kwh}kWh of usage in the last month'.format(kwh=kwh))
