import configparser
import re
from pypdf import PdfReader, PdfWriter
import Compliter

def configObjToArray (option , file):
    #   CREATE OBJECT
    arr = {}
    config_file = configparser.ConfigParser()
    conf = configparser.ConfigParser()
    #   READ CONFIG FILE
    config_file.read(file)
    for i in config_file.options(option):
        arr[i]=config_file.get(option , i)
    return arr



def f8812 (schedulePath, scheduleFields ,f1040_l1 , f1040_l11 ,f1040_l18_tax ,s3_l1_1116 ,dependancesNum, conf='.\\.editconfig'):

    childCredit = 2000
    additionalChildCredit = 1500
    otherStatuses=200000
    workSheetA = f1040_l18_tax - s3_l1_1116   #Tax there - Tax here
    l5=dependancesNum*childCredit
    l16b = dependancesNum*additionalChildCredit

    fields = configObjToArray('FIELDS' , scheduleFields)
    data   = configObjToArray('CALC_DATA' , conf)
    personal_data = configObjToArray('FILLER_DETAILS', '.\\.editconfig')

    reader = PdfReader(schedulePath)
    writer = PdfWriter()
    writer.append(reader)

    writer.update_page_form_field_values(
        writer.pages[0], {
            fields['name'] : personal_data['name'] +' '+ personal_data['family_name'],
            fields['ssn'] : personal_data ['ssn'],
            fields['l1_gross_income']:str (f1040_l11),
            fields['l2d_0']:'0',
            fields['l3__gross_income']: str (f1040_l11),
            fields['l4_num_children']:  str(dependancesNum),
            fields['l5_mult_l4_2000']: str(l5),
            fields['l6_non_qualified_children-0']:'0',
            fields['l7_mult_l6_500']: '0',
            fields['l8_add_l7_l5']: str(l5),
            fields['l9_status_200k']: str(otherStatuses),
            fields['l10_sub_from_l3_l9-0']: '0', #is wages > 200k ? I wish...
            fields['l11_mult_l10_0.05']: '0',
            fields['l12_sub_l8_l11']: str(l5), #as l8
            fields['l13_credit_limit_worksheet_A']: str (workSheetA),
            fields['l14-0']:'0',
            fields['l16a_sub_l12_l14']:  str(l5), #as l8
            fields['l16b1_num_children']: str(dependancesNum),
            fields['l16b2_l16b1*1500']: str(l16b),
            fields['l17_smaller_l16a_l16b2']: str(l16b), #nowadays cannot be otherwise
            fields['l18a_earned_income']: str(f1040_l1),
            fields['l18b_combat_pay-0']: '0',
            fields['l19_l18a_isBigger_2500']:str(f1040_l1 - 2500),
            fields['L20_mult_l19_by_0.15']:str((f1040_l1 - 2500)*0.15),
            fields['l21_medicare-0']: '0',
            fields['l22_s1l15-0']: '0',
            fields['l23_add_l22_21-0']: '0',
            fields['l24_2040L27-0']: '0',
            fields['l25_sub_l23_l24-0']: '0',
            fields['l26_bigger_l20_l25-l20']: str((f1040_l1 - 2500)*0.15),
            fields['l27_smaller_l26_l17-l17']: str(l16b)

            })


