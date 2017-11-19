---
title: PostgreSQL Locking
---

# Lock Types

[$<]

* ACCESS SHARE
* ROW SHARE
* ROW EXCLUSIVE
* SHARE UPDATE EXCLUSIVE
* SHARE
* SHARE ROW EXCLUSIVE
* EXCLUSIVE
* ACCESS EXCLUSIVE

[>$]

***

# Virtual XID

[$<]

	postgres=# SELECT virtualtransaction AS vxid,
	postgres-#        transactionid::text
	postgres-#   FROM pg_locks
	postgres-#  WHERE pid = pg_backend_pid()
	postgres-#  ORDER BY 1, 2
	postgres-#  LIMIT 1;
	  vxid  | transactionid 
	--------+---------------
	 2/4657 | 
	(1 row)

2 is the backend slot number, and 4657 is the virtual transaction id for this slot.

[>$]

***

# Virtual XIDs increment

[$<]

	postgres=# SELECT virtualtransaction AS vxid, 
	postgres-#        transactionid::text
	postgres-#   FROM pg_locks
	postgres-#  WHERE pid = pg_backend_pid()
	postgres-#  ORDER BY 1, 2
	postgres-#  LIMIT 1;
	  vxid  | transactionid 
	--------+---------------
	 2/4657 | 
	(1 row)
	
	postgres=# SELECT virtualtransaction AS vxid, 
	postgres-#        transactionid::text
	postgres-#   FROM pg_locks
	postgres-#  WHERE pid = pg_backend_pid()
	postgres-#  ORDER BY 1, 2
	postgres-#  LIMIT 1;
	  vxid  | transactionid 
	--------+---------------
	 2/4658 | 
	(1 row)

[>$]

***

# Getting a Real XID

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# SELECT virtualtransaction AS vxid, 
	postgres-#        transactionid::text
	postgres-#   FROM pg_locks
	postgres-#  WHERE pid = pg_backend_pid()
	postgres-#  ORDER BY 1, 2
	postgres-#  LIMIT 1;
	  vxid  | transactionid 
	--------+---------------
	 2/4659 | 
	(1 row)
	
	postgres=# ANALYZE foo;
	ANALYZE

[>$]

***

# Getting a Real XID

[$<]

	postgres=# SELECT virtualtransaction AS vxid, 
	postgres-#        transactionid::text
	postgres-#   FROM pg_locks
	postgres-#  WHERE pid = pg_backend_pid()
	postgres-#  ORDER BY 1, 2
	postgres-#  LIMIT 1;
	  vxid  | transactionid 
	--------+---------------
	 2/4659 | 8504
	(1 row)
	
	postgres=# SELECT txid_current();
	 txid_current 
	--------------
	         8504
	(1 row)
	
	postgres=# COMMIT;
	COMMIT

[>$]

***

# ACCESS SHARE Locking

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# LOCK TABLE foo IN ACCESS SHARE MODE;
	LOCK TABLE
	
	
	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l, pg_class c
	postgres-#  WHERE l.relation = c.oid
	postgres-#    AND l.pid != pg_backend_pid()
	postgres-#    AND c.relname NOT LIKE 'pg_%'
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid | locktype |      mode       
	---------+--------+---------------+----------+-----------------
	 foo     | 2/4662 |               | relation | AccessShareLock
	(1 row)

[>$]

***

# ACCESS SHARE Locking

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# SELECT COUNT(*) FROM foo;
	 count 
	-------
	     2
	(1 row)
	
	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l, pg_class c
	postgres-#  WHERE l.relation = c.oid
	postgres-#    AND l.pid != pg_backend_pid()
	postgres-#    AND c.relname NOT LIKE 'pg_%'
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid | locktype |      mode       
	---------+--------+---------------+----------+-----------------
	 foo     | 2/4663 |               | relation | AccessShareLock
	(1 row)

[>$]

***

# Multi-table ACCESS SHARE Locking

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# SELECT count(*)
	postgres-#   FROM foo JOIN bar ON (b1 = f1);
	 count 
	-------
	     2
	(1 row)
	
	
	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l, pg_class c
	postgres-#  WHERE l.relation = c.oid
	postgres-#    AND l.pid != pg_backend_pid()
	postgres-#    AND c.relname NOT LIKE 'pg_%'
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid | locktype |      mode       
	---------+--------+---------------+----------+-----------------
	 bar     | 2/4672 |               | relation | AccessShareLock
	 foo     | 2/4672 |               | relation | AccessShareLock
	(2 rows)

