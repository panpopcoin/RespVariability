from datetime import timedelta
from pandas import DataFrame, concat


class TableFuncBasic():
    def __init__(self) -> None:
        pass


class TableCobine(TableFuncBasic):
    '''
    func: get the 'ICU' from DF1 and conbine with DF2
    '''

    __colname = ['PID', 'ICU', 'Record_t', 'endo_t']

    def __init__(self, df_1, df_2):
        super().__init__()
        self.__df_1 = df_1
        self.__df_2 = df_2
        self.__icu = []

    def __InfoFilter(self, df_1, df_2):

        icu_v = ''

        for i in df_2.index:

            t_gap = timedelta(minutes=1)
            t_filt = abs(df_1.Record_t - df_2.endo_t[i]) < t_gap
            t_index = df_1.loc[t_filt].index

            for j in t_index:
                icu_v = df_1.ICU[j]
                if icu_v:
                    self.__icu.append(icu_v)
                    return
            self.__icu.append(icu_v)

    def Conbine(self):

        gp_1 = self.__df_1.groupby(self.__df_1.PID)
        gp_2 = self.__df_2.groupby(self.__df_2.PID)

        for pid in self.__df_2.PID.unique():

            df_tmp_gp_1 = gp_1.get_group(pid)
            df_tmp_gp_2 = gp_2.get_group(pid)

            df_tmp_gp_1 = df_tmp_gp_1.sort_values(by=self.__colname[2])
            df_tmp_gp_2 = df_tmp_gp_2.sort_values(by=self.__colname[3])

            self.__InfoFilter(df_tmp_gp_1, df_tmp_gp_2)

        self.__df_2[self.__colname[1]] = self.__icu


class TableFilt(TableFuncBasic):

    __colname_list = ['PID', 'Resp_t', 'endo_t']

    def __init__(self, df_1, df_2, result):
        super().__init__()
        self.__df_1 = df_1
        self.__df_2 = df_2
        self.result = result
        self.__result_type = list(self.result.keys())

    def __TimeFilt(self, df, t_tag_1, t_tag_2):
        '''
        t_tag_1: record_t_n
        t_tag_2: baguan_t
        '''
        gap_setting = {
            'gap_forward_h': 3,
            'gap_forward_m': 10,
            'gap_post_h': 6,
            'gap_post_m': 5
        }

        self.__index_list = []

        time_gap = timedelta(hours=gap_setting['gap_forward_h'],
                             minutes=gap_setting['gap_forward_m'])

        time_gap_max = timedelta(hours=gap_setting['gap_post_h'],
                                 minutes=gap_setting['gap_post_m'])

        differ_t = (t_tag_1 - t_tag_2).total_seconds()

        if differ_t <= 0:
            #TODO baguan - time_gap <--> baguan
            forward_t = t_tag_2 - time_gap
            post_t = t_tag_2
            self.__CollectIndex_t(forward_t, post_t, df, self.__index_list)

        elif differ_t > 0 and differ_t <= time_gap_max.seconds:
            #TODO baguan - time_gap <--> record_t_end
            forward_t = t_tag_2 - time_gap
            post_t = t_tag_1
            self.__CollectIndex_t(forward_t, post_t, df, self.__index_list)

        elif differ_t > time_gap_max.seconds:
            #TODO baguan - time_gap <--> baguan + time_gap_max
            forward_t = t_tag_2 - time_gap
            post_t = t_tag_2 + time_gap_max
            self.__CollectIndex_t(forward_t, post_t, df, self.__index_list)

    def __CollectIndex_t(self, t_0, t_1, df, list_):

        for i in df.index:
            cur_t = df.loc[i, self.__colname_list[1]]

            if cur_t >= t_0 and cur_t <= t_1:
                list_.append(i)

            if cur_t > t_1:
                break

    def Filt(self):

        gp_1 = self.__df_1.groupby(self.__colname_list[0])
        gp_2 = self.__df_2.groupby(self.__colname_list[0])

        for pid in self.__df_2[self.__colname_list[0]].unique():

            try:
                df_tmp_gp_1 = gp_1.get_group(pid)
                df_tmp_gp_2 = gp_2.get_group(pid)

            except:
                filt = self.__df_2[self.__colname_list[0]] == pid
                pid_index = self.__df_2.loc[filt].index[0]
                self.result[self.__result_type[0]].append(pid_index)
                print('pid missing: ', pid)
                continue

            df_tmp_gp_1 = df_tmp_gp_1.sort_values(by=self.__colname_list[1],
                                                  ascending=True)
            df_tmp_gp_2 = df_tmp_gp_2.sort_values(by=self.__colname_list[2],
                                                  ascending=True)

            for i in df_tmp_gp_2.index:

                record_t_n = df_tmp_gp_1[self.__colname_list[1]].max()
                baguan_t = df_tmp_gp_2.loc[i, self.__colname_list[2]]

                self.__TimeFilt(df_tmp_gp_1, record_t_n, baguan_t)

                if not self.__index_list:
                    self.result[self.__result_type[1]].append(i)
                    print('Invalid data BaguanTime: ',
                          df_tmp_gp_2.loc[i, self.__colname_list[2]])
                else:

                    copy_times = len(self.__index_list)

                    self.result[self.__result_type[2]].extend(
                        self.__index_list)
                    self.result[self.__result_type[3]].append(i)
                    self.result[self.__result_type[4]].append(copy_times)
                    self.result[self.__result_type[5]].extend([record_t_n] *
                                                              copy_times)


