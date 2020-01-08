from django.shortcuts import render
from blackbird.models import Formula, NormativeCategory


def calculate(*args, **kwargs):
    since_date = kwargs.get('since_date', None)  # Дата с начала расчета
    up_to_date = kwargs.get('up_to_date', None)  # Дата конца расчета
    stat_value = kwargs.get('stat_value', None)  # Значение показателя (м2, кол. чел. и т.д.)
    norm_value = kwargs.get('norm_value', None)  # Ключ на норматив

    # Что делать с активными днями и днями невывоза?

    if stat_value and norm_value and since_date and up_to_date:
        raise AttributeError()

    # Получаем количество прошедших месяцев
    # проходим по ним
    # Для каждого месяца мы находим:
    #       - формулу для рассчета основываясь на дате =
    #          formula(t) -> f'{var} + smt / smt * (smt - smt)'
    #       - нормаив основываясь на дате = norm_value(t)
    # Расчитываем таким образом:
    #   -- стоимость дня в месяц <норматив за конкретный месяц
    #       (norm_value(t)) / 30 дней (либо за период?)> = day_price
    #   -- объем выполненых за месяц работ 
    #       <day_price * stat_value * 30 дней (либо за период?)> = V_month_rough
    #   -- Стоимость за конкретный месяц без НДС 
    #       <V_month_rough * -цена тарифа за конкретный месяц задается в фотмуле -> = Val_wo_tax
    #   -- Стоимость за конкретный месяц c НДС 
    #       <Val_wo_tax * 1.2 > = Val_w_tax
    #   -- цена тарифа за конкретный месяц c НДС 
    #       <Val_w_tax / V_month_rough > = Tariff_w_tax
    #   -- цена тарифа за конкретный месяц без НДС 
    #       <Val_wo_tax / V_month_rough > = Tariff_wo_tax
    #   + Берем фотмулу и подставляем туда значения
    result = []
    for curr_date in range():
        norm = get_normative(curr_date, norm_value)
        formula_rough = get_formula(curr_date)
        formula_precise = get_formula(curr_date, rough=False)
        V_as_rough = eval(eval(formula_rough))
        V_as_precise = eval(eval(formula_precise))
        result.append({'V_as_rough': V_as_rough, 'V_as_precise': V_as_precise})
    return result


def get_formula(curr_date, rough=True):
    formulas = Formula.objects.get(is_rough=rough)
    for f in formulas:
        if f.since_date <= curr_date <= f.up_to_date:
            return f.equasion


def get_normative(curr_date, norm_value):
    norm = NormativeCategory.objects.get(norm=norm_value)
    for n in norm.normatives:
        if n.since_date <= curr_date <= n.up_to_date:
            return n.value
