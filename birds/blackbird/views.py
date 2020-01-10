try:
    from blackbird.models import Formula
    from bluebird.models import NormativeCategory
except ModuleNotFoundError:
    import os, sys
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    sys.path.append(parent_dir_path)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.path.join(parent_dir_path, 'birds/settings'))
    import django
    django.setup()

    from blackbird.models import Formula
    from bluebird.models import NormativeCategory

from datetime import date
import calendar



def calculate(*args, **kwargs):
    since_date = kwargs.get('since_date', None)  # Дата с начала расчета
    up_to_date = kwargs.get('up_to_date', None)  # Дата конца расчета
    stat_value = kwargs.get('stat_value', None)  # Значение показателя (м2, кол. чел. и т.д.)
    norm_value = kwargs.get('norm_value', None)  # Ключ на норматив

    # Что делать с активными днями и днями невывоза?

    if not (stat_value and norm_value and since_date and up_to_date):
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
    print(since_date, up_to_date, stat_value, norm_value)
    start_day = since_date.day

    for dt in month_year_iter(since_date.month, since_date.year,
                              up_to_date.month, up_to_date.year,):
        curr_date = date(day=calendar.monthrange(dt[0], dt[1])[1],
                         month=dt[1],
                         year=dt[0])
        print(curr_date)
        norm = get_normative(curr_date, norm_value)

        formula_obj_r = get_formula_object(curr_date)
        formula_rough = formula_obj_r.get_formula()

        formula_obj_p = get_formula_object(curr_date, rough=False)
        formula_precise = formula_obj_p.get_formula()

        m_day_count = calendar.monthrange(curr_date.year, curr_date.month)[1]
        a_day_count = m_day_count - start_day
        V_as_rough = eval(eval(formula_rough))
        V_as_precise = eval(eval(formula_precise))

        summ_precise = V_as_precise * formula_obj_p.get_tariff()
        tax_price_precise = summ_precise * formula_obj_p.get_tax()
        summ_tax_precise = summ_precise + tax_price_precise

        summ_rough = V_as_rough * formula_obj_r.get_tariff()
        tax_price_rough = summ_rough * formula_obj_r.get_tax()
        summ_tax_rough = summ_rough + tax_price_rough

        result.append(
            {
                'date': curr_date,
                'V_as_rough': format(V_as_rough, '.5f'),
                'summ_rough': format(summ_rough, '.2f'),
                'tax_price_rough': format(tax_price_rough, '.2f'),
                'summ_tax_rough': format(summ_tax_rough, '.2f'),
                'tax': formula_obj_p.get_tax(),
                'tariff': formula_obj_p.get_tariff(),
                'V_as_precise': format(V_as_precise, '.5f'),
                'summ_precise': format(summ_precise, '.2f'),
                'tax_price_precise': format(tax_price_precise, '.2f'),
                'summ_tax_precise': format(summ_tax_precise, '.2f')
            })
        start_day = 0
    return result


def get_formula_object(curr_date, rough=True):
    formulas = Formula.objects.filter(is_rough=rough)
    for f in formulas:
        if f.since_date <= curr_date <= f.up_to_date:
            return f


def get_normative(curr_date, norm_value):
    norm = NormativeCategory.objects.get(pk=norm_value)
    norm_vals = norm.normative.all()
    for n in norm_vals:
        if n.since_date <= curr_date <= n.up_to_date:
            return n.value


def month_year_iter(start_month, start_year, end_month, end_year):
    ym_start = 12*start_year + start_month - 1
    ym_end = 12*end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        yield y, m + 1


if __name__ == '__main__':
    p = calculate(since_date=date.fromisoformat('2019-01-05'),
                  up_to_date=date.fromisoformat('2020-01-10'),
                  stat_value=75,
                  norm_value=2)
    print(p)
