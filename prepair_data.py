'''
created 18.07.2022
вносит записи в таблицы базы даннхы. В модуле описан класс prepar_data. На входе документ формата excel = результат опроса в яндекс (см. пример файла 'DOD_V_2022+Ипостаси.xlsx'). Документ должен содержать обязательные поля:
					'Фамилия:', 'Имя:', 'Отчество:', 'Номер телефона:', 'E-mail:', 'Страна:', 'Регион:', 'Город:','Учебное заведение:', 'Класс:', 'Время создания'. 
					Остальные столбцы представляют собой ответы на вопросы.  Для того, что бы программа понимала, какие именно столбцы обрабатываем, на вход подается файл, содержащий список
					полей являющихся вопросами для обработки (см. пример файла 'list_questions.csv').
					Результатом работы программы является внесение записей в базу данных. 

	prepair_data.py - основной объект prepar_data. Рассмотрим методы
		def __init__(self, df, list_questions, event,anket, regular_columns=
                    ['Фамилия:', 'Имя:', 'Отчество:', 'Номер телефона:',
                    'E-mail:', 'Страна:', 'Регион:', 'Город:',
                    'Учебное заведение:', 'Класс:', 'Время создания'
                    ]) -> None: - инициализация класса. Основные входы: файл с результатами опросов (аналогичный 'DOD_V_2022+Ипостаси.xlsx'), 
								  файл с перечнем полей, являющихся вопросами (аналогичный 'list_questions.csv'), 
								  event - словарь содержащий сведения о мероприятии по форме: event={'event':'название', 'date':'дата'},
								  anket - словарь содержащий сведения об опросе (анкете) по форме: anket={'type_anket':'тип анкеты', 'name_anket':'имя анкеты'}
		def connect_base(self) -> bool - соединение с БД
		def disconnect(self) -> bool - закрытие соединения
		def execute_values(self, conn, df, table) - ДОЗАПИСЬ данные в таблицу. conn - соединение с БД, df - таблица по форме pandas DataFrame, которую необходимо записать (важно, что бы поля важно,
													что бы поля в df совпадали с полями таблицы table в БД, кроме поля PK id, которое создается и заполняется автоматически), 
													table - имя таблицы в которую необходимо произвести дозапись
		
		def query_get_city(self): - запрашиваем из базы все города, которые записаны в настоящий момент
		def query_set(self, df, table_name) -> bool: - интерфейс для execute_values включающий в себя открытие соединения, вызов записи, коммит, закрытие соединения
		def query_get_school(self): - запрос таблицы школ. (важно, школа мерджится со страной, регионом, городом и в таком формате возвращается)
		def query_get_subject(self): - запрашиваем из базы субъектов учитывая, что субъект опредялются вместе со школой и городом и в этом формате возвращается
		def query_get_id_event(self): - находим event_id в базе данных для текущего евента. Предполагается, что текущий евент к этому моменту уже записан в базу данных. Если подходящих event_id 
										не нашлось выдаем ошибку и прерываем выполнение программы. Если подходящих event_id больше одного - выдаем ошибку и прерываем программу
		def query_get_id_anket(self): - аналогично query_get_id_event, но для 'anket_id'
		def query_get_question(self): - запрашиваем из базы все вопросы
		def query_get_possible_anser(self): - запрашиваем из базы все возможные ответы
		def query_get_event_record(self) - запрашиваем из базы таблицу event_record
		def predict(self): - основная функция обеспечивающая реализацую основного сценария. Предполагается, что к этому моменту объект класса корректно инициирован, создана база данных и
							соответствующие таблицы. В функции производится последовательный вызов функций по преобразованию данных и записи таблиц
		def check_data(self): - проверяем наличие обязательных столбцов во входящем файле ( аналогичный 'DOD_V_2022+Ипостаси.xlsx')
		def get_stru_questions(self): - на основе входящего файла ( аналогичный 'list_questions.csv') формируем перечень уникальных вопросов. Вопросы парсятся следующим образом:
										1. если в вопрос не содержит символа ' / ', то он относится к открытым одностолбцовым вопросами
										2. если вопрос содержит символ ' / ', то часть до этого символа отностися к вопросу, часть после этого символа относится к ответу. Вопрос считается закрытм типом
										3. если в вопросе содержистя несколько симоволов ' / ', то учитывается только последний символ. Обработка аналогична случаю 2. 
		def parsing_question(self): - переходим от многостолбцового представления ответов, к одностолбцовому
									вариант когда на вопрос имеется много ответов и каждый ответ в отдельном столбце
									формируем таблицу, когда один вопрос со всеми ответами представляются в одном столбце
		
		def get_tab_city(self) -> bool: на основании файла ( аналогичный 'DOD_V_2022+Ипостаси.xlsx') Формируем перечень уникальных городов, 
										находим те из них, которые отсутствуют в базе данных и Дополняем таблицу городов новыми городами
		def get_tab_school(self) -> bool: аналогично get_tab_city, только со школами, но с учетом того, что школа мерджится со страной, регионом и городом
		def get_tab_subject(self) -> bool: - аналогично get_tab_city, только с субъектами, но с учетом того, что субъект мерджится по фамилии, имени, отчетству, стране, региону, городу, школе
		def get_tab_event_record(self) -> bool: - заполняем таблицу event_record.
		def get_tab_question(self) -> bool:  - заполняем таблицу вопросов. Находим все уникальные вопросы в файле и записываем их в таблицу с привязкой к анкете
		def get_tab_possible_answer(self) -> bool: - заполняем таблицу возможных ответов. Парсим все ответы для закрытых вопросов и указываем отсутствие ответа для открытых вопросов. Записываем
													возможные ответы в таблицу с привязкой к вопросами
		def get_tab_answer(self) -> bool: - и наконец-то заполняем таблицу  ответов. Берем все ответы, мерджим по вопросам, для привязки к вопросам, мерджим по субъектам, событию и анкете для 
											привязки к event_record, мерджим по возможным ответам для привязки к возможным ответам. Записываем в таблицу. 
		Основной сценарий работы:
		df=pd.read_excel('DOD_V_2022+Ипостаси.xlsx') - Загрузка файла данных
		list_questions=pd.read_csv('list_questions.csv', sep='  ') - загрузка вариантов ответов
		event={'event':'ДОД2022-весна', 'date':'2022.04.10'} - указываем сведения о событии
		anket={'type_anket':'тип анкеты', 'name_anket':'имя анкеты'} - указываем сведения об анкете
		
		prepair=prepar_data(df=df, list_questions=list_questions, event=event,anket=anket ) - инициируем объект класса
		if prepair.predict()==False: 														- запускаем на исполнение с контролем
			print('Format of data is not valid')
		print('Format of data is valid')
			
'''

