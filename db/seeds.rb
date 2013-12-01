# ruby encoding: utf-8
# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([ name: 'Chicago' ,  name: 'Copenhagen' ])
#   Mayor.create(name: 'Emanuel', city: cities.first)

User.create( username: 'Stephen', password: 'admin' )

Log.create( name: 'Test Log', user_id: 1)

Entry.create(log_id: 1, date: '2011-11-15', time: '15:31:16', protocol: 'tcp', conn_type: '-',
		   src_port: 21439, dest_port: 445, src_ip: '209.13.97.38', dest_ip: '10.250.40.42',
		   info: '48 S', environment: 'Windows XP SP1')

