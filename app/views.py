from app import app,db
from app.models import Issue,ProStatus,Post
from flask import jsonify,render_template,url_for,request,current_app,redirect,flash
from app.assist import jira_get_new,jira_get_all
import flask_excel as excel
from app.forms import PostForm,CreateBigIssueForm

@app.route('/')
def index():
    last_search = None
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['ISSUES_PER_PAGE']
    pagination = Issue.query.order_by(Issue.jira_id.desc()).paginate(page,per_page=per_page)
    issues = pagination.items
    # db.session.close()
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
    return render_template('index.html', pagination=pagination, issues=issues,pro_status=pro_status,last_search = last_search)


@app.route('/showform/<int:issue_id>')
def show_form(issue_id):
    all_pro_status = ProStatus.query.order_by(ProStatus.id).all()
    issue = Issue.query.get_or_404(issue_id)
    return jsonify(html=render_template('_form.html',issue=issue,all_pro_status=all_pro_status))


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
    msg = '%s 已更新' % issue.key
    if issue.pro_status_id:
        callback_pro_status = issue.pro_status.name
    else:
        callback_pro_status = ''
    return jsonify(pro_status=callback_pro_status,
                   ui_schedule=issue.ui_schedule,
                   back_schedule=issue.back_schedule,
                   front_schedule=issue.front_schedule,
                   test_schedule=issue.test_schedule,
                   msg=msg
                   )


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
    msg = jira_get_new()
    return jsonify(msg=msg)


@app.route('/getallissuesAreYouSure')
def get_all():
    a = jira_get_all()
    return a


@app.route('/readme')
def readme():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    main_post = Post.query.get_or_404(1)
    return render_template('post.html',posts=posts,main_post=main_post)


@app.route('/newpost',methods=['GET','POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        body = form.body.data
        body_html = form.body_html.data
        post = Post(body=body,body_html=body_html)
        db.session.add(post)
        db.session.commit()
        flash('文章发布成功')
        return redirect(url_for('readme'))
    return render_template('edit_post.html',form=form)


@app.route('/editpost/<int:post_id>',methods=['GET','POST'])
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.body = form.body.data
        post.body_html = form.body_html.data
        db.session.commit()
        flash('文章更新成功')
        return redirect(url_for('readme'))
    form.body.data = post.body
    form.body_html.data = post.body_html
    return render_template('edit_post.html', form=form)


# @app.route('/showform/<int:issue_id>')
# def show_form(issue_id):
#     all_pro_status = ProStatus.query.order_by(ProStatus.id).all()
#     issue = Issue.query.get_or_404(issue_id)
#     return jsonify(html=render_template('_form.html',issue=issue,all_pro_status=all_pro_status))


@app.route('/create_pro',methods=['GET','POST'])
def create_pro():
    return render_template('creat_pro.html')


@app.route('/handle_big_pro',methods=['POST'])
def handle_big_pro():
    summary = request.form.get('summary')
    creator = request.form.get('pm')
    pro_status = request.form.get('pro_status')
    if len(pro_status) > 0:
        pro_status_id = int(pro_status)
    ui_schedule = request.form.get("ui_schedule")
    back_schedule = request.form.get('back_schedule')
    front_schedule = request.form.get('front_schedule')
    test_schedule = request.form.get('test_schedule')
    ui_staff = request.form.get("ui_staff")
    back_staff = request.form.get('back_staff')
    front_staff = request.form.get('front_staff')
    test_staff = request.form.get('test_staff')
    is_pro = 1
    big_pro = Issue(summary=summary,creator=creator,pro_status_id=pro_status_id,ui_schedule=ui_schedule,back_schedule=back_schedule,
                    front_schedule=front_schedule,test_schedule=test_schedule,ui_staff=ui_staff,back_staff=back_staff,
                    front_staff=front_staff,test_staff=test_staff,is_pro=is_pro)
    db.session.add(big_pro)
    db.session.commit()
    msg = '%s 已更新' % summary
    flash('大项目：%s 创建成功' % summary)
    return redirect(url_for('big_pro'))

# 大项目视图
@app.route('/big_pro')
def big_pro():
    last_search = None
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ISSUES_PER_PAGE']
    pagination = Issue.query.filter_by(is_pro=1).order_by(Issue.created_time.desc()).paginate(page, per_page=per_page)
    issues = pagination.items
    return render_template('index.html', pagination=pagination, issues=issues,last_search = last_search)