import pandas as pd
import psycopg2
import psycopg2.extras

param_dic_base = {
    "host"      : "localhost",
    "dbname"  : "abiturient_db",
    "user"      : "postgres",
    "password"  : "postgres"
}

def str2qwe(s):
    
    mas=s.rpartition(' / ')
    if mas[0]!='':
        qwe=mas[0]
    else:
        qwe=mas[2]
    return qwe

def str2ans(s):
    mas=s.split(' / ')
    if len(mas)==1:
        ans=None
    else:
        ans=mas[-1]
    return ans

class prepar_data:
    def __init__(self, df, list_questions, event,anket, regular_columns=
                    ['Фамилия:', 'Имя:', 'Отчество:', 'Номер телефона:',
                    'E-mail:', 'Страна:', 'Регион:', 'Город:',
                    'Учебное заведение:', 'Класс:', 'Время создания'
                    ]) -> None:
        self.df=df
        self.list_questions=list_questions
        self.regular_columns=regular_columns
        self.event=event
        self.anket=anket
        
        return
    def connect_base(self) -> bool:
        try:
            self.conn = psycopg2.connect(dbname=param_dic_base['dbname'], user=param_dic_base['user'], 
                                        password=param_dic_base['password'], host=param_dic_base['host'], port="5432")
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception as e:
            print(e)
            return False
        
        return True
    def disconnect(self) -> bool:
        try:
            self.conn.close()
        except Exception as e:
            print(e)
            return False
        return True
    def execute_values(self, conn, df, table):
        """
        Using psycopg2.extras.execute_values() to insert the dataframe
        """
        # Create a list of tupples from the dataframe values
        tuples = [[y if y==y else None for y in list(x)] for x in df.to_numpy()]
        # Comma-separated dataframe columns
        cols = ','.join(list(df.columns))
       
        query  = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
        cursor = conn.cursor()
        try:
            psycopg2.extras.execute_values(cursor, query, tuples)
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            conn.rollback()
            cursor.close()
            return 1
        print("execute_values() done")
        cursor.close()    
        return
    def query_get_city(self):
        #запрашиваем из базы все города, которые записаны в настоящий момент
        if self.connect_base()==False:
            return False
        try:
            df_city = pd.read_sql_query(
                            '''SELECT *
                                    FROM public.city 
                            ; '''.format(),self.conn)
                            
        except Exception as e:
            print(e)
            return False
        self.disconnect()
        return df_city
    
    def query_set(self, df, table_name) -> bool:
        #интерфейс для execute_values включающий
        #в себя открытие соединения, вызов записи, коммит, закрытие соединения
        if self.connect_base()==False:
            return False
        try:
            
            self.execute_values( self.conn, df, table_name)
            
            self.conn.commit()        
                    
        except:
            print("Ошибка записи городов")
            self.conn.close()
            return False

        self.disconnect()
        return True

    def query_get_school(self):
        #запрашиваем из базы все школы и учитывая, что школы опредялются вместе с городами мерджим их с городами
        if self.connect_base()==False:
            return False
        try:
            df_school = pd.read_sql_query(
                            '''SELECT *
                                FROM public.school AS school
                                LEFT JOIN public.city AS city ON school."city_id_city" = city."city_id"
                            ; '''.format(),self.conn)
                            
        except Exception as e:
            print(e)
            return False
        self.disconnect()
        return df_school

    def query_get_subject(self):
        #запрашиваем из базы субъектов учитывая, что субъект опредялются вместе со школой и городом
        if self.connect_base()==False:
            return False
        try:
            df_subject = pd.read_sql_query(
                            '''
                            SELECT *

                            FROM(
                                SELECT *
                                FROM public.school AS school
                                LEFT JOIN public.city AS city ON school."city_id_city" = city."city_id"
                                ) AS tab_school
                                RIGHT JOIN public.subject AS subject ON tab_school."school_id"=subject."school_id_school"

                            ; '''.format(),self.conn)
                            
        except Exception as e:
            print(e)
            return False
        self.disconnect()
        return df_subject[['subject_id', 'school_id', 'school', 'city', 'region',
       'country', 'last_name', 'first_name', 'middle_name',
       'class', 'telephon', 'email', 'school_id_school']]
    
    def query_get_id_event(self):
        #запрашиваем id event
        if self.connect_base()==False:
            return False
        try:
            df_event = pd.read_sql_query(
                            '''SELECT *
                                    FROM public.event as event
                                    WHERE  event.event='{0}' AND event.date='{1}'
                            ; '''.format(self.event['event'], self.event['date']),self.conn)
                            
        except Exception as e:
            print(e)
            return False
        self.disconnect()
        if len(df_event)==0:
            print('event отсутствует в базе')
            return False
        elif len(df_event)>1:
            print('в базе встречается {0} event. Нарушение целостности базы'.format(len(df_event)))
            return False
        
        return df_event['event_id'].iloc[0]
    def query_get_id_anket(self):
        #запрашиваем id anket
        if self.connect_base()==False:
            return False
        try:
            df_anket = pd.read_sql_query(
                            '''SELECT *
                                    FROM public.anket as anket
                                    WHERE  anket.type_anket='{0}' AND anket.name_anket='{1}'
                            ; '''.format(self.anket['type_anket'], self.anket['name_anket']),self.conn)
                            
        except Exception as e:
            print(e)
            return False
        self.disconnect()
        if len(df_anket)==0:
            print('Анкета отсутствует в базе')
            return False
        elif len(df_anket)>1:
            print('в базе встречается {0} анкет. Нарушение целостности базы'.format(len(df_anket)))
            return False
        
        return df_anket['anket_id'].iloc[0]
    def query_get_question(self):
        #запрашиваем из базы все вопросы
        if self.connect_base()==False:
            return False
        try:
            df_question = pd.read_sql_query(
                            '''SELECT *
                                    FROM public.question
                            ; '''.format(),self.conn)
                            
        except Exception as e:
            print(e)
            return False
        self.disconnect()
        return df_question
    
    def query_get_possible_anser(self):
        #запрашиваем из базы все возможные ответы
        if self.connect_base()==False:
            return False
        try:
            df_possible_answer = pd.read_sql_query(
                            '''SELECT *
                                    FROM public.possible_answer
                            ; '''.format(),self.conn)
                            
        except Exception as e:
            print(e)
            return False
        self.disconnect()
        return df_possible_answer
    
    def query_get_event_record(self):
        #запрашиваем из базы таблицу event_record
        if self.connect_base()==False:
            return False
        try:
            df_event_record = pd.read_sql_query(
                            '''SELECT *
                                    FROM public.event_record
                            ; '''.format(),self.conn)
                            
        except Exception as e:
            print(e)
            return False
        self.disconnect()
        return df_event_record

    def predict(self):
        if self.check_data()==False:
            return False
        self.get_stru_questions()
        self.parsing_question()
        self.get_tab_city()
        self.get_tab_school()
        self.get_tab_subject()
        df_event=pd.DataFrame([[self.event['event'], self.event['date']]], columns=['event', 'date'])
        df_anket=pd.DataFrame([[self.anket['type_anket'], self.anket['name_anket']]], columns=['type_anket', 'name_anket'])
        self.query_set(df_event, 'public.event')
        self.query_set(df_anket, 'public.anket')
        self.id_event=self.query_get_id_event()
        if type(self.id_event)==bool:
            print('ошибка получения id_event')
            return False
        self.id_anket=self.query_get_id_anket()
        if type(self.id_anket)==bool:
            print('ошибка получения id_anket')
            return False
        self.get_tab_event_record()
        self.get_tab_question()
        self.get_tab_possible_answer()
        self.get_tab_answer()
        
        
        return

        
    def check_data(self):
        #проверяем наличие обязательных столбцов
        df=self.df
        columns=list(df.columns)
        regular_columns=['Фамилия:', 'Имя:', 'Отчество:', 'Номер телефона:',
                        'E-mail:', 'Страна:', 'Регион:', 'Город:',
                        'Учебное заведение:', 'Класс:', 'Время создания'
                        ]
        for col in regular_columns:
            if (col in columns)==False:
                return False
        return True


    def get_stru_questions(self):
        #формируем список вопросов
        df=self.list_questions.copy()
        df['questions']=df['list_questions'].apply(str2qwe)
        df['answers']=df['list_questions'].apply(str2ans)
        self.stru_qwe=df
        return True

    def parsing_question(self):
        #переходим от многостолбцового представления ответов, к одностолбцовому
        #вариант когда на вопрос имеется много ответов и каждый ответ в отдельном столбце
        #формируем таблицу, когда один вопрос со всеми ответами представляются в одном столбце
        uniq_qwe=self.stru_qwe['questions'].unique()
        fl_df=False
        for uq in uniq_qwe:
            df_uq=self.stru_qwe[self.stru_qwe['questions']==uq] 
            list_qwe=list(df_uq['list_questions'])
            for qwe in list_qwe:
                df_qwe=self.df[self.regular_columns+[qwe]]
                df_qwe['questions']=[uq]*len(df_qwe)
                df_qwe.rename(columns={qwe:'answers' }, inplace=True)
                df_qwe.dropna(subset=['answers'], inplace=True)
                if fl_df==False:
                    df_rez=df_qwe
                    fl_df=True
                else:
                    df_rez=pd.concat([df_rez, df_qwe], axis=0)
        self.df_rez=df_rez
        return
    
    def get_tab_city(self) -> bool:
        #Дополняем таблицу городов новыми городами, если такие есть в файле
        city=['Страна:', 'Регион:', 'Город:']
        #Заменяем пропуски 
        for s in city:
            self.df_rez[s].fillna('отсутствует', inplace=True)

        #составляем список городов из файла
        file_city=self.df_rez.groupby(city).size()
        file_city=file_city.reset_index()
        file_city=file_city[city]
        
        #загружаем список городов из базы
        df_base_city=self.query_get_city()
        if type(df_base_city)==bool:
            return False

        #находим города, которые есть в файле, но нет в списке городов
        rez_city=pd.merge(file_city, df_base_city, how='left', left_on=city, right_on=['country', 'region','city'])
        ind=rez_city['city'].isnull()
        rez_city=rez_city[ind]
        rez_city=rez_city[city]
        rez_city.rename(columns={city[0]:'country',city[1]:'region',city[2]:'city', }, inplace=True)
        
        #Дополняем базу отсутствующими городами
        if self.query_set(rez_city, 'public.city')==False:
            return False
        return True

    def get_tab_school(self) -> bool:
        #заполняем таблицу школ новыми школами, если такие есть 
        city=['Страна:', 'Регион:', 'Город:']
        school='Учебное заведение:'

        #Заменяем пропуски 
        self.df_rez[school].fillna('отсутствует', inplace=True)

        #составляем список школ из файла с учетом того, что школа определяется только в городе
        file_school=self.df_rez.groupby(city+[school]).size()
        file_school=file_school.reset_index()
        file_school=file_school[city+[school]]
        
        #загружаем список школ из базы
        df_base_school=self.query_get_school()
        if type(df_base_school)==bool:
            return False

        #находим школы, которые есть в файле, но нет в списке школ в базе
        rez_school=pd.merge(file_school, df_base_school, how='left', left_on=city+[school], right_on=['country', 'region','city','school' ])
        ind=rez_school['school'].isnull()
        rez_school=rez_school[ind]
        rez_school=rez_school[city+[school]]
        
        
        #мерджим такие школы с id городами
        df_base_city=self.query_get_city()
        if type(df_base_city)==bool:
            return False
        rez_school=pd.merge(rez_school, df_base_city, how='left', left_on=city, right_on=['country', 'region','city'])
        rez_school=rez_school[['Учебное заведение:', 'city_id']]
        rez_school.rename(columns={'Учебное заведение:':'school','city_id':'city_id_city' }, inplace=True)
        
        if self.query_set(rez_school, 'public.school')==False:
            return False
        return True                

    

    def get_tab_subject(self) -> bool:
        #заполняем таблицу субъектов новыми субъектами, если такие есть 
        #субъектов сравниваем по фамилии, имени, отчетсву, городу, школе

        city=['Страна:', 'Регион:', 'Город:']
        school='Учебное заведение:'
        fio=['Фамилия:', 'Имя:', 'Отчество:']
        info=['Класс:','Номер телефона:','E-mail:']
        #Заменяем пропуски 
        for s in fio+city+['Номер телефона:','E-mail:']+[school]:
            self.df_rez[s].fillna('отсутствует', inplace=True)
        self.df_rez['Класс:'].fillna(-1, inplace=True)

        #составляем список субъектов из файла с учетом того, что субъект определяется:
        #фамилией, именем,  школой городом
        file_sub=self.df_rez.groupby(fio+info+city+[school]).size()
        file_sub=file_sub.reset_index()
        file_sub=file_sub[fio+info+city+[school]]
        
        #загружаем список субъектов из базы
        df_base_sub=self.query_get_subject()
        if type(df_base_sub)==bool:
            return False

        #находим субъектов, которые есть в файле, но нет в базе
        rez_sub=pd.merge(file_sub, df_base_sub, how='left', left_on=fio+city+[school], 
                right_on=[ 'last_name', 'first_name', 'middle_name','country', 'region','city','school' ])
        ind=rez_sub['last_name'].isnull()
        rez_sub=rez_sub[ind]
        rez_sub=rez_sub[fio+info+city+[school]]
        
        
        #мерджим таких субъектов со id школам

        df_base_school=self.query_get_school()
        if type(df_base_school)==bool:
            return False
        rez_sub=pd.merge(rez_sub, df_base_school, how='left', left_on=city+[school], right_on=['country', 'region','city', 'school'])
        rez_sub=rez_sub[['Фамилия:', 'Имя:', 'Отчество:','Класс:','Номер телефона:','E-mail:', 'school_id']]
        rez_sub.rename(columns={'Фамилия:':'last_name',
                                'Имя:':'first_name',
                                'Отчество:':'middle_name',
                                'Класс:':'class',
                                'Номер телефона:':'telephon',
                                'E-mail:':'email', 
                                'school_id':'school_id_school'}, inplace=True)
        
        if self.query_set(rez_sub, 'public.subject')==False:
            return False
        return True 

    def get_tab_event_record(self) -> bool:
        #заполняем таблицу event_record 
        

        city=['Страна:', 'Регион:', 'Город:']
        school='Учебное заведение:'
        fio=['Фамилия:', 'Имя:', 'Отчество:']
        # info=['Класс:','Номер телефона:','E-mail:']
        date=['Время создания']
        #Заменяем пропуски 
        for s in fio+city+[school]:
            self.df_rez[s].fillna('отсутствует', inplace=True)

        #составляем список субъектов из файла с учетом того, что субъект определяется:
        #фамилией, именем,  школой, городом
        file_sub=self.df_rez.groupby(fio+date+city+[school]).size()
        file_sub=file_sub.reset_index()
        file_sub=file_sub[fio+date+city+[school]]
        
        #загружаем список субъектов из базы
        df_base_sub=self.query_get_subject()
        if type(df_base_sub)==bool:
            return False

        #находим id субъектов, которые есть в файле
        rez_sub=pd.merge(file_sub, df_base_sub, how='left', left_on=fio+city+[school], 
                right_on=[ 'last_name', 'first_name', 'middle_name','country', 'region','city','school' ])
        
        
        if len(rez_sub)!=len(file_sub):
            print('ошибка получения subject_id_subject при построении таблицы event_record')
        rez_sub=rez_sub[date+['subject_id']]
        rez_sub['event_id_event']=[self.id_event]*len(rez_sub)
        rez_sub['anket_id_anket']=[self.id_anket]*len(rez_sub)
        rez_sub.rename(columns={'subject_id':'subject_id_subject', date[0]:'creation_time' }, inplace=True)
        
        if self.query_set(rez_sub, 'public.event_record')==False:
            return False
        return True
    
    def get_tab_question(self) -> bool:
        #заполняем таблицу вопросов 
        
        #устанавливаем тип вопроса: открытый или закрытый
        self.stru_qwe['qtype']=['закрытый']*len(self.stru_qwe)
        ind=self.stru_qwe['answers'].isnull()
        self.stru_qwe.loc[ind, 'qtype']=['открытый']*sum(ind)

        #формируем перечень вопросов
        file_qwe=self.stru_qwe.groupby(['questions', 'qtype']).size()
        file_qwe=file_qwe.reset_index()
        file_qwe=file_qwe[['questions', 'qtype']]
        file_qwe['id_anket']=[self.id_anket]*len(file_qwe)
        
        #загружаем список вопросов из базы
        df_question=self.query_get_question()
        if type(df_question)==bool:
            return False

        #находим вопросы, которые есть в файле, но нет в базе
        rez_qwe=pd.merge(file_qwe, df_question, how='left', left_on=['questions', 'qtype', 'id_anket'],
                                 right_on=['questiontext', 'questiontype','anket_id_anket'])
        ind=rez_qwe['questiontext'].isnull()
        rez_qwe=rez_qwe[ind]
        rez_qwe=rez_qwe[['questions', 'qtype', 'id_anket']]
        rez_qwe.rename(columns={'questions':'questiontext','qtype':'questiontype','id_anket':'anket_id_anket' }, inplace=True)
        
        #Дополняем базу отсутствующими городами
        if self.query_set(rez_qwe, 'public.question')==False:
            return False
        return True

    
    def get_tab_possible_answer(self) -> bool:
        #заполняем таблицу возможных ответов 
        
        #формируем перечень ответов
        file_ans=self.stru_qwe.copy()

        #заполняем пропуски
        file_ans['answers'].fillna('отсутствует', inplace=True)
        file_ans['id_anket']=[self.id_anket]*len(file_ans)

        #загружаем список вопросов из базы
        df_question=self.query_get_question()
        if type(df_question)==bool:
            return False

        #находим id вопросов
        rez_ans=pd.merge(file_ans, df_question, how='left', left_on=['questions', 'qtype', 'id_anket'],
                                 right_on=['questiontext', 'questiontype','anket_id_anket'])
        
        rez_ans=rez_ans[['answers', 'question_id']]
        rez_ans.rename(columns={'answers':'possible_answer','question_id':'question_id_question' }, inplace=True)
        
        #Дополняем базу отсутствующими городами
        if self.query_set(rez_ans, 'public.possible_answer')==False:
            return False
        return True
    def get_tab_answer(self) -> bool:
        #и наконец-то заполняем таблицу  ответов 
        rez=self.df_rez.copy()
        
        city=['Страна:', 'Регион:', 'Город:']
        school='Учебное заведение:'
        fio=['Фамилия:', 'Имя:', 'Отчество:']
        
        #Заменяем пропуски 
        for s in fio+city+[school]:
           rez[s].fillna('отсутствует', inplace=True)
        

        #отрабатываем связку по вопросам
        #формируем перечень вопросов
        file_qwe=self.stru_qwe.groupby(['questions', 'qtype']).size()
        file_qwe=file_qwe.reset_index()
        file_qwe=file_qwe[['questions', 'qtype']]
        file_qwe['id_anket']=[self.id_anket]*len(file_qwe)

        #загружаем список вопросов из базы
        df_question=self.query_get_question()
        if type(df_question)==bool:
            return False

        #находим id вопросов
        rez_qwe=pd.merge(file_qwe, df_question, how='left', left_on=['questions', 'qtype', 'id_anket'],
                                 right_on=['questiontext', 'questiontype','anket_id_anket'])

        rez_qwe=rez_qwe[['questions', 'qtype', 'id_anket', 'question_id']]
        
        #мерджим id вопросов
        rez=pd.merge(rez, rez_qwe, how='left', left_on='questions', right_on='questions')

        #отрабатываем связку по возможным ответам
        df_possible_ansers=self.query_get_possible_anser()
        if type(df_possible_ansers)==bool:
            return False

        #делим ответы на открытые и закрытые
        rez_open=rez[rez['qtype']=='открытый']
        rez_close=rez[rez['qtype']=='закрытый']
        
        rez_open=pd.merge(rez_open, df_possible_ansers, how='left', left_on=['question_id'], right_on=['question_id_question'])
        rez_close=pd.merge(rez_close, df_possible_ansers, how='left', left_on=['question_id', 'answers'], right_on=['question_id_question', 'possible_answer'])
        rez=pd.concat([rez_open, rez_close], axis=0)

        #отрабатываем связку по event_record
        #загружаем список субъектов из базы
        df_base_sub=self.query_get_subject()
        if type(df_base_sub)==bool:
            return False
        #находим id субъектов
        rez=pd.merge(rez, df_base_sub, how='left', left_on=fio+city+[school], 
                right_on=[ 'last_name', 'first_name', 'middle_name','country', 'region','city','school' ])
        #Чистим rez
        rez=rez[['answers', 'question_id_question', 'possible_answer_id', 'id_anket', 'subject_id', 'Время создания']]
        rez['event_id']=[self.id_event]*len(rez)
        # rez['Время создания'] = pd.to_datetime(rez['Время создания'], utc = True)
        # rez['Время создания']=rez['Время создания'].apply(str)
        
        #загружаем список event_record
        
        df_base_event_record=self.query_get_event_record()
        # df_base_event_record['creation_time']=df_base_event_record['creation_time'].apply(str)
        if type(df_base_event_record)==bool:
            return False
        #находим id event_record
        rez=pd.merge(rez, df_base_event_record, how='left', left_on=['Время создания','subject_id','event_id', 'id_anket' ], 
                right_on=[ 'creation_time', 'subject_id_subject', 'event_id_event','anket_id_anket' ])

        #чистим rez
        rez=rez[['answers', 'event_record_id', 'question_id_question', 'possible_answer_id']]
        rez.rename(columns={'answers':'answer', 'event_record_id':'event_record_id_event_record','possible_answer_id':'possible_answer_id_possible_answer'}, inplace=True)
        #Дополняем базу отсутствующими городами
        if self.query_set(rez, 'public.answer')==False:
            return False
        return True
if __name__ == '__main__':
    df=pd.read_excel('DOD_V_2022+Ипостаси.xlsx')
    list_questions=pd.read_csv('list_questions.csv', sep='  ')
    event={'event':'ДОД2022-весна', 'date':'2022.04.10'}
    anket={'type_anket':'тип анкеты', 'name_anket':'имя анкеты'}
    
    prepair=prepar_data(df=df, list_questions=list_questions, event=event,anket=anket )
    if prepair.predict()==False:
        print('Format of data is not valid')
    print('Format of data is valid')
    
    
    
