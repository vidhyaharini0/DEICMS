from datetime import datetime, timezone
from app import db
from app.utils import now_local

class CustodyLog(db.Model):
    """
    Records every custody event for an evidence item.
    This table is the backbone of the chain-of-custody system.
    Once a record is written, it should never be modified or deleted.
    """
    __tablename__ = 'custody_logs'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Which evidence item this log entry belongs to
    evidence_id = db.Column(db.Integer, db.ForeignKey('evidence_items.id'), nullable=False)

    # Type of custody event.
    # Behaviour note: the application writes 'Upload' (at registration) and
    # 'Transfer' (on custody hand-off). 'Access' and 'Verification' are RESERVED
    # values - file-access and integrity-verification events are recorded in the
    # AuditRecord table (the append-only audit trail), NOT as custody-graph
    # nodes, so that the custody chain stays a clean sequence of ownership
    # hand-offs. They are kept in the enum for forward-compatibility should
    # access ever be promoted to a first-class custody node.
    event_type = db.Column(db.Enum('Upload', 'Transfer', 'Access', 'Verification', name='custody_event_type'), nullable=False)

    # Who transferred FROM (Null for the initial upload event)
    from_investigator_id = db.Column(db.Integer, db.ForeignKey('investigators.id'), nullable=True)
    # Who transferred TO (null for access-only events)
    to_investigator_id = db.Column(db.Integer, db.ForeignKey('investigators.id'), nullable=True)

    # When and where the event happened.
    # Convention: the whole system stores NAIVE local timestamps produced by
    # app.utils.now_local() (a single source of truth for the local offset).
    # This default previously used tz-aware UTC, which made comparisons against
    # the naive local timestamps elsewhere raise "can't compare offset-naive
    # and offset-aware datetimes" and introduced a silent offset. It now matches
    # every other model so the graph verifier's timestamp-monotonicity check and
    # the risk scorer never mix aware and naive values.
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: now_local())
    location = db.Column(db.String(200), nullable=True)

    # Why the transfer or access happened
    reason = db.Column(db.Text, nullable=True)

    # SHA-256 hash of the evidence file at the moment of this event
    # Used by the Graph Integrity Verification Algorithm to verify the chain
    file_hash_at_event = db.Column(db.String(64), nullable=False)

    # Ed25519 digital signature of this custody record
    # Signed by the from_investigator (or uploader for Upload events)
    digital_signature = db.Column(db.Text, nullable=False)

    # Optional notes about the event
    notes = db.Column(db.Text, nullable=True)

    #  Relationships 
    from_investigator = db.relationship('Investigator', foreign_keys=[from_investigator_id], backref='transfers_sent')
    to_investigator = db.relationship('Investigator', foreign_keys=[to_investigator_id], backref='transfers_received')

    def __repr__(self):
        return (f'<CustodyLog evidence={self.evidence_id} '
                f'event={self.event_type} at={self.timestamp}>')