class TableBuild(TableFuncBasic):

    __index_name = [
        'pid_miss_index', 'time_miss_index', 'filt_index_a', 'filt_index_b',
        'copy_times', 'end_time'
    ]

    def __init__(self, df_1, df_2, filt_dict):
        super().__init__()
        self.__df_1 = df_1
        self.__df_2 = df_2
        self.__result = filt_dict
        self.df = None

    def __BuildByIndex(self, df, index):

        return df.iloc[index]

    def __BuildByCopy(self, df, index, copy_list):

        df_tmp_list = []

        if len(index) != len(copy_list):
            print('Index and copytimes list length not matched')
            return DataFrame(df_tmp_list)
        else:
            for i in range(len(index)):

                df_copy = [df.iloc[index[i]]] * copy_list[i]
                df_tmp_list.extend(df_copy)

            df_tmp = DataFrame(df_tmp_list)

        return df_tmp

    def PidmissBuild(self):
        self.df = None
        self.df = self.__BuildByIndex(self.__df_2,
                                      self.__result[self.__index_name[0]])

    def TimemissBuild(self):
        self.df = None
        self.df = self.__BuildByIndex(self.__df_2,
                                      self.__result[self.__index_name[1]])

    def FiltedDataBuild(self):
        self.df = None
        table_left = self.__BuildByIndex(self.__df_1,
                                         self.__result[self.__index_name[2]])

        table_right = self.__BuildByCopy(self.__df_2,
                                         self.__result[self.__index_name[3]],
                                         self.__result[self.__index_name[4]])

        table_left = table_left.reset_index(drop=True)
        table_right = table_right.reset_index(drop=True)
        # drop pid column
        table_right = table_right[list(self.__df_2.columns)[1:]]
        # add end time column
        table_right[self.__index_name[5]] = self.__result[self.__index_name[5]]

        table_conbine = concat((table_left, table_right), axis=1)

        self.df = table_conbine


class TableProcess(TableFuncBasic):

    __colname = [
        'zdt_1', 'zpx_1', 'Record_id', 'Resp_id', 'PID', 'Resp_t', 'endo_end',
        'ICU'
    ]

    def __init__(self, df, re_colname):
        super().__init__()
        self.__df = df
        self.__re_colname = re_colname
        self.__df = self.__df[self.__re_colname]  # Reorder
        self.df = None

    def ValidProcess(self):

        filt_zdt = self.__df[self.__colname[0]].notna()
        filt_zpx = self.__df[self.__colname[1]].notna()
        filt_endo = self.__df[self.__colname[6]].notna()
        filt_icu = self.__df[self.__colname[7]].notna()

        filt_col = filt_zdt & filt_zpx & filt_endo & filt_icu
        filt_not_monitor = self.__df[self.__colname[2]].eq(
            self.__df[self.__colname[3]], fill_value=0)

        self.df = None
        self.df = self.__df.loc[filt_col & filt_not_monitor]
        self.df = self.df.sort_values(by=self.__colname[4:6])

    def inValidProcess(self):

        filt_zdt = self.__df[self.__colname[0]].isna()
        filt_zpx = self.__df[self.__colname[1]].isna()
        filt_endo = self.__df[self.__colname[6]].isna()
        filt_icu = self.__df[self.__colname[7]].isna()

        filt_col = filt_zdt | filt_zpx | filt_endo | filt_icu
        filt_monitor = self.__df[self.__colname[2]].ne(
            self.__df[self.__colname[3]], fill_value=0)

        self.df = None
        self.df = self.__df.loc[filt_col | filt_monitor]
        self.df = self.df.sort_values(by=self.__colname[4:6])
