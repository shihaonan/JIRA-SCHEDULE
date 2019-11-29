from app import db
from app.models import ProStatus

def init():
    pro_status = ProStatus.query.first()
    if not pro_status:
        print('Creating the default pro_status...')
        pro_status1 = ProStatus(name='原型设计')
        pro_status2 = ProStatus(name='待技术评审')
        pro_status3 = ProStatus(name='待排期')
        pro_status4 = ProStatus(name='开发中')
        pro_status5 = ProStatus(name='测试中')
        pro_status6 = ProStatus(name='已上线')
        pro_status7 = ProStatus(name='已暂停')
        pro_status8 = ProStatus(name='遗留')
        db.session.add(pro_status1)
        db.session.add(pro_status2)
        db.session.add(pro_status3)
        db.session.add(pro_status4)
        db.session.add(pro_status5)
        db.session.add(pro_status6)
        db.session.add(pro_status7)
        db.session.add(pro_status8)
        db.session.commit()


# 需要在上下文环境中执行