[>$]

***

# ROW SHARE Locking

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# LOCK TABLE foo IN ROW SHARE MODE;
	LOCK TABLE
	
	
	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l, pg_class c
	postgres-#  WHERE l.relation = c.oid
	postgres-#    AND l.pid != pg_backend_pid()
	postgres-#    AND c.relname NOT LIKE 'pg_%'
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid | locktype |     mode     
	---------+--------+---------------+----------+--------------
	 foo     | 2/4673 |               | relation | RowShareLock
	(1 row)

[>$]

***

# ROW SHARE Locking

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# SELECT * FROM foo FOR SHARE;
	 f1 
	----
	 41
	 42
	(2 rows)
	
	
	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l, pg_class c
	postgres-#  WHERE l.relation = c.oid
	postgres-#    AND l.pid != pg_backend_pid()
	postgres-#    AND c.relname NOT LIKE 'pg_%'
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid | locktype |     mode     
	---------+--------+---------------+----------+--------------
	 foo     | 2/4674 |               | relation | RowShareLock
	(1 row)
	
[>$]

***

# ROW EXCLUSIVE Locking

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# LOCK TABLE foo IN ROW EXCLUSIVE MODE;
	LOCK TABLE
	
	
	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l, pg_class c
	postgres-#  WHERE l.relation = c.oid
	postgres-#    AND l.pid != pg_backend_pid()
	postgres-#    AND c.relname NOT LIKE 'pg_%'
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid | locktype |       mode       
	---------+--------+---------------+----------+------------------
	 foo     | 2/4675 |               | relation | RowExclusiveLock
	(1 row)
	
[>$]

***

# ROW EXCLUSIVE Locking

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# DELETE FROM foo;
	DELETE 2
	
	
	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l LEFT OUTER JOIN pg_class c 
	postgres-#     ON (l.relation = c.oid)
	postgres-#  WHERE l.pid != pg_backend_pid();
	 relname |  vxid  | transactionid |   locktype    |       mode       
	---------+--------+---------------+---------------+------------------
	         | 2/4676 | 8508          | transactionid | ExclusiveLock
	 foo     | 2/4676 |               | relation      | RowExclusiveLock
	         | 2/4676 |               | virtualxid    | ExclusiveLock
	(3 rows)

[>$]

***

# SHARE UPDATE EXCLUSIVE Locking

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# LOCK TABLE foo IN SHARE UPDATE EXCLUSIVE MODE;
	LOCK TABLE
	
	
	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l LEFT OUTER JOIN pg_class c 
	postgres-#     ON (l.relation = c.oid)
	postgres-#  WHERE l.pid != pg_backend_pid()
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid |  locktype  |           mode           
	---------+--------+---------------+------------+--------------------------
	 foo     | 2/4679 |               | relation   | ShareUpdateExclusiveLock
	         | 2/4679 |               | virtualxid | ExclusiveLock
	(2 rows)

[>$]

***

# SHARE Locking

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# LOCK TABLE foo IN SHARE MODE;
	LOCK TABLE
	
	
	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l LEFT OUTER JOIN pg_class c 
	postgres-#     ON (l.relation = c.oid)
	postgres-#  WHERE l.pid != pg_backend_pid()
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid |  locktype  |     mode      
	---------+--------+---------------+------------+---------------
	 foo     | 2/4681 |               | relation   | ShareLock
	         | 2/4681 |               | virtualxid | ExclusiveLock
	(2 rows)

[>$]

***

# SHARE Locking

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# CREATE UNIQUE INDEX foo_idx ON foo(f1);
	CREATE INDEX
	
	
	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l LEFT OUTER JOIN pg_class c 
	postgres-#     ON (l.relation = c.oid)
	postgres-#  WHERE l.pid != pg_backend_pid()
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid |   locktype    |        mode         
	---------+--------+---------------+---------------+---------------------
	 foo     | 2/4682 |               | relation      | AccessShareLock
	 foo     | 2/4682 |               | relation      | ShareLock
	         | 2/4682 | 8511          | transactionid | ExclusiveLock
	         | 2/4682 |               | relation      | AccessExclusiveLock
	         | 2/4682 |               | virtualxid    | ExclusiveLock
	(5 rows)

