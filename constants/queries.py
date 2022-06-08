class Queries:
    CreateDatasetTableQuery = lambda dataset_id: f"""create table DATASET_{dataset_id}(code text not null,
                                                     value int not null,
                                                     date_created timestamp default current_timestamp,
                                                     constraint DATASET_{dataset_id}_CH check (DATASET_{dataset_id}.value>=0))"""

    GetLastValue = lambda dataset_id, code: f"""select value
                                                from DATASET_{dataset_id}
                                                where date_created = (select max(date_created) from DATASET_{dataset_id} where code = '{code}')
                                                and code = '{code}'"""

    InsertItem = lambda dataset_id, code, value: f"""insert into DATASET_{dataset_id} (code, value)
                                                     values ('{code}', {value})"""

# con = sqlite3.connect('../database/database.db')
# cur = con.cursor()
# # cur.execute(Queries.InsertItem(1, 'CODE_DIGITAL', 2, datetime.datetime.now().timestamp()))
# cur.execute(Queries.GetLastValue(1, 'CODE_ANALOG'))
# print(cur.fetchone()[0])
# # con.commit()
# con.close()

# print(Queries.InsertItem(1, 'CODE_ANALOG', 5, datetime.datetime.now()))
