---
title: PostgreSQL System Catalogs
---

# Catalog

[$<]

* The postgres system catalog (pg_catalog) contains a number of tables, views and functions that are used internally by postgres to keep order of the database structure.
* 
* They can be categorized as
	* Structural 
		* Tables that postgres uses to manage the RDBMS
	* Informational
		* Functions / tables that can be used to view table size, monitor activity, etc...
	* Performance
		* Functions / tables that can be used to monitor performance statistics about queries, tables, indexes, etc…

[>$]

***

# pg_catalog Tables

[$<]

* pg_aggregate
* pg_am
* pg_amop
* pg_amproc
* pg_attrdef
* pg_attribute
* pg_auth_members
* pg_authid
* pg_cast
* pg_class
* pg_collation
* pg_constraint
* pg_conversion
* pg_database
* pg_db_role_setting
* pg_default_acl
* pg_depend
* pg_description
* pg_enum
* pg_event_trigger
* pg_extension
* pg_foreign_data_wrapper
* pg_foreign_server
* pg_foreign_table
* pg_index
* pg_inherits
* pg_language
* pg_largeobject

[>$]

***

# pg_catalog Tables

[$<]

* pg_largeobject_metadata
* pg_namespace
* pg_opclass
* pg_operator
* pg_opfamily
* pg_pltemplate
* pg_policy
* pg_proc
* pg_range
* pg_replication_origin
* pg_rewrite
* pg_seclabel
* pg_shdepend
* pg_shdescription
* pg_shseclabel
* pg_statistic
* pg_tablespace
* pg_transform
* pg_trigger
* pg_ts_config
* pg_ts_config_map
* pg_ts_dict
* pg_ts_parser
* pg_ts_template
* pg_type
* pg_user_mapping

[>$]

***

# pg_catalog Views

[$<]

* pg_available_extension_versions
* pg_available_extensions
* pg_cursors
* pg_file_settings
* pg_group
* pg_indexes
* pg_locks
* pg_matviews
* pg_policies
* pg_prepared_statements
* pg_prepared_xacts
* pg_replication_origin_status
* pg_replication_slots
* pg_roles
* pg_rules
* pg_seclabels
* pg_settings
* pg_shadow
* pg_stat_activity
* pg_stat_all_indexes
* pg_stat_all_tables
* pg_stat_archiver
* pg_stat_bgwriter
* pg_stat_database
* pg_stat_database_conflicts
* pg_stat_replication

[>$]

***

# pg_catalog Views

[$<]

* pg_stat_ssl
* pg_stat_sys_indexes
* pg_stat_sys_tables
* pg_stat_user_functions
* pg_stat_user_indexes
* pg_stat_user_tables
* pg_stat_xact_all_tables
* pg_stat_xact_sys_tables
* pg_stat_xact_user_functions
* pg_stat_xact_user_tables
* pg_statio_all_indexes
* pg_statio_all_sequences
* pg_statio_all_tables
* pg_statio_sys_indexes
* pg_statio_sys_sequences
* pg_statio_sys_tables
* pg_statio_user_indexes
* pg_statio_user_sequences
* pg_statio_user_tables
* pg_stats
* pg_tables
* pg_timezone_abbrevs
* pg_timezone_names
* pg_user
* pg_user_mappings
* pg_views

[>$]

***

# Object Identifiers (OID)

[$<]

###Each system object has a hidden Object Identifier

	gnb=# \d pg_namespace
	 Table "pg_catalog.pg_namespace"
	  Column  |   Type    | Modifiers 
	----------+-----------+-----------
	 nspname  | name      | not null
	 nspowner | oid       | not null
	 nspacl   | aclitem[] | 
	Indexes:
	    "pg_namespace_nspname_index" UNIQUE, btree (nspname)
	    "pg_namespace_oid_index" UNIQUE, btree (oid)
	
	gnb=# select oid, * from pg_namespace;
	  oid  |      nspname       | nspowner |        nspacl        
	-------+--------------------+----------+----------------------
	    99 | pg_toast           |       10 | 
	 11310 | pg_temp_1          |       10 | 
	 11311 | pg_toast_temp_1    |       10 | 
	    11 | pg_catalog         |       10 | {jim=UC/jim,=U/jim}
	  2200 | public             |       10 | {jim=UC/jim,=UC/jim}
	 11613 | information_schema |       10 | {jim=UC/jim,=U/jim}
	(6 rows)

