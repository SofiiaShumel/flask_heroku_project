import os

#
# username = 'qhsmovulrcixsq'
# password = '4de2d87cc269e6e20a3b9d3a3cafd5b28eb5deb674a965ccb74db00dffc5e9f8'
# host = 'ec2-174-129-255-11.compute-1.amazonaws.com'
# port = '5432'
# database = 'dd8urtd5qotins'
#
#
# DATABASE_URI = os.getenv("DATABASE_URL", 'postgres://qhsmovulrcixsq:4de2d87cc269e6e20a3b9d3a3cafd5b28eb5deb674a965ccb74db00dffc5e9f8@ec2-174-129-255-11.compute-1.amazonaws.com:5432/dd8urtd5qotins')
username = 'postgres'
password = 'edcpolo'
host = 'localhost'
database = 'DB'

DATABASE_URI = os.getenv("DATABASE_URL", 'postgresql://postgres:edcpolo@localhost/DB')