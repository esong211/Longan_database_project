#!/usr/bin/env python
import os
import sys
from django.db import connection

"""                 *** DO NOT TOUCH ***
    def insert():
        attends(companyID, cfID)
        hostedBy(cfID, schoolID)
        recruitedBy(schoolID, companyID)

        with connection.cursor() as cursor:
            #SAMPLE QUERIES
            #cursor.execute("INSERT INTO <table_name>(att1,att2) VALUES (val1,val2)")
            #cursor.execute("DELETE FROM <table_name> WHERE <att1>=<val1>")
            #cursor.execute("UPDATE <table_name> <att1> = <val1> WHERE <att2> = <val2>")

            #cursor.execute("INSERT INTO recruitedBy SELECT schoolID,companyID FROM attends,hostedBy WHERE attends.cfID = hostedBy.cfID")
"""

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Longan.settings")
    try:    # NOTE: NEED TO CALL IN TRY
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
