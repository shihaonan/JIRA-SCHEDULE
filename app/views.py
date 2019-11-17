from app import app,db
from app.models import Issue
from flask import jsonify,render_template,url_for,request,current_app,redirect,flash
from app.assist import jira,jira_connect
from app.forms import ScheduleForm

@app.route('/')
def index():
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['ISSUES_PER_PAGE']
    pagination = Issue.query.paginate(page,per_page=per_page)
    issues = pagination.items
    form = ScheduleForm()
    return render_template('index.html',pagination=pagination,issues=issues,form=form)

@app.route('/showform/<int:issue_id>')
def show_form(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    form = ScheduleForm()
    form.ui_schedule.data = issue.ui_schedule
    form.back_schedule.data = issue.back_schedule
    form.front_schedule.data = issue.front_schedule
    form.test_schedule.data = issue.test_schedule
    return jsonify(html=render_template('_form.html', form=form,issue=issue))


@app.route('/edit/<int:issue_id>',methods=['POST'])
def edit(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    form = ScheduleForm()
    if form.validate_on_submit():
        issue.ui_schedule = form.ui_schedule.data
        issue.back_schedule = form.back_schedule.data
        issue.front_schedule = form.front_schedule.data
        issue.test_schedule = form.test_schedule.data
        db.session.commit()
        flash('%s 排期成功' % issue.key)
        return redirect(url_for('index'))
    return redirect(url_for('index'))










@app.route('/assist')
def assist():
    jira_connect()
    return 'done'