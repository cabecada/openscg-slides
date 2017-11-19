---
title: PostgreSQL storage, MVCC and issues related to it
---

***
# Terminology

[$<]

* **Relation** - A table
* **Tuple** - Version of a row as well as index entries
* **Heap** - The data files containing data tuples
* **Index** - The data files containing index tuples
* **TOAST** - The best thing since sliced bread (oversized attributes)
* **Page** - One block of data (typically 8k)

[>$]

***
# Heap structure

[$<]

* All data files (heap, index, toast) are split into 1GB segments
* Each segment consists of up to 131,072 8k pages

[>$]

***
# Heap Page layout

[$<]

* Every tuple is identified by its CTID.
* The CTID is the page number and Item number
* Adding a tuple is done by adding a Tuple and adding/reusing an Item

![](images/pg_page_layout_1.odg)

[>$]

***
# Non-Overwriting storage

[$<]

* Postgres was an academic research project
* The non-overwriting storage concept was meant to provide time travel
* When a row is UPDATEd, PostgreSQL doesn't change the existing tuple but creates a new row version
* Different versions of a row (may) have different CTIDs
* Different versions with different CTIDs require their own index entries

[>$]

***
# Tuple visibility (REPEATABLE READ ++)

[$<]

* Each tuple has several header fields
* The XMIN is the transaction ID that created this row version
* The XMAX is the transaction ID that destroyed this row version
* CMIN and CMAX prevent a statement from seeing its own changes
* A tuple is visible when XMIN was committed in the past and XMAX is either invalid, aborted or committed in the future

[>$]

***
# Defining past and future

[$<]

* On the first DML statement a transaction defines its MVCC stapshot
* It scans the PROC array in shared memory for transactions currently in progress
* The snapshot is a list of those XIDs, the min() of that and the latest xid counter as max()
* In the past is any XID that is < min() or (<= max() and not in the list)
* In the future is any XID that is > max() or in the list)

[>$]

***
# Defining past and future

[$<]

* In an ACID compliant database changes of a transaction become visible to the rest of the world when that transaction commits
* REPEATABLE READ or SERIALIZABLE isolation level transactions only see changes from transactions, that committed in the past
* In other words past and future are defined as another transactions moment of commit relative to the visibility snapshot of the current transaction

[>$]

***
# An example snapshot

[$<]

* XIP: 1001, 1003, 1005
* MIN: 1001
* MAX: 1008

```
```

* XID 1000 is in the past because it committed or aborted before this snapshot was created
* XID 1002 is also in the past for the same reason
* XID 1006 is also in the past
* XID 1003 is in the future because it was still in progress when this snapshot was created
* XID 1009 is in the future because it had not started when this snapshot was created

[>$]

***
# An example snapshot

[$<]

* XIP: 1001, 1003, 1005
* MIN: 1001
* MAX: 1008

![](images/snapshot_1.odg)

[>$]

***
# What happens on INSERT

[$<]

* On INSERT
    * The new tuple is added to a page
    * The new tuple has XMIN = current_xid and XMAX = Invalid
    * All index entries are created

[>$]

***
# What happens on UPDATE

[$<]

* On UPDATE
    * The new tuple is added to a page
    * The new tuple has XMIN = current_xid and XMAX = Invalid
    * Normally all index entries are created for the new tuple
    * The old tuple gets stamped XMAX = current_xid

[>$]

***
# What happens on DELETE

[$<]

* On DELETE
    * The old tuple gets stamped XMAX = current_xid

[>$]

***
# MVCC based on all that

[$<]

* After INSERT or UPDATE
    * the (new) tuple will have the current transaction as XMIN
    * it will be ignored by transactions that consider XMIN in the future
* After an UPDATE or DELETE
    * the (old) tuple is still there and will have the current transaction as XMAX
    * it will be ignored by transactions that consider XMAX in the past
* This means that PostgreSQL keeps **ALL** row versions around

[>$]

***
# What VACUUM does

[$<]

* Removal of dead tuples that are no longer visible to any transaction
* Removal of index tuples for those data tuples that are to be removed
* Freezing of XIDs
* Adding information to the freeze map
* Adding information to the freespace map

[>$]

***
# Heap Page after VACUUM

[$<]

* After a VACUUM the Item list might have holes
* Data tuples however have been compacted

![](images/pg_page_layout_2.odg)

[>$]

***
# HOT updates

[$<]

* On UPDATE if there is enough free space in the page of the old tuple AND no indexed columns are changed, a Heap Only Tuple is performed.
    * The tuple is added to the data section
    * The Item pointer points to the new tuple
    * The new tuple chains to the previous tuple
    * No index entries are created
* Since we don't have extra index tuples and the row's CTID did not change another UPDATE can later remove the old row if is is no longer visible to anyone

[>$]

***
# Pros and Cons

[$<]

* Pros
    * The non-overwriting storage manager made implementation of MVCC really easy
    * Rollback is really fast
    * Theoretically time travel should still be possible if we disable vacuum/autovacuum
* Cons
    * Considerable overhead for cleanup
    * Bloat of data and indexes

[>$]

***
# A little surprise

[$<]

* A SELECT can produce a huge amount of write?
    * The commit/abort state of a transaction is recorded in the pg_clog files
    * To avoid constant lookup of that data the tuple header is stamped with bits that say "known committed/aborted" by the next scan

[>$]

***
# TOAST

[$<]

* A tuple must fit into one 8k page
* To fit larger than 8k rows PostgreSQL compresses individual datums or stores them sliced up in the toast table
* Toast entries are reused on UPDATE if their value was not updated
* Toasted data is not pulled in if not specified in the query
* Only the toast entries in the final result set are ever read
* Toast entries will become unclustered and have a different order on disk from their main tuples

[>$]

***
# Physical replication

[$<]

* Physical replication in PostgreSQL, including streaming replication and hot standby, is implemented by constantly keeping the replica database in startup mode, performing crash recovery
* The WAL contains all changes to data and index files as well as the commit/abort information

[>$]

***
# This creates possible replication conflicts

[$<]

* VACUUM only removes dead tuples that are no longer visible by any running transaction
* In hot standby there can be transactions on other servers
* If VACUUM removes tuples that remote transactions can see we have two choices
    * Stall replication and let the secondary fall behind
    * Abort the conflicting read-only transaction on the secondary
* The third choice is to feed back visibility information from the standby to the primary

[>$]

***
# Letting the standby fall behind

[$<]

To let the standby fall behind we configure

* wal_keep_segments on the primary or use WAL archiving
* max_wal_archive_delay on the secondary
* max_wal_streaming_delay on the secondary

Drawbacks

* The archive location or the primary must have enough disk space to accomodate all the WAL
* A long running transaction on the standby stalls visibility for everyone on that standby

[>$]

***
# Cancel conflicting queries

[$<]

To let the standby cancel conflicting queries

* wal_keep_segments on the primary or use WAL archiving
* max_wal_archive_delay on the secondary
* max_wal_streaming_delay on the secondary

Drawback

* Long running operations can never finish on a standby

[>$]

***
# Visibility feedback

[$<]

To let the standby feed back visibility to the primary

* hot_standby_feedback=true on the secondary

Drawback

* Long running transactions now cause bloat on the primary again, even though they have been offloaded onto a standby

[>$]