[>$]

***

# ACCESS EXCLUSIVE Locking

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# LOCK TABLE foo IN ACCESS EXCLUSIVE MODE;
	LOCK TABLE
	
	
	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l LEFT OUTER JOIN pg_class c 
	postgres-#     ON (l.relation = c.oid)
	postgres-#  WHERE l.pid != pg_backend_pid()
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid |  locktype  |        mode         
	---------+--------+---------------+------------+---------------------
	 foo     | 2/4684 |               | relation   | AccessExclusiveLock
	         | 2/4684 |               | virtualxid | ExclusiveLock
	(2 rows)

[>$]

***

# ACCESS EXCLUSIVE Locking

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# DROP TABLE foo;
	DROP TABLE
	
	
	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l LEFT OUTER JOIN pg_class c 
	postgres-#     ON (l.relation = c.oid)
	postgres-#  WHERE l.pid != pg_backend_pid()
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid |   locktype    |        mode         
	---------+--------+---------------+---------------+---------------------
	 foo     | 2/4685 |               | relation      | AccessExclusiveLock
	         | 2/4685 | 8513          | transactionid | ExclusiveLock
	         | 2/4685 |               | object        | AccessExclusiveLock
	         | 2/4685 |               | virtualxid    | ExclusiveLock
	         | 2/4685 |               | object        | AccessExclusiveLock
	(5 rows)

[>$]

***

# Locking Examples

[$<]

[>$]

***

# Rows Locks Are Not Visible

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# INSERT INTO foo VALUES (43), (44);
	INSERT 0 2
	
	
	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l LEFT OUTER JOIN pg_class c 
	postgres-#     ON (l.relation = c.oid)
	postgres-#  WHERE l.pid != pg_backend_pid()
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid |   locktype    |       mode       
	---------+--------+---------------+---------------+------------------
	 foo     | 2/4688 |               | relation      | RowExclusiveLock
	         | 2/4688 | 8515          | transactionid | ExclusiveLock
	         | 2/4688 |               | virtualxid    | ExclusiveLock
	(3 rows)

[>$]

***

# Updates Cause Index Locks

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# UPDATE foo SET f1=41 WHERE f1=41;
	UPDATE 1
	
	
	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l LEFT OUTER JOIN pg_class c 
	postgres-#     ON (l.relation = c.oid)
	postgres-#  WHERE l.pid != pg_backend_pid()
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid |   locktype    |       mode       
	---------+--------+---------------+---------------+------------------
	 foo     | 2/4689 |               | relation      | RowExclusiveLock
	 foo_idx | 2/4689 |               | relation      | RowExclusiveLock
	         | 2/4689 | 8516          | transactionid | ExclusiveLock
	         | 2/4689 |               | virtualxid    | ExclusiveLock
	(4 rows)

[>$]

***

# SELECT and UPDATE Don't Block

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# SELECT COUNT(*) FROM foo;
	 count 
	-------
	     2
	(1 row)
	
	--------------------------------------------------------
	postgres=# BEGIN;
	BEGIN
	postgres=# UPDATE foo SET f1=41 WHERE f1=41;
	UPDATE 1

[>$]

***

# SELECT and UPDATE Don't Block

[$<]

	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l LEFT OUTER JOIN pg_class c 
	postgres-#     ON (l.relation = c.oid)
	postgres-#  WHERE l.pid != pg_backend_pid()
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid |   locktype    |       mode       
	---------+--------+---------------+---------------+------------------
	 foo     | 2/4691 |               | relation      | AccessShareLock
	 foo     | 4/765  |               | relation      | RowExclusiveLock
	 foo_idx | 2/4691 |               | relation      | AccessShareLock
	 foo_idx | 4/765  |               | relation      | RowExclusiveLock
	         | 2/4691 |               | virtualxid    | ExclusiveLock
	         | 4/765  | 8517          | transactionid | ExclusiveLock
	         | 4/765  |               | virtualxid    | ExclusiveLock
	(7 rows)

[>$]

***

