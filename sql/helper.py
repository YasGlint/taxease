'''Strings'''

collected_taxes_exceeds_target = 'The taxes collected exceeds the target'

target_exceeds_collected_taxes = 'The taxes collected falls behind the target'


def checkIfTaxGoalsAreMet(tax, target):
    if (target - tax) > tax:
        return f'Significant losses: The average taxes ({tax}) collected fall significantly behind the target ({target})'
    elif (tax - target) > target:
        return f'Tax goals met: The average taxes ({tax}) collected exceed the target ({target})'