'''
@qualifiedDivindends = line 3a
@amountTaxtable - line 15 in 1040.
@sched_D_smaller_l15_or_16 = schedule D line 15 [usually is zero, then it will be o] OR line 16

:return 1040 tax amount to entry space
'''
def calcTax(amountTaxtable, conf = '.\\.editconfig'):

    short_term = configObjToArray('SHORT_TERM', conf)
    long_term = configObjToArray('LONG_TERM', conf)
    dividents = configObjToArray('DIVIDENDS', conf)
    qualifiedDivindends =int( dividents['qualified_dividend'])
    sched_D_smaller_l15_or_16 = int(long_term['realized_gain'])

    if sched_D_smaller_l15_or_16 <= 0 and qualifiedDivindends <=0 :
        return getTaxFromTable(amountTaxtable , '61')

    if  int(short_term['realized_gain']) < sched_D_smaller_l15_or_16:
        sched_D_smaller_l15_or_16=int(short_term['realized_gain'])

    l4 = qualifiedDivindends + sched_D_smaller_l15_or_16  # line4
    l5 = amountTaxtable - l4
    if l5 > 0:
        l5 = 0
    headOfHousehold = 55800
    l7 = headOfHousehold
    if amountTaxtable < headOfHousehold:
        l7 = amountTaxtable
    l8 = l5
    if l7 < l5:
        l8 = l7
    l9 = l7 - l8
    l10 = amountTaxtable
    if l4 < amountTaxtable:
        l10 = l4
    l12 = l10 - l9
    l13 = 488300
    l14 = amountTaxtable
    if l13 < amountTaxtable:
        l14 = amountTaxtable
    l15 = l5 + l9
    l16 = l14 - l15
    if l16 < 0:
        l16 = 0
    l17 = l12
    if l16 < l12:
        l17 = l16
    l18 = l17 * 0.15
    l19 = l9 + l17
    l20 = l10 - l19
    l21 = l20 * 0.20
    l22 = getTaxFromTable(l5)
    l23 = l18 + l21 + l22
    l24 = getTaxFromTable(amountTaxtable)
    l25 = l24
    if l23 > l24:
        l25 = l24

    with open('.\\Worksheet_qualified_dividnends_and_capital_gain_tax_output.txt', 'w') as file:
        file.write('Line        |       value       \n')
        file.write('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        file.write('1           |       ' + amountTaxtable + '  \n')
        file.write('4           |       ' + l4 + '       \n')
        file.write('5           |       ' + l5 + '       \n')
        file.write('7           |       ' + l7 + '       \n')
        file.write('8           |       ' + l8 + '       \n')
        file.write('9           |       ' + l9 + '       \n')
        file.write('10          |       ' + l10 + '       \n')
        file.write('12          |       ' + l12 + '       \n')
        file.write('13          |       ' + l13 + '       \n')
        file.write('14          |       ' + l14 + '       \n')
        file.write('15          |       ' + l15 + '       \n')
        file.write('16          |       ' + l16 + '       \n')
        file.write('17          |       ' + l17 + '       \n')
        file.write('18          |       ' + l18 + '       \n')
        file.write('19          |       ' + l19 + '       \n')
        file.write('20          |       ' + l20 + '       \n')
        file.write('21          |       ' + l21 + '       \n')
        file.write('22          |       ' + l22 + '       \n')
        file.write('23          |       ' + l23 + '       \n')
        file.write('24          |       ' + l24 + '       \n')
        file.write('25          |       ' + l25 + '       \n')

    print('Created summerized file : Worksheet_qualified_dividnends_and_capital_gain_tax_output.txt')
    return l25


def getTaxFromTable(amount, ppInIstructionTable):
    # TODO For future developing make the table automatically
    a = input('Look tax table in instruction in 1040ins '+ ppInIstructionTable + ' :> ' + amount)
    return a


def form_1116(schedulePath, scheduleFields, schedule3Path, schedule3Fields, f1040_l15_taxtableAmount, f1040_l16_tax , conf = '.\\.editconfig'):

    data = configObjToArray('CALC_DATA', conf)
    fields = configObjToArray('FIELDS', scheduleFields)
    personal_data = configObjToArray('FILLER_DETAILS',conf)

    usd = float(data['ILS_USD_rate'])
    salary_usd = float(data['salary_in_ILS']) / usd
    tax = float(data['tax_in_ILS']) / usd
    bituch_briut = float(data['bituch_briut_ILS']) / usd
    bituch_leumi = float(data['bituch_leumi_ILS']) / usd
    totalTaxUSD = tax + bituch_leumi + bituch_briut
    totalTaxILS = int(data['bituch_briut_ILS']) + int(data['bituch_leumi_ILS']) + int(data['tax_in_ILS'])
    print(
        'in USD :\nTaxes = ' + tax + '\nBituch-Briut = ' + bituch_briut + '\nBituch-Leumi = ' + bituch_leumi + '\nTotal = ' + totalTaxUSD)

    taxtable_income = salary_usd - int(data['standard_deduction'])
    wages_incomes_ratio = salary_usd / f1040_l15_taxtableAmount
    l21 = f1040_l16_tax * wages_incomes_ratio
    l24 = totalTaxUSD
    if l21 < totalTaxUSD:
        l24 = l21
    reader = PdfReader(schedulePath)
    writer = PdfWriter()
    writer.append(reader)

    writer.update_page_form_field_values(
        writer.pages[0], {
            fields['name']: personal_data['name'] + ' ' + personal_data['family_name'],
            fields['ssn']: personal_data['ssn'],
            fields['country']: 'ISRAEL',
            fields['income_reason']: 'WAGES',
            fields['income_sum']: salary_usd,
            fields['total_income_sum']: salary_usd,
            fields['itimazed_deduction']: data['standard_deduction'],
            fields['sum_deduction']: data['standard_deduction'],
            fields['gross_income']: salary_usd,
            fields['gross_income_all_sources']: salary_usd,
            fields['divide_e_by_d']: '1' ,
            fields['mult_f_by_c']: data['standard_deduction'],
            fields['deduction_from_all']: data['standard_deduction'],
            fields['deduction_from_all_sum']: data['standard_deduction'],
            fields['wage_sub_deduction']: str(taxtable_income),
            fields['date_range']: '1.1.22 - 12.31.22',
            fields['forigen_texes_paid_ILS']: str(totalTaxILS),
            fields['forigen_texes_paid_USD']: str(totalTaxUSD),
            fields['forigen_texes_paid_USD_sum']: str(totalTaxUSD),
            fields['forigen_texes_paid_USD_total']: str(totalTaxUSD)
        })
    writer.update_page_form_field_values(
        writer.pages[1], {
            fields['tax']: str(totalTaxUSD),
            fields['carry_over']: '0',
            fields['tax_carry']: str(totalTaxUSD),
            fields['combine_all_tax']: str(totalTaxUSD),
            fields['income_after_deduction']: str(taxtable_income),
            fields['adjestment']: '0',
            fields['income_total']: str(taxtable_income),
            fields['amount_in_1040_line_15']: str(f1040_l15_taxtableAmount),
            fields['div_income_by_line_15']: str(wages_incomes_ratio),
            fields['amount_in_1040_line_16']: str(f1040_l16_tax),
            fields['mult_l20_by_l19']: str(l21),
            fields['add_lines_20_21']: str(l21),
            fields['smaller_l14_or_l23']: str(l24),
            fields['from_l24']: str(l24),
            fields['boycott_reduction_always_0']: '0',
            fields['sum_to_1040_schedule_3_l2']: str(l24)

        })
    schedule_3(schedule3Path, schedule3Fields ,l24)
    return l24

'''
line 8 - put in 1040 l_20
'''
def schedule_3(schedulePath, scheduleFields, _1116amount):

    fields = configObjToArray('FIELDS', scheduleFields)

    personal_data = configObjToArray('FILLER_DETAILS', '.\\.editconfig')
    reader = PdfReader(schedulePath)
    writer = PdfWriter()
    writer.append(reader)

    writer.update_page_form_field_values(
        writer.pages[0], {
            fields['name']: personal_data['name'] + ' ' + personal_data['family_name'],
            fields['ssn']: personal_data['ssn'],
            fields['_1116form']: str(_1116amount),
            fields['total']: str(_1116amount)
        })


# schedule D
def capitalGain(schedulePath, scheduleFields, conf =  '.\\.editconfig'):
    fields = configObjToArray('FIELDS', scheduleFields)

    data = configObjToArray('CALC_DATA', conf)
    personal_data = configObjToArray('FILLER_DETAILS', conf)
    short_terms = configObjToArray('SHORT_TERM', conf)
    long_term = configObjToArray('LONG_TERM', conf)

    totalGainShort = int(short_terms['realized_gain']) - int(short_terms['loss_carry_over'])
    totalGainLong = int(long_term['realized_gain']) - int(long_term['loss_carry_over'])
    totalShortAndLong = totalGainLong + totalGainShort

    reader = PdfReader(schedulePath)
    writer = PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(
        writer.pages[0], {
            fields['name']: personal_data['name'] + ' ' + personal_data['family_name'],
            fields['ssn']: personal_data['ssn'],
            fields['proceed_short_term']: short_terms['proceeds'],
            fields['cost_short_term(basis)']: short_terms['cost_basis'],
            fields['gain_short_term']: short_terms['realized_gain'],
            fields['loss_carryover']: short_terms['loss_carry_over'],
            fields['sum_gain_carryover']: str(totalGainShort),

            fields['proceed_long_term']: long_term['proceeds'],
            fields['cost_long_term']: long_term['proceeds'],
            fields['gain_long_term']: long_term['realized_gain'],

            fields['long_term_carryover']: long_term['loss_carry_over'],
            fields['sum_long_term_gain']: str(totalGainLong),

            fields['sum_short_long']: str[totalShortAndLong]
        })

    return totalShortAndLong


# other income - DMEI LIYDA
# 'C:\\Users\\aman\\PycharmProjects\\pdfAutoCompliter\\fields_forms\\schedule1_fields'
def schedule_1(schedulePath, scheduleFields ,reason='PAYMENTS INSTEAD OF SALARY DURING BIRTH-VACATION'):

    data = configObjToArray('CALC_DATA', '.\\.editconfig')
    if not data['dmei_liyda'].isnumeric():
        print('Error in file: '+schedulePath+ ': Dmei-lyda is not recognized value')
        return

    if  data['dmei_liyda'].isnumeric() and int(data['dmei_liyda']) <= 0 :
        return 0


    fields = configObjToArray('FIELDS', scheduleFields)
    personal_data = configObjToArray('FILLER_DETAILS', '.\\.editconfig')

    reader = PdfReader(schedulePath)
    writer = PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(
        writer.pages[0], {
            fields['name']: personal_data['name'] + ' ' + personal_data['family_name'],
            fields['ssn']: personal_data['ssn'],
            # fields['other_income_sum'] : ,
            fields['other_income_src']: reason,
            fields['other_income_amount']: data['dmei_liyda'],
            fields['total_income']: data['dmei_liyda'],
            fields['sum']: data['dmei_liyda']})

    return int (data['dmei_liyda'])