# Concurrent Updates

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# UPDATE foo SET f1=41 WHERE f1=41;
	UPDATE 1
	
	--------------------------------------------------------
	postgres=# BEGIN;
	BEGIN
	postgres=# UPDATE foo SET f1=42 WHERE f1=42;
	UPDATE 1

[>$]

***

# Concurrent Updates

[$<]

	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode
	postgres-#   FROM pg_locks l LEFT OUTER JOIN pg_class c 
	postgres-#     ON (l.relation = c.oid)
	postgres-#  WHERE l.pid != pg_backend_pid()
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid |   locktype    |       mode       
	---------+--------+---------------+---------------+------------------
	 foo     | 2/4692 |               | relation      | RowExclusiveLock
	 foo     | 4/766  |               | relation      | RowExclusiveLock
	 foo_idx | 2/4692 |               | relation      | RowExclusiveLock
	 foo_idx | 4/766  |               | relation      | RowExclusiveLock
	         | 2/4692 | 8518          | transactionid | ExclusiveLock
	         | 2/4692 |               | virtualxid    | ExclusiveLock
	         | 4/766  | 8519          | transactionid | ExclusiveLock
	         | 4/766  |               | virtualxid    | ExclusiveLock
	(8 rows)

[>$]

***

# Concurrent Updates

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# UPDATE foo SET f1=41 WHERE f1=41;
	UPDATE 1
	
	--------------------------------------------------------
	BEGIN
	postgres=# UPDATE foo SET f1=40 WHERE f1=41;

[>$]

***

# Concurrent Updates

[$<]

	postgres=# SELECT c.relname, l.virtualtransaction AS vxid, 
	postgres-#        l.transactionid::text, l.locktype, l.mode, l.granted
	postgres-#   FROM pg_locks l LEFT OUTER JOIN pg_class c 
	postgres-#     ON (l.relation = c.oid)
	postgres-#  WHERE l.pid != pg_backend_pid()
	postgres-#  ORDER BY 1, 2, 3;
	 relname |  vxid  | transactionid |   locktype    |       mode       | granted 
	---------+--------+---------------+---------------+------------------+---------
	 foo     | 2/4693 |               | relation      | RowExclusiveLock | t
	 foo     | 4/767  |               | tuple         | ExclusiveLock    | t
	 foo     | 4/767  |               | relation      | RowExclusiveLock | t
	 foo_idx | 2/4693 |               | relation      | RowExclusiveLock | t
	 foo_idx | 4/767  |               | relation      | RowExclusiveLock | t
	         | 2/4693 | 8520          | transactionid | ExclusiveLock    | t
	         | 2/4693 |               | virtualxid    | ExclusiveLock    | t
	         | 4/767  | 8520          | transactionid | ShareLock        | f
	         | 4/767  | 8521          | transactionid | ExclusiveLock    | t
	         | 4/767  |               | virtualxid    | ExclusiveLock    | t
	(10 rows)

[>$]

***

# Deadlocks

[$<]

	postgres=# BEGIN;
	BEGIN
	postgres=# UPDATE foo SET f1=41 WHERE f1=41;
	UPDATE 1
	
	--------------------------------------------------------
	postgres=# BEGIN;
	BEGIN
	postgres=# UPDATE foo SET f1=43 WHERE f1=42;
	UPDATE 1
	postgres=# UPDATE foo SET f1=40 WHERE f1=41;
	
	
	--------------------------------------------------------
	postgres=# UPDATE foo SET f1=42 WHERE f1=42;
	ERROR:  deadlock detected
	DETAIL:  Process 30528 waits for ShareLock on transaction 8529; blocked by process 6804.
	Process 6804 waits for ShareLock on transaction 8528; blocked by process 30528.
	HINT:  See server log for query details.

[>$]

***

# Lab Exercise 1

[$<]

Last night, your developers rolled out a new database migration to add a column to the accounts table, but it was killed after 5 minutes because it appeared to be doing nothing. 

* Open 3 connections to the gnb database.
* In the first session, open a transaction that sums the balances in the pgbench_accounts table.
* In the second session, add a column called modified_date to the pgbench_accounts table with a default of the current timestamp.
* In the third session, investigate the pg_locks view to see why the DDL is not completing.

[>$]