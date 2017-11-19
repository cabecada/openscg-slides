---
title: PostgreSQL psql
---

# psql client

[$<]

* The native, command-line client to postgresql 

* Supports unix sockets and TCP/IP

* psql has many flags that control input, output and general modes

* Written in C and uses libpq to connect

[>$]

***

# psql client

[$<]

Some of the most common flags:
	
	-h      Hostname to connect to
	-p      port to connect to
	-U     (*capitalized)  user name to connect with 
	-d      Database to connect to

Also via environment variables: 

	-f       Execute a file against a database
	-c      Execute the command specificed --help 

You can configure psql to execute a set of commands on startup with the 

	$HOME/.psqlrc file  

[>$]

***

# psql client

[$<]

To connect:

	psql -h localhost -p 7777 -U postgres -d postgres

	$ psql
	psql (9.5.4)
	Type "help" for help.

	postgres=#

[>$]

***

# psql client

[$<]

The help options are very powerful  
\? provides help with psql specific options 

	postgres=# \?

\h provides context-specific help with SQL commands

	postgres=# \h ALTER ::tab:: ::tab::
	postgres=# \h ALTER SCHEMA

Command:     ALTER SCHEMA  
Description: change the definition of a schema

Syntax:

	ALTER SCHEMA name RENAME TO newname
	ALTER SCHEMA name OWNER TO newowner

[>$]

***

[$<]

# psql client

* Natively supports up / down arrow based history

* If libreadline / libedit is available full bash-style history search is available

* There are a number of backslash commands ( see \? ) available for controlling input, output and other behavior

[>$]

***

[$<]

# Create a test table

	create table people 
 		(id int, fname text, lname text);

	insert into people VALUES (1,'Scott','Mead'), 		(2,'Danielle','Renodin-Mead'),
		(3,'Amelia','Mead'),
		(4,'Charles','Mead'),
		(5,'Marley','Mead'),
		(6,'Howard','Mead');


[>$]

***

[$<]

# Describe the people table

To list tables:

	\dt+
	( Describe all tables with size ( + ) )

To describe a table:

	\d+ people

[>$]

***

[$<]

# psql client

* Make a CSV
	* Using the output control flags, we can easily make a CSV file
	* A standard query, returns 'aligned' output  

			postgres=# select * from people;  
id |  fname   |    lname
----+----------+--------------
  1 | Scott    | Mead
  2 | Danielle | Renodin-Mead
  3 | Amelia   | Mead
  4 | Charles  | Mead
  5 | Marley   | Mead
  6 | Howard   | Mead
(6 rows)

[>$]

***

[$<]

# psql client

Disabling 'aligned' output mode, you can specify a field-separator

	postgres=# \a

Output format is unaligned.

	postgres=# \f ,

Field separator is ",".

	postgres=# select * from people;

id |  fname   |    lname
----+----------+--------------
  1 | Scott    | Mead
  2 | Danielle | Renodin-Mead
  3 | Amelia   | Mead
  4 | Charles  | Mead
  5 | Marley   | Mead
  6 | Howard   | Mead
(6 rows)

You can also have psql redirect its output with the \o FILENAME command

[>$]

***

[$<]

# psql client

* \timing
	* Toggles concise timings on query execution

* Expanded output mode
	* When there is a lot of data to deal with ( i.e. screen wrap), expanded mode provides a clear view of what is what



			postgres=# select * from longchar ;
 
 id | dttm | msg
----+----------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  1 | 2013-07-11 10:22:44.244546 | =IF(ISERROR(INDEX($B$4:$B$100,SMALL(IF(D$4:D$100=$Q$13,ROW($B$4:$B$100)-ROW($B$4)+1),ROWS($P$17:P17))))," ",INDEX($B$4:$B$100,SMALL(IF(D$4:D$100=$Q$13,ROW($B$4:$B$100)-ROW($B$4)+1),ROWS($P$17:P17))))
(1 row)

[>$]

***

[$<]

# psql client

