from app import app,db
from app.models import Issue,ProStatus
from flask import jsonify,render_template,url_for,request,current_app,redirect,flash
from app.assist import jira_get_new,jira_get_all
from app.forms import ScheduleForm
import flask_excel as excel

@app.route('/')
def index():
    all_pro_status = ProStatus.query.order_by(ProStatus.id).all()
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['ISSUES_PER_PAGE']
    pagination = Issue.query.order_by(Issue.jira_id.desc()).paginate(page,per_page=per_page)
    issues = pagination.items
    form = ScheduleForm()
    return render_template('index.html',pagination=pagination,issues=issues,form=form,all_pro_status=all_pro_status)

# 项目状态分类视图
@app.route('/project_status/<int:pro_status_id>')
def project_status(pro_status_id):
    all_pro_status = ProStatus.query.order_by(ProStatus.id).all()
    pro_status = ProStatus.query.get_or_404(pro_status_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ISSUES_PER_PAGE']
    pagination = Issue.query.with_parent(pro_status).order_by(Issue.jira_id.desc()).paginate(page, per_page=per_page)
    issues = pagination.items
    form = ScheduleForm()
    return render_template('index.html', pagination=pagination, issues=issues, form=form,pro_status=pro_status,all_pro_status=all_pro_status)


@app.route('/showform/<int:issue_id>')
def show_form(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    form = ScheduleForm()
    form.pro_status.data = issue.pro_status_id
    form.ui_schedule.data = issue.ui_schedule
    form.back_schedule.data = issue.back_schedule
    form.front_schedule.data = issue.front_schedule
    form.test_schedule.data = issue.test_schedule
    return jsonify(html=render_template('_form.html', form=form,issue=issue))


@app.route('/ajaxedit/<int:issue_id>',methods=['POST'])
def ajax_edit(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    issue.pro_status_id = request.form.get('pro_status')
    issue.ui_schedule = request.form.get("ui_schedule")
    issue.back_schedule = request.form.get('back_schedule')
    issue.front_schedule = request.form.get('front_schedule')
    issue.test_schedule = request.form.get('test_schedule')
    db.session.commit()
    flash('%s %s 操作成功' % (issue.key,issue.summary))
    # return 'ok'
    return jsonify(pro_status=ProStatus.query.get_or_404(issue.pro_status_id).name,
                   ui_schedule=issue.ui_schedule,
                   back_schedule=issue.back_schedule,
                   front_schedule=issue.front_schedule,
                   test_schedule=issue.test_schedule
                   )


@app.route('/edit/<int:issue_id>',methods=['POST'])
def edit(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    form = ScheduleForm()
    if form.validate_on_submit():
        issue.pro_status_id = form.pro_status.data
        issue.ui_schedule = form.ui_schedule.data
        issue.back_schedule = form.back_schedule.data
        issue.front_schedule = form.front_schedule.data
        issue.test_schedule = form.test_schedule.data
        db.session.commit()
        flash('%s %s 操作成功' % (issue.key,issue.summary))
        if issue.pro_status_id:
            url = '/project_status/' + str(issue.pro_status_id) + '#' + str(issue.id)
        else:
            url = '/#' + str(issue.id)
        return redirect(url)
    return redirect(url_for('index'))


@app.route('/search')
def search():
    q = request.args.get('q','')
    if q == '':
        flash('Enter keyword about photo, user or tag.', 'warning')
        return redirect(url_for('index'))
    all_pro_status = ProStatus.query.order_by(ProStatus.id).all()
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['ISSUES_PER_PAGE']
    pagination = Issue.query.whooshee_search(q).order_by(Issue.jira_id.desc()).paginate(page,per_page=per_page)
    issues = pagination.items
    return render_template('index.html',pagination=pagination,issues=issues,all_pro_status=all_pro_status)


@app.route('/export')
def export():
    query_sets = Issue.query.all()
    return excel.make_response_from_query_sets(
        query_sets,
        column_names=[
            'id',
            'key',
            'status',
            'pro_status_id',
            'created_time',
            'summary',
            'creator',
            'url',
            'ui_schedule',
            'back_schedule',
            'front_schedule',
            'test_schedule'
        ],
        file_type='xlsx',
        file_name='全部需求.xlsx'
    )


@app.route('/getnew')
def get_new():
    a = jira_get_new()
    return a

@app.route('/getallissuesAreYouSure')
def get_all():
    a = jira_get_all()
    return a














