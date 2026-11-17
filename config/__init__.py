import pymysql

# Django checks the driver's version number, so report a compatible one.
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()