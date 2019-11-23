from app import app,db
from app.models import Issue,ProStatus
from flask import jsonify,render_template,url_for,request,current_app,redirect,flash
from app.assist import jira_get_new,jira_get_all
from app.forms import ScheduleForm
import flask_excel as excel

@app.route('/')
def index():
    last_search = None
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['ISSUES_PER_PAGE']
    pagination = Issue.query.order_by(Issue.jira_id.desc()).paginate(page,per_page=per_page)
    issues = pagination.items
    return render_template('index.html',pagination=pagination,issues=issues,last_search=last_search)

# 项目状态分类视图
@app.route('/project_status/<int:pro_status_id>')
def project_status(pro_status_id):
    last_search = None
    pro_status = ProStatus.query.get_or_404(pro_status_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ISSUES_PER_PAGE']
    pagination = Issue.query.with_parent(pro_status).order_by(Issue.jira_id.desc()).paginate(page, per_page=per_page)
    issues = pagination.items
    form = ScheduleForm()
    return render_template('index.html', pagination=pagination, issues=issues, form=form,pro_status=pro_status,last_search = last_search)


@app.route('/showform/<int:issue_id>')
def show_form(issue_id):
    all_pro_status = ProStatus.query.order_by(ProStatus.id).all()
    issue = Issue.query.get_or_404(issue_id)
    form = ScheduleForm()
    form.pro_status.data = issue.pro_status_id
    form.ui_schedule.data = issue.ui_schedule
    form.back_schedule.data = issue.back_schedule
    form.front_schedule.data = issue.front_schedule
    form.test_schedule.data = issue.test_schedule
    return jsonify(html=render_template('_form.html', form=form,issue=issue,all_pro_status=all_pro_status))


@app.route('/ajaxedit/<int:issue_id>',methods=['POST'])
def ajax_edit(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    pro_status = request.form.get('pro_status')
    if len(pro_status)>0:
        issue.pro_status_id = int(pro_status)
    issue.ui_schedule = request.form.get("ui_schedule")
    issue.back_schedule = request.form.get('back_schedule')
    issue.front_schedule = request.form.get('front_schedule')
    issue.test_schedule = request.form.get('test_schedule')
    issue.ui_staff = request.form.get("ui_staff")
    issue.back_staff = request.form.get('back_staff')
    issue.front_staff = request.form.get('front_staff')
    issue.test_staff = request.form.get('test_staff')
    db.session.commit()
    flash('%s %s 操作成功' % (issue.key,issue.summary))
    if issue.pro_status_id:
        callback_pro_status = issue.pro_status.name
    else:
        callback_pro_status = ''
    return jsonify(pro_status=callback_pro_status,
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


@app.route('/multisearch')
def multi_search():
    condition = []
    jira_key = request.args.get('jira_key', '')
    summary = request.args.get('summary', '')
    pm = request.args.get('pm', '')
    jira_status = request.args.get('jira_status', '')
    pro_status = request.args.get('pro_status', '')
    if jira_key:
        condition.append(Issue.key.like('%'+jira_key+'%'))
    if summary:
        condition.append(Issue.summary.like('%'+summary+'%'))
    if pm:
        condition.append(Issue.creator == pm)
    if jira_status:
        condition.append(Issue.status == jira_status)
    if pro_status:
        pro_status=int(pro_status)
        condition.append(Issue.pro_status_id == pro_status)
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['ISSUES_PER_PAGE']
    pagination = Issue.query.filter(*condition).order_by(Issue.jira_id.desc()).paginate(page,per_page=per_page)
    issues = pagination.items
    if not issues:
        flash('找不到数据')
    last_search = {'jira_key':jira_key,'summary':summary,'pm':pm,'jira_status':jira_status,'pro_status':pro_status}
    return render_template('index.html',pagination=pagination,issues=issues,last_search=last_search)


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