Becomes:

	postgres=# \x
	Expanded display is on.
	postgres=# select * from longchar ;

	[ RECORD1 ]
	
id | dttm | msg
----+----------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  1 | 2013-07-11 10:22:44.244546 | =IF(ISERROR(INDEX($B$4:$B$100,SMALL(IF(D$4:D$100=$Q$13,ROW($B$4:$B$100)-ROW($B$4)+1),ROWS($P$17:P17))))," ",INDEX($B$4:$B$100,SMALL(IF(D$4:D$100=$Q$13,ROW($B$4:$B$100)-ROW($B$4)+1),ROWS($P$17:P17))))
(1 row)

[>$]

***

[$<]

# psql client

### Query buffer:

* Psql maintains the last query in a buffer, this query can be modified, post-execution by invoking the editor ( controlled by the EDITOR environment variable )
* After running a query, use \e to open it in an editor
* Saving and closing will send the text in the editor back to postgres for execution
* \w FILENAME saves the query buffer to a file
* \s FILENAME saves the command history to a file

[>$]

***

[$<]

# psql client

Metadata commands:  
		
	\l   list databases
	\dt  describe tables
	\d <table>  describe a specific table
	\df   describe functions
	see \? for an exhaustive list
Each of these commands supports adding '+' at the end for expanded information

You can see how the metadata commands query the catalogs by launching psql with the -E flag

[>$]

***

[$<]

# psql client

	postgres=# \q
	[farrukh@localhost bigsql]$ psql -E
	psql (9.5.4)
	Type "help" for help.

	postgres=# \dt+
	
	********* QUERY **********
	SELECT n.nspname as "Schema",
 		c.relname as "Name",
  		CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized view' WHEN 	'i' THEN 'index' WHEN 'S'
  	THEN 'sequence' WHEN 's' THEN 'special' WHEN 'f' THEN 'foreign table' END as "Type",  
  		pg_catalog.pg_get_userbyid(c.relowner) as "Owner",
  		pg_catalog.pg_size_pretty(pg_catalog.pg_table_size(c.oid)) as "Size",
  		pg_catalog.obj_description(c.oid, 'pg_class') as "Description"
  	FROM pg_catalog.pg_class c
 		LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
 	WHERE c.relkind IN ('r','')  
		AND n.nspname <> 'pg_catalog'  
		AND n.nspname <> 'information_schema'  
  		AND n.nspname !~ '^pg_toast'  
  		AND pg_catalog.pg_table_is_visible(c.oid)
  	ORDER BY 1,2;
**************************
                    	
List of relations:
                    	
 Schema |   Name	| Type  |  Owner   |	Size	| Description
--------+-----------+-------+----------+------------+-------------
 public | employees | table | postgres | 8192 bytes |
(1 row)

	postgres=#

[>$]

***

[$<]

# psql client

### Interacting with the OS

* You can execute commands in the parent shell from psql by using the \! COMMAND:
	 
		postgres=# \! pwd

* Change the working directory:

		postgres=# \cd <directory>

* Execute a file
	
		postgres=# \i /path/to/file.sql

[>$]

***

[$<]

# SET Parameters

* \SET [parameter] {value}
* [parameter] {value} in ~/.psqlrc file

* Example Parameters:

		AUTOCOMMIT 
		DBNAME. 
		ECHO 
		ECHO_HIDDEN
		ON_ERROR_ROLLBACK
		ON_ERROR_STOP
		PROMPT1
		PROMPT2
		PROMPT3

[>$]

***

[$<]

# Watching Queries

1. First, execute a query

		SELECT count(*) from pg_stat_activity;

2. \watch 2

Replays the query at a specific interval

[>$]

***

[$<]

# Lab Exercise 1

Use the psql meta-data commands to see a list of all of the tables in the gnb database.  

((\dt+))

[>$]

***

[$<]

# Lab Exercise 2

Setup a simple monitor to show the total balance of all of the branches every 30 seconds.

((Select sum(bbalance) FROM pgbench_branches;))

[>$]