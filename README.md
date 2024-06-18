# pals-analysis

## possible primary key for each table

### Palworld_Data-comparison of ordinary BOSS attributes
3 column ? name is primary key for each column

### Palworld_Data-hide pallu attributes
primary key could be code name, Tribe, BPClass

### Palworld_Data--Palu combat attribute table
primary key could be chinese name, name, code name, Tribe, BPClass

### Palworld_Data-Palu Job Skills Table
primary key could be chinese name, english name

### Palworld_Data--Palu refresh level
3 column ? name is primary key for each column

### Palworld_Data-Tower BOSS attribute comparison
name is primary key

## possible foreign key
name is found in Palworld_Data-comparison of ordinary BOSS attributes, Palworld_Data--Palu combat attribute table, Palworld_Data--Palu refresh level, Palworld_Data-Tower BOSS attribute comparison.
chinese name is found in Palworld_Data--Palu combat attribute table, Palworld_Data-Palu Job Skills Table
code name is found in Palworld_Data-hide pallu attributes, Palworld_Data--Palu combat attribute table
Tribe ans BPClass are found in Palworld_Data-hide pallu attributes, Palworld_Data--Palu combat attribute table
ID is found in Palworld_Data--Palu combat attribute table, Palworld_Data-Palu Job Skills Table, Palworld_Data--Palu refresh level