[>$]

***

# Finding Relationships

[$<]

Use the -E option to echo psql meta data queries

	$ ./psql -E gnb
	psql (9.4beta1)
	Type "help" for help.
	
	gnb=# \dt
	********* QUERY **********
	SELECT n.nspname as "Schema",
	  c.relname as "Name",
	  CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'm' 
	THEN 'materialized view' WHEN 'i' THEN 'index' WHEN 'S' 
	THEN 'sequence' WHEN 's' THEN 'special' WHEN 'f' 
	THEN 'foreign table' END as "Type",
	  pg_catalog.pg_get_userbyid(c.relowner) as "Owner"
	FROM pg_catalog.pg_class c
	     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
	WHERE c.relkind IN ('r','')
	      AND n.nspname <> 'pg_catalog'
	      AND n.nspname <> 'information_schema'
	      AND n.nspname !~ '^pg_toast'
	  AND pg_catalog.pg_table_is_visible(c.oid)
	ORDER BY 1,2;
	**************************

[>$]

***

# Server Signaling Functions

[$<]

* pg_cancel_backend(pid int)
* pg_reload_conf()
* pg_rotate_logfile()
* pg_terminate_backend(pid int)

[>$]

***

# Backup Control Functions

[$<]

* pg_create_restore_point(name text)
* pg_current_xlog_insert_location()
* pg_current_xlog_location()
* pg_start_backup(label text [, fast boolean ])
* pg_stop_backup()
* pg_is_in_backup()
* pg_backup_start_time()
* pg_switch_xlog()
* pg_xlogfile_name(location text)
* pg_xlogfile_name_offset(location text)
* pg_xlog_location_diff(location text, location text)

[>$]

***

# Object Management Functions

[$<]

* pg_column_size(any)
* pg_database_size(oid)
* pg_database_size(name)
* pg_indexes_size(regclass)
* pg_relation_size(relation regclass)
* pg_size_pretty(bigint)
* pg_size_pretty(numeric)
* pg_table_size(regclass)
* pg_tablespace_size(oid)
* pg_tablespace_size(name)
* pg_total_relation_size(regclass)

[>$]

***

# Lab Exercise 1

[$<

GNB needs a few daily reports on system health.  We're going to implement a few:

* Write a query to get the total size of all tables in a database
* Write a query to show the schema, table and size of all tables, ( largest table to smallest table )

[>$]

((

DB Size:

 \l+
 select pg_size_pretty(pg_database_size('gnb'));
select pg_size_pretty(sum(pg_total_relation_size(schemaname || '.' || relname) ) ) from pg_stat_user_tables;

select pg_size_pretty(sum(pg_total_relation_size(schemaname || '.' || relname) ) ) from pg_stat_all_tables;

Tables:
Select schemaname, relname,pg_total_relation_size(schemaname || '.' || relname) rawsize,                                  pg_size_pretty(pg_total_relation_size(schemaname || '.' || relname) ) from pg_stat_user_tables ORDER BY rawsize DESC;

))

***

# Lab Exercise 2

[$<

GNB is having a performance problem on their system.  After monitoring the system, you find some long-running queries. 

* Write a query to forcefully disconnect any session in the database

[>$

(( 
 
1) Find the query:

  Select * from pg_stat_activity ; 

Select pid from pg_stat_activity where ….. ; 

Select pg_terminate_backend(<pid> ) ; 

2) Advanced: 

Select pg_terminate_backend(pid) 
   FROM pg_stat_activity WHERE….  
   
))
