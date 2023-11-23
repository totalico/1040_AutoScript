from pypdf import PdfReader, PdfWriter
import Util
from pdfAutoCompliter.Schedules import configObjToArray, capitalGain, schedule_1, calcTax, f8812, form_1116

pdfs = configObjToArray('PDF_FORMS_PATH','.editconfig')
dir = pdfs['dir']
formsMap = configObjToArray('FIELDS_FROM_PDFS' , '.editorconfig')
formsMapDir = dir +'.\\'+ formsMap['fields_map_dir']

def pdf (confPath = '.editconfig'):
    c ={}
    a = configObjToArray('PDF_FORMS_PATH',confPath) # a = {sch , dsdssaas}
    for i in a:
        c[i] = Util.extractArrFromStringConfigFile(a[i])

    print(c)


def reader():


    forms = ['1040']
    calc   = configObjToArray('CALC_DATA', '.editorconfig')
    fields = configObjToArray('FIELDS' , '.editorconfig')
    filler = configObjToArray('FILLER_DETAILS' , '.editorconfig')
    dependets = configObjToArray('DEPENDENCE', '.editorconfig')
    dividends = configObjToArray('DIVIDENDS','.editorconfig')
    short_term= configObjToArray('SHORT_TERM' , '.editorconfig')
    long_term= configObjToArray('LONG_TERM' , '.editorconfig')

    dependetsArr = {}
    for i in dependets:
        dependetsArr[i] = Util.extractArrFromStringConfigFile(dependets[i])



    #lines in 1040 2002
    l1a = calc['salary']
    l1h =calc['salary']
    l3a = dividends['qualified_dividend']
    l3b = dividends['ordinary_dividend']
    l7 = capitalGain(pdfs['schedleD']['name'] , pdfs['schedleD']['fieldsFile'])
    l8 = schedule_1(pdfs['schedle1']['name'] , pdfs['schedle1']['fieldsFile'])
    l9 = l1a+l3b+l7+l8
    l10 = 0 #adjestmnets
    l11 = l9-l10
    l12= int(calc['standard_deduction'])
    l14=l12
    l15=l11-l14

    l16 = calcTax(l15)
    l17 = 0
    l18 = l16+l17
    # this line is bifore l19, due i need l20 to b in l19
    l20 = form_1116 (pdfs['form_1116']['name'] , pdfs['form_1116']['fieldsFile'],pdfs['schedule3']['name'] , pdfs['schedule3']['fieldsFile'],
                   l15, l16 )
    l19 = f8812(pdfs['schedleD']['name'] , pdfs['schedleD']['fieldsFile'], l1a , l11,l18, l20  , len(dependets))#Suppose to b after s3

    l21 = l19 + l20
    l22 = l18 - l21
    if l22 < 0:
        l22=0
    l23=0
    l24=l22+l23

    l25a = 0
    l25b = 0
    l25c = 0
    l25d = 0
    l26 =  0
    l27 =  0
    l28 =

    reader = PdfReader('f1040.pdf')
    writer = PdfWriter()

    writer.append(reader)


    writer.update_page_form_field_values(
            writer.pages[0] , {
                                fields['first_name']:filler['name'],
                               fields['family_name']:filler['family_name'],
                               fields['personal_ssn']:filler['ssn'],
                               fields['apartment']: filler['apt'],
                               fields['address']:filler['address'],
                               fields['city']:filler['city'],
                               fields['country1']:filler['country'],
                               fields['zip1']:filler['zip'],
                               fields['country2']:filler['country'],
                               fields['country3']:filler['country'],
                               fields['zip2']:filler['zip'],

            #
                                fields['salary']:str(l1a),
                                fields['sum_salary']:str(l1h),
                                fields['qualified_dividends']:str(l3a),
                                fields['ordinary_dividends'] : str(l3b),
                                fields['capital_gain']:str(l7),
                                fields['total_income']:doCalcs(int(calc['salary']),int (dividends['ordinary_dividend']), int(short_term['realized_gain']) ,long_term['realized_gain'] ,int(calc['standard_deduction'])),
                                fields['total_adjusted']:str(totalIncome),
                                fields['total_income_adjusted']:str(totalIncome),
                                fields['standard_deduction']:calc['standard_deduction'],
                                fields['total_dedction']:calc['standard_deduction'],
                                fields['taxable_income']:str(incomeTaxable),
        })

                    writer.update_page_form_field_values(
                        writer.pages[1], {
                                fields['l16_tax']:
                                fields['l17_amount_s2l3-0']:
                                fields['l18_add_l16_l17']:
                                fields['l19_childTaxCredit_8812l19-0']:
                                fields['l20_amount_s3l8-0']:
                                fields['l21_add_l20_l19']:
                                fields['l22_l18_sub_l21']:
                                fields['l23_otherTaxes_s2l21-0']:
                                fields['l24_add_22_23']:
                                fields['l25a_federalIncome_w2-0']:
                                fields['l25b_federalIncome_1099-0']:
                                fields['l25c_other_forms-0']:
                                fields['l25d_total_a-c-0']:
                                fields['l26_estimated_2021_return_overpaid-0']:
                                fields['l27_EIC-0']:
                                fields['l28_aditional_childTaxCredit_8812l27']:
                                fields['l29_american_oppornunity-0']:
                                fields['l31_amount_s3l15-0']:
                                fields['l32_add_ll27_l28_l29_l31-l28']:
                                fields['l33_totalPayments_add_l25b_l26_l32']:
                                fields['l34_l33_isBigger_l24_sub_l33_l24']:
                                fields['l35a_amount_to_refound']:
                                fields['l35b_routing']:
                                fields['l35d_account']:
                                fields['l36_sum_to_applied_in_2023-0']:
                                fields['l37_l24_sub_l33-0']:
                                fields['l38_estimated_tax_penalty-0']:
                                fields['occupation']:
                                fields['phone']:
                                fields['email']:
                                   })

    with open("declarations.txt", "w") as declarations:
        declarations.write('===========     ILS/DOLLAR RATE   ============\n\n')
        declarations.write('1 USD = ' + calc['ils_dollar_rate'] + ' ILS')

    j = 1
    for i in dependetsArr:
        if j <= 4:
            writer.update_page_form_field_values(writer.pages[0], {
                fields['dep_' + str(j) + '_name']: dependetsArr[i]['name'],
                fields['dep_' + str(j) + '_ssn']: dependetsArr[i]['ssn'],
                fields['dep_' + str(j) + '_gen']: dependetsArr[i]['rel']
            })
        else:
            with open("declarations.txt", "a") as declarations:
                if j == 5:
                    declarations.write('\n\n\n\n\n\n===========     DEPENDENCIES    ===================\n\n')
                declarations.write(str(j) + ' > ' + 'Name:' +dependetsArr[i]['name']+
                     '  SSN: ' +dependetsArr[i]['ssn']+ '  Relation: ' +dependetsArr[i]['rel']+'\n')

        j+=1
    declarations.close()
    # writer.update_page_form_field_values(
    #     writer.pages[1], {
    #     fields['rout_num']:filler['rout'],
    #     fields['phone']:filler['phone'],
    #     fields['email']: filler['email'],
    #     fields['occupation']: filler['occupation'],
    #     fields['account_num']: filler['account']
    #     })
    with open("declarations.txt", "a") as declarations:
        declarations.write('\n\n\n\n\n\n===========     ADDED FORMS     =================\n\n')
        for i in forms:
            declarations.write(str(forms.index(i)+1)+' > '+i+'\n')

    # write "output" to pypdf-output.pdf
    with open("filled-out.pdf", "wb") as output_stream:
        writer.write(output_stream)

# reader()
pdf()