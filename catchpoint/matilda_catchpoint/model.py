from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

from matilda_catchpoint import config_reader as cr

base = declarative_base()

class Catchpoint(base):
    __tablename__ = cr.get_lookup_data('DATABASE', 'catchpoint_table')

    report_time = Column(String)
    processing_time = Column(String)
    level_id = Column(String)
    level_name = Column(String)
    test_id = Column(String)
    test_name = Column(String)
    test_description = Column(String)
    test_link = Column(String)
    test_perf_url = Column(String)
    test_waterfall_url = Column(String)
    test_type_id = Column(String)
    test_type_name = Column(String)
    alert_type_id = Column(String)
    alert_type_name = Column(String)
    alert_subtype_id = Column(String)
    alert_subtype_name = Column(String)
    trigger_type_id = Column(String)
    trigger_type_name = Column(String)
    operation_type_id = Column(String)
    operation_type_name = Column(String)
    acknowledged_by_id = Column(String)
    acknowledged_by_name = Column(String)
    node = Column(String)
    company = Column(String)
    vsad = Column(String)
    prod_name = Column(String)
    node_ip = Column(String)
    node_host_ip = Column(String)
    error = Column(String)
    cause = Column(String)
