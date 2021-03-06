class Queries:
    CreateDatasetTableQuery = lambda dataset_id: f"""create table DATASET_{dataset_id}(code text not null,
                                                     value int not null,
                                                     date_created timestamp default current_timestamp,
                                                     constraint DATASET_{dataset_id}_CH check (DATASET_{dataset_id}.value>=0))"""

    GetLastValue = lambda dataset_id, code: f"""select value
                                                from DATASET_{dataset_id}
                                                where date_created = (select max(date_created) from DATASET_{dataset_id} where code = '{code}')
                                                and code = '{code}'"""
    GetAllValue = lambda dataset_id, code: f"""select value
                                            from DATASET{dataset_id}
                                            where code = '{code}'"""
    GetData = lambda dataset_id, code: f"""select datecreated, code, value
                                            from DATASET{dataset_id}
                                            where code = '{code}'"""

    InsertItem = lambda dataset_id, code, value: f"""insert into DATASET_{dataset_id} (code, value)
                                                     values ('{code}', {value})"""
