# -*- coding: utf-8 -*-
"""
Created on Wed May 27 16:29:44 2020
    В файле описывается класс create_base создающий таблиы базы данных в соответствии с установленной структурой. ВАЖНО!!! предполагается, что сама база данных уже создана 
        средствами администрирования БД. В текущий момент БД либо пустая, либо содержит таблицы согласно установленной структуре. При запуске скрипта все текущие таблицы будут удалены
        если они были созданы и буду созданы таблицы с нуля. Таким образом можно полностью создать или пересоздать базу данных. 
						
    def __init__(self, id_users): - инициализация класса и подключение к базе данных (конструктор класса)
    def __del__(self): - закрытия соединение с базой данных (деструктор класса)
    def del_all(self): - удаление всех таблиц, если существуют
    def cr_city(self) - создаем таблицу городов
    def cr_school(self):  - создаем таблицу школ
    def cr_event(self): - создаем таблиу мероприятий (эвентов)
    def cr_anket(self):  - создаем таблицу анкет
    def cr_question(self): - создаем таблицу вопросов
    def cr_possible_answer(self):  - создаем таблицу вариантов ответов.
    def cr_subject(self):  - создаем таблицу субъектов
    def cr_event_record(self):  - создаем таблицу event_record
    def cr_answer(self):  - создаем таблицу ответов. 
    !!! некоторые поля могут отличаться от полей в установленной структуре. Например для поля email в таблице субъектов 16 символов оказаолось мало и даже 32. Это поле установлено в 64 символа
    поле creation_time - установлено без часового пояся, т.к. данные собираются без часового пояся. Могут быть и другие мелкие отличия
    
    Основной сценарий работы: 
    db=create_base() - создаем объект и полключаемся
    db.del_all() - удаляем все таблицы, если они есть
    #создаем чистые таблицы
    db.cr_city()
    db.cr_school()
    db.cr_subject()
    db.cr_event()
    db.cr_anket()
    db.cr_question()
    db.cr_possible_answer()
    db.cr_event_record()
    db.cr_answer()

    #коммитим и закрываем соединение
    db.conn.close()

@author: Леонид
"""
import psycopg2
import psycopg2.extras
import pandas as pd

import datetime
param_dic_base = {
    "host"      : "localhost",
    "dbname"  : "abiturient_db",
    "user"      : "postgres",
    "password"  : "postgres"
}
class create_base:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=param_dic_base['dbname'], user=param_dic_base['user'], 
                                password=param_dic_base['password'], host=param_dic_base['host'], port="5432")
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
#        self.conn.close()
        return
#==============================================================================
    def __del__(self):
        self.conn.close()
        return
        
#==============================================================================    
    def del_all(self): 
        
        self.cursor.execute("""
                    DROP TABLE IF EXISTS    city,
                                            school,
                                            event,
                                            subject,
                                            anket,
                                            question,
                                            possible_answer,
                                            event_record,
                                            answer

                    CASCADE; 
                    
                    """ )
        
        self.conn.commit()
        
        return

#==============================================================================    
    def cr_city(self): 
        #создаем таблицу городов
        self.cursor.execute("""
                     CREATE TABLE public.city
                    (
                        city_id SERIAL NOT NULL,
                        city character varying(50),
                        region character varying(150),
                        country character varying(100),
                        CONSTRAINT city_pk PRIMARY KEY (city_id)
                        
                    )
                    WITH (
                        OIDS = FALSE
                    );
                    
                    
                    """ )
        self.conn.commit()
        
        return
#==============================================================================    
    def cr_school(self): 
        #создаем таблицу школ
        self.cursor.execute("""
                     CREATE TABLE public.school
                    (
                        school_id SERIAL NOT NULL,
                        school character varying(50),
                        city_id_city integer,
                       
                        CONSTRAINT school_pk PRIMARY KEY (school_id),
                        
                        CONSTRAINT city_fk FOREIGN KEY (city_id_city)
                            REFERENCES public.city (city_id) MATCH SIMPLE
                            ON UPDATE NO ACTION
                            ON DELETE NO ACTION
                            NOT VALID
                    )
                    WITH (
                        OIDS = FALSE
                    );
                    
                    
                    """ )
        self.conn.commit()
        
        return
#==============================================================================    
    def cr_event(self): 
        #создаем таблицу обытий
        self.cursor.execute("""
                     CREATE TABLE public.event
                    (
                        event_id SERIAL NOT NULL,
                        event character varying(256),
                        date date,
                        CONSTRAINT Events_pk PRIMARY KEY (event_id),
                        CONSTRAINT object_name_key UNIQUE (event)
                    )
                    WITH (
                        OIDS = FALSE
                    );
                    
                    
                    """ )
        self.conn.commit()
        
        return
#==============================================================================    
    def cr_anket(self): 
        #создаем таблицу анкет
        self.cursor.execute("""
                     CREATE TABLE public.anket
                    (
                        anket_id SERIAL NOT NULL,
                        type_anket character varying(100),
                        name_anket character varying(100),
                        CONSTRAINT anket_pk PRIMARY KEY (anket_id)
                    )
                    WITH (
                        OIDS = FALSE
                    );
                    
                    
                    """ )
        self.conn.commit()
        
        return
