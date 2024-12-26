class CVE(db.Model):
    id = db.Column(db.Integer,nullable=False,unique=True)
    cve_id = db.Column(db.String(100), nullable=False,primary_key=True)
    source_identifier = db.Column(db.String(100),nullable=False)
    published = db.Column(db.DateTime,nullable=False)
    last_modified = db.Column(db.DateTime,nullable=False)
    vuln_status = db.Column(db.String(100),nullable=False)
    score = db.Column(db.String)

class Details(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    cve_id = db.Column(db.String(100),db.ForeignKey('cve.cve_id'))
    description = db.Column(db.String(100),nullable=False)
    severity=db.Column(db.String(100),nullable=False)
    score = db.Column(db.String)
    exploitable_score = db.Column(db.String)
    impact_score = db.Column(db.String)
    vectorString = db.Column(db.String(100))
    access_vector = db.Column(db.String(100))
    authentication = db.Column(db.String(100))
    integrity_impact = db.Column(db.String(100))
    confidentiality_impact = db.Column(db.String(100))
    access_complexity = db.Column(db.String(100))
    availability_impact = db.Column(db.String(100))


with app.app_context():
    db.create_all()