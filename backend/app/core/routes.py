from random import randrange

from flask import flash, redirect, render_template, url_for
from flask.json import jsonify
# CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./static"))
from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from app.core import bp

from app.core import data
from app.forms import LoginForm

@bp.route('/')
@bp.route('/index')
def index():
    user = {'username': 'leao'}
    return render_template('index.html', title='base', user=user)


@bp.route('/geo')
def geo():
    return render_template('geo.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('core.index'))
    return render_template('login.html', title="sign in", form=form)


@bp.route('/charts')
def charts():
    # return Markup(c.render_embed())
    return render_template('chart1.html')


@bp.route('/chart2')
def chart2():
    return render_template('chart2.html')


@bp.route("/lineChart")
def get_line_chart():
    c = line_base()
    return c.dump_options_with_quotes()


@bp.route('/getPieChart')
# @cache.cached(timeout=100)
def getPieChart():
    c = data.getPie()
    return c.dump_options_with_quotes()


idx = 9


@bp.route("/lineDynamicData")
def update_line_data():
    global idx
    idx = idx + 1
    return jsonify({"name": idx, "value": randrange(50, 80)})


@bp.route('/bar_base')
def bar_base() -> Bar:
    c = (Bar().add_xaxis([
        "衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"
    ]).add_yaxis("商家A", [5, 20, 36, 10, 75, 90]).add_yaxis(
        "商家B", [15, 25, 16, 55, 48, 8]).set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-web1", subtitle="testtest")))
    return c.dump_options_with_quotes()


def line_base() -> Line:
    line = (Line().add_xaxis(["{}".format(i) for i in range(10)]).add_yaxis(
        series_name="",
        y_axis=[randrange(50, 80) for _ in range(10)],
        is_smooth=True,
        label_opts=opts.LabelOpts(is_show=False),
    ).set_global_opts(
        title_opts=opts.TitleOpts(title="动态数据"),
        xaxis_opts=opts.AxisOpts(type_="value"),
        yaxis_opts=opts.AxisOpts(type_="value"),
    ))
    return line