#==============================================================================    
    def cr_question(self): 
        #создаем таблицу вопросов
        self.cursor.execute("""
                     CREATE TABLE public.question
                    (
                        question_id SERIAL NOT NULL,
                        QuestionType character varying(50),
                        QuestionText character varying(256),
                        anket_id_anket integer,
                        CONSTRAINT question_pk PRIMARY KEY (question_id),
                        CONSTRAINT anket_fk FOREIGN KEY (anket_id_anket)
                            REFERENCES public.anket (anket_id) MATCH SIMPLE
                            ON UPDATE NO ACTION
                            ON DELETE NO ACTION
                            NOT VALID
                    )
                    WITH (
                        OIDS = FALSE
                    );
                    
                    
                    """ )
        self.conn.commit()
        
        return
#==============================================================================    
    def cr_possible_answer(self): 
        #создаем таблицу вопросов
        self.cursor.execute("""
                     CREATE TABLE public.possible_answer
                    (
                        possible_answer_id SERIAL NOT NULL,
                        possible_answer character varying(100),
                        question_id_question integer,
                        
                        CONSTRAINT possible_answer_pk PRIMARY KEY (possible_answer_id),
                        CONSTRAINT question_fk FOREIGN KEY (question_id_question)
                            REFERENCES public.question (question_id) MATCH SIMPLE
                            ON UPDATE NO ACTION
                            ON DELETE NO ACTION
                            NOT VALID
                    )
                    WITH (
                        OIDS = FALSE
                    );
                    
                    
                    """ )
        self.conn.commit()
        
        return

#==============================================================================    
    def cr_subject(self): 
        #создаем таблицу вопросов
        self.cursor.execute("""
                     CREATE TABLE public.subject
                    (
                        subject_id SERIAL NOT NULL,
                        last_name character varying(32),
                        first_name character varying(32),
                        middle_name character varying(32),
                        class smallint,
                        telephon character varying(32),
                        email character varying(64),
                        school_id_school integer,
                        
                        
                        CONSTRAINT subject_pk PRIMARY KEY (subject_id),
                        CONSTRAINT school_fk FOREIGN KEY (school_id_school)
                            REFERENCES public.school (school_id) MATCH SIMPLE
                            ON UPDATE NO ACTION
                            ON DELETE NO ACTION
                            NOT VALID
                    )
                    WITH (
                        OIDS = FALSE
                    );
                    
                    
                    """ )
        self.conn.commit()
        
        return
#==============================================================================    
    def cr_event_record(self): 
        #создаем таблицу вопросов
        self.cursor.execute("""
                     CREATE TABLE public.event_record
                    (
                        event_record_id SERIAL NOT NULL,
                        --creation_time timestamp with time zone,
                        creation_time timestamp,
                        subject_id_subject integer,
                        event_id_event integer,
                        anket_id_anket integer,
                        
                        CONSTRAINT event_record_pk PRIMARY KEY (event_record_id),
                        
                        CONSTRAINT subject_fk FOREIGN KEY (subject_id_subject)
                            REFERENCES public.subject (subject_id) MATCH SIMPLE
                            ON UPDATE NO ACTION
                            ON DELETE NO ACTION
                            NOT VALID,
                        
                        CONSTRAINT event_fk FOREIGN KEY (event_id_event)
                            REFERENCES public.event (event_id) MATCH SIMPLE
                            ON UPDATE NO ACTION
                            ON DELETE NO ACTION
                            NOT VALID,

                        CONSTRAINT anket_fk FOREIGN KEY (anket_id_anket)
                            REFERENCES public.anket (anket_id) MATCH SIMPLE
                            ON UPDATE NO ACTION
                            ON DELETE NO ACTION
                            NOT VALID
                    )
                    WITH (
                        OIDS = FALSE
                    );
                    
                    
                    """ )
        self.conn.commit()
        
        return
    #==============================================================================    
    def cr_answer(self): 
        #создаем таблицу вопросов
        self.cursor.execute("""
                     CREATE TABLE public.answer
                    (
                        answer_id SERIAL NOT NULL,
                        answer text,
                        event_record_id_event_record integer,
                        question_id_question integer,
                        possible_answer_id_possible_answer integer,

                        
                        CONSTRAINT answer_pk PRIMARY KEY (answer_id),

                        CONSTRAINT event_record_fk FOREIGN KEY (event_record_id_event_record)
                            REFERENCES public.event_record (event_record_id) MATCH SIMPLE
                            ON UPDATE NO ACTION
                            ON DELETE NO ACTION
                            NOT VALID,

                        CONSTRAINT question_fk FOREIGN KEY (question_id_question)
                            REFERENCES public.question (question_id) MATCH SIMPLE
                            ON UPDATE NO ACTION
                            ON DELETE NO ACTION
                            NOT VALID,
                        
                        CONSTRAINT possible_answer_fk FOREIGN KEY (possible_answer_id_possible_answer)
                            REFERENCES public.possible_answer (possible_answer_id) MATCH SIMPLE
                            ON UPDATE NO ACTION
                            ON DELETE NO ACTION
                            NOT VALID
                    )
                    WITH (
                        OIDS = FALSE
                    );
                    
                    
                    """ )
        self.conn.commit()
        
        return
#==============================================================================    
#//////////////////////////////////////////////////////////////////////////////
#********************************конец класса*************************************
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#==============================================================================    

if __name__ == "__main__":
    db=create_base()
    db.del_all()
    db.cr_city()
    db.cr_school()
    db.cr_subject()
    db.cr_event()
    db.cr_anket()
    db.cr_question()
    db.cr_possible_answer()
    db.cr_event_record()
    db.cr_answer()

    
    db.conn.close()
    