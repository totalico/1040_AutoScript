from pypdf import PdfReader, PdfWriter
import Schedules
import Util

#totalincome is All incomes, includes capital gain
totalIncome = 0
incomeTaxable = 0
adjested = 0


def reader():

    forms = ['1040']
    calc   = Schedules.configObjToArray('CALC_DATA', '.editorconfig')
    fields = configObjToArray('FIELDS' , '.editorconfig')
    filler = configObjToArray('FILLER_DETAILS' , '.editorconfig')
    dependets = configObjToArray('DEPENDENCE', '.editorconfig')
    dividends = configObjToArray('DIVIDENDS','.editorconfig')
    short_term= configObjToArray('SHORT_TERM' , '.editorconfig')
    long_term= configObjToArray('LONG_TERM' , '.editorconfig')

    dependetsArr = {}
    for i in dependets:
        dependetsArr[i] = Util.extractArrFromStringConfigFile(dependets[i])

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
                                fields['salary']:calc['salary'],
                                fields['sum_salary']:calc['salary'],
                                fields['qualified_dividends']:dividends['qualified_dividend'],
                                fields['ordinary_dividends'] : dividends['ordinary_dividend'],
                                fields['capital_gain']:capitalGain(),
                                fields['total_income']:doCalcs(int(calc['salary']),int (dividends['ordinary_dividend']), int(short_term['realized_gain']) ,long_term['realized_gain'] ,int(calc['standard_deduction'])),
                                fields['total_adjusted']:str(totalIncome),
                                fields['total_income_adjusted']:str(totalIncome),
                                fields['standard_deduction']:calc['standard_deduction'],
                                fields['total_dedction']:calc['standard_deduction'],
                                fields['taxable_income']:str(incomeTaxable),
                                fields['tax']:calc['tax'],      #In future looking for AI whom will get this info for us
                                fields['tax_added']:calc['tax'],
                                fields['child_credit']:sche8812()   ,      #8812 filler
                                fields['addiitional_child_tex_credit']:sche3(), # additinal? ?????
                                fields['refunds_sum']:'',
                                fields['total_refunds_sum']:'',
                                fields['total_sum_to_refund']:'',
                                fields['rout_num']:'',
                                fields['accuont_num']:'',
                                # fields['occupation']:
                                # fields['phone']:
                                # fields['email']:    }
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
    writer.update_page_form_field_values(
        writer.pages[1], {
        fields['rout_num']:filler['rout'],
        fields['phone']:filler['phone'],
        fields['email']: filler['email'],
        fields['occupation']: filler['occupation'],
        fields['account_num']: filler['account']
        })
    with open("declarations.txt", "a") as declarations:
        declarations.write('\n\n\n\n\n\n===========     ADDED FORMS     =================\n\n')
        for i in forms:
            declarations.write(str(forms.index(i)+1)+' > '+i+'\n')

    # write "output" to pypdf-output.pdf
    with open("filled-out.pdf", "wb") as output_stream:
        writer.write(output_stream)

reader()
